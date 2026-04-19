#!/usr/bin/env bash
# Optional smoke using agent-browser (https://agent-browser.dev/).
# Start the console first: npm run dev  (default http://127.0.0.1:3000)
set -euo pipefail
BASE_URL="${PLAYWRIGHT_BASE_URL:-http://127.0.0.1:3000}"

if ! command -v agent-browser >/dev/null 2>&1; then
  echo "agent-browser not installed; skipping smoke."
  echo "Install: npm install -g agent-browser  OR  brew install agent-browser"
  exit 0
fi

echo "Opening ${BASE_URL}/dashboard …"
agent-browser open "${BASE_URL}/dashboard"
agent-browser snapshot -i | tee /dev/stderr | grep -q "Dashboard" || {
  echo "Expected 'Dashboard' in snapshot"
  agent-browser close || true
  exit 1
}
agent-browser open "${BASE_URL}/scans/new"
agent-browser snapshot -i | tee /dev/stderr | grep -q "New scan" || {
  echo "Expected 'New scan' in snapshot"
  agent-browser close || true
  exit 1
}
agent-browser close || true
echo "agent-browser smoke OK."
