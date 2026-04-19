"""Console data access: findings triage, artifacts, policy uploads (US-DG-12-004–006)."""

from __future__ import annotations

import csv
import io
import json
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, Protocol, cast
from uuid import UUID, uuid4, uuid5

from deepguard_core.models.agent_error import AgentRuntimeError
from deepguard_policies.parse import parse_policy_file
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from deepguard_api.config import Settings
from deepguard_api.repositories.scans import MemoryScanRepository
from deepguard_api.s3_presign import parse_s3_uri, presigned_get_url
from deepguard_api.schemas import (
    ArtifactSummary,
    FindingListItem,
    FindingsPage,
    PolicyUploadListItem,
    PolicyUploadListResponse,
    PolicyUploadResponse,
    PolicyUploadWarning,
)


@dataclass(frozen=True, slots=True)
class ArtifactDownload:
    mode: Literal["redirect", "bytes"]
    redirect_url: str | None = None
    content: bytes | None = None
    media_type: str = "application/pdf"


class ConsoleStore(Protocol):
    async def assert_scan_owned(self, *, tenant_id: UUID, scan_id: UUID) -> None: ...

    async def list_findings(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        cursor: UUID | None,
        limit: int,
        severity: str | None,
        framework: str | None,
    ) -> FindingsPage: ...

    async def list_findings_for_export(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        finding_ids: Sequence[UUID] | None,
        severity: str | None,
        framework: str | None,
    ) -> list[FindingListItem]: ...

    async def list_artifacts(
        self, *, tenant_id: UUID, scan_id: UUID
    ) -> list[ArtifactSummary]: ...

    async def resolve_artifact_download(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        artifact_id: UUID,
        settings: Settings,
    ) -> ArtifactDownload | None: ...

    async def upload_policy(
        self, *, tenant_id: UUID, filename: str, data: bytes
    ) -> PolicyUploadResponse: ...

    async def list_policy_uploads(self, *, tenant_id: UUID) -> PolicyUploadListResponse: ...


_STUB_NS = UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")


def _stub_findings(scan_id: UUID) -> list[FindingListItem]:
    now = datetime.now(UTC)
    return [
        FindingListItem(
            finding_id=uuid5(_STUB_NS, f"{scan_id}-f1"),
            framework="ISO27001",
            control_id="A.10.1",
            status="FAIL",
            severity="HIGH",
            title="TLS minimum version not enforced",
            evidence_refs=[
                {
                    "type": "file_reference",
                    "path": "src/tls.py",
                    "line": 42,
                    "snippet": "ssl.PROTOCOL_TLS",
                }
            ],
            reasoning_summary="Server accepts legacy TLS handshakes.",
            confidence_score=0.81,
            policy_version="iso-2026-01",
            created_at=now,
        ),
        FindingListItem(
            finding_id=uuid5(_STUB_NS, f"{scan_id}-f2"),
            framework="SOC2",
            control_id="CC6.1",
            status="PARTIAL",
            severity="MEDIUM",
            title="Secrets scanning gaps in CI",
            evidence_refs=[{"type": "config_snippet", "path": ".github/workflows/ci.yml"}],
            reasoning_summary="No gitleaks or equivalent stage detected.",
            confidence_score=0.62,
            policy_version="soc2-2025",
            created_at=now,
        ),
    ]


def _filter_findings(
    items: Sequence[FindingListItem],
    *,
    severity: str | None,
    framework: str | None,
) -> list[FindingListItem]:
    out = list(items)
    if severity:
        out = [x for x in out if x.severity.upper() == severity.upper()]
    if framework:
        fw = framework.strip().lower()
        out = [x for x in out if x.framework.lower() == fw or fw in x.framework.lower()]
    return out


