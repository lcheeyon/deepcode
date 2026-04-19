"""Phase L14 — tenant isolation + auditor redaction."""

from __future__ import annotations

import uuid

from deepguard_api.audit_redact import redact_for_auditor
from deepguard_api.config import Settings
from deepguard_api.main import create_app
from starlette.testclient import TestClient


def test_cross_tenant_scan_get_returns_404() -> None:
    tid_a = uuid.UUID("00000000-0000-4000-8000-0000000000a1")
    tid_b = uuid.UUID("00000000-0000-4000-8000-0000000000b2")
    body = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    h = {"X-API-Key": "same-secret"}
    app_a = create_app(
        Settings(
            database_url=None,
            redis_url=None,
            dev_tenant_id=tid_a,
            dev_api_key="same-secret",
            use_memory_store=True,
        )
    )
    app_b = create_app(
        Settings(
            database_url=None,
            redis_url=None,
            dev_tenant_id=tid_b,
            dev_api_key="same-secret",
            use_memory_store=True,
        )
    )
    with TestClient(app_a) as ca, TestClient(app_b) as cb:
        sid = ca.post("/v1/scans", json=body, headers=h).json()["scan_id"]
        r = cb.get(f"/v1/scans/{sid}", headers=h)
        assert r.status_code == 404


def test_auditor_redact_strips_secret_classified_keys() -> None:
    payload = {
        "scan_id": "s1",
        "client_secret": "supersecret",
        "nested": {"api_key_plain": "k", "ok": 1},
    }
    out = redact_for_auditor(payload)
    assert out["client_secret"] == "[REDACTED]"
    assert out["nested"]["api_key_plain"] == "[REDACTED]"
    assert out["nested"]["ok"] == 1
