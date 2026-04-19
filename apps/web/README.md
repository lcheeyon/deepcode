# DeepGuard web console (EPIC-DG-14 MVP)

Next.js 14 (App Router) + TypeScript + Tailwind. Visual rules follow **`.cursor/skills/deepguard-ui-style-guide/SKILL.md`** and **`reference.md`**. Wireframes: **`docs/design/frontend-console-mvp-wireframes-and-mockups.md`**. Step-by-step delivery order: **`docs/design/frontend-implementation-plan.md`**.

## Environment variables

| Variable | Where | Purpose |
|----------|--------|---------|
| `NEXT_PUBLIC_APP_VERSION` | build-time | Shown in sidebar footer (default `0.1.0`). |
| `NEXT_PUBLIC_DEEPGUARD_ENV` | build-time | Environment pill, e.g. `staging` (default `local`). |

API **base URL** and **API key** are stored in **browser `localStorage`** from the Settings page (MVP dev pattern — not for production secrets).

## Run locally

```bash
cd apps/web
npm install
npm run dev
```

Open **http://127.0.0.1:3000**. Configure **Settings → API connection** with your control plane URL (e.g. `http://127.0.0.1:8000`) and `X-API-Key`.

### CORS (browser → API on another port)

The FastAPI app must allow your dev origin, for example:

```bash
export DEEPGUARD_CORS_ORIGINS=http://127.0.0.1:3000,http://localhost:3000
uvicorn deepguard_api.main:app --reload --port 8000
```

See repository **`.env.example`** for `DEEPGUARD_CORS_ORIGINS`.

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Next dev server (port 3000). |
| `npm run build` | Production build. |
| `npm run test:e2e` | Playwright tests (`e2e/`): mocked API routes + **skipped** real MinIO tests unless `E2E_REAL_API=1`. |
| `npm run test:e2e:compose` | Only **`e2e/repo-upload-minio.spec.ts`** — hits a real API + MinIO (set `E2E_API_BASE_URL` / `E2E_API_KEY` as needed). |
| `npm run test:e2e:ui` | Playwright UI mode. |
| `./scripts/agent-browser-smoke.sh` | Optional snapshot smoke (requires [agent-browser](https://agent-browser.dev/) CLI). Set `PLAYWRIGHT_BASE_URL` if not using default `http://127.0.0.1:3000`. |

CI should set **`CI=1`** so Playwright starts its own dev server (see `playwright.config.ts`).

### Playwright HTML report (step screenshots)

After **`npm run test:e2e`**, open the report:

```bash
npx playwright show-report playwright-report
```

Each BDD step uses **`e2e/helpers/bdd-step-screenshot.ts`** (`stepScreenshot`) to attach a **full-page PNG** under that step in the HTML UI. GitHub Actions uploads the **`playwright-report/`** directory as artifacts (**`playwright-report-console`**, **`playwright-report-minio`**). Set **`PW_TRACE=1`** before the run to record full **traces** (heavier than screenshots alone).

### Compose-backed MinIO (real `POST /v1/repo-uploads`)

GitHub Actions job **`web-console-e2e-compose`** starts **MinIO** (`docker/compose.dev.yml`), runs **`minio-init`** (bucket + **`mc cors set-json`** from `docker/minio-cors.json` so the browser can **`PUT`** to the presigned host from `http://127.0.0.1:3000`), starts **`uvicorn`** with **`DEEPGUARD_S3_*`**, then runs **`E2E_REAL_API=1`** Playwright against **`e2e/repo-upload-minio.spec.ts`**. Local reproduction: **`docs/dev-setup.md`** section *Web console — Playwright with real MinIO presign*.

## Implemented user stories (traceability)

| ID | Summary |
|----|---------|
| US-DG-14-001 | App shell, sidebar 240px, disabled nav placeholders, version/env footer, mobile drawer. |
| US-DG-14-002 | Settings: base URL, API key, Bearer vs X-API-Key, test health + auth probe, 401 alert. |
| US-DG-14-003 | Dashboard health card + Redis info card. |
| US-DG-14-004 | Full create-scan form + client validation + 422 mapping. |
| US-DG-14-005 | Repo upload modal (presign + PUT, 503 handling). |
| US-DG-14-006 | Scan detail, 5s poll (skips when tab hidden), job_config expand. |
| US-DG-14-007 | Cancel with confirm dialog. |
| US-DG-14-008 | Recent scans + open-by-UUID + clear list. |
| US-DG-14-009 | Status badges with dot + semantic colours. |
| US-DG-14-010 | Responsive padding + drawer. |
| US-DG-14-011 | Focus rings, `aria-live` toasts, reduced-motion CSS. |
| US-DG-14-012 | Theme: system / light / dark (persisted). |
| US-DG-14-013 | Playwright `e2e/console.spec.ts`. |
| US-DG-14-014 | This README + env docs. |
