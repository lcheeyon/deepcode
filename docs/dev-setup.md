# Developer setup (local laptop)

## Python environment

Requires **Python 3.12+**.

```bash
cd /path/to/deep-code
python3 -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate           # Windows
pip3 install -U pip
pip3 install -e ".[dev]"
```

The workspace installs editable packages: `deepguard_core`, `deepguard_graph`, `deepguard_policies`, `deepguard_parsers`, `deepguard_connectors`, `deepguard_agents`, `deepguard_reporting`, `deepguard_observability`, `deepguard_api`, `deepguard_worker`.

## Quality gates (Phase L0)

```bash
ruff check .
mypy -p deepguard_core -p deepguard_graph -p deepguard_policies -p deepguard_parsers \
  -p deepguard_connectors -p deepguard_agents -p deepguard_reporting -p deepguard_observability \
  -p deepguard_api -p deepguard_worker
python3 -m pyright
pytest -q --cov --cov-fail-under=80
```

- **Ruff** applies to `packages/`, `apps/`, and `tests/`.
- **Mypy strict** applies to all `deepguard_*` packages listed above. Root `pyproject.toml` sets `mypy_path` so `mypy -p …` works from a clean checkout.
- **Pyright** (`python3 -m pyright`) uses `[tool.pyright]` in `pyproject.toml` (`extraPaths` mirror the monorepo `src` roots). Run from the repo root with dev deps installed.
- **Pytest** with coverage threshold 80% on all listed packages.
- **Integration tests** (`@pytest.mark.integration`) are **skipped by default** (`-m "not integration"` in `pyproject.toml`). Run `pytest -m integration` when Docker is up.

### Pre-commit, import boundaries, dependencies, security

- **Pre-commit** (`.pre-commit-config.yaml`): Ruff check + format, Mypy, Pyright, fast pytest (`-m "not integration"`, `--maxfail=5`), **import-linter** (`scripts/run_lint_imports.sh`), **Bandit** on `apps/api/src`, `apps/worker/src`, `packages/agents/src`, `packages/connectors/src`. Requires a **git** checkout: `pre-commit install` then `pre-commit run --all-files` (or `make pre-commit`).
- **CI / no-git full gate:** `make ci-quality` runs `scripts/ci_quality.sh` (same hooks as pre-commit, plus **`deptry`**, then full **`pytest --cov`**). Use this in CI or when the tree is not a git repo.
- **Dependency CVE audit:** `make audit` runs **`deptry`** again plus **`pip-audit`** (often surfaces transitive advisories; triage pins/upgrades separately). GitHub Actions runs this in a **`continue-on-error`** job (see `.github/workflows/quality.yml`).
- **import-linter** contracts live under `[tool.importlinter]` in `pyproject.toml` (core independence + library packages must not import apps).
- **deptry** is configured under `[tool.deptry]` (first-party packages, excludes legacy root scripts, `per_rule_ignores` for dev/runtime tooling).
- **Bandit** reads `[tool.bandit]` from `pyproject.toml` (skips `B101` assert warnings; excludes `tests/`).

## Optional — agent-browser (AI / agent troubleshooting)

