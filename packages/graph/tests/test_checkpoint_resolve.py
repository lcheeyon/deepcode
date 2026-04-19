"""Unit tests for checkpoint URI resolution (§7.1)."""

from __future__ import annotations

import pytest
from deepguard_graph.checkpoint_resolve import resolve_checkpoint_postgres_uri, to_sync_postgres_uri


def test_to_sync_postgres_uri_strips_async_driver() -> None:
    assert to_sync_postgres_uri("postgresql+asyncpg://u:p@h:5432/db") == "postgresql://u:p@h:5432/db"
    assert to_sync_postgres_uri("postgresql://h/db") == "postgresql://h/db"


def test_resolve_checkpoint_prefers_checkpoint_db_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CHECKPOINT_DB_URL", raising=False)
    monkeypatch.delenv("LANGGRAPH_CHECKPOINT_BACKEND", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("CHECKPOINT_DB_URL", "postgresql+asyncpg://a/b")
    assert resolve_checkpoint_postgres_uri() == "postgresql://a/b"


def test_resolve_checkpoint_from_backend_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CHECKPOINT_DB_URL", raising=False)
    monkeypatch.setenv("LANGGRAPH_CHECKPOINT_BACKEND", "postgres")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://x:y@db:5432/app")
    assert resolve_checkpoint_postgres_uri() == "postgresql://x:y@db:5432/app"
