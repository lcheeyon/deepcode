#!/usr/bin/env bash
# Full L12 path: Compose + migrate + seed + API + worker in background, then pytest poll for COMPLETE.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export DATABASE_URL_SYNC="${DATABASE_URL_SYNC:-postgresql://deepguard:deepguard@127.0.0.1:5432/deepguard}"
export DATABASE_URL="${DATABASE_URL:-postgresql+asyncpg://deepguard:deepguard@127.0.0.1:5432/deepguard}"
export REDIS_URL="${REDIS_URL:-redis://127.0.0.1:6379/0}"

docker compose -f docker/compose.dev.yml up -d
python3 -m alembic upgrade head
python3 scripts/seed_dev_tenant.py

export DEEPGUARD_DEV_TENANT_ID="$(
  python3 -c "
import os
import psycopg
url = os.environ['DATABASE_URL_SYNC']
with psycopg.connect(url) as c:
    with c.cursor() as cur:
        cur.execute('select id::text from tenants order by created_at limit 1')
        print(cur.fetchone()[0])
"
)"
export DEEPGUARD_DEV_API_KEY="${DEEPGUARD_DEV_API_KEY:-dev}"
export DEEPGUARD_E2E_LOCAL=1
export DEEPGUARD_E2E_FULL=1
export DEEPGUARD_API_BASE="${DEEPGUARD_API_BASE:-http://127.0.0.1:8000}"

cleanup() {
  kill "${WORKER_PID:-}" 2>/dev/null || true
  kill "${API_PID:-}" 2>/dev/null || true
}
trap cleanup EXIT

python3 -m uvicorn deepguard_api.main:app --host 127.0.0.1 --port 8000 &
API_PID=$!
python3 -m deepguard_worker &
WORKER_PID=$!

for _ in $(seq 1 60); do
  if curl -sf "${DEEPGUARD_API_BASE}/v1/healthz" >/dev/null; then
    break
  fi
  sleep 0.5
done

python3 -m pytest tests/e2e/test_full_scan_local.py -m integration \
  -k "test_scan_reaches_complete" \
  --override-ini="addopts=-q --strict-markers" -v
