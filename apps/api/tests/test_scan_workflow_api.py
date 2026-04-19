"""GET /v1/scans/{id}/workflow and trace-links (US-DG-14-015 / 017)."""

from __future__ import annotations

import asyncio
import uuid
from typing import cast

from deepguard_api.config import Settings
from deepguard_api.main import create_app
from deepguard_api.repositories.scans import MemoryScanRepository
from deepguard_core.models import CreateScanRequest, RepoSpec, ScanLayers
from pydantic import AnyHttpUrl
from starlette.testclient import TestClient


def test_workflow_returns_checklist_and_redacted_events() -> None:
    tid = uuid.UUID("00000000-0000-4000-8000-000000000099")
    app = create_app(
        Settings(
            database_url=None,
            redis_url=None,
            dev_tenant_id=tid,
            dev_api_key="k",
            use_memory_store=True,
        )
    )
    repo: MemoryScanRepository = app.state.memory_repo

    async def seed() -> str:
        body = CreateScanRequest(
            repo=RepoSpec(url=cast(AnyHttpUrl, "https://github.com/acme/svc"), ref="main"),
            policy_ids=["ISO-27001-2022"],
            scan_layers=ScanLayers(code=True, iac=False, cloud=False),
        )
        row = await repo.create_scan(tenant_id=tid, body=body, idempotency_key=None)
        await repo.append_scan_run_event(
            tenant_id=tid,
            scan_id=row.id,
            event_type="node_progress",
            node="hermes",
            payload={"client_secret": "x"},
            correlation_id="corr-1",
            graph_version="0.1.0",
        )
        return str(row.id)

    scan_id = asyncio.run(seed())
    h = {"X-API-Key": "k"}
    with TestClient(app) as client:
        r = client.get(f"/v1/scans/{scan_id}/workflow", headers=h)
        assert r.status_code == 200
        data = r.json()
        assert data["status"] in ("QUEUED", "PENDING")
        assert "ingestion" in data["planned_nodes"]
        assert any(x["node"] == "ingestion" for x in data["checklist"])
        evs = data["events"]
        assert len(evs) == 1
        assert evs[0]["payload"].get("client_secret") == "[REDACTED]"
        r2 = client.get(f"/v1/scans/{scan_id}/workflow?include_events=false", headers=h)
        assert r2.status_code == 200
        assert r2.json()["events"] == []


def test_trace_links_empty_without_refs() -> None:
    tid = uuid.UUID("00000000-0000-4000-8000-000000000098")
    app = create_app(
        Settings(
            database_url=None,
            redis_url=None,
            dev_tenant_id=tid,
            dev_api_key="k",
            use_memory_store=True,
        )
    )
    repo: MemoryScanRepository = app.state.memory_repo

    async def seed() -> str:
        body = CreateScanRequest(
            repo=RepoSpec(url=cast(AnyHttpUrl, "https://github.com/acme/svc"), ref="main"),
            policy_ids=["ISO-27001-2022"],
            scan_layers=ScanLayers(code=True, iac=False, cloud=False),
        )
        row = await repo.create_scan(tenant_id=tid, body=body, idempotency_key=None)
        return str(row.id)

    scan_id = asyncio.run(seed())
    with TestClient(app) as client:
        r = client.get(f"/v1/scans/{scan_id}/trace-links", headers={"X-API-Key": "k"})
        assert r.status_code == 200
        assert r.json()["links"] == []
