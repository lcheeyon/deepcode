"""Publish scan jobs to Redis Streams (Phase L4 producer)."""

from __future__ import annotations

from typing import Any, cast
from uuid import UUID

from deepguard_core.queue import SCAN_STREAM_KEY, ScanJobMessage
from redis.asyncio import Redis


async def publish_scan_job(redis: Redis, *, tenant_id: UUID, scan_id: UUID) -> None:
    """Append a ``ScanJobMessage`` to ``stream:scans`` (Architecture §30.2)."""

    msg = ScanJobMessage(scan_id=scan_id, tenant_id=tenant_id)
    fields = msg.to_stream_fields()
    await redis.xadd(SCAN_STREAM_KEY, cast(Any, fields))
