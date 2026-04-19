"""Redis Streams helpers (consumer group + stale pending / ``XCLAIM`` notes)."""

from __future__ import annotations

from deepguard_core.queue import SCAN_CONSUMER_GROUP, SCAN_STREAM_KEY
from redis.asyncio import Redis
from redis.exceptions import ResponseError


async def ensure_scan_consumer_group(redis: Redis) -> None:
    """Create ``stream:scans`` and group ``workers`` if missing (idempotent).

    Stale pending entries (worker crash) are reclaimed with ``XCLAIM`` after the
    visibility timeout configured on ``XREADGROUP`` (e.g. 15m in production). This
    skeleton documents the contract; the watchdog loop is not implemented in L4.
    """

    try:
        await redis.xgroup_create(
            SCAN_STREAM_KEY,
            SCAN_CONSUMER_GROUP,
            id="0",
            mkstream=True,
        )
    except ResponseError as exc:
        if "BUSYGROUP" not in str(exc):
            raise
