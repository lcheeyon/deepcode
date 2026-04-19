#!/usr/bin/env bash
# Run Playwright BDD against the real local API + worker, using https://github.com/lcheeyon/power-rag
# as the Git scan target (Hermes performs a real shallow clone when enabled).
#
# Prerequisite stack (from repo root):
#   docker compose -f docker/compose.dev.yml up -d
#   pip3 install -e ".[dev]"
#   export DATABASE_URL_SYNC=postgresql://deepguard:deepguard@127.0.0.1:5432/deepguard
#   export DATABASE_URL=postgresql+asyncpg://deepguard:deepguard@127.0.0.1:5432/deepguard
#   export REDIS_URL=redis://127.0.0.1:6379/0
#   python3 -m alembic upgrade head
#   python3 scripts/seed_dev_tenant.py
#   export DEEPGUARD_DEV_TENANT_ID=<printed uuid>
#   export DEEPGUARD_DEV_API_KEY=dev
#   export DEEPGUARD_CORS_ORIGINS=http://127.0.0.1:3000,http://localhost:3000
#
# API (terminal 1):
#   uvicorn deepguard_api.main:app --reload --host 127.0.0.1 --port 8000
#
# Worker (terminal 2) — enable Hermes + MinIO for a real clone + staging tarball:
#   export DEEPGUARD_HERMES_ENABLED=1
#   export DEEPGUARD_REPO_CLONE_DEPTH=50
#   export DEEPGUARD_S3_BUCKET=deepguard-dev
#   export DEEPGUARD_S3_REGION=us-east-1
#   export DEEPGUARD_S3_ENDPOINT_URL=http://127.0.0.1:9000
#   export DEEPGUARD_S3_ACCESS_KEY_ID=deepguard
#   export DEEPGUARD_S3_SECRET_ACCESS_KEY=deepguarddev
#   docker compose -f docker/compose.dev.yml run --rm minio-init   # once, for bucket + CORS
#   python3 -m deepguard_worker
#
# Next dev server on :3000 (terminal 3) or let Playwright start it (CI sets CI=1).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export E2E_POWER_RAG_BACKEND="${E2E_POWER_RAG_BACKEND:-1}"
export E2E_API_BASE_URL="${E2E_API_BASE_URL:-http://127.0.0.1:8000}"
export E2E_API_KEY="${E2E_API_KEY:-dev}"

API_BASE="${E2E_API_BASE_URL%/}"
if ! curl -sf "${API_BASE}/v1/healthz" >/dev/null; then
  echo "error: ${API_BASE}/v1/healthz not reachable — start uvicorn first." >&2
  exit 1
fi

cd apps/web
exec npm run test:e2e:power-rag -- "$@"
