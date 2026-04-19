#!/usr/bin/env bash
# CI / full gate: same checks as pre-commit (when git is unavailable, run this script instead of
# ``pre-commit run --all-files``) plus dependency audit and full pytest with coverage.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# EPIC-DG-11: keep CI hermetic (no LangSmith/LangFuse network); OTEL console noise down.
export LANGCHAIN_TRACING_V2="${LANGCHAIN_TRACING_V2:-false}"
export DEEPGUARD_OTEL_BOOTSTRAP="${DEEPGUARD_OTEL_BOOTSTRAP:-0}"

python3 -m ruff check .
python3 -m ruff format --check .
python3 -m mypy -p deepguard_core -p deepguard_graph -p deepguard_policies -p deepguard_parsers \
  -p deepguard_connectors -p deepguard_agents -p deepguard_reporting -p deepguard_observability \
  -p deepguard_api -p deepguard_worker
python3 -m pyright
python3 -m pytest -q -m "not integration" --tb=short --maxfail=5
bash scripts/run_lint_imports.sh
python3 -m bandit -c pyproject.toml -q -r apps/api/src apps/worker/src packages/agents/src packages/connectors/src
python3 -m deptry .
python3 -m pytest -q --cov --cov-fail-under=80
