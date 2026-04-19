# DeepGuard console (EPIC-DG-14) — frontend implementation plan

**Status:** Implemented in **`apps/web`** (Next.js 14). Use this document as a **verification checklist** and for future slices.

**Purpose:** Ordered steps to implement and verify the MVP console against **`docs/user-stories/EPIC-14-console-frontend-backend-mvp.md`**, **`docs/design/frontend-console-mvp-wireframes-and-mockups.md`**, and **`.cursor/skills/deepguard-ui-style-guide/`** (with `reference.md`).

**Stack (normative for this epic):** Next.js 14 App Router, TypeScript, Tailwind CSS, client-side API calls to configurable base URL.

---

## Phase A — Foundation

1. **Scaffold** `apps/web` with Next 14 + Tailwind + `src/` layout (`create-next-app`).
2. **Tokens & theme** — Map `reference.md` §1–2 to CSS variables on `:root` and `.dark`; set Tailwind `darkMode: 'class'`; remove raw hex from components outside token definitions.
3. **Root layout** — System font stack per style guide; `lang="en"`; wrap children in **theme** + **toast** providers; add `prefers-reduced-motion` global rule (skill §14 / US-DG-14-011).
4. **App shell (US-DG-14-001)** — 240px sidebar, top bar 56px, nav order (logo → tenant → Dashboard → Scans → disabled Findings/Policies/Reports with tooltip → Settings), footer version + environment pill.
5. **Mobile (US-DG-14-010)** — `<lg` drawer for sidebar with overlay z-index per reference §6; page padding 16px on small breakpoints.

## Phase B — API client & settings

6. **Connection settings (US-DG-14-002)** — `localStorage` schema: base URL, secret, auth mode (`X-API-Key` vs `Bearer`, mutually exclusive); **Test connection** → `GET /v1/healthz` (no auth); success toast per copy deck §3.1; **401** → `role="alert"` inline using `status.error.*` tokens.
7. **API helper** — Central `fetch` wrapper: attach auth header, JSON parse, surface errors for toasts/alerts.

## Phase C — Operator flows

8. **Dashboard (US-DG-14-003)** — Health card with Refresh → `GET /v1/healthz`, skeleton/spinner on card; sticky error toast on failure until dismissed; second card explains Redis queue behaviour.
9. **Recent scans registry (US-DG-14-008)** — `localStorage` list (max 50 entries); Scans hub: New scan, Open-by-ID (UUID validate), clear list with confirm; empty state CTA.
10. **Create scan (US-DG-14-004)** — Single-page form max-width 560px: Git vs archive, full `CreateScanRequest` parity with **`deepguard_core`** validators; client validation messages; **201** → success toast + navigate to detail + push recent; **422** → per-field alerts.
11. **Repo upload (US-DG-14-005)** — Modal: `POST /v1/repo-uploads`, client `PUT` with `upload_headers`; **503** `REPO_UPLOAD_S3_UNCONFIGURED` → inline alert + link to `.env.example`; success → auto-fill `storage_uri` on create form.
12. **Scan detail (US-DG-14-006)** — `GET /v1/scans/{id}` poll every **5s**; **Page Visibility**: backoff when tab hidden; read-only `job_config` with accessible expand/collapse; **404** empty state.
13. **Cancel (US-DG-14-007)** — Confirm modal (`<dialog>`); `POST …/cancel`; **202** toast + refresh; **404** error path.
14. **Status badges (US-DG-14-009)** — Map lifecycle statuses to `status.*` tokens; dot + label; tabular nums for `percent_complete`.

## Phase D — Polish & optional

15. **Dark mode (US-DG-14-012)** — Toggle; persist; validate no harsh pure black/white large fields.
16. **Accessibility pass (US-DG-14-011)** — Focus rings 2px `brand.primary`, targets ≥24px, `aria-*` on tables/modals/dialogs, one primary per view.

## Phase E — Verification

17. **Playwright (US-DG-14-013)** — `@playwright/test`; `webServer` starts Next dev; **mock HTTP API** (or dockerised backend) for deterministic CI: health → create scan (git) → GET detail shows `scan_id`; use `test.step` for BDD-readable traces; optional `e2e/features/*.md` as human-readable scenarios mirroring steps. **`e2e/api-validation.spec.ts`** covers **503 repo-upload** and **422** field mapping via `page.route`. GitHub Actions job **`web-console-e2e-compose`** runs **`e2e/repo-upload-minio.spec.ts`** with **real MinIO** (`docker/compose.dev.yml` + `E2E_REAL_API=1`).
18. **agent-browser** — `apps/web/scripts/agent-browser-smoke.sh`: optional smoke (open shell, snapshot, assert key strings); document install from [agent-browser.dev](https://agent-browser.dev/); exit 0 with skip message if CLI missing (skill: ad-hoc complement to Playwright).
19. **CORS for local dev** — Set `DEEPGUARD_CORS_ORIGINS` on the FastAPI process when serving from `http://localhost:3000` (documented in `apps/web/README.md` and `.env.example`).
20. **Handoff (US-DG-14-014)** — `apps/web/README.md`: `NEXT_PUBLIC_*`, scripts, link to wireframes doc; root `README` or MkDocs index may link to `apps/web`.

---

## Execution checklist (copy for PR / release)

- [ ] `npm run build` in `apps/web` passes.
- [ ] `npm run test:e2e` passes (Playwright + mock API).
- [ ] Manual: Settings → Test connection against real `uvicorn` with CORS origins set.
- [ ] Optional: `./scripts/agent-browser-smoke.sh` with dev server running.
- [ ] API: `DEEPGUARD_CORS_ORIGINS` documented for browser→API local dev.
