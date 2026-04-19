# Getting started

## Prerequisites

- **Python 3.12+**
- **Git** (optional but recommended for pre-commit)
- **Docker Desktop** or compatible engine when you use the local data plane (Postgres, Redis, MinIO)

## Install the workspace

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip3 install -U pip
pip3 install -e ".[dev]"
```

Editable packages include: `deepguard_core`, `deepguard_graph`, `deepguard_policies`, `deepguard_parsers`, `deepguard_connectors`, `deepguard_agents`, `deepguard_reporting`, `deepguard_observability`, `deepguard_api`, `deepguard_worker`.

## Documentation site (this book)

```bash
pip3 install -e ".[docs]"
python3 -m mkdocs serve
```

## Fast quality loop

```bash
ruff check .
mypy -p deepguard_core -p deepguard_graph -p deepguard_policies -p deepguard_parsers \
  -p deepguard_connectors -p deepguard_agents -p deepguard_reporting -p deepguard_observability \
  -p deepguard_api -p deepguard_worker
python3 -m pyright
pytest -q --cov --cov-fail-under=80
```

Integration tests (`@pytest.mark.integration`) are skipped by default; run them when Docker services are up. See [Testing & CI](testing-ci.md) and the canonical **`docs/dev-setup.md`** in the repo for full detail, optional pre-commit, `make ci-quality`, and phase-by-phase commands (L1–L14).

## Run the control plane API (minimal)

- **In-memory store (no database):** omit `DATABASE_URL`; optional `DEEPGUARD_L3_MEMORY_STORE=1` for clarity.
- **Postgres + Redis (enqueue):** set `DATABASE_URL` (async Postgres URL), `REDIS_URL`, `DEEPGUARD_DEV_TENANT_ID`, and optionally `DEEPGUARD_DEV_API_KEY`.

```bash
uvicorn deepguard_api.main:app --reload --port 8000
```

Interactive OpenAPI: **`http://127.0.0.1:8000/v1/docs`**.

See [Control plane API](control-plane-api.md) and [Docker & data plane](docker-data-plane.md) for a typical local stack.