[agent-browser](https://agent-browser.dev/) is a **native Rust CLI** for browser automation from the terminal: compact **accessibility snapshots** with stable **`@eN` refs**, clicks, forms, screenshots, and sessions. It is **not** a Python dependency of this repo; install globally when you want agents (or you) to debug a **running** web UI without writing Playwright first.

**Install:** `npm install -g agent-browser` or `brew install agent-browser`; first Chrome fetch: `agent-browser install`.

**When to use:** reproduce issues against local `uvicorn` + `/docs`, explore flows, capture screenshots. **Regression tests** stay in **pytest / Playwright** per the delivery skill.

**How agents use it:** read `.cursor/skills/deepguard-agent-browser/SKILL.md`.

## Optional — MCPorter (MCP from the shell, including Chrome DevTools)

[MCPorter](https://mcporter.dev/) is a **CLI and TypeScript runtime** for the [Model Context Protocol](https://modelcontextprotocol.io/): it **imports** MCP configs from Cursor / Claude Code / Codex, runs **`npx mcporter list`** to show **tool names and signatures**, and **`npx mcporter call …`** to invoke them—so agents can use **Chrome DevTools MCP** (`chrome-devtools-mcp` via stdio) without relying on a free MCP slot in the editor. **`mcporter generate-cli`** can package a server as a **standalone CLI** for sharing.

**Try:** `npx mcporter list` then `npx mcporter list chrome-devtools` (or ad-hoc `--stdio "npx -y chrome-devtools-mcp@latest"` per upstream docs).

**How agents use it:** read `.cursor/skills/deepguard-mcporter/SKILL.md`. Not a Python dependency; respect **air-gap** policy if `npx` cannot reach a registry.

## Phase L3 — Control plane API (`deepguard_api`)

1. Install deps: ``pip3 install -e ".[dev]"``.
2. **Postgres-backed API:** set ``DATABASE_URL`` (``postgresql+asyncpg://…``), ``REDIS_URL`` (required with Postgres for Phase L4 enqueue), ``DEEPGUARD_DEV_TENANT_ID`` (UUID of a row in ``tenants`` from seed), and ``DEEPGUARD_DEV_API_KEY`` (optional, default ``dev``). Run ``uvicorn deepguard_api.main:app --reload --port 8000``.
3. **No database (memory store):** omit ``DATABASE_URL``; the process uses an in-memory scan repository (tests use this path explicitly via ``create_app(Settings(...))``).
4. Unit tests: ``pytest tests/test_l3_api.py -q``.
5. Optional integration (real DB + Redis): ``DEEPGUARD_API_TEST=1`` plus ``DATABASE_URL``, ``REDIS_URL``, and tenant env vars, then ``pytest -m integration tests/integration/test_l3_api_postgres.py -v``.

## Phase L4 — Queue producer + worker skeleton

1. With **Postgres API** (see above), each new ``POST /v1/scans`` appends a job to Redis Stream ``stream:scans`` (consumer group ``workers`` is created by the worker on startup).
2. Run the consumer: ``python3 -m deepguard_worker`` (or ``python3 -m apps.worker.main`` from the repo root with the usual ``PYTHONPATH`` / editable install). Required env: ``DATABASE_URL``, ``REDIS_URL``. Optional: ``DEEPGUARD_WORKER_CONSUMER``, ``DEEPGUARD_WORKER_HEARTBEAT_SEC``, ``DEEPGUARD_WORKER_STUB_ITERATIONS``.
3. Unit tests: ``pytest tests/test_l4_api.py tests/test_l4_worker_unit.py packages/core/tests/test_queue_scan_message.py -q``.

## Phase L5 — Odysseus LangGraph shell (`deepguard_graph`)

1. **Graph:** ``build_odysseus_graph()`` returns a ``StateGraph`` wired per Architecture §4.1 (Hermes → Penelope) with stub nodes and parallel Laocoon / Cassandra branches. Compile with a checkpointer; use ``configurable={"thread_id": str(scan_id)}`` when invoking (Architecture §4.6).
2. **Tests (MemorySaver):** ``pytest packages/graph/tests -q``. Checkpoint resume: ``pytest packages/graph/tests -q -k checkpoint``.
3. **Postgres checkpointer (dev):** sync URI ``postgresql://…`` (not ``+asyncpg``). Set ``CHECKPOINT_DB_URL`` (see ``.env.example``) or reuse metadata DB; open ``postgres_checkpointer(conn_string)`` before ``compile(checkpointer=…)`` and exit the context after the worker stops. Call ``setup()`` once per process (handled inside the helper).

## Phases L6–L14 — agent / policy / parser / reporting scaffolds

Scaffold packages live under ``packages/{agents,policies,parsers,connectors,reporting,observability}/``. Quick test slices:

```bash
pytest packages/agents/tests -q -k "hermes or athena"
pytest packages/policies/tests -q
pytest packages/parsers/tests packages/connectors/tests -q
pytest packages/reporting/tests packages/observability/tests -q
pytest apps/api/tests -q -k "tenant or auditor"
```

- **L12 E2E:** ``tests/e2e/test_full_scan_local.py`` is marked ``integration``. With the API running (Postgres + Redis per L3/L4), set ``DEEPGUARD_E2E_LOCAL=1`` and run ``make e2e-local`` for healthz + create/get scan + P95 smoke. For **worker → COMPLETE + PDF**, run ``python3 -m deepguard_worker`` in another terminal (same ``DATABASE_URL`` / ``REDIS_URL``), then ``DEEPGUARD_E2E_FULL=1 make e2e-local`` to poll until ``COMPLETE``, or ``make e2e-full`` to start compose + API + worker + that poll via ``scripts/e2e_full_scan.sh``.
- **LangSmith / LangFuse / OTEL (EPIC-DG-11):** Workspace includes ``langsmith``, ``langfuse``, and ``langchain`` for callbacks. ``LANGCHAIN_TRACING_V2`` defaults to **true** outside CI when unset; set ``LANGSMITH_API_KEY`` (or ``LANGCHAIN_API_KEY``) to export traces. For **air-gap**, set ``LANGCHAIN_TRACING_V2=false`` or ``DEEPGUARD_AIR_GAP=1``. **LangFuse** activates when ``LANGFUSE_HOST``, ``LANGFUSE_PUBLIC_KEY``, and ``LANGFUSE_SECRET_KEY`` are all set (see ``docker/langfuse/README.md``). **OpenTelemetry:** API/worker call ``configure_observability_at_startup``; FastAPI instrumentation attaches when an SDK ``TracerProvider`` is installed. Unit tests default ``DEEPGUARD_OTEL_BOOTSTRAP=0`` via ``tests/conftest.py``.

## Phase L2 — Core domain models (`packages/core`)

Pydantic models live under ``deepguard_core.models`` (``CreateScanRequest`` / ``ScanJobConfig``, ``ScanStatePartial``, ``PolicyControl``, ``Finding``, ``AgentError``, enums). Run unit tests:

```bash
pytest packages/core/tests -q --cov=deepguard_core --cov-report=term-missing
```

## HTML test reports (per implementation phase)

Uses **pytest-html** (self-contained HTML). From the repo root, with dev deps installed:

```bash
python3 scripts/generate_phase_html_reports.py
```

This writes ``reports/html/index.html`` plus ``reports/html/phase-<L0|L1|…|C5>/report.html``. Phases without mapped tests get a short stub page. **L1** uses the same environment variables as manual integration runs (`DATABASE_URL_SYNC`, `REDIS_URL`, `MINIO_HEALTH_URL`, `DEEPGUARD_INTEGRATION`); export them before running if your Compose ports differ from the defaults.

Open the index in a browser after generation: ``python3 scripts/generate_phase_html_reports.py --open``. Generated HTML under ``reports/html/`` is gitignored.

## Phase L1 — Docker data plane (Postgres + Redis + MinIO)

1. Start services:

```bash
docker compose -f docker/compose.dev.yml up -d
```

Wait until Postgres is healthy (`docker compose -f docker/compose.dev.yml ps`).

If Compose fails with **port already allocated** (often `6379` or `5432`), add a repo-root `.env` with overrides (see `.env.example`): `DEEPGUARD_REDIS_PORT`, `DEEPGUARD_POSTGRES_PORT`, etc., then point `DATABASE_URL_SYNC` / `REDIS_URL` at the mapped host ports.

2. Run migrations (**sync** URL — not `+asyncpg`). Use the project venv (`pip3 install -e ".[dev]"`) so `psycopg` is available to Alembic’s SQLAlchemy driver.

```bash
source .venv/bin/activate   # if you use a venv
export DATABASE_URL_SYNC=postgresql://deepguard:deepguard@127.0.0.1:5432/deepguard
alembic upgrade head
```

3. Seed dev tenant:

```bash
python3 scripts/seed_dev_tenant.py
```

4. Quick checks:

```bash
docker compose -f docker/compose.dev.yml exec postgres psql -U deepguard -d deepguard -c "SELECT extname FROM pg_extension WHERE extname = 'vector';"
docker compose -f docker/compose.dev.yml exec postgres psql -U deepguard -d deepguard -c "SELECT count(*) FROM tenants;"
docker compose -f docker/compose.dev.yml exec redis redis-cli ping
curl -sf http://127.0.0.1:9000/minio/health/live
```

5. Optional automated integration tests (after migrations + seed):

```bash
export DEEPGUARD_INTEGRATION=1
# If Redis is mapped to a non-default host port, also set REDIS_URL (see .env.example).
pytest -m integration tests/integration/ -v
```

## Web console — Playwright with real MinIO presign (optional)

Mirrors CI job **`web-console-e2e-compose`** (see `.github/workflows/quality.yml`):

1. `docker compose -f docker/compose.dev.yml up -d minio`
2. `bash scripts/wait_minio_health.sh`
3. `docker compose -f docker/compose.dev.yml run --rm minio-init` (creates `deepguard-dev` and applies **`docker/minio-cors.json`** for browser `PUT` from the Next dev server)
4. Start **`uvicorn`** with `DEEPGUARD_S3_BUCKET`, `DEEPGUARD_S3_ENDPOINT_URL=http://127.0.0.1:9000`, keys `deepguard` / `deepguarddev`, `DEEPGUARD_CORS_ORIGINS=http://127.0.0.1:3000` (no `DATABASE_URL` needed for presign-only checks)
5. In **`apps/web`**: `npm run dev`, then in another shell `E2E_REAL_API=1 E2E_API_BASE_URL=http://127.0.0.1:8000 npm run test:e2e:compose`

**Reports:** Playwright HTML (with **per-step screenshots**) → `npx playwright show-report playwright-report` under `apps/web`. Integration API tests with **request/response JSON** in pytest-html → see **`documentation/testing-ci.md`** (section *Integration API tests*).

## Optional: pre-commit

If `.pre-commit-config.yaml` is present:

```bash
pip3 install pre-commit
pre-commit install
pre-commit run --all-files
```
