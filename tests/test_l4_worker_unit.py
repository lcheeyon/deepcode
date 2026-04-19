"""Phase L4 — worker stub loop, stream group helper (no Postgres)."""

from __future__ import annotations

import asyncio
import uuid
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock

from deepguard_api.repositories.scans import MemoryScanRepository, PostgresScanRepository
from deepguard_core.models import CreateScanRequest, RepoSpec, ScanLayers
from deepguard_worker.ingest_stub import heartbeat_and_cancel_poll_loop
from deepguard_worker.stream_util import ensure_scan_consumer_group
from fakeredis import FakeAsyncRedis
from pydantic import AnyHttpUrl


def _minimal_create_body() -> CreateScanRequest:
    return CreateScanRequest(
        repo=RepoSpec(url=cast(AnyHttpUrl, "https://github.com/acme/svc"), ref="main"),
        policy_ids=["ISO-27001-2022"],
        scan_layers=ScanLayers(code=True, iac=False, cloud=False),
    )


def test_ensure_scan_consumer_group_idempotent() -> None:
    async def run() -> None:
        r = FakeAsyncRedis(decode_responses=True)
        await ensure_scan_consumer_group(r)
        await ensure_scan_consumer_group(r)

    asyncio.run(run())


def test_heartbeat_sets_key_with_ttl() -> None:
    async def run() -> None:
        tenant_id = uuid.UUID("00000000-0000-4000-8000-000000000001")
        repo = MemoryScanRepository()
        row = await repo.create_scan(
            tenant_id=tenant_id,
            body=_minimal_create_body(),
            idempotency_key=None,
        )
        await repo.try_claim_scan_for_ingest(tenant_id=tenant_id, scan_id=row.id)
        redis = FakeAsyncRedis(decode_responses=True)
        await heartbeat_and_cancel_poll_loop(
            repo,
            redis,
            tenant_id=tenant_id,
            scan_id=row.id,
            heartbeat_interval_sec=0.01,
            iterations=1,
        )
        ttl = await redis.ttl(f"scan:{row.id}:heartbeat")
        assert ttl > 0

    asyncio.run(run())


def test_cooperative_cancel_marks_scan_cancelled() -> None:
    async def run() -> None:
        tenant_id = uuid.UUID("00000000-0000-4000-8000-000000000001")
        repo = MemoryScanRepository()
        row = await repo.create_scan(
            tenant_id=tenant_id,
            body=_minimal_create_body(),
            idempotency_key=None,
        )
        await repo.try_claim_scan_for_ingest(tenant_id=tenant_id, scan_id=row.id)
        await repo.set_cancellation_requested(tenant_id=tenant_id, scan_id=row.id)
        redis = FakeAsyncRedis(decode_responses=True)
        await heartbeat_and_cancel_poll_loop(
            repo,
            redis,
            tenant_id=tenant_id,
            scan_id=row.id,
            heartbeat_interval_sec=0.01,
            iterations=5,
        )
        out = await repo.get_scan(tenant_id=tenant_id, scan_id=row.id)
        assert out is not None
        assert out.status == "CANCELLED"
        assert out.current_stage == "CANCELLED"

    asyncio.run(run())


def test_heartbeat_postgres_repo_wraps_cancel_in_session_transaction() -> None:
    """``PostgresScanRepository`` cancel path uses ``session.begin()`` (L4 worker)."""

    async def run() -> None:
        begin_cm = MagicMock()
        begin_cm.__aenter__ = AsyncMock(return_value=None)
        begin_cm.__aexit__ = AsyncMock(return_value=None)
        session = MagicMock()
        session.begin = MagicMock(return_value=begin_cm)
        repo = PostgresScanRepository(cast(Any, session))

        async def _cancel_requested(**_: object) -> bool:
            return True

        repo.is_cancel_requested = _cancel_requested  # type: ignore[method-assign]
        repo.mark_cancelled = AsyncMock()  # type: ignore[method-assign]

        redis = FakeAsyncRedis(decode_responses=True)
        await heartbeat_and_cancel_poll_loop(
            repo,
            redis,
            tenant_id=uuid.UUID("00000000-0000-4000-8000-000000000001"),
            scan_id=uuid.UUID("00000000-0000-4000-8000-000000000002"),
            heartbeat_interval_sec=0.01,
            iterations=2,
        )
        session.begin.assert_called()
        repo.mark_cancelled.assert_awaited_once()

    asyncio.run(run())
