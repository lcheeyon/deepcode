"""Phase L4 — worker env loading."""

from __future__ import annotations

from deepguard_worker.settings import WorkerSettings, load_worker_settings


def test_load_worker_settings_defaults(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://u:p@localhost/db")
    monkeypatch.setenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    monkeypatch.delenv("DEEPGUARD_WORKER_CONSUMER", raising=False)
    monkeypatch.delenv("DEEPGUARD_WORKER_HEARTBEAT_SEC", raising=False)
    monkeypatch.delenv("DEEPGUARD_WORKER_STUB_ITERATIONS", raising=False)
    s = load_worker_settings()
    assert s.database_url == "postgresql+asyncpg://u:p@localhost/db"
    assert s.redis_url == "redis://127.0.0.1:6379/0"
    assert s.consumer_name.startswith("worker-")
    assert s.heartbeat_interval_sec == 30.0
    assert s.stub_iterations == 0
    assert s.hermes_enabled is False
    assert s.repo_max_bytes == 2_147_483_648
    assert s.repo_clone_depth == 50
    assert s.s3_bucket is None


def test_load_worker_settings_overrides(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://x")
    monkeypatch.setenv("REDIS_URL", "redis://h/1")
    monkeypatch.setenv("DEEPGUARD_WORKER_CONSUMER", "c1")
    monkeypatch.setenv("DEEPGUARD_WORKER_HEARTBEAT_SEC", "0.5")
    monkeypatch.setenv("DEEPGUARD_WORKER_STUB_ITERATIONS", "7")
    s = load_worker_settings()
    assert s.consumer_name == "c1"
    assert s.heartbeat_interval_sec == 0.5
    assert s.stub_iterations == 7


def test_worker_settings_frozen_slots() -> None:
    s = WorkerSettings(
        database_url="postgresql+asyncpg://x",
        redis_url="redis://x",
        consumer_name="w",
        heartbeat_interval_sec=1.0,
        stub_iterations=1,
        hermes_enabled=False,
        repo_max_bytes=100,
        repo_clone_depth=2,
        s3_bucket=None,
        s3_region="us-east-1",
        s3_endpoint_url=None,
        s3_access_key_id=None,
        s3_secret_access_key=None,
    )
    assert s.stub_iterations == 1
