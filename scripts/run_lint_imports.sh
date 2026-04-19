#!/usr/bin/env bash
# import-linter needs the same source roots as editable installs / mypy_path.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/packages/core/src:${ROOT}/packages/graph/src:${ROOT}/packages/policies/src:${ROOT}/packages/parsers/src:${ROOT}/packages/connectors/src:${ROOT}/packages/agents/src:${ROOT}/packages/reporting/src:${ROOT}/packages/observability/src:${ROOT}/apps/api/src:${ROOT}/apps/worker/src"
LINT_IMPORTS="${ROOT}/.venv/bin/lint-imports"
if [ ! -x "$LINT_IMPORTS" ]; then
  LINT_IMPORTS="lint-imports"
fi
exec "$LINT_IMPORTS"
