# EPIC-DG-12 — Web console & operator experience (Next.js)

> **AC-level test specifications (generated):** Squad copy [`squads/frontend/EPIC-DG-12-detailed.md`](squads/frontend/EPIC-DG-12-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py`.


**Goal:** Provide a cohesive UI (per business architecture: Next.js 14 + Tailwind) for configuring scans, monitoring progress, triaging findings, downloading reports, and administering policies — aligned to API capabilities in §28.

**Primary personas:** Developer, Security analyst, Tenant admin.

---

## US-DG-12-001 — Authenticated landing & tenant context

**As a** user, **I want** to sign in and see my tenant’s scans, **so that** I never confuse environments.

**Wireframe — app shell**

```text
┌──────────────────────────────────────────────────────────────┐
│ DeepGuard   Tenant: ACME Prod        user@acme.com [avatar▼]│
├───────────────┬──────────────────────────────────────────────┤
│ Nav           │  Home > Scans                                   │
│ • Dashboard   │                                               │
│ • Scans       │   (content)                                   │
│ • Policies    │                                               │
│ • Settings    │                                               │
└───────────────┴──────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-12-001-01:** OIDC login establishes session; JWT forwarded to API on each request (maps EPIC-DG-03).
- **AC-DG-12-001-02:** Tenant switcher (if permitted) only lists authorised tenants; default from token `tenant_id`.

---

## US-DG-12-002 — Scan list with filters

**As a** security analyst, **I want** a sortable scan list, **so that** I can find failed or high-cost runs quickly.

**Wireframe — scans table**

```text
┌──────── Scans ───────────────────────────────────────────────┐
│ Filters: Status[All▼] Stage[All▼] Repo[search____] [Refresh] │
├───────────┬─────────┬──────────┬─────────┬──────────────────┤
│ Started   │ Repo    │ Status   │ Stage% │ Actions          │
├───────────┼─────────┼──────────┼─────────┼──────────────────┤
│ 10:12Z    │ payments│ COMPLETE │ 100%    │ [View][Report]   │
│ 09:40Z    │ auth    │ FAILED   │ 35%     │ [View][Retry?]   │
└───────────┴─────────┴──────────┴─────────┴──────────────────┘
```

**Acceptance criteria**

- **AC-DG-12-002-01:** Table columns include `scan_id`, `repo`, `status`, `current_stage`, `percent_complete`, `updated_at`.
- **AC-DG-12-002-02:** Row actions deep-link to scan detail (`/scans/:id`).
- **AC-DG-12-002-03:** Polling interval backs off when tab inactive (performance NFR).

---

## US-DG-12-003 — Scan detail timeline

**As a** developer, **I want** a visual timeline of graph stages, **so that** I know where time was spent.

**Wireframe — timeline**

```text
┌──────── Scan 3fa2… ──────────────────────────────────────────┐
│ Repo: payments @ a1b2c3d   Policies: ISO27001, SOC2          │
│                                                             │
│  ●── Hermes    ●── Tiresias   ●── Argus   ◌── Laocoon       │
│ 2m              30s            6m          running…         │
│                                                             │
│ Live logs [tail ▼]   Errors (0)   [ Cancel scan ]           │
└─────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-12-003-01:** Timeline binds to `GET /v1/scans/{id}` fields; handles `AWAITING_REVIEW` with resume CTA for authorised roles.
- **AC-DG-12-003-02:** Cancel button calls `POST …/cancel` and disables when terminal (EPIC-DG-01/02).

---

## US-DG-12-004 — Findings triage workspace

**As a** security analyst, **I want** filterable findings with evidence preview, **so that** I can prepare remediation tickets.

**Wireframe — findings board**

```text
┌──────── Findings ────────────────────────────────────────────┐
│ Severity [High▼] Framework [ISO27001▼] Text [crypto__]      │
├───────────────┬─────────────────────────────────────────────┤
│ List          │ Detail                                       │
│ □ F-001 HIGH  │ Title: TLS min version not enforced         │
│   ISO A.10…   │ Status: FAIL  Conf: 0.81                     │
│ □ F-002 MED   │ Evidence snippets + links to blob viewer    │
│               │ [Export CSV] [Create Jira ticket] (optional) │
└───────────────┴─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-12-004-01:** Uses paginated findings API with cursor preservation in URL query.
- **AC-DG-12-004-02:** Evidence opens read-only code viewer; never exposes raw presigned URL in logs.
- **AC-DG-12-004-03:** Bulk select exports minimal JSON/CSV schema versioned `v1`.

---

## US-DG-12-005 — Report download & integrity display

**As an** auditor, **I want** one-click PDF download with checksum visible, **so that** I can archive evidence.

**Wireframe — report card**

```text
┌──────── Report ─────────────────────────────────────────────┐
│ File: report.pdf                                            │
│ SHA-256: d14a…c49   Generated: 2026-04-18T10:45Z             │
│ [ Download ]   [ Copy checksum ]                            │
└─────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-12-005-01:** Download uses artefact endpoint; handles `302` redirect transparently to browser.
- **AC-DG-12-005-02:** UI displays checksum from API metadata (EPIC-DG-02/10).

---

## US-DG-12-006 — Policy admin (upload & diff)

**As a** tenant admin, **I want** to upload policies and see parse summary, **so that** I know controls extracted.

**Wireframe — upload result**

```text
┌──────── Parse summary ──────────────────────────────────────┐
│ Policy version: acme-sdlc-2026-04-18                         │
│ Controls extracted: 128   Warnings: 2                        │
│ Warnings:                                                    │
│  • Page 14: table OCR low confidence                        │
│ [ View controls table ]                                     │
└─────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-12-006-01:** Upload flow maps to `POST /v1/policies:upload` (EPIC-DG-05).
- **AC-DG-12-006-02:** Error states show sanitised server messages; no stack traces to end users.

---

## US-DG-12-007 — Runtime flags read-only for auditors

**As an** auditor, **I want** to view effective runtime flags, **so that** I can verify safety settings during examination.

**Acceptance criteria**

- **AC-DG-12-007-01:** `auditor` role sees read-only merged JSON; cannot edit (EPIC-DG-03).

---

## US-DG-12-008 — Budget & notification editing (scanner/admin)

**As a** project lead, **I want** to set webhook URL and LLM budget on scan create, **so that** CI failures notify Slack.

**Wireframe — notifications**

```text
┌──────── Notifications ──────────────────────────────────────┐
│ Webhook URL: [https://hooks.slack.com/…        ]           │
│ Events: [x] completed  [x] failed  [ ] cancelled           │
│ Budget USD: [12.5]   Wall seconds: [3600]                  │
└──────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-12-008-01:** Form maps 1:1 to `CreateScanRequest.notifications` and `budget` (Architecture §28.4).
- **AC-DG-12-008-02:** Webhook URL validated as HTTPS only in production (configurable exception for dev).
- **AC-DG-12-008-03:** Test webhook button sends signed sample event (EPIC-DG-02).

---

## US-DG-12-009 — Cross-layer insight page

**As an** analyst, **I want** dedicated view for `cross_layer_findings`, **so that** composite risks are not buried in flat tables.

**Acceptance criteria**

- **AC-DG-12-009-01:** Page lists composite title, severity, participating layers, evidence links.
- **AC-DG-12-009-02:** Visual diagram export PNG optional from same data (reuse EPIC-DG-10 chart components if shared).
- **AC-DG-12-009-03:** Empty state explains when layer flags prevented correlation.

---

## US-DG-12-010 — Accessibility and i18n baseline

**As a** enterprise buyer, **I want** WCAG 2.1 AA targets for core flows, **so that** procurement passes.

**Acceptance criteria**

- **AC-DG-12-010-01:** Keyboard navigable scan list and findings table; focus traps in modals.
- **AC-DG-12-010-02:** Colour contrast meets AA for default theme; high-contrast theme optional.
- **AC-DG-12-010-03:** UI strings externalised for `en` + `zh` bundles at minimum.

---

## US-DG-12-011 — API key management page (optional SaaS)

**As a** tenant admin, **I want** to rotate API keys for automation, **so that** leaked keys can be revoked.

**Acceptance criteria**

- **AC-DG-12-011-01:** Aligns with EPIC-DG-03 service account stories; UI never shows full key twice.
- **AC-DG-12-011-02:** Key usage last_seen updated on authenticated API calls.
- **AC-DG-12-011-03:** mTLS-only tenants hide API key UI entirely.

---

## US-DG-12-012 — Embedded reasoning excerpt (auditor)

**As an** auditor, **I want** to view redacted reasoning excerpt per finding, **so that** I sample LLM logic without raw payload.

**Acceptance criteria**

- **AC-DG-12-012-01:** UI calls documented endpoint returning `redacted_excerpt` ≤4KiB policy (Architecture §23.1 Q9).
- **AC-DG-12-012-02:** Full trace export gated behind admin break-glass (EPIC-DG-11).
- **AC-DG-12-012-03:** Copy-to-clipboard strips HTML and limits size.

---

## US-DG-12-013 — Mobile-friendly scan status view

**As an** on-call engineer, **I want** readable scan status on phone, **so that** I can approve cancel/resume away from desk.

**Acceptance criteria**

- **AC-DG-12-013-01:** Scan detail timeline stacks vertically <768px width without horizontal scroll.
- **AC-DG-12-013-02:** Critical actions reachable in ≤2 taps from home.
- **AC-DG-12-013-03:** Performance: LCP <2.5s on 4G for scan list page (NFR).

---

## US-DG-12-014 — Tenant settings: retention and classification defaults

**As a** tenant admin, **I want** to set default report classification and artefact retention, **so that** every scan inherits policy.

**Acceptance criteria**

- **AC-DG-12-014-01:** Settings persist in `tenants.runtime_config` or dedicated columns per ADR.
- **AC-DG-12-014-02:** Overrides on single scan allowed only where EPIC-DG-03 permits.
- **AC-DG-12-014-03:** Dangerous retention below legal minimum blocked with validation error.
