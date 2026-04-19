"""Stub ingest loop: heartbeat + cooperative cancel (Phase L4, no LangGraph)."""

from __future__ import annotations

import asyncio
from uuid import UUID

from deepguard_api.repositories.scans import PostgresScanRepository, ScanRepository
from redis.asyncio import Redis


async def heartbeat_and_cancel_poll_loop(
    repo: ScanRepository,
    redis: Redis,
    *,
    tenant_id: UUID,
    scan_id: UUID,
    heartbeat_interval_sec: float,
    iterations: int,
) -> None:
    """Refresh Redis heartbeat (EX 120s) and honour DB ``cancellation_requested``."""

    hb_key = f"scan:{scan_id}:heartbeat"
    for _ in range(iterations):
        await redis.set(hb_key, "1", ex=120)
        await asyncio.sleep(heartbeat_interval_sec)
        if isinstance(repo, PostgresScanRepository):
            async with repo.session.begin():
                if await repo.is_cancel_requested(tenant_id=tenant_id, scan_id=scan_id):
                    await repo.mark_cancelled(tenant_id=tenant_id, scan_id=scan_id)
                    return
        else:
            if await repo.is_cancel_requested(tenant_id=tenant_id, scan_id=scan_id):
                await repo.mark_cancelled(tenant_id=tenant_id, scan_id=scan_id)
                return
