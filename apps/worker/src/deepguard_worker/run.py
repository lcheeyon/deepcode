"""Redis Streams consumer + DB updates (Phase L4 worker skeleton)."""

from __future__ import annotations

import logging

import redis.asyncio as redis_async
from deepguard_api.repositories.scans import PostgresScanRepository
from deepguard_core.queue import SCAN_CONSUMER_GROUP, SCAN_STREAM_KEY, ScanJobMessage
from deepguard_observability.runtime import configure_observability_at_startup
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from deepguard_worker.job_executor import run_scan_job_pipeline
from deepguard_worker.settings import WorkerSettings, load_worker_settings
from deepguard_worker.stream_util import ensure_scan_consumer_group

log = logging.getLogger("deepguard_worker")


async def run_worker(*, settings: WorkerSettings | None = None) -> None:
    """Blocking loop: read ``stream:scans``, claim ``QUEUED`` rows, stub ingest."""

    cfg = settings or load_worker_settings()
    configure_observability_at_startup(service_name="deepguard-worker")
    engine = create_async_engine(cfg.database_url, pool_pre_ping=True)
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    redis = redis_async.from_url(cfg.redis_url, decode_responses=True)
    await ensure_scan_consumer_group(redis)
    log.info("worker_started consumer=%s", cfg.consumer_name)
    try:
        while True:
            resp = await redis.xreadgroup(
                SCAN_CONSUMER_GROUP,
                cfg.consumer_name,
                streams={SCAN_STREAM_KEY: ">"},
                count=1,
                block=5000,
            )
            if not resp:
                continue
            for _sname, messages in resp:
                for msg_id, raw_fields in messages:
                    fields = {str(k): str(v) for k, v in raw_fields.items()}
                    try:
                        await _process_one(
                            session_maker=session_maker,
                            redis=redis,
                            msg_id=str(msg_id),
                            fields=fields,
                            heartbeat_interval_sec=cfg.heartbeat_interval_sec,
                            stub_iterations=cfg.stub_iterations,
                            worker_settings=cfg,
                        )
                    except Exception:
                        log.exception("job_failed msg_id=%s", msg_id)
                    finally:
                        await redis.xack(SCAN_STREAM_KEY, SCAN_CONSUMER_GROUP, msg_id)
    finally:
        await redis.aclose()
        await engine.dispose()


async def _process_one(
    *,
    session_maker: async_sessionmaker[AsyncSession],
    redis: Redis,
    msg_id: str,
    fields: dict[str, str],
    heartbeat_interval_sec: float,
    stub_iterations: int,
    worker_settings: WorkerSettings,
) -> None:
    _ = msg_id
    payload = ScanJobMessage.from_stream_fields(fields)
    async with session_maker() as session:
        repo = PostgresScanRepository(session)
        async with repo.session.begin():
            claimed = await repo.try_claim_scan_for_ingest(
                tenant_id=payload.tenant_id,
                scan_id=payload.scan_id,
            )
        if not claimed:
            log.info(
                "scan_skip_not_queued scan_id=%s tenant_id=%s",
                payload.scan_id,
                payload.tenant_id,
            )
            return
        try:
            await run_scan_job_pipeline(
                repo,
                redis,
                tenant_id=payload.tenant_id,
                scan_id=payload.scan_id,
                heartbeat_interval_sec=heartbeat_interval_sec,
                stub_iterations=stub_iterations,
                worker_settings=worker_settings,
            )
        except Exception as exc:
            log.exception("scan_job_pipeline_failed scan_id=%s", payload.scan_id)
            async with session_maker() as sess2:
                r2 = PostgresScanRepository(sess2)
                await r2.mark_scan_failed(
                    tenant_id=payload.tenant_id,
                    scan_id=payload.scan_id,
                    error_code="WORKER_UNHANDLED",
                    error_message=str(exc)[:8192],
                )


def run_worker_forever() -> None:
    """CLI entry: ``python3 -m deepguard_worker``."""

    import asyncio
    import logging as lg

    lg.basicConfig(level=lg.INFO)
    asyncio.run(run_worker())
