"""Hermes local ingestion + sandbox read boundary (Phase L6 / EPIC DG-04)."""

from __future__ import annotations

import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from deepguard_agents.hermes_s3 import ObjectStoreConfig

from deepguard_core.models.agent_error import AgentError, AgentRuntimeError
from deepguard_core.models.artifact_ref import ArtifactRef
from deepguard_core.models.enums import AgentErrorSeverity

REPO_MAX_BYTES_DEFAULT = 50_000_000


def safe_read_bytes(sandbox_root: Path, relative: str) -> bytes:
    """Read a file under ``sandbox_root``; reject path traversal (``..`` / absolute escapes)."""

    root = sandbox_root.resolve()
    target = (root / relative).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise AgentRuntimeError(
            AgentError(
                agent="hermes",
                code="SANDBOX_PATH_ESCAPE",
                message="Path resolves outside sandbox root.",
                severity=AgentErrorSeverity.RECOVERABLE,
            )
        ) from exc
    if not target.is_file():
        raise AgentRuntimeError(
            AgentError(
                agent="hermes",
                code="SANDBOX_NOT_A_FILE",
                message=f"Not a file: {relative}",
                severity=AgentErrorSeverity.RECOVERABLE,
            )
        )
    return target.read_bytes()


def _tree_size_bytes(path: Path) -> int:
    total = 0
    for p in path.rglob("*"):
        if p.is_file():
            total += p.stat().st_size
    return total


@dataclass(frozen=True, slots=True)
class HermesStageResult:
    """State fields after local staging (no raw archive bytes in graph state)."""

    repo_local_path: str
    repo_metadata: dict[str, Any]
    archive_artifact: ArtifactRef


class HermesAgent:
    """Copy a fixture tree into ``TOOL_SANDBOX_ROOT`` / ``scan_id`` / ``repo``."""

    def __init__(
        self,
        *,
        sandbox_root: Path,
        repo_max_bytes: int = REPO_MAX_BYTES_DEFAULT,
    ) -> None:
        self._root = sandbox_root.resolve()
        self._repo_max_bytes = repo_max_bytes

    def stage_fixture_copy(self, src: Path, *, scan_id: str) -> HermesStageResult:
        """Copy ``src`` (dir) into sandbox; enforce size cap; return ``ArtifactRef`` only."""

        src_r = src.resolve()
        if not src_r.is_dir():
            raise AgentRuntimeError(
                AgentError(
                    agent="hermes",
                    code="HERMES_SRC_NOT_DIR",
                    message="Source must be a directory for L6 fixture staging.",
                    severity=AgentErrorSeverity.RECOVERABLE,
                )
            )
        dest = self._root / scan_id / "repo"
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src_r, dest)
        nbytes = _tree_size_bytes(dest)
        if nbytes > self._repo_max_bytes:
            shutil.rmtree(dest, ignore_errors=True)
            raise AgentRuntimeError(
                AgentError(
                    agent="hermes",
                    code="REPO_MAX_BYTES_EXCEEDED",
                    message=f"Staged tree {nbytes} bytes exceeds limit {self._repo_max_bytes}.",
                    severity=AgentErrorSeverity.RECOVERABLE,
                )
            )
        aid = uuid.uuid4()
        ref = ArtifactRef(
            artifact_id=aid,
            store="local",
            bucket="sandbox",
            key=f"{scan_id}/repo.tgz",
            checksum="0" * 64,
            size_bytes=nbytes,
            encrypted=False,
        )
        meta: dict[str, Any] = {
            "source_path": str(src_r),
            "file_count": sum(1 for _ in dest.rglob("*") if _.is_file()),
            "bytes_total": nbytes,
        }
        return HermesStageResult(
            repo_local_path=str(dest),
            repo_metadata=meta,
            archive_artifact=ref,
        )

    def stage_fixture_copy_and_upload(
        self,
        src: Path,
        *,
        scan_id: str,
        object_store: ObjectStoreConfig | None = None,
    ) -> HermesStageResult:
        """Copy to sandbox, then optionally tar the tree and upload to S3-compatible storage."""

        from deepguard_agents.hermes_s3 import stage_directory_tar_and_upload

        base = self.stage_fixture_copy(src, scan_id=scan_id)
        if object_store is None:
            return base
        ref = stage_directory_tar_and_upload(
            Path(base.repo_local_path),
            scan_id=scan_id,
            config=object_store,
        )
        return HermesStageResult(
            repo_local_path=base.repo_local_path,
            repo_metadata={**base.repo_metadata, "object_store_uploaded": True},
            archive_artifact=ref,
        )
