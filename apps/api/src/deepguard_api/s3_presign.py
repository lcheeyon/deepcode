"""Presigned PUT helpers for repo artefact staging (US-DG-02-011 / US-DG-04-008)."""

from __future__ import annotations

from typing import Any
from uuid import UUID


def presigned_put_url(
    *,
    bucket: str,
    key: str,
    endpoint_url: str | None,
    access_key_id: str,
    secret_access_key: str,
    region: str,
    content_type: str,
    expires_in: int = 3600,
) -> tuple[str, dict[str, str]]:
    """Return ``(url, headers)`` for a single-shot PUT (MinIO / AWS S3-compatible)."""

    import boto3  # type: ignore[import-untyped]
    from botocore.config import Config as BotoConfig  # type: ignore[import-untyped]

    bcfg = BotoConfig(s3={"addressing_style": "path"}) if endpoint_url else BotoConfig()
    client: Any = boto3.client(
        "s3",
        region_name=region,
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        config=bcfg,
    )
    url = client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": bucket,
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=expires_in,
        HttpMethod="PUT",
    )
    headers = {"Content-Type": content_type}
    return url, headers


def parse_s3_uri(uri: str) -> tuple[str, str] | None:
    """Return ``(bucket, key)`` for ``s3://bucket/key`` URIs."""

    if not uri.startswith("s3://"):
        return None
    rest = uri.removeprefix("s3://")
    bucket, _, key = rest.partition("/")
    if not bucket or not key:
        return None
    return bucket, key


def presigned_get_url(
    *,
    bucket: str,
    key: str,
    endpoint_url: str | None,
    access_key_id: str,
    secret_access_key: str,
    region: str,
    expires_in: int = 3600,
) -> str:
    """Return a presigned GET URL for downloading an object."""

    import boto3  # type: ignore[import-untyped]
    from botocore.config import Config as BotoConfig  # type: ignore[import-untyped]

    bcfg = BotoConfig(s3={"addressing_style": "path"}) if endpoint_url else BotoConfig()
    client: Any = boto3.client(
        "s3",
        region_name=region,
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        config=bcfg,
    )
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
        HttpMethod="GET",
    )


def staging_object_key(*, tenant_id: UUID, upload_id: UUID, filename: str) -> str:
    """Tenant-scoped staging key for CI / browser uploads prior to ``POST /v1/scans``."""

    safe = filename.replace("\\", "/").split("/")[-1][:256] or "upload.bin"
    return f"uploads/{tenant_id}/{upload_id}/{safe}"
