"""Phase L1 integration checks (Postgres + Redis + MinIO via Docker Compose).

Run (adjust host ports if you set DEEPGUARD_POSTGRES_PORT / DEEPGUARD_REDIS_PORT):

  docker compose -f docker/compose.dev.yml up -d
  export DEEPGUARD_INTEGRATION=1 \\
    DATABASE_URL_SYNC=postgresql://deepguard:deepguard@127.0.0.1:5432/deepguard \\
    REDIS_URL=redis://127.0.0.1:6379/0
  alembic upgrade head
  python3 scripts/seed_dev_tenant.py
  pytest -m integration tests/integration/test_l1_data_plane.py -v
"""

from __future__ import annotations

import os
import urllib.error
import urllib.request

import pytest

pytestmark = pytest.mark.integration


def _integration_enabled() -> bool:
    return os.environ.get("DEEPGUARD_INTEGRATION") == "1"


@pytest.fixture(scope="module")
def pg_url() -> str:
    return os.environ.get(
        "DATABASE_URL_SYNC",
        "postgresql://deepguard:deepguard@127.0.0.1:5432/deepguard",
    )


@pytest.mark.skipif(
    not _integration_enabled(), reason="Set DEEPGUARD_INTEGRATION=1 and start compose"
)
def test_postgres_vector_extension_and_tables(pg_url: str) -> None:
    import psycopg

    with psycopg.connect(pg_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = %s)",
                ("vector",),
            )
            ext_row = cur.fetchone()
            assert ext_row is not None
            assert ext_row[0] is True
            cur.execute(
                """
                SELECT tablename FROM pg_tables
                WHERE schemaname = 'public' AND tablename IN (
                    'tenants', 'scans', 'findings', 'reasoning_traces',
                    'artifacts', 'webhook_deliveries', 'code_chunks', 'policy_chunks'
                )
                ORDER BY tablename
                """
            )
            names = [r[0] for r in cur.fetchall()]
    assert names == [
        "artifacts",
        "code_chunks",
        "findings",
        "policy_chunks",
        "reasoning_traces",
        "scans",
        "tenants",
        "webhook_deliveries",
    ]


@pytest.mark.skipif(
    not _integration_enabled(), reason="Set DEEPGUARD_INTEGRATION=1 and start compose"
)
def test_dev_tenant_seeded(pg_url: str) -> None:
    import psycopg

    with psycopg.connect(pg_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM tenants WHERE name = %s", ("Dev Tenant",))
            cnt_row = cur.fetchone()
            assert cnt_row is not None
            assert cnt_row[0] >= 1


@pytest.mark.skipif(
    not _integration_enabled(), reason="Set DEEPGUARD_INTEGRATION=1 and start compose"
)
def test_redis_ping() -> None:
    import redis

    url = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")
    r = redis.Redis.from_url(url)
    assert r.ping() is True


@pytest.mark.skipif(
    not _integration_enabled(), reason="Set DEEPGUARD_INTEGRATION=1 and start compose"
)
def test_minio_health_live() -> None:
    host = os.environ.get("MINIO_HEALTH_URL", "http://127.0.0.1:9000/minio/health/live")
    try:
        with urllib.request.urlopen(host, timeout=5) as resp:
            assert resp.status == 200
    except urllib.error.URLError as e:
        pytest.fail(f"MinIO not reachable at {host}: {e}")
