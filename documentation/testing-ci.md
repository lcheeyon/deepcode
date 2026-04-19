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

### Playwright — real API + worker (power-rag Git BDD)

The file **`apps/web/e2e/bdd-console-power-rag.spec.ts`** drives the **Next console** against a **real** `uvicorn` instance (no route mocks). It creates a scan for **[lcheeyon/power-rag](https://github.com/lcheeyon/power-rag)** with **`clone_depth: 1`**, then waits until the UI shows **`COMPLETE`** (worker must be running with **Redis** job delivery).

- **Opt-in:** set **`E2E_POWER_RAG_BACKEND=1`**. Optional: **`E2E_API_BASE_URL`** (default `http://127.0.0.1:8000`), **`E2E_API_KEY`** (default `dev`).
- **Hermes (real clone + tar upload to MinIO):** on the worker set **`DEEPGUARD_HERMES_ENABLED=1`** and the **`DEEPGUARD_S3_*`** variables aligned with **`docker/compose.dev.yml`** (see **`.env.example`**). Run **`docker compose -f docker/compose.dev.yml run --rm minio-init`** once for the bucket and browser CORS.
- **Convenience:** from the repo root, **`bash scripts/run_web_e2e_power_rag_bdd.sh`** checks **`GET /v1/healthz`** then runs **`npm run test:e2e:power-rag`** in **`apps/web`** (pass extra Playwright args after `--`).
- **CI default:** that spec’s suite is **skipped** unless **`E2E_POWER_RAG_BACKEND`** is set (too slow and needs Docker + worker). The **mocked** UI tour stays in **`apps/web/e2e/bdd-console-power-rag-mock.spec.ts`** and runs in **`web-console-e2e`**.

### Playwright — live E2E (no route mocks)

**`apps/web/e2e/e2e-live-control-plane.spec.ts`** drives the console against a **real** FastAPI base URL with **no `page.route` interception** — useful to confirm **`GET /v1/healthz`**, **`POST /v1/scans`**, **`GET /v1/scans/{id}`**, and auth headers end-to-end.

- **Opt-in:** **`E2E_LIVE_BACKEND=1`**. Optional: **`E2E_API_BASE_URL`** (default `http://127.0.0.1:8000`), **`E2E_API_KEY`** (default `dev`).
- **Run:** `cd apps/web && npm run test:e2e:live` (same CORS / API key expectations as manual Settings testing).
- **CI default:** suite is **skipped** unless **`E2E_LIVE_BACKEND`** is set (needs a reachable API; not part of the default **`npm run test:e2e`** gate).

### Playwright BDD → single PDF (step screenshots)

After a normal Playwright run, **`playwright-report/results.json`** is produced (see **`apps/web/playwright.config.ts`**, JSON reporter). The repo script **`scripts/playwright_bdd_report_to_pdf.py`** reads that file, decodes **PNG attachments** (including BDD **`stepScreenshot`** frames), and writes **`reports/playwright-bdd-report.pdf`** (one image per page section under each test).

```bash
cd apps/web
npm run test:e2e
npm run report:bdd-pdf
open ../../reports/playwright-bdd-report.pdf   # macOS
```

From the repository root (defaults assume **`apps/web/playwright-report`**):

```bash
python3 scripts/playwright_bdd_report_to_pdf.py --output reports/playwright-bdd-report.pdf
```

**Note:** If you pass **`--reporter=…`** on the Playwright CLI and omit the JSON reporter, **`results.json`** will not be written; use the default **`npm run test:e2e`** config or add **`json`** to your reporter list.

## User-story traceability

Generator and validator:

```bash
python3 scripts/generate_ac_details_and_squad_docs.py
python3 scripts/generate_bdd_stubs_from_traceability.py
python3 scripts/validate_user_stories_traceability.py
```

Canonical epics live in **`docs/user-stories/EPIC-*.md`**. Supplements that must not be picked up by the generator use the **`SUPPLEMENT-*.md`** filename pattern (see [Backlog & traceability](backlog.md)).

**EPIC-DG-14 (console MVP) — BDD ↔ CI evidence:** Per-AC Gherkin anchors are in **`apps/web/e2e/features/epic-dg-14-bdd-catalog.feature.md`**. The supplementary matrix **`docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`** maps each **AC-DG-14-*** to Playwright spec hints, **`web-console-e2e`** / artifact **`playwright-report-console`**, a GitHub Actions workflow URL template, and **`reports/playwright-bdd-report.pdf`**. Index: **`apps/web/e2e/features/README.md`**.

## Benchmark campaign BDD (OSS corpus + report endpoints)

- Manifest: **`docs/benchmarks/deepguard-benchmark-manifest.json`** (10 OSS repos, mixed git/zip).
- Mocked E2E: **`apps/web/e2e/bdd-benchmark-manifest-mock.spec.ts`** (always CI-safe).
- Real backend E2E (opt-in): **`apps/web/e2e/bdd-benchmark-manifest.spec.ts`** with **`E2E_BENCHMARK_BACKEND=1`**.

Example local run (real API + worker):

```bash
cd apps/web
E2E_BENCHMARK_BACKEND=1 E2E_BENCHMARK_LIMIT=3 E2E_API_BASE_URL=http://127.0.0.1:8000 E2E_API_KEY=dev npm run test:e2e -- e2e/bdd-benchmark-manifest.spec.ts
```

After scans complete, generate reviewer/investor index markdown:

```bash
python3 scripts/export_benchmark_reports_index.py \
  --api-base-url http://127.0.0.1:8000 \
  --api-key dev \
  --scan-ids-file reports/benchmark/scan-ids.txt \
  --output reports/benchmark/index.md
```
