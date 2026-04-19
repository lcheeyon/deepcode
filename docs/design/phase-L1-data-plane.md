---
status: approved
approved_date: 2026-04-18
approvers: [Engineering — per IMPLEMENTATION_PLAN Phase L1]
related_phases: [L1]
---

# Design: L1 local data plane

## Goal

**Docker Compose** provides Postgres **16 + pgvector**, **Redis 7**, **MinIO** (S3-compatible), with **Alembic** migrations and a **dev tenant** seed.

## Decisions

| Topic | Choice |
|-------|--------|
| Postgres | `pgvector/pgvector:pg16`; DB/user/password `deepguard` / `deepguard` |
| Redis | `redis:7-alpine`; port `6379` |
| MinIO | Root user `deepguard` / `deepguarddev`; bucket `deepguard-dev` via `minio/mc` init |
| Migrations | Alembic sync URL `DATABASE_URL_SYNC` (`postgresql://`, not `asyncpg`) |
| Vector index | IVFFlat **not** created on empty tables (pgvector guidance); follow-up in L8+ |

## Out of scope (L1)

- LangGraph checkpointer tables (library-managed migration later).
- Application DB pools / FastAPI (L3+).

## Tests

- Default `pytest` excludes `integration` marker.
- With compose up: `DEEPGUARD_INTEGRATION=1 pytest -m integration`.
