"""Phase L12 — HTTP smoke against a running API (opt-in via ``DEEPGUARD_E2E_LOCAL``)."""

from __future__ import annotations

import os
import time
from collections.abc import Iterator

import httpx
import pytest

pytestmark = pytest.mark.integration


@pytest.fixture
def e2e_http() -> Iterator[httpx.Client]:
    if os.environ.get("DEEPGUARD_E2E_LOCAL") != "1":
        pytest.skip(
            "Set DEEPGUARD_E2E_LOCAL=1 and start the API with DB/Redis per docs/dev-setup.md."
        )
    base = os.environ.get("DEEPGUARD_API_BASE", "http://127.0.0.1:8000").rstrip("/")
    key = os.environ.get("DEEPGUARD_DEV_API_KEY", "dev")
    headers = {"X-API-Key": key}
    with httpx.Client(base_url=base, headers=headers, timeout=60.0) as client:
        yield client


def test_healthz_ok(e2e_http: httpx.Client) -> None:
    r = e2e_http.get("/v1/healthz")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_create_and_get_scan_roundtrip(e2e_http: httpx.Client) -> None:
    body = {
        "repo": {"url": "https://github.com/example/demo", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    r = e2e_http.post("/v1/scans", json=body)
    assert r.status_code == 201, r.text
    scan_id = r.json()["scan_id"]
    g = e2e_http.get(f"/v1/scans/{scan_id}")
    assert g.status_code == 200, g.text
    assert g.json()["scan_id"] == scan_id


def test_p95_create_scan_wall_seconds(e2e_http: httpx.Client) -> None:
    """Budget guard for L12 SLO direction (local laptop; not a substitute for load tests)."""

    body = {
        "repo": {"url": "https://github.com/example/demo", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    durations: list[float] = []
    for _ in range(5):
        t0 = time.perf_counter()
        r = e2e_http.post("/v1/scans", json=body)
        durations.append(time.perf_counter() - t0)
        assert r.status_code == 201, r.text
    s = sorted(durations)
    n = len(s)
    idx = (n - 1) * 0.95
    lo = int(idx)
    hi = min(lo + 1, n - 1)
    w = idx - lo
    p95 = s[lo] * (1 - w) + s[hi] * w
    assert p95 < 30.0


def test_scan_reaches_complete_with_worker_and_pdf_pipeline(e2e_http: httpx.Client) -> None:
    """Needs ``DEEPGUARD_E2E_FULL=1``, API, Postgres, Redis, and ``python3 -m deepguard_worker``."""

    if os.environ.get("DEEPGUARD_E2E_FULL") != "1":
        pytest.skip("Set DEEPGUARD_E2E_FULL=1 and run the worker (see docs/dev-setup.md).")
    body = {
        "repo": {"url": "https://github.com/example/demo", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    r = e2e_http.post("/v1/scans", json=body)
    assert r.status_code == 201, r.text
    scan_id = r.json()["scan_id"]
    deadline = time.monotonic() + 120.0
    while time.monotonic() < deadline:
        g = e2e_http.get(f"/v1/scans/{scan_id}")
        assert g.status_code == 200, g.text
        status = g.json().get("status")
        if status == "COMPLETE":
            assert g.json().get("percent_complete") == 100
            return
        if status == "FAILED":
            pytest.fail(f"scan failed: {g.text}")
        time.sleep(2.0)
    pytest.fail("timed out waiting for COMPLETE (is the worker running?)")
