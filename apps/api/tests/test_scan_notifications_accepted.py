"""L12 — API accepts webhook notification settings on create (delivery deferred to worker)."""

from __future__ import annotations

import uuid

from deepguard_api.config import Settings
from deepguard_api.main import create_app
from starlette.testclient import TestClient


def test_post_scan_accepts_notifications_webhook_url() -> None:
    tid = uuid.UUID("00000000-0000-4000-8000-0000000000a1")
    app = create_app(
        Settings(
            database_url=None,
            redis_url=None,
            dev_tenant_id=tid,
            dev_api_key="dev",
            use_memory_store=True,
        )
    )
    body = {
        "repo": {"url": "https://github.com/example/demo", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
        "notifications": {
            "webhook_url": "https://example.com/hooks/deepguard",
            "on": ["completed"],
        },
    }
    with TestClient(app) as client:
        r = client.post("/v1/scans", json=body, headers={"X-API-Key": "dev"})
    assert r.status_code == 201
    data = r.json()
    assert "scan_id" in data
    cfg = data["job_config"]
    assert cfg["notifications"]["webhook_url"] == "https://example.com/hooks/deepguard"
