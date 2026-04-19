# DeepGuard Compliance Engine (玄武)

Agentic compliance scanning: **code + IaC + cloud** → policy controls → **findings**, **remediations**, and **PDF reports**.

## Documentation

- **Browseable docs site ([Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)):** install the optional extra, then serve or build:
  - **Published (GitHub Pages):** [https://lcheeyon.github.io/deepcode/](https://lcheeyon.github.io/deepcode/) — enable **Settings → Pages → Source: GitHub Actions** on first use; workflow: `.github/workflows/docs.yml`. If `git push` is rejected for workflow files, refresh credentials with workflow scope: `gh auth refresh -h github.com -s workflow`.
  - Local: `pip3 install -e ".[docs]"` then `python3 -m mkdocs serve` (or `make docs` for a strict build to `site/`).
  - Source pages: `documentation/` · config: `mkdocs.yml`.
- **Architecture:** [`Architecture_Design.md`](Architecture_Design.md)
- **Implementation phases:** [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md)
- **User stories:** [`docs/user-stories/README.md`](docs/user-stories/README.md)
- **Local dev (venv, lint, tests):** [`docs/dev-setup.md`](docs/dev-setup.md)
- **PDF writeups (repo root):**
  - [DeepGuard_Compliance_Engine.pdf](DeepGuard_Compliance_Engine.pdf) — compliance engine overview (PDF).
  - [DeepGuard_Executive_Summary.pdf](DeepGuard_Executive_Summary.pdf) — executive summary (PDF).
  - [玄武合规引擎_商业计划书.pdf](玄武合规引擎_商业计划书.pdf) — business plan (中文 PDF).

## Quick start (Phase L0)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip3 install -U pip
pip3 install -e ".[dev]"
ruff check .
mypy -p deepguard_core -p deepguard_graph
python3 -m pyright
pytest -q --cov --cov-fail-under=80
```

Optional **pre-commit** (git clone only): `pip3 install -e ".[dev]" && pre-commit install && pre-commit run --all-files`.  
Without git, run **`make ci-quality`** (see `scripts/ci_quality.sh`) for the same checks plus **`deptry`**, then full pytest with coverage. For **`pip-audit`**, run **`make audit`** (also used in CI as an advisory job).

### Phase L1 (local database + cache + object store)

```bash
docker compose -f docker/compose.dev.yml up -d
export DATABASE_URL_SYNC=postgresql://deepguard:deepguard@127.0.0.1:5432/deepguard
alembic upgrade head
python3 scripts/seed_dev_tenant.py
```

If Compose reports **port already allocated**, set `DEEPGUARD_POSTGRES_PORT` / `DEEPGUARD_REDIS_PORT` in a repo-root `.env` (see `.env.example`) and match `DATABASE_URL_SYNC` / `REDIS_URL` to those host ports.

Details: [`docs/dev-setup.md`](docs/dev-setup.md).

Use **python3** and **pip3** per project conventions.

## Web console (EPIC-DG-14)

The product MVP UI lives in **`apps/web`** (Next.js). Quick start, CORS, Playwright, and optional **agent-browser** smoke: see **`apps/web/README.md`**.

**Per-phase HTML test reports:** ``python3 scripts/generate_phase_html_reports.py`` → ``reports/html/index.html`` (see [`docs/dev-setup.md`](docs/dev-setup.md)).

**Phase L2 (core Pydantic models):** ``pytest packages/core/tests -q --cov=deepguard_core --cov-report=term-missing`` (or full workspace ``pytest -q --cov``).

**Phase L3 (FastAPI):** ``uvicorn deepguard_api.main:app --port 8000`` with ``DATABASE_URL`` + ``DEEPGUARD_DEV_TENANT_ID`` for Postgres persistence, or omit ``DATABASE_URL`` for in-memory dev. Tests: ``pytest tests/test_l3_api.py -q``.
