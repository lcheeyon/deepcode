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
class ScanRunEventRow:
    """One persisted workflow / timeline row (``scan_run_events``)."""

    id: UUID
    tenant_id: UUID
    scan_id: UUID
    event_seq: int
    event_type: str
    node: str | None
    correlation_id: str | None
    graph_version: str | None
    payload: dict[str, Any]
    created_at: datetime


@dataclass(frozen=True, slots=True)
class ExternalTraceRefRow:
    """LangSmith / LangFuse pointers for deep links."""

    id: UUID
    tenant_id: UUID
    scan_id: UUID
    vendor: str
    root_run_id: str | None
    trace_id: str | None
    project_id: str | None
    workspace_id: str | None
    trace_metadata: dict[str, Any]
    updated_at: datetime


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
    report_artifact_id: UUID | None = None

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
            report_artifact_id=self.report_artifact_id,
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

    async def mark_scan_awaiting_review(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        message: str | None = None,
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

    async def append_scan_run_event(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        event_type: str,
        node: str | None,
        payload: dict[str, Any],
        correlation_id: str | None,
        graph_version: str | None = None,
    ) -> ScanRunEventRow: ...

    async def list_scan_run_events(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        since_event_seq: int = 0,
        limit: int = 500,
    ) -> list[ScanRunEventRow]: ...

    async def upsert_external_trace_ref(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        vendor: str,
        root_run_id: str | None = None,
        trace_id: str | None = None,
        project_id: str | None = None,
        workspace_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None: ...

    async def list_external_trace_refs(
        self, *, tenant_id: UUID, scan_id: UUID
    ) -> list[ExternalTraceRefRow]: ...


class MemoryScanRepository:
    """In-process store for fast API tests (no Docker)."""

    def __init__(self) -> None:
        self._rows: dict[UUID, ScanRow] = {}
        self._idempotency: dict[tuple[UUID, str], UUID] = {}
        self._report_artifacts: dict[UUID, dict[str, Any]] = {}
        self._workflow_events: dict[tuple[UUID, UUID], list[ScanRunEventRow]] = {}
        self._trace_refs: dict[tuple[UUID, UUID], dict[str, ExternalTraceRefRow]] = {}
        self._event_seq_ctr = 0

    def report_storage_meta(self, scan_id: UUID) -> dict[str, Any] | None:
        """Return last persisted report artifact metadata (memory store; tests / diagnostics)."""

        return self._report_artifacts.get(scan_id)

    def report_pdf_download(
        self, *, scan_id: UUID, artifact_id: UUID
    ) -> tuple[bytes, str, str, datetime] | None:
        """Return ``(pdf_bytes, checksum_hex, storage_uri, created_at)`` if ids match."""

        meta = self._report_artifacts.get(scan_id)
        if meta is None:
            return None
        if str(meta.get("artifact_id")) != str(artifact_id):
            return None
        raw = meta.get("pdf_bytes")
        if not isinstance(raw, (bytes, bytearray)):
            return None
        created = meta.get("created_at")
        if not isinstance(created, datetime):
            created = datetime.now(UTC)
        return (
            bytes(raw),
            str(meta.get("checksum_sha256", "")),
            str(meta.get("storage_uri", "")),
            created,
        )

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
            report_artifact_id=None,
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

    async def mark_scan_awaiting_review(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        message: str | None = None,
    ) -> None:
        row = await self.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        if row is None:
            return
        self._put(
            replace(
                row,
                status="AWAITING_REVIEW",
                current_stage="AWAITING_REVIEW",
                percent_complete=max(row.percent_complete, 55),
                updated_at=datetime.now(UTC),
            )
        )
        _ = message

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
            "pdf_bytes": pdf_bytes,
            "created_at": datetime.now(UTC),
        }
        self._put(
            replace(
                row,
                status="COMPLETE",
                current_stage="COMPLETE",
                percent_complete=100,
                updated_at=datetime.now(UTC),
                report_artifact_id=aid,
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

    async def append_scan_run_event(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        event_type: str,
        node: str | None,
        payload: dict[str, Any],
        correlation_id: str | None,
        graph_version: str | None = None,
    ) -> ScanRunEventRow:
        row = await self.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        if row is None:
            msg = "scan not found"
            raise ValueError(msg)
        self._event_seq_ctr += 1
        eid = uuid4()
        now = datetime.now(UTC)
        ev = ScanRunEventRow(
            id=eid,
            tenant_id=tenant_id,
            scan_id=scan_id,
            event_seq=self._event_seq_ctr,
            event_type=event_type[:128],
            node=node[:256] if node else None,
            correlation_id=correlation_id[:512] if correlation_id else None,
            graph_version=graph_version[:128] if graph_version else None,
            payload=dict(payload),
            created_at=now,
        )
        key = (tenant_id, scan_id)
        self._workflow_events.setdefault(key, []).append(ev)
        return ev

    async def list_scan_run_events(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        since_event_seq: int = 0,
        limit: int = 500,
    ) -> list[ScanRunEventRow]:
        key = (tenant_id, scan_id)
        rows = [r for r in self._workflow_events.get(key, []) if r.event_seq > since_event_seq]
        rows.sort(key=lambda r: r.event_seq)
        return rows[:limit]

    async def upsert_external_trace_ref(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        vendor: str,
        root_run_id: str | None = None,
        trace_id: str | None = None,
        project_id: str | None = None,
        workspace_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        row = await self.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        if row is None:
            return
        now = datetime.now(UTC)
        key = (tenant_id, scan_id)
        bucket = self._trace_refs.setdefault(key, {})
        prev = bucket.get(vendor)
        rid = prev.id if prev else uuid4()
        rr = root_run_id if root_run_id is not None else (prev.root_run_id if prev else None)
        tr = trace_id if trace_id is not None else (prev.trace_id if prev else None)
        pr = project_id if project_id is not None else (prev.project_id if prev else None)
        ws = workspace_id if workspace_id is not None else (prev.workspace_id if prev else None)
        bucket[vendor] = ExternalTraceRefRow(
            id=rid,
            tenant_id=tenant_id,
            scan_id=scan_id,
            vendor=vendor[:64],
            root_run_id=rr,
            trace_id=tr,
            project_id=pr,
            workspace_id=ws,
            trace_metadata={**(prev.trace_metadata if prev else {}), **(metadata or {})},
            updated_at=now,
        )

    async def list_external_trace_refs(
        self, *, tenant_id: UUID, scan_id: UUID
    ) -> list[ExternalTraceRefRow]:
        key = (tenant_id, scan_id)
        return list(self._trace_refs.get(key, {}).values())


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
            report_artifact_id=m.get("report_artifact_id"),
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
                SELECT s.id, s.tenant_id, s.status, s.current_stage, s.percent_complete,
                       s.job_config, s.created_at, s.updated_at, s.idempotency_key,
                       s.repo_commit_sha, s.cancellation_requested,
                       (SELECT a.id FROM artifacts a
                        WHERE a.scan_id = s.id AND a.tenant_id = s.tenant_id
                          AND a.kind = 'report_pdf'
                        ORDER BY a.created_at DESC
                        LIMIT 1) AS report_artifact_id
                FROM scans s
                WHERE s.id = CAST(:sid AS uuid) AND s.tenant_id = CAST(:tid AS uuid)
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

    async def mark_scan_awaiting_review(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        message: str | None = None,
    ) -> None:
        async with self._session.begin():
            await self._session.execute(
                text(
                    """
                    UPDATE scans
                    SET status = 'AWAITING_REVIEW',
                        current_stage = 'AWAITING_REVIEW',
                        percent_complete = GREATEST(percent_complete, 55),
                        updated_at = now(),
                        error_code = NULL,
                        error_message = :msg
                    WHERE id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                    """
                ),
                {
                    "sid": str(scan_id),
                    "tid": str(tenant_id),
                    "msg": (message or "")[:8192] or None,
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

    async def append_scan_run_event(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        event_type: str,
        node: str | None,
        payload: dict[str, Any],
        correlation_id: str | None,
        graph_version: str | None = None,
    ) -> ScanRunEventRow:
        payload_json = json.dumps(payload)
        async with self._session.begin():
            res = await self._session.execute(
                text(
                    """
                    INSERT INTO scan_run_events (
                        tenant_id, scan_id, event_type, node, correlation_id,
                        graph_version, payload
                    ) VALUES (
                        CAST(:tid AS uuid), CAST(:sid AS uuid), :etype, :node, :corr,
                        :gver, CAST(:payload AS jsonb)
                    )
                    RETURNING id, tenant_id, scan_id, event_seq, event_type, node,
                              correlation_id, graph_version, payload, created_at
                    """
                ),
                {
                    "tid": str(tenant_id),
                    "sid": str(scan_id),
                    "etype": event_type[:128],
                    "node": node[:256] if node else None,
                    "corr": correlation_id[:512] if correlation_id else None,
                    "gver": graph_version[:128] if graph_version else None,
                    "payload": payload_json,
                },
            )
            m = res.mappings().one()
        pl = m["payload"]
        if isinstance(pl, str):
            pl = json.loads(pl)
        elif not isinstance(pl, dict):
            pl = dict(pl)
        return ScanRunEventRow(
            id=m["id"],
            tenant_id=m["tenant_id"],
            scan_id=m["scan_id"],
            event_seq=int(m["event_seq"]),
            event_type=str(m["event_type"]),
            node=m.get("node"),
            correlation_id=m.get("correlation_id"),
            graph_version=m.get("graph_version"),
            payload=pl,
            created_at=m["created_at"],
        )

    async def list_scan_run_events(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        since_event_seq: int = 0,
        limit: int = 500,
    ) -> list[ScanRunEventRow]:
        res = await self._session.execute(
            text(
                """
                SELECT id, tenant_id, scan_id, event_seq, event_type, node,
                       correlation_id, graph_version, payload, created_at
                FROM scan_run_events
                WHERE tenant_id = CAST(:tid AS uuid)
                  AND scan_id = CAST(:sid AS uuid)
                  AND event_seq > :since
                ORDER BY event_seq ASC
                LIMIT :lim
                """
            ),
            {"tid": str(tenant_id), "sid": str(scan_id), "since": since_event_seq, "lim": limit},
        )
        out: list[ScanRunEventRow] = []
        for m in res.mappings().all():
            pl = m["payload"]
            if isinstance(pl, str):
                pl = json.loads(pl)
            elif not isinstance(pl, dict):
                pl = dict(pl)
            out.append(
                ScanRunEventRow(
                    id=m["id"],
                    tenant_id=m["tenant_id"],
                    scan_id=m["scan_id"],
                    event_seq=int(m["event_seq"]),
                    event_type=str(m["event_type"]),
                    node=m.get("node"),
                    correlation_id=m.get("correlation_id"),
                    graph_version=m.get("graph_version"),
                    payload=pl,
                    created_at=m["created_at"],
                )
            )
        return out

    async def upsert_external_trace_ref(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        vendor: str,
        root_run_id: str | None = None,
        trace_id: str | None = None,
        project_id: str | None = None,
        workspace_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        meta = json.dumps(metadata or {})
        async with self._session.begin():
            await self._session.execute(
                text(
                    """
                    INSERT INTO scan_external_trace_refs (
                        tenant_id, scan_id, vendor, root_run_id, trace_id,
                        project_id, workspace_id, trace_metadata, updated_at
                    ) VALUES (
                        CAST(:tid AS uuid), CAST(:sid AS uuid), :vendor, :rr, :tr,
                        :pid, :wid, CAST(:meta AS jsonb), now()
                    )
                    ON CONFLICT (tenant_id, scan_id, vendor)
                    DO UPDATE SET
                        root_run_id = COALESCE(EXCLUDED.root_run_id,
                            scan_external_trace_refs.root_run_id),
                        trace_id = COALESCE(EXCLUDED.trace_id,
                            scan_external_trace_refs.trace_id),
                        project_id = COALESCE(EXCLUDED.project_id,
                            scan_external_trace_refs.project_id),
                        workspace_id = COALESCE(EXCLUDED.workspace_id,
                            scan_external_trace_refs.workspace_id),
                        trace_metadata = scan_external_trace_refs.trace_metadata
                            || EXCLUDED.trace_metadata,
                        updated_at = now()
                    """
                ),
                {
                    "tid": str(tenant_id),
                    "sid": str(scan_id),
                    "vendor": vendor[:64],
                    "rr": root_run_id,
                    "tr": trace_id,
                    "pid": project_id,
                    "wid": workspace_id,
                    "meta": meta,
                },
            )

    async def list_external_trace_refs(
        self, *, tenant_id: UUID, scan_id: UUID
    ) -> list[ExternalTraceRefRow]:
        res = await self._session.execute(
            text(
                """
                SELECT id, tenant_id, scan_id, vendor, root_run_id, trace_id,
                       project_id, workspace_id, trace_metadata, updated_at
                FROM scan_external_trace_refs
                WHERE tenant_id = CAST(:tid AS uuid) AND scan_id = CAST(:sid AS uuid)
                ORDER BY vendor
                """
            ),
            {"tid": str(tenant_id), "sid": str(scan_id)},
        )
        out: list[ExternalTraceRefRow] = []
        for m in res.mappings().all():
            meta = m["trace_metadata"]
            if isinstance(meta, str):
                meta = json.loads(meta)
            elif not isinstance(meta, dict):
                meta = dict(meta)
            out.append(
                ExternalTraceRefRow(
                    id=m["id"],
                    tenant_id=m["tenant_id"],
                    scan_id=m["scan_id"],
                    vendor=str(m["vendor"]),
                    root_run_id=m.get("root_run_id"),
                    trace_id=m.get("trace_id"),
                    project_id=m.get("project_id"),
                    workspace_id=m.get("workspace_id"),
                    trace_metadata=meta,
                    updated_at=m["updated_at"],
                )
            )
        return out
