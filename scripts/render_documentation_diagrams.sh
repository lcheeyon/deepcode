#!/usr/bin/env bash
# Render Mermaid sources under documentation/diagrams/ to PNG in documentation/images/.
# Uses Kroki (HTTPS) so no local Chromium is required. Run from repo root:
#   bash scripts/render_documentation_diagrams.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIAG="$ROOT/documentation/diagrams"
IMG="$ROOT/documentation/images"
mkdir -p "$IMG"

render_one() {
  local name="$1"
  echo "Rendering ${name}.mmd -> images/${name}.png"
  curl -sS -f -o "$IMG/${name}.png" \
    -H "Content-Type: text/plain" \
    --data-binary "@$DIAG/${name}.mmd" \
    "https://kroki.io/mermaid/png"
}

render_one odysseus-full-agent-flow
echo "OK: $IMG/odysseus-full-agent-flow.png"
