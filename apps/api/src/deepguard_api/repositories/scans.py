"""Scan row persistence (Postgres + in-memory for tests)."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import Any, Protocol, cast
from uuid import UUID, uuid4

from deepguard_core.models import CreateScanRequest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from deepguard_api.schemas import ScanResponse


def _initial_repo_commit_sha(body: CreateScanRequest) -> str | None:
    if body.repo is None or body.repo.source != "git":
        return None
    return body.repo.commit_sha


@dataclass(frozen=True, slots=True)
class ScanRow:
    """Normalized scan row for repository ↔ API boundary."""

    id: UUID
    tenant_id: UUID
    status: str
    current_stage: str
    percent_complete: int
    job_config: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    idempotency_key: str | None
    repo_commit_sha: str | None
    cancellation_requested: bool = False
    reused_from_idempotency: bool = False

    def to_response(self) -> ScanResponse:
        return ScanResponse(
            scan_id=self.id,
            tenant_id=self.tenant_id,
            status=self.status,
            current_stage=self.current_stage,
            percent_complete=self.percent_complete,
            job_config=self.job_config,
            created_at=self.created_at,
            updated_at=self.updated_at,
            idempotency_key=self.idempotency_key,
            repo_commit_sha=self.repo_commit_sha,
            cancellation_requested=self.cancellation_requested,
        )


class ScanRepository(Protocol):
    async def create_scan(
        self,
        *,
        tenant_id: UUID,
        body: CreateScanRequest,
        idempotency_key: str | None,
    ) -> ScanRow: ...

    async def get_scan(self, *, tenant_id: UUID, scan_id: UUID) -> ScanRow | None: ...

    async def set_cancellation_requested(self, *, tenant_id: UUID, scan_id: UUID) -> bool: ...

    async def try_claim_scan_for_ingest(self, *, tenant_id: UUID, scan_id: UUID) -> bool: ...

    async def is_cancel_requested(self, *, tenant_id: UUID, scan_id: UUID) -> bool: ...

    async def mark_cancelled(self, *, tenant_id: UUID, scan_id: UUID) -> None: ...

    async def mark_scan_failed(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        error_code: str,
        error_message: str,
    ) -> None: ...

    async def mark_scan_complete_with_report(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        pdf_bytes: bytes,
        storage_uri: str,
    ) -> UUID: ...

    async def update_scan_post_hermes(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        repo_commit_sha: str | None,
        job_config_merge: dict[str, Any],
        current_stage: str,
        percent_complete: int,
    ) -> None: ...


class MemoryScanRepository:
    """In-process store for fast API tests (no Docker)."""

    def __init__(self) -> None:
        self._rows: dict[UUID, ScanRow] = {}
        self._idempotency: dict[tuple[UUID, str], UUID] = {}
        self._report_artifacts: dict[UUID, dict[str, Any]] = {}

    def report_storage_meta(self, scan_id: UUID) -> dict[str, Any] | None:
        """Return last persisted report artifact metadata (memory store; tests / diagnostics)."""

        return self._report_artifacts.get(scan_id)

    def _put(self, row: ScanRow) -> None:
        self._rows[row.id] = row

    async def create_scan(
        self,
        *,
        tenant_id: UUID,
        body: CreateScanRequest,
        idempotency_key: str | None,
    ) -> ScanRow:
        if idempotency_key:
            existing_id = self._idempotency.get((tenant_id, idempotency_key))
            if existing_id is not None:
                prev = self._rows[existing_id]
                return replace(prev, reused_from_idempotency=True)

        sid = uuid4()
        job = body.model_dump(mode="json")
        repo_sha = _initial_repo_commit_sha(body)
        now = datetime.now(UTC)
        row = ScanRow(
            id=sid,
            tenant_id=tenant_id,
            status="QUEUED",
            current_stage="QUEUED",
            percent_complete=0,
            job_config=job,
            created_at=now,
            updated_at=now,
            idempotency_key=idempotency_key,
            repo_commit_sha=repo_sha,
            cancellation_requested=False,
            reused_from_idempotency=False,
        )
        self._put(row)
        if idempotency_key:
            self._idempotency[(tenant_id, idempotency_key)] = sid
        return row

    async def get_scan(self, *, tenant_id: UUID, scan_id: UUID) -> ScanRow | None:
        row = self._rows.get(scan_id)
        if row is None or row.tenant_id != tenant_id:
            return None
        return row

    async def set_cancellation_requested(self, *, tenant_id: UUID, scan_id: UUID) -> bool:
        row = await self.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        if row is None:
            return False
        self._put(
            replace(
                row,
                cancellation_requested=True,
                updated_at=datetime.now(UTC),
            )
        )
        return True

    async def try_claim_scan_for_ingest(self, *, tenant_id: UUID, scan_id: UUID) -> bool:
        row = await self.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        if row is None or row.status != "QUEUED":
            return False
        self._put(
            replace(
                row,
                status="INGESTING",
                current_stage="INGESTING",
                updated_at=datetime.now(UTC),
            )
        )
        return True

    async def is_cancel_requested(self, *, tenant_id: UUID, scan_id: UUID) -> bool:
        row = await self.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        return bool(row and row.cancellation_requested)

    async def mark_cancelled(self, *, tenant_id: UUID, scan_id: UUID) -> None:
        row = await self.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        if row is None:
            return
        self._put(
            replace(
                row,
                status="CANCELLED",
                current_stage="CANCELLED",
                updated_at=datetime.now(UTC),
            )
        )

    async def mark_scan_failed(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        error_code: str,
        error_message: str,
    ) -> None:
        _ = (error_code, error_message)
        row = await self.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        if row is None:
            return
        self._put(
            replace(
                row,
                status="FAILED",
                current_stage="FAILED",
                percent_complete=0,
                updated_at=datetime.now(UTC),
            )
        )

    async def mark_scan_complete_with_report(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        pdf_bytes: bytes,
        storage_uri: str,
    ) -> UUID:
        import hashlib

        row = await self.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        if row is None:
            raise ValueError("scan not found")
        aid = uuid4()
        digest = hashlib.sha256(pdf_bytes).hexdigest()
        self._report_artifacts[scan_id] = {
            "artifact_id": str(aid),
            "storage_uri": storage_uri,
            "checksum_sha256": digest,
            "size_bytes": len(pdf_bytes),
        }
        self._put(
            replace(
                row,
                status="COMPLETE",
                current_stage="COMPLETE",
                percent_complete=100,
                updated_at=datetime.now(UTC),
            )
        )
        return aid

    async def update_scan_post_hermes(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        repo_commit_sha: str | None,
        job_config_merge: dict[str, Any],
        current_stage: str,
        percent_complete: int,
    ) -> None:
        row = await self.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        if row is None:
            return
        merged_job = {**row.job_config, **job_config_merge}
        new_sha = repo_commit_sha if repo_commit_sha is not None else row.repo_commit_sha
        self._put(
            replace(
                row,
                job_config=merged_job,
                repo_commit_sha=new_sha,
                current_stage=current_stage,
                percent_complete=percent_complete,
                updated_at=datetime.now(UTC),
            )
        )


class PostgresScanRepository:
    """Writes ``scans`` rows via SQLAlchemy async + asyncpg."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        """Exposed for the L4 worker to bracket transactions around job steps."""

        return self._session

    async def _select_by_idempotency(self, tenant_id: UUID, idempotency_key: str) -> ScanRow | None:
        res = await self._session.execute(
            text(
                """
                SELECT id, tenant_id, status, current_stage, percent_complete,
                       job_config, policy_versions, created_at, updated_at,
                       idempotency_key, repo_commit_sha, cancellation_requested
                FROM scans
                WHERE tenant_id = CAST(:tid AS uuid) AND idempotency_key = :ik
                """
            ),
            {"tid": str(tenant_id), "ik": idempotency_key},
        )
        m = res.mappings().first()
        return self._mapping_to_row(cast(Mapping[str, Any], m), reused=True) if m else None

    def _mapping_to_row(self, m: Mapping[str, Any], *, reused: bool = False) -> ScanRow:
        jc = m["job_config"]
        if isinstance(jc, str):
            jc = json.loads(jc)
        elif not isinstance(jc, dict):
            jc = dict(jc)
        return ScanRow(
            id=m["id"],
            tenant_id=m["tenant_id"],
            status=m["status"],
            current_stage=m["current_stage"],
            percent_complete=int(m["percent_complete"]),
            job_config=jc,
            created_at=m["created_at"],
            updated_at=m["updated_at"],
            idempotency_key=m.get("idempotency_key"),
            repo_commit_sha=m.get("repo_commit_sha"),
            cancellation_requested=bool(m.get("cancellation_requested", False)),
            reused_from_idempotency=reused,
        )

    async def create_scan(
        self,
        *,
        tenant_id: UUID,
        body: CreateScanRequest,
        idempotency_key: str | None,
    ) -> ScanRow:
        if idempotency_key:
            hit = await self._select_by_idempotency(tenant_id, idempotency_key)
            if hit is not None:
                return hit

        job_json = json.dumps(body.model_dump(mode="json"))
        repo_sha = _initial_repo_commit_sha(body)
        stmt = text(
            """
            INSERT INTO scans (
                tenant_id, status, current_stage, job_config, policy_versions,
                percent_complete, cancellation_requested, idempotency_key, repo_commit_sha
            ) VALUES (
                CAST(:tid AS uuid), 'QUEUED', 'QUEUED', CAST(:jc AS jsonb), CAST(:pv AS jsonb),
                0, false, :ik, :sha
            )
            RETURNING id, tenant_id, status, current_stage, percent_complete,
                      job_config, created_at, updated_at, idempotency_key, repo_commit_sha,
                      cancellation_requested
            """
        )
        params = {
            "tid": str(tenant_id),
            "jc": job_json,
            "pv": "{}",
            "ik": idempotency_key,
            "sha": repo_sha,
        }
        try:
            res = await self._session.execute(stmt, params)
        except IntegrityError:
            await self._session.rollback()
            if idempotency_key:
                hit = await self._select_by_idempotency(tenant_id, idempotency_key)
                if hit is not None:
                    return hit
            raise
        m = res.mappings().one()
        return self._mapping_to_row(cast(Mapping[str, Any], m), reused=False)

    async def get_scan(self, *, tenant_id: UUID, scan_id: UUID) -> ScanRow | None:
        res = await self._session.execute(
            text(
                """
                SELECT id, tenant_id, status, current_stage, percent_complete,
                       job_config, created_at, updated_at, idempotency_key, repo_commit_sha,
                       cancellation_requested
                FROM scans
                WHERE id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                """
            ),
            {"sid": str(scan_id), "tid": str(tenant_id)},
        )
        m = res.mappings().first()
        if m is None:
            return None
        return self._mapping_to_row(cast(Mapping[str, Any], m), reused=False)

    async def set_cancellation_requested(self, *, tenant_id: UUID, scan_id: UUID) -> bool:
        res = await self._session.execute(
            text(
                """
                UPDATE scans
                SET cancellation_requested = true, updated_at = now()
                WHERE id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                RETURNING id
                """
            ),
            {"sid": str(scan_id), "tid": str(tenant_id)},
        )
        return res.first() is not None

    async def try_claim_scan_for_ingest(self, *, tenant_id: UUID, scan_id: UUID) -> bool:
        res = await self._session.execute(
            text(
                """
                UPDATE scans
                SET status = 'INGESTING', current_stage = 'INGESTING', updated_at = now()
                WHERE id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                  AND status = 'QUEUED'
                RETURNING id
                """
            ),
            {"sid": str(scan_id), "tid": str(tenant_id)},
        )
        return res.first() is not None

    async def is_cancel_requested(self, *, tenant_id: UUID, scan_id: UUID) -> bool:
        res = await self._session.execute(
            text(
                """
                SELECT cancellation_requested
                FROM scans
                WHERE id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                """
            ),
            {"sid": str(scan_id), "tid": str(tenant_id)},
        )
        row = res.first()
        if row is None:
            return False
        return bool(row[0])

    async def mark_cancelled(self, *, tenant_id: UUID, scan_id: UUID) -> None:
        await self._session.execute(
            text(
                """
                UPDATE scans
                SET status = 'CANCELLED', current_stage = 'CANCELLED', updated_at = now()
                WHERE id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                """
            ),
            {"sid": str(scan_id), "tid": str(tenant_id)},
        )

    async def mark_scan_failed(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        error_code: str,
        error_message: str,
    ) -> None:
        async with self._session.begin():
            await self._session.execute(
                text(
                    """
                    UPDATE scans
                    SET status = 'FAILED',
                        current_stage = 'FAILED',
                        percent_complete = 0,
                        error_code = :ec,
                        error_message = :em,
                        updated_at = now()
                    WHERE id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                    """
                ),
                {
                    "sid": str(scan_id),
                    "tid": str(tenant_id),
                    "ec": error_code[:256],
                    "em": error_message[:8192],
                },
            )

    async def mark_scan_complete_with_report(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        pdf_bytes: bytes,
        storage_uri: str,
    ) -> UUID:
        import hashlib

        checksum = hashlib.sha256(pdf_bytes).hexdigest()
        size_b = len(pdf_bytes)
        async with self._session.begin():
            res = await self._session.execute(
                text(
                    """
                    INSERT INTO artifacts (
                        tenant_id,
                        scan_id,
                        kind,
                        storage_uri,
                        checksum_sha256,
                        size_bytes,
                        encryption
                    ) VALUES (
                        CAST(:tid AS uuid),
                        CAST(:sid AS uuid),
                        'report_pdf',
                        :uri,
                        :sha,
                        :sz,
                        'sse-s3'
                    )
                    RETURNING id
                    """
                ),
                {
                    "tid": str(tenant_id),
                    "sid": str(scan_id),
                    "uri": storage_uri,
                    "sha": checksum,
                    "sz": size_b,
                },
            )
            art_id = cast(UUID, res.scalar_one())
            await self._session.execute(
                text(
                    """
                    UPDATE scans
                    SET status = 'COMPLETE',
                        current_stage = 'COMPLETE',
                        percent_complete = 100,
                        completed_at = now(),
                        updated_at = now(),
                        error_code = NULL,
                        error_message = NULL
                    WHERE id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                    """
                ),
                {"sid": str(scan_id), "tid": str(tenant_id)},
            )
        return art_id

    async def update_scan_post_hermes(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        repo_commit_sha: str | None,
        job_config_merge: dict[str, Any],
        current_stage: str,
        percent_complete: int,
    ) -> None:
        patch = json.dumps(job_config_merge)
        apply_sha = repo_commit_sha is not None
        async with self._session.begin():
            await self._session.execute(
                text(
                    """
                    UPDATE scans
                    SET repo_commit_sha = CASE
                            WHEN :apply_sha THEN CAST(:sha AS text)
                            ELSE repo_commit_sha
                        END,
                        job_config = job_config || CAST(:patch AS jsonb),
                        current_stage = :stage,
                        percent_complete = :pct,
                        updated_at = now()
                    WHERE id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                    """
                ),
                {
                    "apply_sha": apply_sha,
                    "sha": repo_commit_sha or "",
                    "patch": patch,
                    "stage": current_stage[:64],
                    "pct": percent_complete,
                    "sid": str(scan_id),
                    "tid": str(tenant_id),
                },
            )
