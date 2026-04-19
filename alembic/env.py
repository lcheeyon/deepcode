"""Alembic migration environment (sync PostgreSQL)."""

from __future__ import annotations

import os
from urllib.parse import urlsplit, urlunsplit

from alembic import context
from sqlalchemy import engine_from_config, pool

config = context.config

target_metadata = None  # SQL-only migrations for L1


def get_url() -> str:
    """Return a SQLAlchemy URL using the psycopg (v3) driver.

    Bare ``postgresql://`` defaults to the psycopg2 dialect in SQLAlchemy; this
    project depends on ``psycopg[binary]`` (v3) only.
    """
    url = os.environ.get(
        "DATABASE_URL_SYNC",
        "postgresql://deepguard:deepguard@127.0.0.1:5432/deepguard",
    )
    parts = urlsplit(url)
    if parts.scheme == "postgresql":
        url = urlunsplit(parts._replace(scheme="postgresql+psycopg"))
    return url


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
