"""Postgres checkpointer for Odysseus (Architecture §4.6, §29.2)."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from langgraph.checkpoint.postgres import PostgresSaver


@contextmanager
def postgres_checkpointer(conn_string: str) -> Iterator[PostgresSaver]:
    """Context-managed ``PostgresSaver`` with one-time ``setup()`` (sync).

    Use a **sync** libpq URI (``postgresql://…``), not ``+asyncpg``. Prefer
    ``CHECKPOINT_DB_URL`` when set, else the same database as the worker metadata.
    """

    with PostgresSaver.from_conn_string(conn_string) as saver:
        saver.setup()
        yield saver
