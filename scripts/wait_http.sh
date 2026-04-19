#!/usr/bin/env bash
# Usage: wait_http.sh <url> [max_seconds]
set -euo pipefail
URL="${1:?url required}"
MAX="${2:-60}"
for _ in $(seq 1 "$MAX"); do
  if curl -sf "$URL" >/dev/null; then
    exit 0
  fi
  sleep 1
done
echo "Timeout waiting for ${URL}" >&2
exit 1
