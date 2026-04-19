#!/usr/bin/env python3
"""Insert default dev tenant if missing (Phase L1).

Usage: set DATABASE_URL_SYNC to sync postgres URL, then run this script after
alembic upgrade head.
"""

from __future__ import annotations

import os
import sys

import psycopg


def main() -> int:
    url = os.environ.get(
        "DATABASE_URL_SYNC",
        "postgresql://deepguard:deepguard@127.0.0.1:5432/deepguard",
    )
    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM tenants WHERE name = %s", ("Dev Tenant",))
            row = cur.fetchone()
            if row:
                print(f"Dev tenant already exists: {row[0]}")
                return 0
            cur.execute(
                """
                INSERT INTO tenants (name, runtime_config)
                VALUES (%s, %s::jsonb)
                RETURNING id
                """,
                ("Dev Tenant", "{}"),
            )
            ins = cur.fetchone()
            assert ins is not None
            tid = ins[0]
        conn.commit()
    print(f"Inserted Dev Tenant: {tid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
