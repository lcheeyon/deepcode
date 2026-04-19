# Monorepo layout

The workspace matches **Architecture §25** (repository layout and ownership boundaries).

## Applications

| Path | Package | Role |
|------|---------|------|
| `apps/api/src` | `deepguard_api` | FastAPI control plane (`/v1`, OpenAPI at `/v1/openapi.json`). |
| `apps/worker/src` | `deepguard_worker` | Async worker: Redis stream consumer, scan job execution. |

## Libraries (`packages/*/src`)

| Package | Role (summary) |
|---------|------------------|
| `deepguard_core` | Domain models, shared types, queue payload shapes. |
| `deepguard_graph` | LangGraph Odysseus graph, checkpoint helpers. |
| `deepguard_policies` | Policy engine pieces (Tiresias direction). |
| `deepguard_parsers` | Parsing / normalization helpers. |
| `deepguard_connectors` | External and cloud-oriented connectors. |
| `deepguard_agents` | Agent nodes and tools (Hermes, Athena, etc.). |
| `deepguard_reporting` | Report pipeline (Penelope direction). |
| `deepguard_observability` | Telemetry and hooks. |

## Supporting directories

| Path | Purpose |
|------|---------|
| `tests/` | Cross-cutting API and integration tests. |
| `packages/*/tests/` | Package-scoped unit tests. |
| `docker/compose.dev.yml` | Local Postgres, Redis, MinIO. |
| `alembic/` | Database migrations (sync driver URL for CLI). |
| `docs/` | Design specs, user stories, dev-setup prose (not MkDocs source). |
| `scripts/` | Seeds, traceability generators, CI helpers. |
| `eval/` | Evaluation fixtures and harness tests. |

## Import boundaries

**import-linter** enforces that library packages do not import FastAPI apps and that `deepguard_core` stays independent. Run `bash scripts/run_lint_imports.sh` or rely on pre-commit / `make ci-quality`. Configuration: `[tool.importlinter]` in `pyproject.toml`.
