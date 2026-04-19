# BDD feature files (Playwright)

Human-readable **Gherkin-style** scenarios live here. **Automation** is implemented in **`apps/web/e2e/*.spec.ts`** using `@playwright/test` and **`test.step`** + **`stepScreenshot()`** for HTML report evidence.

**Init scripts:** use `page.addInitScript(fn, arg)` (two-argument form) for anything that depends on Node constants (for example `baseUrl` or `scan_id`). A plain `addInitScript(() => { localStorage.setItem(..., SOME_CONST) })` does **not** serialize outer variables into the browser, so `SOME_CONST` would be missing at runtime.

| File | Scope |
|------|--------|
| [`console-mvp.feature.md`](console-mvp.feature.md) | Short mirror of the original **mocked** console smoke (`console.spec.ts`). |
| [`epic-dg-14-bdd-catalog.feature.md`](epic-dg-14-bdd-catalog.feature.md) | **Full EPIC-DG-14** catalog: all **32** **AC-DG-14-*** headings with epic-quoted criteria plus **concrete** multi-scenario Gherkin; anchors match `traceability-epic-dg-14-bdd-evidence.csv`. |
| [`benchmark-manifest.feature.md`](benchmark-manifest.feature.md) | Benchmark campaign flow for 10 OSS repos: create scans, poll completion, and verify report retrieval endpoints for GitHub-sharing evidence. |

## Evidence chain (audit)

1. **Canonical ACs:** `docs/user-stories/EPIC-14-console-frontend-backend-mvp.md` and `docs/user-stories/traceability-ac-detail-matrix.csv`.
2. **BDD ↔ AC mapping + CI/PDF links:** `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv` (columns include GitHub anchor URL, Playwright specs, CI workflow URL, HTML artifact name, local PDF path).
3. **CI HTML report:** GitHub Actions → workflow **Quality** → job **`web-console-e2e`** → artifact **`playwright-report-console`** → open `index.html` (per-run URL is under the run’s **Artifacts** section). Example workflow list: `https://github.com/lcheeyon/deepcode/actions/workflows/quality.yml` (replace owner/repo for your fork).
4. **Single PDF bundle (screenshots):** after `cd apps/web && npm run test:e2e`, run `npm run report:bdd-pdf` → `reports/playwright-bdd-report.pdf` (repo root).

## Currently automated spec files

| Spec | Role |
|------|------|
| `e2e/console.spec.ts` | MVP smoke: settings, create scan, cancel (mocked API). |
| `e2e/api-validation.spec.ts` | 503 repo-upload, 422 field mapping (mocked). |
| `e2e/bdd-console-power-rag-mock.spec.ts` | Long BDD tour + **power-rag** URL (mocked). |
| `e2e/e2e-live-control-plane.spec.ts` | **Live E2E (no HTTP mocks):** real browser → real `/v1` (`healthz`, dashboard refresh, default Git create, API cross-check, Bearer path, recent scans). Gated by **`E2E_LIVE_BACKEND=1`** — run `npm run test:e2e:live` when API (+ CORS) is up. |
| `e2e/bdd-epic-dg-14-comprehensive-mock.spec.ts` | **Broad EPIC-DG-14 BDD**: shell/theme/mobile, settings auth (X-API-Key / Bearer / 401), dashboard health, create-form validation, presign prepare-only, scans hub, scan detail/cancel, edge cases (many `test.step` entries for the HTML report). |
| `e2e/bdd-console-power-rag.spec.ts` | Real API + worker (opt-in `E2E_POWER_RAG_BACKEND=1`). |
| `e2e/bdd-benchmark-manifest-mock.spec.ts` | Benchmark corpus campaign (10 repos, mocked API): create all scans + validate eventual report endpoints. |
| `e2e/bdd-benchmark-manifest.spec.ts` | Real backend benchmark campaign (opt-in `E2E_BENCHMARK_BACKEND=1`, git subset by default). |
| `e2e/repo-upload-minio.spec.ts` | Real MinIO + API (`E2E_REAL_API=1`). |
