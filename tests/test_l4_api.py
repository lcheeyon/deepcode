"""Phase L4 — cancel endpoint + optional Redis enqueue (memory + FakeRedis)."""

from __future__ import annotations

import asyncio
import uuid
from collections.abc import Iterator

import pytest
from deepguard_api.config import Settings
from deepguard_api.main import create_app
from deepguard_core.queue import SCAN_STREAM_KEY
from fakeredis import FakeAsyncRedis
from starlette.testclient import TestClient


@pytest.fixture
def memory_settings() -> Settings:
    return Settings(
        database_url=None,
        redis_url=None,
        dev_tenant_id=uuid.UUID("00000000-0000-4000-8000-000000000001"),
        dev_api_key="test-secret",
        use_memory_store=True,
    )


@pytest.fixture
def client(memory_settings: Settings) -> Iterator[TestClient]:
    app = create_app(memory_settings)
    with TestClient(app) as c:
        yield c


def test_cancel_scan_returns_202(client: TestClient) -> None:
    body = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    h = {"X-API-Key": "test-secret"}
    sid = client.post("/v1/scans", json=body, headers=h).json()["scan_id"]
    r = client.post(f"/v1/scans/{sid}/cancel", headers=h)
    assert r.status_code == 202
    assert r.json() == {"scan_id": sid, "cancellation_requested": True}
    g = client.get(f"/v1/scans/{sid}", headers=h)
    assert g.status_code == 200
    assert g.json()["cancellation_requested"] is True


def test_cancel_scan_404(client: TestClient) -> None:
    r = client.post(
        f"/v1/scans/{uuid.uuid4()}/cancel",
        headers={"X-API-Key": "test-secret"},
    )
    assert r.status_code == 404


def test_post_scan_enqueues_when_redis_configured(memory_settings: Settings) -> None:
    app = create_app(memory_settings)
    fake = FakeAsyncRedis(decode_responses=True)
    app.state.redis = fake

    body = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    h = {"X-API-Key": "test-secret"}

    async def run() -> None:
        with TestClient(app) as c:
            r = c.post("/v1/scans", json=body, headers=h)
            assert r.status_code == 201
            sid = r.json()["scan_id"]
            n = await fake.xlen(SCAN_STREAM_KEY)
            assert n == 1
            fields = (await fake.xrange(SCAN_STREAM_KEY, count=1))[0][1]
            assert fields["scan_id"] == sid

    asyncio.run(run())


def test_idempotent_create_does_not_enqueue_second_message(memory_settings: Settings) -> None:
    app = create_app(memory_settings)
    fake = FakeAsyncRedis(decode_responses=True)
    app.state.redis = fake
    body = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    headers = {"X-API-Key": "test-secret", "Idempotency-Key": "idem-l4-no-dup"}

    async def run() -> None:
        with TestClient(app) as c:
            r1 = c.post("/v1/scans", json=body, headers=headers)
            r2 = c.post("/v1/scans", json=body, headers=headers)
            assert r1.status_code == 201 and r2.status_code == 201
            assert await fake.xlen(SCAN_STREAM_KEY) == 1

    asyncio.run(run())
