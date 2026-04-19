"""Optional S3-compatible upload for Hermes archives (MinIO / AWS; Phase L6)."""

from __future__ import annotations

import hashlib
import io
import tarfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from deepguard_core.models.agent_error import AgentError, AgentRuntimeError
from deepguard_core.models.artifact_ref import ArtifactRef
from deepguard_core.models.enums import AgentErrorSeverity


@dataclass(frozen=True, slots=True)
class ObjectStoreConfig:
    """S3-compatible API (MinIO dev: set ``endpoint_url`` to ``http://127.0.0.1:9000``)."""

    bucket: str
    access_key_id: str
    secret_access_key: str
    endpoint_url: str | None = None
    region_name: str = "us-east-1"


def directory_to_tar_gz_bytes(directory: Path) -> tuple[bytes, str]:
    """Pack directory into a single ``.tar.gz`` in memory; return bytes + SHA-256 hex."""

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        tf.add(directory.resolve(), arcname="repo")
    raw = buf.getvalue()
    digest = hashlib.sha256(raw).hexdigest()
    return raw, digest


def upload_tar_gz_to_object_store(
    body: bytes,
    *,
    key: str,
    config: ObjectStoreConfig,
) -> ArtifactRef:
    """``put_object`` to S3-compatible store; returns ``ArtifactRef`` (no raw bytes in callers)."""

    try:
        import boto3  # type: ignore[import-untyped]
        from botocore.config import Config as BotoConfig  # type: ignore[import-untyped]
    except ImportError as exc:
        raise AgentRuntimeError(
            AgentError(
                agent="hermes",
                code="HERMES_BOTO3_MISSING",
                message="Install boto3 to enable object-store upload.",
                severity=AgentErrorSeverity.RECOVERABLE,
            )
        ) from exc

    bcfg = BotoConfig(s3={"addressing_style": "path"}) if config.endpoint_url else BotoConfig()
    client = boto3.client(
        "s3",
        region_name=config.region_name,
        endpoint_url=config.endpoint_url,
        aws_access_key_id=config.access_key_id,
        aws_secret_access_key=config.secret_access_key,
        config=bcfg,
    )
    digest = hashlib.sha256(body).hexdigest()
    client.put_object(Bucket=config.bucket, Key=key, Body=body)
    aid = uuid.uuid4()
    return ArtifactRef(
        artifact_id=aid,
        store="s3",
        bucket=config.bucket,
        key=key,
        checksum=digest,
        size_bytes=len(body),
        encrypted=False,
    )


def stage_directory_tar_and_upload(
    directory: Path,
    *,
    scan_id: str,
    config: ObjectStoreConfig,
    tenant_id: str | None = None,
    key_prefix: str = "scans",
) -> ArtifactRef:
    """Tar-gz ``directory`` and upload.

    When ``tenant_id`` is set, key is ``tenants/{tenant_id}/scans/{scan_id}/repo.tar.gz``
    (US-DG-04-003 layout). Otherwise ``{key_prefix}/{scan_id}/repo.tar.gz`` (legacy L6).
    """

    raw, _digest = directory_to_tar_gz_bytes(directory)
    if tenant_id:
        key = f"tenants/{tenant_id}/scans/{scan_id}/repo.tar.gz"
    else:
        key = f"{key_prefix.strip('/')}/{scan_id}/repo.tar.gz"
    return upload_tar_gz_to_object_store(raw, key=key, config=config)


def parse_s3_uri(uri: str) -> tuple[str, str]:
    """Return ``(bucket, key)`` for ``s3://bucket/key/with/slashes``."""

    u = uri.strip()
    if not u.startswith("s3://"):
        msg = "storage_uri must start with s3://"
        raise ValueError(msg)
    rest = u.removeprefix("s3://")
    idx = rest.find("/")
    if idx <= 0 or idx >= len(rest) - 1:
        msg = "invalid s3:// URI (need bucket and key)"
        raise ValueError(msg)
    return rest[:idx], rest[idx + 1 :]


def _s3_client(config: ObjectStoreConfig) -> Any:
    try:
        import boto3
        from botocore.config import Config as BotoConfig
    except ImportError as exc:
        raise AgentRuntimeError(
            AgentError(
                agent="hermes",
                code="HERMES_BOTO3_MISSING",
                message="Install boto3 to enable object-store operations.",
                severity=AgentErrorSeverity.RECOVERABLE,
            )
        ) from exc
    bcfg = BotoConfig(s3={"addressing_style": "path"}) if config.endpoint_url else BotoConfig()
    return boto3.client(
        "s3",
        region_name=config.region_name,
        endpoint_url=config.endpoint_url,
        aws_access_key_id=config.access_key_id,
        aws_secret_access_key=config.secret_access_key,
        config=bcfg,
    )


def copy_s3_object_to_dest(
    *,
    src_uri: str,
    dest_bucket: str,
    dest_key: str,
    config: ObjectStoreConfig,
) -> ArtifactRef:
    """Server-side copy from ``src_uri`` into ``dest_bucket``/``dest_key``."""

    src_bucket, src_key = parse_s3_uri(src_uri)
    client = _s3_client(config)
    client.copy_object(
        Bucket=dest_bucket,
        Key=dest_key,
        CopySource={"Bucket": src_bucket, "Key": src_key},
    )
    head = client.head_object(Bucket=dest_bucket, Key=dest_key)
    size_b = int(head["ContentLength"])
    aid = uuid.uuid4()
    return ArtifactRef(
        artifact_id=aid,
        store="s3",
        bucket=dest_bucket,
        key=dest_key,
        checksum="0" * 64,
        size_bytes=size_b,
        encrypted=False,
    )


def verify_s3_object_sha256_stream(
    *,
    bucket: str,
    key: str,
    expected_hex: str,
    max_bytes: int,
    config: ObjectStoreConfig,
) -> int:
    """Stream object through SHA-256; raises ``AgentRuntimeError`` on mismatch or oversize."""

    client = _s3_client(config)
    resp = client.get_object(Bucket=bucket, Key=key)
    body = resp["Body"]
    h = hashlib.sha256()
    total = 0
    while True:
        chunk = body.read(1024 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise AgentRuntimeError(
                AgentError(
                    agent="hermes",
                    code="REPO_MAX_BYTES_EXCEEDED",
                    message=f"object exceeded REPO_MAX_BYTES ({max_bytes})",
                    severity=AgentErrorSeverity.RECOVERABLE,
                )
            )
        h.update(chunk)
    digest = h.hexdigest()
    if digest.lower() != expected_hex.lower():
        raise AgentRuntimeError(
            AgentError(
                agent="hermes",
                code="HERMES_CHECKSUM_MISMATCH",
                message="staged archive checksum does not match repo.checksum_sha256",
                severity=AgentErrorSeverity.RECOVERABLE,
            )
        )
    return total
