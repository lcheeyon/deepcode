# Testing & CI

## Default expectations

After changing Python code, the repo expects (see **`AGENTS.md`**):

1. **Ruff** — lint + format check.
2. **Mypy** — strict, on all `deepguard_*` packages listed in `pyproject.toml`.
3. **Pyright** — `python3 -m pyright` with `extraPaths` aligned to `src` roots.
4. **import-linter** — `bash scripts/run_lint_imports.sh`.
5. **Bandit** — security lint on API, worker, agents, connectors.
6. **pytest** — **`--cov-fail-under=80`** on the agreed package set.
7. **deptry** — unused / undeclared dependencies (`make ci-quality`).

## One-shot gates

| Command | When |
|---------|------|
| `pre-commit run --all-files` | Git checkout; mirrors hook pipeline. |
| `make ci-quality` | No git / CI parity: hooks + **deptry** + full pytest coverage. |
| `make audit` | **deptry** + **pip-audit** (advisory; may fail on transitive CVEs). |

## HTML phase reports

Self-contained pytest-html aggregates:

```bash
python3 scripts/generate_phase_html_reports.py
```

Output: **`reports/html/`** (gitignored). Optional `--open` to launch a browser.

## Integration API tests — pytest-html with request/response JSON

When you run **`pytest`** with **`pytest-html`** and the built-in **`extras`** fixture, integration tests can attach **sample request and response JSON** so the HTML report proves what was exercised.

Example (Postgres-backed L3 API test after Docker + env are set):

```bash
pip3 install -e ".[dev]"
pytest -m integration tests/integration/test_l3_api_postgres.py -v \
  --html=reports/html/integration-l3-api.html \
  --self-contained-html
```

Open the HTML file in a browser: each test row includes collapsible **extras** named **`POST /v1/scans`** and **`GET /v1/scans/{id}`** with structured JSON (`request.json_body`, `response.json_body`, HTTP status). The helper lives in **`tests/integration/reporting.py`**.

## Playwright console — HTML report with step screenshots

The **`apps/web`** suite uses **`stepScreenshot()`** (`e2e/helpers/bdd-step-screenshot.ts`) so each BDD **`test.step`** ends with a **full-page PNG** attached to the Playwright HTML report. Generate the report with **`npm run test:e2e`**, then:

```bash
cd apps/web && npx playwright show-report playwright-report
```

In the report UI, open a test and expand each step to view its screenshot. CI uploads the **`playwright-report/`** folder as workflow artifacts (**`playwright-report-console`** and **`playwright-report-minio`**). Set **`PW_TRACE=1`** for full traces (larger).

## User-story traceability

Generator and validator:

```bash
python3 scripts/generate_ac_details_and_squad_docs.py
python3 scripts/validate_user_stories_traceability.py
```

Canonical epics live in **`docs/user-stories/EPIC-*.md`**. Supplements that must not be picked up by the generator use the **`SUPPLEMENT-*.md`** filename pattern (see [Backlog & traceability](backlog.md)).