class MemoryConsoleStore:
    """In-memory findings stubs + policy uploads; artifacts from ``MemoryScanRepository``."""

    def __init__(self, scans: MemoryScanRepository) -> None:
        self._scans = scans
        self._finding_rows: dict[UUID, list[FindingListItem]] = {}
        self._policy_uploads: list[dict[str, Any]] = []

    async def assert_scan_owned(self, *, tenant_id: UUID, scan_id: UUID) -> None:
        row = await self._scans.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        if row is None:
            raise LookupError("scan not found")

    def _memory_findings(self, scan_id: UUID) -> list[FindingListItem]:
        if scan_id in self._finding_rows:
            return list(self._finding_rows[scan_id])
        return _stub_findings(scan_id)

    async def list_findings(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        cursor: UUID | None,
        limit: int,
        severity: str | None,
        framework: str | None,
    ) -> FindingsPage:
        await self.assert_scan_owned(tenant_id=tenant_id, scan_id=scan_id)
        rows = _filter_findings(
            self._memory_findings(scan_id),
            severity=severity,
            framework=framework,
        )
        rows.sort(key=lambda r: r.finding_id)
        if cursor is not None:
            rows = [r for r in rows if r.finding_id > cursor]
        take = min(max(limit, 1), 100)
        page = rows[: take + 1]
        has_more = len(page) > take
        items = page[:take]
        next_cursor = str(items[-1].finding_id) if has_more and items else None
        return FindingsPage(items=items, next_cursor=next_cursor)

    async def list_findings_for_export(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        finding_ids: Sequence[UUID] | None,
        severity: str | None,
        framework: str | None,
    ) -> list[FindingListItem]:
        await self.assert_scan_owned(tenant_id=tenant_id, scan_id=scan_id)
        rows = _filter_findings(
            self._memory_findings(scan_id),
            severity=severity,
            framework=framework,
        )
        if finding_ids:
            wanted = {UUID(str(x)) for x in finding_ids}
            rows = [r for r in rows if r.finding_id in wanted]
        return rows[:5000]

    async def list_artifacts(
        self, *, tenant_id: UUID, scan_id: UUID
    ) -> list[ArtifactSummary]:
        await self.assert_scan_owned(tenant_id=tenant_id, scan_id=scan_id)
        meta = self._scans.report_storage_meta(scan_id)
        if meta is None:
            return []
        created = meta.get("created_at")
        if not isinstance(created, datetime):
            created = datetime.now(UTC)
        return [
            ArtifactSummary(
                artifact_id=UUID(str(meta["artifact_id"])),
                kind="report_pdf",
                checksum_sha256=str(meta["checksum_sha256"]),
                size_bytes=int(meta["size_bytes"]),
                storage_uri=str(meta["storage_uri"]),
                created_at=created,
            )
        ]

    async def resolve_artifact_download(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        artifact_id: UUID,
        settings: Settings,
    ) -> ArtifactDownload | None:
        _ = settings
        row = await self._scans.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        if row is None:
            return None
        hit = self._scans.report_pdf_download(scan_id=scan_id, artifact_id=artifact_id)
        if hit is None:
            return None
        pdf_bytes, _checksum, _uri, _created = hit
        return ArtifactDownload(mode="bytes", content=pdf_bytes, media_type="application/pdf")

    async def upload_policy(
        self, *, tenant_id: UUID, filename: str, data: bytes
    ) -> PolicyUploadResponse:
        _ = tenant_id
        suffix = Path(filename).suffix.lower()
        if suffix not in {".yaml", ".yml"}:
            raise ValueError("Only YAML policy fixtures are supported for upload.")

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tf:
            tf.write(data)
            tmp_path = Path(tf.name)
        try:
            parsed = parse_policy_file(tmp_path)
        except AgentRuntimeError as exc:
            raise ValueError(exc.record.message) from exc
        finally:
            tmp_path.unlink(missing_ok=True)

        warnings: list[PolicyUploadWarning] = []
        if len(parsed.controls) > 200:
            warnings.append(
                PolicyUploadWarning(
                    detail="Large policy: consider splitting controls across files.",
                )
            )
        uid = uuid4()
        self._policy_uploads.append(
            {
                "upload_id": uid,
                "policy_version": parsed.policy_version,
                "source_filename": filename,
                "controls_extracted": len(parsed.controls),
                "warnings": [w.model_dump() for w in warnings],
                "created_at": datetime.now(UTC),
            }
        )
        return PolicyUploadResponse(
            upload_id=uid,
            policy_version=parsed.policy_version,
            controls_extracted=len(parsed.controls),
            warnings=warnings,
            source_filename=filename,
        )

    async def list_policy_uploads(self, *, tenant_id: UUID) -> PolicyUploadListResponse:
        _ = tenant_id
        items: list[PolicyUploadListItem] = []
        for row in reversed(self._policy_uploads[-50:]):
            items.append(
                PolicyUploadListItem(
                    upload_id=row["upload_id"],
                    policy_version=row["policy_version"],
                    source_filename=row["source_filename"],
                    controls_extracted=int(row["controls_extracted"]),
                    warnings=[PolicyUploadWarning(**w) for w in row.get("warnings", [])],
                    created_at=row["created_at"],
                )
            )
        return PolicyUploadListResponse(uploads=items)


