"""Odysseus stub graph + PDF artifact + COMPLETE row (Phase L12)."""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from deepguard_agents.hermes_ingest import HermesExecutionError, run_hermes_phase
from deepguard_api.repositories.scans import PostgresScanRepository, ScanRepository
from deepguard_graph.graph import build_odysseus_graph
from deepguard_graph.state import empty_odysseus_state
from deepguard_reporting.penelope_pdf import build_scan_pdf_bytes
from langgraph.checkpoint.memory import MemorySaver
from redis.asyncio import Redis

from deepguard_worker.ingest_stub import heartbeat_and_cancel_poll_loop
from deepguard_worker.settings import WorkerSettings

log = logging.getLogger("deepguard_worker.job_executor")


def _invoke_odysseus_stub_graph(*, scan_id: str, job_config: dict[str, Any]) -> dict[str, Any]:
    app = build_odysseus_graph().compile(checkpointer=MemorySaver())
    init = empty_odysseus_state(
        scan_id=scan_id,
        created_at=datetime.now(UTC).replace(microsecond=0).isoformat(),
        job_config=job_config,
    )
    return app.invoke(
        init,
        config={"configurable": {"thread_id": scan_id}},
    )


def _finding_titles_from_graph_state(final: dict[str, Any]) -> list[str]:
    raw = final.get("stub_findings") or []
    out: list[str] = []
    for x in raw:
        s = str(x)
        out.append(s.removeprefix("finding:"))
    return out if out else ["stub-placeholder"]


async def _cancel_poll_once(repo: ScanRepository, *, tenant_id: UUID, scan_id: UUID) -> bool:
    if isinstance(repo, PostgresScanRepository):
        async with repo.session.begin():
            if await repo.is_cancel_requested(tenant_id=tenant_id, scan_id=scan_id):
                await repo.mark_cancelled(tenant_id=tenant_id, scan_id=scan_id)
                return True
    else:
        if await repo.is_cancel_requested(tenant_id=tenant_id, scan_id=scan_id):
            await repo.mark_cancelled(tenant_id=tenant_id, scan_id=scan_id)
            return True
    return False


async def run_scan_job_pipeline(
    repo: ScanRepository,
    redis: Redis,
    *,
    tenant_id: UUID,
    scan_id: UUID,
    heartbeat_interval_sec: float,
    stub_iterations: int,
    worker_settings: WorkerSettings,
) -> None:
    """Heartbeat + optional cooperative-cancel loop, then stub graph, PDF, and ``COMPLETE``."""

    hb_key = f"scan:{scan_id}:heartbeat"
    await redis.set(hb_key, "1", ex=120)
    if stub_iterations > 0:
        await heartbeat_and_cancel_poll_loop(
            repo,
            redis,
            tenant_id=tenant_id,
            scan_id=scan_id,
            heartbeat_interval_sec=heartbeat_interval_sec,
            iterations=stub_iterations,
        )
    else:
        if await _cancel_poll_once(repo, tenant_id=tenant_id, scan_id=scan_id):
            return

    row = await repo.get_scan(tenant_id=tenant_id, scan_id=scan_id)
    if row is None or row.status == "CANCELLED":
        return

    hermes_cfg = worker_settings.hermes_runtime()
    try:
        hermes_out = await asyncio.to_thread(
            run_hermes_phase,
            row.job_config,
            tenant_id=str(tenant_id),
            scan_id=str(scan_id),
            cfg=hermes_cfg,
        )
    except HermesExecutionError as exc:
        log.warning("hermes_failed scan_id=%s code=%s", scan_id, exc.code)
        await repo.mark_scan_failed(
            tenant_id=tenant_id,
            scan_id=scan_id,
            error_code=exc.code,
            error_message=exc.message[:8192],
        )
        return

    if hermes_out is not None:
        resolved_sha, merge = hermes_out
        await repo.update_scan_post_hermes(
            tenant_id=tenant_id,
            scan_id=scan_id,
            repo_commit_sha=resolved_sha,
            job_config_merge=merge,
            current_stage="ANALYZING",
            percent_complete=15,
        )
        row = await repo.get_scan(tenant_id=tenant_id, scan_id=scan_id)
        if row is None or row.status in ("FAILED", "CANCELLED"):
            return

    try:
        final = await asyncio.to_thread(
            _invoke_odysseus_stub_graph,
            scan_id=str(scan_id),
            job_config=row.job_config,
        )
    except Exception as exc:
        log.exception("odysseus_invoke_failed scan_id=%s", scan_id)
        await repo.mark_scan_failed(
            tenant_id=tenant_id,
            scan_id=scan_id,
            error_code="GRAPH_INVOKE_FAILED",
            error_message=str(exc)[:8192],
        )
        return

    titles = _finding_titles_from_graph_state(final)
    # fpdf layout uses document margins; avoid ``asyncio.to_thread`` (fpdf is not thread-safe).
    pdf = build_scan_pdf_bytes(scan_id=str(scan_id), finding_titles=titles)
    uri = f"s3://deepguard-dev/reports/{tenant_id}/{scan_id}/report.pdf"
    await repo.mark_scan_complete_with_report(
        tenant_id=tenant_id,
        scan_id=scan_id,
        pdf_bytes=pdf,
        storage_uri=uri,
    )
    log.info("scan_complete scan_id=%s tenant_id=%s", scan_id, tenant_id)
