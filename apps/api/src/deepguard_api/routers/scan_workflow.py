"""Scan workflow timeline + SSE (US-DG-14-015 / US-DG-14-016)."""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import AsyncIterator
from typing import Annotated, Any
from uuid import UUID

from deepguard_api.auth_deps import get_dev_tenant_id
from deepguard_api.config import Settings
from deepguard_api.deps import get_scan_repository, get_settings
from deepguard_api.repositories.scans import (
    MemoryScanRepository,
    PostgresScanRepository,
    ScanRepository,
)
from deepguard_api.schemas import ScanWorkflowResponse, TraceLinksResponse
from deepguard_api.services.workflow_response import (
    TraceLinkBuildContext,
    build_scan_workflow_response,
    build_trace_link_items,
)
from deepguard_core.queue import scan_timeline_pubsub_channel
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

log = logging.getLogger("deepguard_api.scan_workflow")

router = APIRouter(prefix="/scans", tags=["scans"])


def _event_payload_public(ev: Any) -> dict[str, Any]:
    return {
        "id": str(ev.id),
        "event_seq": ev.event_seq,
        "event_type": ev.event_type,
        "node": ev.node,
        "correlation_id": ev.correlation_id,
        "graph_version": ev.graph_version,
        "created_at": ev.created_at.isoformat(),
        "payload": ev.payload if isinstance(ev.payload, dict) else {},
    }


@router.get("/{scan_id}/workflow", response_model=ScanWorkflowResponse)
async def get_scan_workflow(
    scan_id: UUID,
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
    repo: Annotated[ScanRepository, Depends(get_scan_repository)],
    settings: Annotated[Settings, Depends(get_settings)],
    include_events: Annotated[bool, Query(alias="include_events")] = True,
) -> ScanWorkflowResponse:
    row = await repo.get_scan(tenant_id=tenant_id, scan_id=scan_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="scan not found")
    events = await repo.list_scan_run_events(
        tenant_id=tenant_id, scan_id=scan_id, since_event_seq=0, limit=500
    )
    refs = await repo.list_external_trace_refs(tenant_id=tenant_id, scan_id=scan_id)
    ctx = TraceLinkBuildContext(
        langsmith_ui_origin=settings.langsmith_ui_origin,
        langsmith_organization_id=settings.langsmith_organization_id,
        langsmith_project_id=settings.langsmith_project_id,
        langfuse_host=settings.langfuse_public_host,
    )
    return build_scan_workflow_response(
        scan=row,
        events=events,
        trace_refs=refs,
        include_events=include_events,
        trace_ctx=ctx,
    )


@router.get("/{scan_id}/trace-links", response_model=TraceLinksResponse)
async def get_trace_links(
    scan_id: UUID,
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
    repo: Annotated[ScanRepository, Depends(get_scan_repository)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> TraceLinksResponse:
    row = await repo.get_scan(tenant_id=tenant_id, scan_id=scan_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="scan not found")
    refs = await repo.list_external_trace_refs(tenant_id=tenant_id, scan_id=scan_id)
    ctx = TraceLinkBuildContext(
        langsmith_ui_origin=settings.langsmith_ui_origin,
        langsmith_organization_id=settings.langsmith_organization_id,
        langsmith_project_id=settings.langsmith_project_id,
        langfuse_host=settings.langfuse_public_host,
    )
    links = build_trace_link_items(refs, ctx)
    return TraceLinksResponse(scan_id=row.id, links=links)


@router.get("/{scan_id}/workflow/stream")
async def stream_scan_workflow(
    request: Request,
    scan_id: UUID,
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> Any:
    from starlette.responses import StreamingResponse

    mem: MemoryScanRepository | None = getattr(request.app.state, "memory_repo", None)
    maker: async_sessionmaker[AsyncSession] | None = getattr(
        request.app.state, "session_maker", None
    )
    redis: Redis | None = getattr(request.app.state, "redis", None)

    row = None
    if settings.use_memory_store and mem is not None:
        row = await mem.get_scan(tenant_id=tenant_id, scan_id=scan_id)
    elif maker is not None:
        async with maker() as session:
            row = await PostgresScanRepository(session).get_scan(
                tenant_id=tenant_id, scan_id=scan_id
            )
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="scan not found")

    channel = scan_timeline_pubsub_channel(scan_id=scan_id)

    async def gen() -> AsyncIterator[bytes]:
        since_seq = 0
        pubsub = redis.pubsub(ignore_subscribe_messages=True) if redis is not None else None
        if pubsub is not None:
            await pubsub.subscribe(channel)
        try:
            if settings.use_memory_store and mem is not None:
                while True:
                    rows = await mem.list_scan_run_events(
                        tenant_id=tenant_id, scan_id=scan_id, since_event_seq=since_seq, limit=50
                    )
                    if not rows:
                        yield b":\n\n"
                        await asyncio.sleep(1.0)
                        continue
                    for ev in rows:
                        since_seq = ev.event_seq
                        yield ("data: " + json.dumps(_event_payload_public(ev)) + "\n\n").encode()
            elif maker is not None:
                while True:
                    async with maker() as session:
                        repo = PostgresScanRepository(session)
                        rows = await repo.list_scan_run_events(
                            tenant_id=tenant_id,
                            scan_id=scan_id,
                            since_event_seq=since_seq,
                            limit=50,
                        )
                    for ev in rows:
                        since_seq = ev.event_seq
                        yield ("data: " + json.dumps(_event_payload_public(ev)) + "\n\n").encode()
                    got_redis = False
                    if pubsub is not None:
                        msg = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                        if msg and msg.get("type") == "message" and msg.get("data"):
                            try:
                                raw = msg["data"]
                                if isinstance(raw, bytes):
                                    raw = raw.decode()
                                parsed = json.loads(raw)
                                seq = int(parsed.get("event_seq", 0))
                                if seq > since_seq:
                                    since_seq = seq
                                    yield ("data: " + json.dumps(parsed) + "\n\n").encode()
                                    got_redis = True
                            except (json.JSONDecodeError, TypeError, ValueError):
                                log.debug("timeline_pubsub_bad_message", exc_info=True)
                    if not rows and not got_redis:
                        yield b":\n\n"
                        await asyncio.sleep(0.2)
            else:
                yield b"data: {\"error\":\"workflow_stream_unavailable\"}\n\n"
        finally:
            if pubsub is not None:
                await pubsub.unsubscribe(channel)
                await pubsub.aclose()

    return StreamingResponse(gen(), media_type="text/event-stream")
