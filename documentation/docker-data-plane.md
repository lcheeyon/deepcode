# Docker & data plane

## Compose stack

Local dependencies are defined in **`docker/compose.dev.yml`**:

- **Postgres** (with extensions such as `vector` per migration/seed docs)
- **Redis**
- **MinIO** (S3-compatible API for artefact staging)

## Typical bootstrap

```bash
docker compose -f docker/compose.dev.yml up -d
export DATABASE_URL_SYNC=postgresql://deepguard:deepguard@127.0.0.1:5432/deepguard
alembic upgrade head
python3 scripts/seed_dev_tenant.py
```

Use a **sync** `postgresql://` URL for Alembic; the API uses **`DATABASE_URL`** with **`asyncpg`** (see `.env.example`).

## Port conflicts

If host ports **5432** or **6379** are already taken, set **`DEEPGUARD_POSTGRES_PORT`**, **`DEEPGUARD_REDIS_PORT`**, etc., in a repo-root **`.env`** and align **`DATABASE_URL_SYNC`**, **`DATABASE_URL`**, **`REDIS_URL`**, and MinIO health URLs. Details: **`docs/dev-setup.md`**.

## Integration tests

With services healthy and migrations applied:

```bash
export DEEPGUARD_INTEGRATION=1
pytest -m integration tests/integration/ -v
```

## End-to-end scans

`tests/e2e/` contains HTTP-level flows. **`make e2e-local`** and **`make e2e-full`** wrap compose, API, worker, and pytest with the right environment flags (see **`Makefile`** and **`scripts/e2e_full_scan.sh`**).
