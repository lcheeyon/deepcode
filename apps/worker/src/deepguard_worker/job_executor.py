"""Odysseus stub graph + PDF artifact + COMPLETE row (Phase L12)."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import queue
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID

from deepguard_agents.hermes_ingest import HermesExecutionError, run_hermes_phase
from deepguard_api.repositories.scans import PostgresScanRepository, ScanRepository
from deepguard_core.queue import scan_timeline_pubsub_channel
from deepguard_graph import __version__ as odysseus_graph_version
from deepguard_graph.checkpoint_pg import postgres_checkpointer
from deepguard_graph.checkpoint_resolve import resolve_checkpoint_postgres_uri
from deepguard_graph.compilation import compile_odysseus_app
from deepguard_graph.state import empty_odysseus_state
from deepguard_observability.correlation import graph_correlation_context, primary_correlation_id
from deepguard_observability.langchain_root_run import LangChainRootRunRecorder
from deepguard_observability.llm_callbacks import (
    build_langchain_callbacks,
    graph_invoke_config,
    langsmith_tracing_effective,
)
from deepguard_reporting.penelope_pdf import build_scan_pdf_bytes
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from redis.asyncio import Redis

from deepguard_worker.ingest_stub import heartbeat_and_cancel_poll_loop
from deepguard_worker.settings import WorkerSettings

log = logging.getLogger("deepguard_worker.job_executor")


def _want_hitl_interrupt_before_athena(job_config: dict[str, Any]) -> bool:
    raw = job_config.get("langgraph")
    if isinstance(raw, dict) and bool(raw.get("interrupt_before_athena")):
        return True
    return os.environ.get("LANGGRAPH_INTERRUPT_BEFORE_ATHENA", "").lower() in (
        "1",
        "true",
        "yes",
    )


def _hitl_outcome(final: dict[str, Any], *, hitl: bool) -> str:
    if not hitl:
        return "complete"
    log = final.get("execution_log") or []
    if "penelope" in log:
        return "complete"
    return "hitl"


def _invoke_odysseus_stub_graph(
    *,
    scan_id: str,
    tenant_id: str,
    job_config: dict[str, Any],
    correlation_id: str,
    trail: list[str],
    on_graph_node: Callable[[str], None] | None = None,
    timeline_emit: Callable[[str, str | None, dict[str, Any]], None] | None = None,
    idempotency_key: str | None = None,
    redis_message_id: str | None = None,
) -> tuple[dict[str, Any], str, LangChainRootRunRecorder]:
    """Run Odysseus with optional Postgres checkpointing, value streaming, and HITL."""

    init = empty_odysseus_state(
        scan_id=scan_id,
        created_at=datetime.now(UTC).replace(microsecond=0).isoformat(),
        job_config=job_config,
        tenant_id=tenant_id,
    )
    hitl = _want_hitl_interrupt_before_athena(job_config)
    recorder = LangChainRootRunRecorder()
    base_cbs = build_langchain_callbacks(
        scan_id=scan_id,
        tenant_id=tenant_id,
        run_name="odysseus-stub-graph",
    )
    cfg_callbacks = [*base_cbs, recorder]
    ctok = graph_correlation_context.set(correlation_id)
    try:
        cfg = cast(
            RunnableConfig,
            graph_invoke_config(
                scan_id=scan_id,
                tenant_id=tenant_id,
                callbacks=cfg_callbacks,
                run_name="odysseus-stub-graph",
                idempotency_key=idempotency_key,
                correlation_id=correlation_id,
                graph_version=odysseus_graph_version,
                redis_message_id=redis_message_id,
            ),
        )

        def _run_stream(app: Any) -> dict[str, Any]:
            last: dict[str, Any] | None = None
            for state in app.stream(init, config=cfg, stream_mode="values"):
                last = cast(dict[str, Any], state)
                if last.get("execution_log"):
                    name = str(last["execution_log"][-1])
                    prev = trail[-1] if trail else None
                    trail.append(name)
                    if on_graph_node:
                        on_graph_node(name)
                    if timeline_emit:
                        timeline_emit(
                            "node_progress",
                            name,
                            {"execution_log_tail": name, "stream_mode": "values"},
                        )
                        timeline_emit(
                            "otel_span_mirror",
                            None,
                            {
                                "span_name": f"graph.node.{name}",
                                "observation_kind": "GRAPH_NODE",
                            },
                        )
                        if prev is not None:
                            timeline_emit(
                                "agent_handoff",
                                None,
                                {
                                    "from_agent": prev,
                                    "to_agent": name,
                                    "message_type": "graph_edge",
                                    "summary": f"{prev}->{name}",
                                },
                            )
            if last is None:
                msg = "Odysseus graph produced no state"
                raise RuntimeError(msg)
            return last

        url = resolve_checkpoint_postgres_uri()
        if url:
            with postgres_checkpointer(url) as saver:
                app = compile_odysseus_app(
                    checkpointer=saver,
                    interrupt_before_athena=hitl,
                )
                final = _run_stream(app)
        else:
            app = compile_odysseus_app(
                checkpointer=MemorySaver(),
                interrupt_before_athena=hitl,
            )
            final = _run_stream(app)

        return final, _hitl_outcome(final, hitl=hitl), recorder
    finally:
        graph_correlation_context.reset(ctok)


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


async def _persist_timeline_event(
    repo: ScanRepository,
    redis: Redis,
    *,
    tenant_id: UUID,
    scan_id: UUID,
    event_type: str,
    node: str | None,
    payload: dict[str, Any],
    correlation_id: str,
    graph_version: str,
) -> None:
    row_ev = await repo.append_scan_run_event(
        tenant_id=tenant_id,
        scan_id=scan_id,
        event_type=event_type,
        node=node,
        payload=payload,
        correlation_id=correlation_id,
        graph_version=graph_version,
    )
    pub = {
        "id": str(row_ev.id),
        "event_seq": row_ev.event_seq,
        "event_type": row_ev.event_type,
        "node": row_ev.node,
        "correlation_id": row_ev.correlation_id,
        "graph_version": row_ev.graph_version,
        "created_at": row_ev.created_at.isoformat(),
        "payload": row_ev.payload,
    }
    await redis.publish(scan_timeline_pubsub_channel(scan_id=scan_id), json.dumps(pub))


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

    corr = primary_correlation_id(
        scan_id=str(scan_id),
        redis_message_id=os.environ.get("DEEPGUARD_REDIS_MESSAGE_ID"),
    )
    trail: list[str] = []
    pending: queue.SimpleQueue[tuple[str, str | None, dict[str, Any]]] = queue.SimpleQueue()
    stop_drain = False

    def timeline_emit(etype: str, node: str | None, payload: dict[str, Any]) -> None:
        pending.put((etype, node, payload))

    async def _drain_timeline_queue() -> None:
        while not stop_drain or not pending.empty():
            batch: list[tuple[str, str | None, dict[str, Any]]] = []
            try:
                while True:
                    batch.append(pending.get_nowait())
            except queue.Empty:
                pass
            for etype, node, payload in batch:
                await _persist_timeline_event(
                    repo,
                    redis,
                    tenant_id=tenant_id,
                    scan_id=scan_id,
                    event_type=etype,
                    node=node,
                    payload=payload,
                    correlation_id=corr,
                    graph_version=odysseus_graph_version,
                )
            if not batch:
                if stop_drain and pending.empty():
                    return
                await asyncio.sleep(0.05)

    await _persist_timeline_event(
        repo,
        redis,
        tenant_id=tenant_id,
        scan_id=scan_id,
        event_type="job_started",
        node=None,
        payload={"phase": "odysseus_graph", "graph_version": odysseus_graph_version},
        correlation_id=corr,
        graph_version=odysseus_graph_version,
    )

    recorder: LangChainRootRunRecorder
    drain_task = asyncio.create_task(_drain_timeline_queue())
    try:
        try:
            final, outcome, recorder = await asyncio.to_thread(
                _invoke_odysseus_stub_graph,
                scan_id=str(scan_id),
                tenant_id=str(tenant_id),
                job_config=row.job_config,
                correlation_id=corr,
                trail=trail,
                on_graph_node=None,
                timeline_emit=timeline_emit,
                idempotency_key=row.idempotency_key,
                redis_message_id=os.environ.get("DEEPGUARD_REDIS_MESSAGE_ID"),
            )
        except Exception as exc:
            log.exception("odysseus_invoke_failed scan_id=%s", scan_id)
            await repo.mark_scan_failed(
                tenant_id=tenant_id,
                scan_id=scan_id,
                error_code="GRAPH_INVOKE_FAILED",
                error_message=str(exc)[:8192],
            )
            try:
                await _persist_timeline_event(
                    repo,
                    redis,
                    tenant_id=tenant_id,
                    scan_id=scan_id,
                    event_type="job_error",
                    node=None,
                    payload={"error": str(exc)[:2048]},
                    correlation_id=corr,
                    graph_version=odysseus_graph_version,
                )
            except Exception:
                log.exception("timeline_job_error_failed scan_id=%s", scan_id)
            return
    finally:
        stop_drain = True
        await drain_task

    if trail:
        tail = ",".join(trail[-8:])
        await redis.set(hb_key, f"graph:{tail}", ex=120)

    if langsmith_tracing_effective() and recorder.root_run_id:
        try:
            await repo.upsert_external_trace_ref(
                tenant_id=tenant_id,
                scan_id=scan_id,
                vendor="langsmith",
                root_run_id=recorder.root_run_id,
                project_id=os.environ.get("LANGSMITH_PROJECT_ID", "").strip()
                or os.environ.get("LANGCHAIN_PROJECT", "").strip()
                or None,
                workspace_id=os.environ.get("LANGSMITH_ORGANIZATION_ID", "").strip() or None,
                metadata={"captured_by": "LangChainRootRunRecorder"},
            )
        except Exception:
            log.exception("langsmith_trace_ref_upsert_failed scan_id=%s", scan_id)

    if outcome == "hitl":
        await repo.mark_scan_awaiting_review(
            tenant_id=tenant_id,
            scan_id=scan_id,
            message="LangGraph interrupt_before athena (policy / HITL).",
        )
        log.info("scan_awaiting_review scan_id=%s tenant_id=%s", scan_id, tenant_id)
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
