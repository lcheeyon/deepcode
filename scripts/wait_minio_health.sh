#!/usr/bin/env bash
# Wait until MinIO S3 API responds (compose-backed e2e / local).
set -euo pipefail
HOST="${MINIO_HEALTH_HOST:-127.0.0.1}"
PORT="${DEEPGUARD_MINIO_API_PORT:-9000}"
URL="http://${HOST}:${PORT}/minio/health/live"
for _ in $(seq 1 90); do
  if curl -sf "$URL" >/dev/null; then
    exit 0
  fi
  sleep 1
done
echo "MinIO not healthy at ${URL}" >&2
exit 1