class PostgresConsoleStore:
    """Postgres-backed console queries (findings + artifacts + policy upload audit)."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def assert_scan_owned(self, *, tenant_id: UUID, scan_id: UUID) -> None:
        res = await self._session.execute(
            text(
                """
                SELECT 1 FROM scans
                WHERE id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                """
            ),
            {"sid": str(scan_id), "tid": str(tenant_id)},
        )
        if res.first() is None:
            raise LookupError("scan not found")

    def _row_to_finding(self, m: dict[str, Any]) -> FindingListItem:
        ev = m["evidence_refs"]
        if isinstance(ev, str):
            ev = json.loads(ev)
        if not isinstance(ev, list):
            ev = []
        return FindingListItem(
            finding_id=m["id"],
            framework=str(m["framework"]),
            control_id=str(m["control_id"]),
            status=str(m["status"]),
            severity=str(m["severity"]),
            title=str(m["title"]),
            evidence_refs=[cast(dict[str, Any], x) for x in ev if isinstance(x, dict)],
            reasoning_summary=m.get("reasoning_summary"),
            confidence_score=float(m["confidence_score"]),
            policy_version=str(m["policy_version"]),
            created_at=m["created_at"],
        )

    async def list_findings(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        cursor: UUID | None,
        limit: int,
        severity: str | None,
        framework: str | None,
    ) -> FindingsPage:
        await self.assert_scan_owned(tenant_id=tenant_id, scan_id=scan_id)
        take = min(max(limit, 1), 100)
        cursor_sql = "TRUE" if cursor is None else "id > CAST(:cursor AS uuid)"
        res = await self._session.execute(
            text(
                f"""
                SELECT id, framework, control_id, status, severity, title, evidence_refs,
                       reasoning_summary, confidence_score, policy_version, created_at
                FROM findings
                WHERE scan_id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                  AND ({cursor_sql})
                  AND (:sev IS NULL OR severity = :sev)
                  AND (:fw IS NULL OR framework ILIKE ('%' || :fw || '%'))
                ORDER BY id ASC
                LIMIT :lim
                """
            ),
            {
                "sid": str(scan_id),
                "tid": str(tenant_id),
                **({"cursor": str(cursor)} if cursor is not None else {}),
                "sev": severity,
                "fw": framework,
                "lim": take + 1,
            },
        )
        rows = [self._row_to_finding(dict(r)) for r in res.mappings().all()]
        has_more = len(rows) > take
        items = rows[:take]
        next_cursor = str(items[-1].finding_id) if has_more and items else None
        return FindingsPage(items=items, next_cursor=next_cursor)

    async def list_findings_for_export(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        finding_ids: Sequence[UUID] | None,
        severity: str | None,
        framework: str | None,
    ) -> list[FindingListItem]:
        await self.assert_scan_owned(tenant_id=tenant_id, scan_id=scan_id)
        if finding_ids:
            ids = [UUID(str(x)) for x in finding_ids]
            if not ids:
                return []
            ph = ", ".join(f":fid{i}" for i in range(len(ids)))
            params: dict[str, Any] = {
                "sid": str(scan_id),
                "tid": str(tenant_id),
            }
            for i, u in enumerate(ids):
                params[f"fid{i}"] = str(u)
            res = await self._session.execute(
                text(
                    f"""
                    SELECT id, framework, control_id, status, severity, title, evidence_refs,
                           reasoning_summary, confidence_score, policy_version, created_at
                    FROM findings
                    WHERE scan_id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                      AND id IN ({ph})
                    ORDER BY id ASC
                    LIMIT 5000
                    """
                ),
                params,
            )
            return [self._row_to_finding(dict(r)) for r in res.mappings().all()]
        res = await self._session.execute(
            text(
                """
                SELECT id, framework, control_id, status, severity, title, evidence_refs,
                       reasoning_summary, confidence_score, policy_version, created_at
                FROM findings
                WHERE scan_id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                  AND (:sev IS NULL OR severity = :sev)
                  AND (:fw IS NULL OR framework ILIKE ('%' || :fw || '%'))
                ORDER BY id ASC
                LIMIT 5000
                """
            ),
            {"sid": str(scan_id), "tid": str(tenant_id), "sev": severity, "fw": framework},
        )
        return [self._row_to_finding(dict(r)) for r in res.mappings().all()]

    async def list_artifacts(
        self, *, tenant_id: UUID, scan_id: UUID
    ) -> list[ArtifactSummary]:
        await self.assert_scan_owned(tenant_id=tenant_id, scan_id=scan_id)
        res = await self._session.execute(
            text(
                """
                SELECT id, kind, checksum_sha256, size_bytes, storage_uri, created_at
                FROM artifacts
                WHERE scan_id = CAST(:sid AS uuid) AND tenant_id = CAST(:tid AS uuid)
                ORDER BY created_at DESC
                """
            ),
            {"sid": str(scan_id), "tid": str(tenant_id)},
        )
        out: list[ArtifactSummary] = []
        for r in res.mappings().all():
            m = dict(r)
            out.append(
                ArtifactSummary(
                    artifact_id=m["id"],
                    kind=str(m["kind"]),
                    checksum_sha256=str(m["checksum_sha256"]),
                    size_bytes=int(m["size_bytes"]),
                    storage_uri=str(m["storage_uri"]),
                    created_at=m["created_at"],
                )
            )
        return out

    async def resolve_artifact_download(
        self,
        *,
        tenant_id: UUID,
        scan_id: UUID,
        artifact_id: UUID,
        settings: Settings,
    ) -> ArtifactDownload | None:
        res = await self._session.execute(
            text(
                """
                SELECT id, storage_uri, kind
                FROM artifacts
                WHERE id = CAST(:aid AS uuid)
                  AND scan_id = CAST(:sid AS uuid)
                  AND tenant_id = CAST(:tid AS uuid)
                """
            ),
            {"aid": str(artifact_id), "sid": str(scan_id), "tid": str(tenant_id)},
        )
        m = res.mappings().first()
        if m is None:
            return None
        uri = str(m["storage_uri"])
        parsed = parse_s3_uri(uri)
        if parsed is None:
            return None
        bucket, key = parsed
        if not settings.s3_repo_upload_configured():
            return None
        url = presigned_get_url(
            bucket=bucket,
            key=key,
            endpoint_url=settings.s3_endpoint_url,
            access_key_id=settings.s3_access_key_id or "",
            secret_access_key=settings.s3_secret_access_key or "",
            region=settings.s3_region,
        )
        return ArtifactDownload(mode="redirect", redirect_url=url, media_type="application/pdf")

    async def upload_policy(
        self, *, tenant_id: UUID, filename: str, data: bytes
    ) -> PolicyUploadResponse:
        suffix = Path(filename).suffix.lower()
        if suffix not in {".yaml", ".yml"}:
            raise ValueError("Only YAML policy fixtures are supported for upload.")

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tf:
            tf.write(data)
            tmp_path = Path(tf.name)
        try:
            parsed = parse_policy_file(tmp_path)
        except AgentRuntimeError as exc:
            raise ValueError(exc.record.message) from exc
        finally:
            tmp_path.unlink(missing_ok=True)

        warnings: list[PolicyUploadWarning] = []
        if len(parsed.controls) > 200:
            warnings.append(
                PolicyUploadWarning(
                    detail="Large policy: consider splitting controls across files.",
                )
            )
        uid = uuid4()
        await self._session.execute(
            text(
                """
                INSERT INTO policy_uploads (
                    id, tenant_id, policy_version, source_filename, controls_extracted, warnings
                ) VALUES (
                    CAST(:id AS uuid),
                    CAST(:tid AS uuid),
                    :pv,
                    :fn,
                    :nctrl,
                    CAST(:warn AS jsonb)
                )
                """
            ),
            {
                "id": str(uid),
                "tid": str(tenant_id),
                "pv": parsed.policy_version[:512],
                "fn": filename[:512],
                "nctrl": len(parsed.controls),
                "warn": json.dumps([w.model_dump() for w in warnings]),
            },
        )
        return PolicyUploadResponse(
            upload_id=uid,
            policy_version=parsed.policy_version,
            controls_extracted=len(parsed.controls),
            warnings=warnings,
            source_filename=filename,
        )

    async def list_policy_uploads(self, *, tenant_id: UUID) -> PolicyUploadListResponse:
        res = await self._session.execute(
            text(
                """
                SELECT id, policy_version, source_filename, controls_extracted, warnings, created_at
                FROM policy_uploads
                WHERE tenant_id = CAST(:tid AS uuid)
                ORDER BY created_at DESC
                LIMIT 50
                """
            ),
            {"tid": str(tenant_id)},
        )
        items: list[PolicyUploadListItem] = []
        for r in res.mappings().all():
            m = dict(r)
            raw_warn = m.get("warnings") or []
            if isinstance(raw_warn, str):
                raw_warn = json.loads(raw_warn)
            warn_objs: list[PolicyUploadWarning] = []
            if isinstance(raw_warn, list):
                for w in raw_warn:
                    if isinstance(w, dict) and "detail" in w:
                        warn_objs.append(PolicyUploadWarning(detail=str(w["detail"])))
            items.append(
                PolicyUploadListItem(
                    upload_id=m["id"],
                    policy_version=str(m["policy_version"]),
                    source_filename=str(m["source_filename"]),
                    controls_extracted=int(m["controls_extracted"]),
                    warnings=warn_objs,
                    created_at=m["created_at"],
                )
            )
        return PolicyUploadListResponse(uploads=items)


def export_findings_csv(items: Sequence[FindingListItem]) -> str:
    buf = io.StringIO()
    buf.write("# deepguard-findings-export v1\n")
    w = csv.writer(buf)
    w.writerow(
        [
            "finding_id",
            "framework",
            "control_id",
            "status",
            "severity",
            "title",
            "confidence_score",
            "policy_version",
            "created_at",
        ]
    )
    for it in items:
        w.writerow(
            [
                str(it.finding_id),
                it.framework,
                it.control_id,
                it.status,
                it.severity,
                it.title,
                it.confidence_score,
                it.policy_version,
                it.created_at.isoformat(),
            ]
        )
    return buf.getvalue()


def export_findings_json(items: Sequence[FindingListItem]) -> str:
    payload = {
        "schema": "deepguard-findings-export@1",
        "findings": [it.model_dump(mode="json") for it in items],
    }
    return json.dumps(payload, indent=2)
