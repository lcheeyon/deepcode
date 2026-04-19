"""Resolve a **sync** Postgres URI for LangGraph ``PostgresSaver`` (§7.1 checkpointing)."""

from __future__ import annotations

import os


def to_sync_postgres_uri(url: str) -> str:
    """Strip SQLAlchemy async driver suffix so ``psycopg`` can open the pool."""

    u = url.strip()
    if u.startswith("postgresql+asyncpg://"):
        return "postgresql://" + u.removeprefix("postgresql+asyncpg://")
    return u


def resolve_checkpoint_postgres_uri() -> str | None:
    """Return libpq URI when Postgres checkpointing is enabled, else ``None`` (use memory).

    Precedence:
    1. ``CHECKPOINT_DB_URL`` when non-empty (sync ``postgresql://`` preferred).
    2. Else ``LANGGRAPH_CHECKPOINT_BACKEND`` in ``postgres``, ``pg``, ``1``, ``true``, ``yes``
       with ``DATABASE_URL`` set (worker metadata DB or dedicated checkpoint DB).
    """

    explicit = os.environ.get("CHECKPOINT_DB_URL", "").strip()
    if explicit:
        return to_sync_postgres_uri(explicit)

    flag = os.environ.get("LANGGRAPH_CHECKPOINT_BACKEND", "").strip().lower()
    if flag in ("postgres", "pg", "1", "true", "yes"):
        db = os.environ.get("DATABASE_URL", "").strip()
        if db:
            return to_sync_postgres_uri(db)
    return None
