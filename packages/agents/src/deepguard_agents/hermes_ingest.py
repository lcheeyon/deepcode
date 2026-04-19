"""Hermes ingestion for workers: git clone or archive copy, size caps, S3 staging (EPIC DG-04)."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from deepguard_core.models import CreateScanRequest
from deepguard_core.models.agent_error import AgentRuntimeError

from deepguard_agents.hermes_s3 import (
    ObjectStoreConfig,
    copy_s3_object_to_dest,
    parse_s3_uri,
    stage_directory_tar_and_upload,
    verify_s3_object_sha256_stream,
)


class HermesExecutionError(Exception):
    __slots__ = ("code", "message")

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class HermesRuntimeConfig:
    """Hermes feature flags and limits (from worker env)."""

    enabled: bool
    repo_max_bytes: int
    clone_depth: int
    s3: ObjectStoreConfig | None


def _tree_size(path: Path) -> int:
    total = 0
    for p in path.rglob("*"):
        if p.is_file():
            total += p.stat().st_size
    return total


def _git_clone_to(*, url: str, ref: str, dest: Path, depth: int, timeout_sec: int = 900) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "git",
        "clone",
        "--depth",
        str(depth),
        "--single-branch",
        "--branch",
        ref,
        str(url),
        str(dest),
    ]
    try:
        proc = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired as exc:
        raise HermesExecutionError("HERMES_GIT_CLONE_TIMEOUT", "git clone timed out") from exc
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise HermesExecutionError(
            "HERMES_GIT_CLONE_FAILED",
            err[:8192] or f"git clone exit {proc.returncode}",
        )


def _git_rev_parse(dest: Path) -> str:
    proc = subprocess.run(
        ["git", "-C", str(dest), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if proc.returncode != 0:
        raise HermesExecutionError("HERMES_GIT_REV_PARSE_FAILED", (proc.stderr or "")[:4096])
    return proc.stdout.strip()


def _workspace_root(dest: Path, sub_path: str | None) -> Path:
    if not sub_path:
        return dest
    sp = sub_path.strip().replace("\\", "/").strip("/")
    sub = (dest / sp).resolve()
    try:
        sub.relative_to(dest.resolve())
    except ValueError as exc:
        raise HermesExecutionError(
            "HERMES_SUBPATH_ESCAPE",
            "repo.sub_path escapes clone root",
        ) from exc
    if not sub.exists() or not sub.is_dir():
        raise HermesExecutionError("HERMES_SUBPATH_MISSING", f"not a directory: {sub_path}")
    return sub


def run_hermes_phase(
    job_config: dict[str, Any],
    *,
    tenant_id: str,
    scan_id: str,
    cfg: HermesRuntimeConfig,
) -> tuple[str | None, dict[str, Any]] | None:
    """Clone or copy repo archive, enforce size, stage ``repo.tar.gz`` under tenant prefix.

    Returns ``(repo_commit_sha, job_config_shallow_merge)`` where the merge dict should be
    applied as ``job_config = job_config | returned`` (expects top-level ``hermes`` key),
    or ``None`` when Hermes is skipped for this job.
    """

    try:
        return _run_hermes_phase_impl(job_config, tenant_id=tenant_id, scan_id=scan_id, cfg=cfg)
    except AgentRuntimeError as exc:
        raise HermesExecutionError(exc.record.code, str(exc.record.message)[:8192]) from exc


def _run_hermes_phase_impl(
    job_config: dict[str, Any],
    *,
    tenant_id: str,
    scan_id: str,
    cfg: HermesRuntimeConfig,
) -> tuple[str | None, dict[str, Any]] | None:
    body = CreateScanRequest.model_validate(job_config)
    layers = body.scan_layers
    if body.repo is None or not (layers.code or layers.iac):
        return None
    if not cfg.enabled:
        return None
    if cfg.s3 is None:
        raise HermesExecutionError(
            "HERMES_S3_UNCONFIGURED",
            "Hermes enabled but S3 credentials / bucket are not configured",
        )

    repo = body.repo
    s3 = cfg.s3

    if repo.source == "archive":
        assert repo.storage_uri is not None
        src_bucket, src_key = parse_s3_uri(repo.storage_uri)
        if repo.checksum_sha256:
            verify_s3_object_sha256_stream(
                bucket=src_bucket,
                key=src_key,
                expected_hex=repo.checksum_sha256,
                max_bytes=cfg.repo_max_bytes,
                config=s3,
            )
        ref = copy_s3_object_to_dest(
            src_uri=repo.storage_uri,
            dest_bucket=s3.bucket,
            dest_key=f"tenants/{tenant_id}/scans/{scan_id}/repo.tar.gz",
            config=s3,
        )
        archive_meta: dict[str, Any] = {
            "storage_uri": f"s3://{ref.bucket}/{ref.key}",
            "size_bytes": ref.size_bytes,
            "format": "external_copy",
        }
        if repo.checksum_sha256:
            archive_meta["checksum_sha256"] = repo.checksum_sha256
        return None, {"hermes": {"repo_archive": archive_meta}}

    assert repo.url is not None
    depth = repo.clone_depth if repo.clone_depth is not None else cfg.clone_depth
    with tempfile.TemporaryDirectory(prefix="dg-hermes-") as tmp:
        clone_dest = Path(tmp) / "repo"
        _git_clone_to(url=str(repo.url), ref=repo.ref, dest=clone_dest, depth=depth)
        commit_sha = _git_rev_parse(clone_dest)
        root = _workspace_root(clone_dest, repo.sub_path)
        nbytes = _tree_size(root)
        if nbytes > cfg.repo_max_bytes:
            raise HermesExecutionError(
                "REPO_MAX_BYTES_EXCEEDED",
                f"workspace {nbytes} bytes exceeds limit {cfg.repo_max_bytes}",
            )
        ref = stage_directory_tar_and_upload(
            root,
            scan_id=scan_id,
            config=s3,
            tenant_id=tenant_id,
        )

    return commit_sha, {
        "hermes": {
            "repo_archive": {
                "storage_uri": f"s3://{ref.bucket}/{ref.key}",
                "checksum_sha256": ref.checksum,
                "size_bytes": ref.size_bytes,
                "format": "tar_gz",
            }
        }
    }

