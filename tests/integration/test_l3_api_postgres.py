"""L3 API against real Postgres (optional — Docker + migrate + seed + env)."""

from __future__ import annotations

import os
import uuid
from typing import Any

import pytest
from deepguard_api.config import Settings
from deepguard_api.main import create_app
from starlette.testclient import TestClient

from tests.integration.reporting import attach_api_exchange

pytestmark = pytest.mark.integration


def _enabled() -> bool:
    return (
        os.environ.get("DEEPGUARD_API_TEST") == "1"
        and bool(os.environ.get("DATABASE_URL", "").strip())
        and bool(os.environ.get("DEEPGUARD_DEV_TENANT_ID", "").strip())
        and bool(os.environ.get("REDIS_URL", "").strip())
    )


@pytest.mark.skipif(
    not _enabled(),
    reason="Set DEEPGUARD_API_TEST=1, DATABASE_URL, REDIS_URL, DEEPGUARD_DEV_TENANT_ID",
)
def test_postgres_create_and_get_scan(extras: list[Any]) -> None:
    settings = Settings(
        database_url=os.environ["DATABASE_URL"].strip(),
        dev_tenant_id=uuid.UUID(os.environ["DEEPGUARD_DEV_TENANT_ID"].strip()),
        dev_api_key=os.environ.get("DEEPGUARD_DEV_API_KEY", "dev").strip(),
        use_memory_store=False,
        redis_url=os.environ["REDIS_URL"].strip(),
    )
    app = create_app(settings)
    body = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    headers = {"X-API-Key": settings.dev_api_key}
    with TestClient(app) as client:
        c = client.post("/v1/scans", json=body, headers=headers)
        assert c.status_code == 201, c.text
        resp_create = c.json()
        sid = resp_create["scan_id"]
        attach_api_exchange(
            extras,
            name="POST /v1/scans",
            method="POST",
            path="/v1/scans",
            request_json=body,
            request_headers={"X-API-Key": "(dev key)"},
            response_status=c.status_code,
            response_body=resp_create,
        )
        g = client.get(f"/v1/scans/{sid}", headers=headers)
        assert g.status_code == 200
        resp_get = g.json()
        assert resp_get["scan_id"] == sid
        attach_api_exchange(
            extras,
            name=f"GET /v1/scans/{sid}",
            method="GET",
            path=f"/v1/scans/{sid}",
            request_json=None,
            request_headers={"X-API-Key": "(dev key)"},
            response_status=g.status_code,
            response_body=resp_get,
        )
