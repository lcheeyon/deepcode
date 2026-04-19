"""Phase L12 — worker pipeline drives stub Odysseus graph → PDF → COMPLETE (memory repo)."""

from __future__ import annotations

import asyncio
import uuid
from typing import cast

from deepguard_api.repositories.scans import MemoryScanRepository
from deepguard_core.models import CreateScanRequest, RepoSpec, ScanLayers
from deepguard_worker.job_executor import run_scan_job_pipeline
from deepguard_worker.settings import WorkerSettings
from fakeredis import FakeAsyncRedis
from pydantic import AnyHttpUrl


def _body() -> CreateScanRequest:
    return CreateScanRequest(
        repo=RepoSpec(url=cast(AnyHttpUrl, "https://github.com/acme/svc"), ref="main"),
        policy_ids=["ISO-27001-2022"],
        scan_layers=ScanLayers(code=True, iac=False, cloud=False),
    )


def test_pipeline_marks_scan_complete_and_records_report_metadata() -> None:
    async def run() -> None:
        tenant_id = uuid.UUID("00000000-0000-4000-8000-000000000001")
        repo = MemoryScanRepository()
        row = await repo.create_scan(tenant_id=tenant_id, body=_body(), idempotency_key=None)
        await repo.try_claim_scan_for_ingest(tenant_id=tenant_id, scan_id=row.id)
        redis = FakeAsyncRedis(decode_responses=True)
        ws = WorkerSettings(
            database_url="postgresql://unused",
            redis_url="redis://unused",
            consumer_name="test",
            heartbeat_interval_sec=0.01,
            stub_iterations=0,
            hermes_enabled=False,
            repo_max_bytes=1000,
            repo_clone_depth=1,
            s3_bucket=None,
            s3_region="us-east-1",
            s3_endpoint_url=None,
            s3_access_key_id=None,
            s3_secret_access_key=None,
        )
        await run_scan_job_pipeline(
            repo,
            redis,
            tenant_id=tenant_id,
            scan_id=row.id,
            heartbeat_interval_sec=0.01,
            stub_iterations=0,
            worker_settings=ws,
        )
        out = await repo.get_scan(tenant_id=tenant_id, scan_id=row.id)
        assert out is not None
        assert out.status == "COMPLETE"
        assert out.current_stage == "COMPLETE"
        assert out.percent_complete == 100
        meta = repo.report_storage_meta(row.id)
        assert meta is not None
        assert meta["storage_uri"].endswith(f"/{row.id}/report.pdf")
        assert len(meta["checksum_sha256"]) == 64

    asyncio.run(run())
