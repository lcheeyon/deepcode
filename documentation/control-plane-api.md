# Control plane API

The FastAPI application is created by **`deepguard_api.main:create_app`**. Global OpenAPI and docs:

| URL | Content |
|-----|---------|
| `/v1/openapi.json` | OpenAPI schema |
| `/v1/docs` | Swagger UI |
| `/v1/redoc` | ReDoc |

## Authentication (development)

Routes under **`/v1/scans`** and **`/v1/repo-uploads`** depend on **`require_api_key`**: send header **`X-API-Key`** (default dev key is documented in **`docs/dev-setup.md`** and `.env.example`).

## Implemented `GET` / `POST` routes (`/v1`)

### Health

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/v1/healthz` | Liveness JSON `{"status": "ok"}`. |

### Scans

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v1/scans` | Create scan from **`CreateScanRequest`**. Optional header **`Idempotency-Key`**. With Postgres + Redis, enqueues a job when not a replay. |
| `GET` | `/v1/scans/{scan_id}` | Fetch scan row / status for the dev tenant. |
| `POST` | `/v1/scans/{scan_id}/cancel` | Request cancellation (`202` on success). |

### Repository uploads (presigned PUT)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v1/repo-uploads` | Returns presigned upload URL and metadata when S3/MinIO settings are configured; **`503`** with `REPO_UPLOAD_S3_UNCONFIGURED` otherwise. |

!!! info "Request bodies"
    Pydantic models for create-scan and related payloads live in **`deepguard_core.models`** (see package tests and OpenAPI for field-level detail).

## Configuration surface

Environment-driven settings are loaded in **`deepguard_api.config`**. Canonical lists appear in **`Architecture_Design.md` §27** and **`docs/dev-setup.md`**. Typical variables include:

- **`DATABASE_URL`** — async Postgres URL for persistence (optional for in-memory dev).
- **`REDIS_URL`** — required when **`DATABASE_URL`** is set (queue producer).
- **`DEEPGUARD_DEV_TENANT_ID`** — UUID for the seeded dev tenant when using Postgres.
- **S3 / MinIO** — bucket and credentials for presigned repo uploads (see `.env.example`).
