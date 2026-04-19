"""Phase L3 — FastAPI control plane (memory store, no Docker)."""

from __future__ import annotations

import asyncio
import io
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest
from deepguard_api.config import Settings
from deepguard_api.main import create_app
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


def test_healthz_no_auth_required(client: TestClient) -> None:
    r = client.get("/v1/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_scans_require_auth(client: TestClient) -> None:
    r = client.post(
        "/v1/scans",
        json={
            "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
            "policy_ids": ["ISO-27001-2022"],
            "scan_layers": {"code": True, "iac": False, "cloud": False},
        },
    )
    assert r.status_code == 401


def test_create_scan_with_api_key(client: TestClient) -> None:
    body = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    r = client.post("/v1/scans", json=body, headers={"X-API-Key": "test-secret"})
    assert r.status_code == 201
    data = r.json()
    assert data["status"] == "QUEUED"
    assert data["current_stage"] == "QUEUED"
    assert "scan_id" in data
    assert data["job_config"]["repo"]["ref"] == "main"


def test_idempotency_returns_same_scan_id(client: TestClient) -> None:
    body = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    headers = {"X-API-Key": "test-secret", "Idempotency-Key": "idem-abc-123"}
    r1 = client.post("/v1/scans", json=body, headers=headers)
    r2 = client.post("/v1/scans", json=body, headers=headers)
    assert r1.status_code == 201 and r2.status_code == 201
    assert r1.json()["scan_id"] == r2.json()["scan_id"]


def test_get_scan_404_wrong_id(client: TestClient) -> None:
    r = client.get(
        f"/v1/scans/{uuid.uuid4()}",
        headers={"X-API-Key": "test-secret"},
    )
    assert r.status_code == 404


def test_get_scan_roundtrip(client: TestClient) -> None:
    body = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    h = {"X-API-Key": "test-secret"}
    c = client.post("/v1/scans", json=body, headers=h)
    sid = c.json()["scan_id"]
    g = client.get(f"/v1/scans/{sid}", headers=h)
    assert g.status_code == 200
    assert g.json()["scan_id"] == sid


def test_openapi_contains_create_scan_and_scan_response(client: TestClient) -> None:
    r = client.get("/v1/openapi.json")
    assert r.status_code == 200
    schemas = r.json()["components"]["schemas"]
    assert "CreateScanRequest" in schemas
    assert "ScanResponse" in schemas


def test_bearer_token_auth(client: TestClient) -> None:
    body = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    r = client.post(
        "/v1/scans",
        json=body,
        headers={"Authorization": "Bearer test-secret"},
    )
    assert r.status_code == 201


def test_prepare_repo_upload_returns_503_without_s3(client: TestClient) -> None:
    r = client.post(
        "/v1/repo-uploads",
        json={"filename": "repo.tar.gz"},
        headers={"X-API-Key": "test-secret"},
    )
    assert r.status_code == 503
    assert r.json()["detail"]["error_code"] == "REPO_UPLOAD_S3_UNCONFIGURED"


def test_list_findings_memory_stub(client: TestClient) -> None:
    h = {"X-API-Key": "test-secret"}
    body = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    c = client.post("/v1/scans", json=body, headers=h)
    sid = c.json()["scan_id"]
    r = client.get(f"/v1/scans/{sid}/findings?limit=10", headers=h)
    assert r.status_code == 200
    data = r.json()
    assert len(data["items"]) >= 2
    assert data["items"][0]["severity"] in {"HIGH", "MEDIUM", "LOW", "CRITICAL", "INFO"}


def test_findings_export_csv(client: TestClient) -> None:
    h = {"X-API-Key": "test-secret"}
    body = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    sid = client.post("/v1/scans", json=body, headers=h).json()["scan_id"]
    r = client.get(f"/v1/scans/{sid}/findings/export?format=csv", headers=h)
    assert r.status_code == 200
    assert "deepguard-findings-export v1" in r.text
    assert "finding_id" in r.text


def test_artifact_download_memory_inline(client: TestClient, memory_settings: Settings) -> None:
    h = {"X-API-Key": "test-secret"}
    body = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    sid = uuid.UUID(client.post("/v1/scans", json=body, headers=h).json()["scan_id"])
    tid = memory_settings.dev_tenant_id
    app = client.app
    repo = app.state.memory_repo
    aid = asyncio.run(
        repo.mark_scan_complete_with_report(
            tenant_id=tid,
            scan_id=sid,
            pdf_bytes=b"%PDF-1.4 minimal test",
            storage_uri="s3://test-bucket/reports/x.pdf",
        )
    )
    g = client.get(f"/v1/scans/{sid}", headers=h)
    assert g.json().get("report_artifact_id") == str(aid)
    arts = client.get(f"/v1/scans/{sid}/artifacts", headers=h).json()["artifacts"]
    assert len(arts) == 1
    dl = client.get(f"/v1/scans/{sid}/artifacts/{aid}", headers=h)
    assert dl.status_code == 200
    assert dl.content.startswith(b"%PDF")


def test_policy_upload_yaml(client: TestClient) -> None:
    h = {"X-API-Key": "test-secret"}
    fixture = Path("packages/policies/tests/fixtures/iso_synthetic.yaml").read_bytes()
    files = {"file": ("policy.yaml", io.BytesIO(fixture), "application/x-yaml")}
    r = client.post("/v1/policies:upload", headers=h, files=files)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["controls_extracted"] >= 1
    assert "2022-demo" in data["policy_version"] or data["policy_version"]
    listed = client.get("/v1/policies", headers=h).json()["uploads"]
    assert len(listed) >= 1


def test_cors_preflight_when_origins_configured() -> None:
    settings = Settings(
        database_url=None,
        redis_url=None,
        dev_tenant_id=uuid.UUID("00000000-0000-4000-8000-000000000001"),
        dev_api_key="test-secret",
        use_memory_store=True,
        cors_origins=("http://localhost:3000",),
    )
    app = create_app(settings)
    with TestClient(app) as client:
        r = client.options(
            "/v1/healthz",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert r.status_code == 200
        assert r.headers.get("access-control-allow-origin") == "http://localhost:3000"
