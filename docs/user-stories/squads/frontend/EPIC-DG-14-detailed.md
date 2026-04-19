> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-14-console-frontend-backend-mvp.md`](../EPIC-14-console-frontend-backend-mvp.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-14 — Product console frontend (MVP) — exercise current control plane API

> **AC-level test specifications (generated):** Squad copy [`squads/frontend/EPIC-DG-14-detailed.md`](squads/frontend/EPIC-DG-14-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then `python3 scripts/validate_user_stories_traceability.py`.

**Goal:** Ship a **product-facing** web console (default stack: **Next.js 14 + App Router + Tailwind**) that **exercises every behaviour** exposed by today’s **FastAPI `/v1` surface** (`health`, `scans` create/read/cancel, `repo-uploads` presign), with **visual design** locked to **`.cursor/skills/deepguard-ui-style-guide/SKILL.md`** and **`reference.md`** (tokens, shell, tables, forms, toasts, accessibility).

**Non-goal (this epic):** UI for endpoints **not yet implemented** (e.g. `GET /v1/scans` list pagination, findings grid, policies catalogue) except **clear placeholders** and links to **EPIC-DG-12** backlog stories.

**Primary personas:** Developer integrating scans, internal operator validating staging.

**Relationship**

| Artefact | Role |
|----------|------|
| **EPIC-DG-12** | Long-horizon operator console (OIDC, findings, reports, policies). |
| **EPIC-DG-14** | **MVP slice** that proves the **current** API contract in a real browser app. |
| **`docs/design/frontend-console-mvp-wireframes-and-mockups.md`** | **Pre-implementation** wireframes + high-fidelity mockup notes (this epic’s visual source of truth until Figma exists). |

---


## US-DG-14-001 — App shell, navigation, and design tokens

**As a** user, **I want** a consistent **240px sidebar** + **top bar** console shell, **so that** every screen matches the DeepGuard UI system.

**Wireframe — shell (style guide §10, reference §4)**

```text
┌──240px──┬────────────────────────────────────────────────────────────┐
│ DeepGuard│ Scan detail                                    [?] [bell] [avatar▼]│
│ ────────│ Tenant: ACME Staging ▾   Breadcrumb: Scans › abc…            │
│ ●Dashboard│──────────────────────────────────────────────────────────────│
│  Scans   │  [ page title ]                              [Primary action] │
│  (more…) │  ┌ surface.card (#fff / #18181b dark) ─────────────────────┐  │
│  Settings│  │  body max-width 1440px, padding 24px (16 mobile)       │  │
│  v0.1.0  │  └────────────────────────────────────────────────────────┘  │
└──────────┴────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-14-001-01:** CSS variables (or Tailwind theme) map to **semantic tokens** in `reference.md` §1 (`surface.page`, `surface.card`, `text.primary`, `brand.primary` `#4f46e5` light, `#818cf8` dark, etc.); no raw hex in components except token definitions.
- **AC-DG-14-001-02:** **One primary** button per viewport (style guide §6); destructive actions use **destructive** variant + confirm modal.
- **AC-DG-14-001-03:** Sidebar order matches style guide: logo, tenant, **Scans**, then **disabled/placeholder** entries (Findings, Policies, Reports) with tooltip “Not available in API yet” until EPIC-12 ships.
- **AC-DG-14-001-04:** Footer shows app **version** + **environment** pill (`surface.subtle`, `text.muted`).

---

### AC test specifications (US-DG-14-001)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-001` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | CSS variables (or Tailwind theme) map to **semantic tokens** in `reference.md` §1 (`surface.page`, `surface.card`, `text.primary`, `brand.primary` `#4f46e5` light, `#818cf8` dark, etc.); no raw hex in components except token definitions. |
| **Objective** | Verify AC-DG-14-001-01: CSS variables (or Tailwind theme) map to **semantic tokens** in `reference.md` §1 (`surface.page`, `surface.card`, `text.primary`, `brand.primary` `#4f46e5` light, `#818cf8` dark, etc.); no raw hex in components except t… |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-001-01` |
| **Secondary / negative test ID** | `TC-DG-14-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-001-01") or Xray/TestRail key == AC-DG-14-001-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-001` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | **One primary** button per viewport (style guide §6); destructive actions use **destructive** variant + confirm modal. |
| **Objective** | Verify AC-DG-14-001-02: **One primary** button per viewport (style guide §6); destructive actions use **destructive** variant + confirm modal. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-001-02` |
| **Secondary / negative test ID** | `TC-DG-14-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-001-02") or Xray/TestRail key == AC-DG-14-001-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-001-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-001` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Sidebar order matches style guide: logo, tenant, **Scans**, then **disabled/placeholder** entries (Findings, Policies, Reports) with tooltip “Not available in API yet” until EPIC-12 ships. |
| **Objective** | Verify AC-DG-14-001-03: Sidebar order matches style guide: logo, tenant, **Scans**, then **disabled/placeholder** entries (Findings, Policies, Reports) with tooltip “Not available in API yet” until EPIC-12 ships. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-001-03` |
| **Secondary / negative test ID** | `TC-DG-14-001-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-001-03") or Xray/TestRail key == AC-DG-14-001-03 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-001-04

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-001` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Footer shows app **version** + **environment** pill (`surface.subtle`, `text.muted`). |
| **Objective** | Verify AC-DG-14-001-04: Footer shows app **version** + **environment** pill (`surface.subtle`, `text.muted`). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-001-04` |
| **Secondary / negative test ID** | `TC-DG-14-001-04.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-001-04") or Xray/TestRail key == AC-DG-14-001-04 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-002 — API connection & developer API key (dev auth)

**As a** developer, **I want** to store **`X-API-Key`** (or Bearer) and **base URL** in browser settings, **so that** the SPA can call the same API as curl/Swagger.

**Wireframe — settings / connection**

```text
┌──────── API connection ──────────────────────────────────────┐
│ Base URL   [ https://api.example.com        ] (mono 13px)    │
│ API key    [ ••••••••••••••     ] [Show]  Help: X-API-Key      │
│ [ Test connection ]   Last OK: 12:04   status: success dot   │
│ Danger: key kept in localStorage only — dev MVP.             │
└────────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-14-002-01:** **Test connection** calls `GET /v1/healthz` (no auth); success shows **toast** “Saved” / “Connected” per `reference.md` §3.1.
- **AC-DG-14-002-02:** All authenticated requests send **`X-API-Key`** header; optional toggle to send **`Authorization: Bearer`** instead (mutually exclusive).
- **AC-DG-14-002-03:** On **401**, show **inline alert** (`status.error.bg`, `role="alert"`) with copy deck error “You don’t have access” variant where applicable.

---

### AC test specifications (US-DG-14-002)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-002` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | **Test connection** calls `GET /v1/healthz` (no auth); success shows **toast** “Saved” / “Connected” per `reference.md` §3.1. |
| **Objective** | Verify AC-DG-14-002-01: **Test connection** calls `GET /v1/healthz` (no auth); success shows **toast** “Saved” / “Connected” per `reference.md` §3.1. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-002-01` |
| **Secondary / negative test ID** | `TC-DG-14-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-002-01") or Xray/TestRail key == AC-DG-14-002-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-002-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-002` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P0` / `Post-MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `2` |
| **Requirement (verbatim)** | All authenticated requests send **`X-API-Key`** header; optional toggle to send **`Authorization: Bearer`** instead (mutually exclusive). |
| **Objective** | Verify AC-DG-14-002-02: All authenticated requests send **`X-API-Key`** header; optional toggle to send **`Authorization: Bearer`** instead (mutually exclusive). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-14-002-02` |
| **Secondary / negative test ID** | `TC-DG-14-002-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-002-02") or Xray/TestRail key == AC-DG-14-002-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-002-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-002` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | On **401**, show **inline alert** (`status.error.bg`, `role="alert"`) with copy deck error “You don’t have access” variant where applicable. |
| **Objective** | Verify AC-DG-14-002-03: On **401**, show **inline alert** (`status.error.bg`, `role="alert"`) with copy deck error “You don’t have access” variant where applicable. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-002-03` |
| **Secondary / negative test ID** | `TC-DG-14-002-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-002-03") or Xray/TestRail key == AC-DG-14-002-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-003 — Dashboard: health and queue readiness

**As an** operator, **I want** a **Dashboard** card that shows API health, **so that** I know the control plane is up before creating scans.

**Wireframe — dashboard**

```text
┌──────── Dashboard ───────────────────────────────────────────┐
│ ┌ surface.card md radius, shadow.sm ───────────────────────┐ │
│ │ Control plane   [badge: OK]                                │ │
│ │ GET /v1/healthz → 200  latency 24ms   [Refresh]          │ │
│ └────────────────────────────────────────────────────────────┘ │
│ ┌ surface.card ──────────────────────────────────────────────┐ │
│ │ Redis queue (inferred)                                      │ │
│ │ “Jobs publish when Redis configured.” [Learn more]          │ │
│ └────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-14-003-01:** **Refresh** triggers `GET /v1/healthz`; loading state uses **skeleton** or spinner on card only (no global success toast on poll — style guide §11).
- **AC-DG-14-003-02:** If health fails, **sticky error toast** until dismissed (`reference.md` §3.2).

---

### AC test specifications (US-DG-14-003)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-003` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | **Refresh** triggers `GET /v1/healthz`; loading state uses **skeleton** or spinner on card only (no global success toast on poll — style guide §11). |
| **Objective** | Verify AC-DG-14-003-01: **Refresh** triggers `GET /v1/healthz`; loading state uses **skeleton** or spinner on card only (no global success toast on poll — style guide §11). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-003-01` |
| **Secondary / negative test ID** | `TC-DG-14-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-003-01") or Xray/TestRail key == AC-DG-14-003-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-003` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | If health fails, **sticky error toast** until dismissed (`reference.md` §3.2). |
| **Objective** | Verify AC-DG-14-003-02: If health fails, **sticky error toast** until dismissed (`reference.md` §3.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-003-02` |
| **Secondary / negative test ID** | `TC-DG-14-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-003-02") or Xray/TestRail key == AC-DG-14-003-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-004 — Create scan (full `CreateScanRequest` shape)

**As a** developer, **I want** a **single-page form** that builds **`POST /v1/scans`** JSON, **so that** every field of `CreateScanRequest` is exercisable from the UI.

**Wireframe — create scan (dense form, max 560px form column per §4)**

```text
┌──────── New scan ────────────────────────────────────────────┐
│ Source  ( ) Git   (•) Archive                                │
│ ── Git ──                                                     │
│ Repo URL [https://…                    ]  Ref [main    ]       │
│ Clone depth [ 50 ]   Sub-path (opt) [ services/api ]         │
│ ── Archive ──                                                 │
│ [ Prepare upload ]  staging URI: s3://… (mono, truncate mid) │
│ Checksum SHA-256 (opt) [________________________]           │
│ Policies  [ ISO-27001-2022 , … ]  (tags/chips, removable)      │
│ Layers    [x] Code  [x] IaC  [ ] Cloud                        │
│ Cloud profiles  [ + Add ]  (repeatable cards when Cloud on)  │
│ Budget (opt)  max LLM USD [    ]  wall sec [    ]            │
│ Webhook (opt) URL [        ] Events [completed▼][failed▼]    │
│ Idempotency-Key (opt) [________________]                       │
│                                    [ Cancel ] [ Create scan ]  │
└──────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-14-004-01:** Client-side validation mirrors **Pydantic** rules: at least one layer; cloud requires repo and/or profiles; code/IaC requires repo; `policy_ids` min 1; **archive** requires `storage_uri` `s3://` and no `url` (see `RepoSpec` in `packages/core`).
- **AC-DG-14-004-02:** Successful **201** → **toast** “Scan queued” (`reference.md` §3.1) + navigate to **Scan detail** + append `scan_id` to **recent scans** (US-DG-14-008).
- **AC-DG-14-004-03:** **422** maps field errors to **inline** `role="alert"` per field (style guide §8).

---

### AC test specifications (US-DG-14-004)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-004` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Client-side validation mirrors **Pydantic** rules: at least one layer; cloud requires repo and/or profiles; code/IaC requires repo; `policy_ids` min 1; **archive** requires `storage_uri` `s3://` and no `url` (see `RepoSpec` in `packages/core`). |
| **Objective** | Verify AC-DG-14-004-01: Client-side validation mirrors **Pydantic** rules: at least one layer; cloud requires repo and/or profiles; code/IaC requires repo; `policy_ids` min 1; **archive** requires `storage_uri` `s3://` and no `url` (see `RepoSp… |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-004-01` |
| **Secondary / negative test ID** | `TC-DG-14-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-004-01") or Xray/TestRail key == AC-DG-14-004-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-004-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-004` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `US-DG-14-008`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Successful **201** → **toast** “Scan queued” (`reference.md` §3.1) + navigate to **Scan detail** + append `scan_id` to **recent scans** (US-DG-14-008). |
| **Objective** | Verify AC-DG-14-004-02: Successful **201** → **toast** “Scan queued” (`reference.md` §3.1) + navigate to **Scan detail** + append `scan_id` to **recent scans** (US-DG-14-008). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-004-02` |
| **Secondary / negative test ID** | `TC-DG-14-004-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-004-02") or Xray/TestRail key == AC-DG-14-004-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-004-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-004` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | **422** maps field errors to **inline** `role="alert"` per field (style guide §8). |
| **Objective** | Verify AC-DG-14-004-03: **422** maps field errors to **inline** `role="alert"` per field (style guide §8). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-004-03` |
| **Secondary / negative test ID** | `TC-DG-14-004-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-004-03") or Xray/TestRail key == AC-DG-14-004-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-005 — Presigned repo upload (`POST /v1/repo-uploads`)

**As a** developer, **I want** to **prepare upload** then **PUT** a file from the browser, **so that** archive-based scans work end-to-end when S3 is configured.

**Wireframe — upload modal (modal lg radius, §12)**

```text
┌──────── Upload repo archive ─────────────────────────────────┐
│ Step 1: POST /v1/repo-uploads  → upload_url + storage_uri    │
│ Step 2: PUT file (Content-Type from response headers)          │
│ [ Choose file… ]  repo.tar.gz  12 MB                           │
│ Progress ████████░░ 80%                                        │
│ [ Cancel ]                         [ Use this URI in form ]    │
└────────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-14-005-01:** On **503** with `REPO_UPLOAD_S3_UNCONFIGURED`, show **inline alert** + link to docs (`.env.example` S3 vars); do not crash.
- **AC-DG-14-005-02:** On success, **auto-fill** `storage_uri` on create-scan form (`sentence case` labels).
- **AC-DG-14-005-03:** PUT uses **`upload_headers`** from API response; CORS failures show error deck “Something went wrong” with optional **request id** if exposed by future middleware.

---

### AC test specifications (US-DG-14-005)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-005` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | On **503** with `REPO_UPLOAD_S3_UNCONFIGURED`, show **inline alert** + link to docs (`.env.example` S3 vars); do not crash. |
| **Objective** | Verify AC-DG-14-005-01: On **503** with `REPO_UPLOAD_S3_UNCONFIGURED`, show **inline alert** + link to docs (`.env.example` S3 vars); do not crash. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-005-01` |
| **Secondary / negative test ID** | `TC-DG-14-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-005-01") or Xray/TestRail key == AC-DG-14-005-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-005-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-005` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | On success, **auto-fill** `storage_uri` on create-scan form (`sentence case` labels). |
| **Objective** | Verify AC-DG-14-005-02: On success, **auto-fill** `storage_uri` on create-scan form (`sentence case` labels). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-005-02` |
| **Secondary / negative test ID** | `TC-DG-14-005-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-005-02") or Xray/TestRail key == AC-DG-14-005-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-005-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-005` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P2` / `Post-MVP` |
| **MoSCoW** | `Could` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `2` |
| **Requirement (verbatim)** | PUT uses **`upload_headers`** from API response; CORS failures show error deck “Something went wrong” with optional **request id** if exposed by future middleware. |
| **Objective** | Verify AC-DG-14-005-03: PUT uses **`upload_headers`** from API response; CORS failures show error deck “Something went wrong” with optional **request id** if exposed by future middleware. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-14-005-03` |
| **Secondary / negative test ID** | `TC-DG-14-005-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-005-03") or Xray/TestRail key == AC-DG-14-005-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-006 — Scan detail, polling, and job config inspection

**As an** operator, **I want** to **poll `GET /v1/scans/{id}`**, **so that** I see `status`, `current_stage`, `percent_complete`, and raw **`job_config`**.

**Wireframe — scan detail**

```text
┌──────── Scan 3fa2… ──────────────────────────────────────────┐
│ Status [QUEUED ▾ badge + dot]   Stage INGESTING   15%        │
│ Repo commit (if any)  `a1b2c3d…`  (mono)         [ Refresh ]   │
│ ┌ job_config JSON (surface.subtle, mono 13px) ───────────────┐ │
│ │ { "repo": { "source": "git", ... }, ... }                  │ │
│ └────────────────────────────────────────────────────────────┘ │
│ [ Request cancel ]  (destructive styling only after confirm)   │
└────────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-14-006-01:** Poll every **5s** with **backoff when tab hidden** (EPIC-12 AC pattern); **no toast** on each successful poll.
- **AC-DG-14-006-02:** **404** → dedicated empty state card (“Scan not found”) + link back to Scans hub.
- **AC-DG-14-006-03:** `job_config` viewer is **read-only**; expand/collapse with **accessible** button (`aria-expanded`).

---

### AC test specifications (US-DG-14-006)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-006` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Poll every **5s** with **backoff when tab hidden** (EPIC-12 AC pattern); **no toast** on each successful poll. |
| **Objective** | Verify AC-DG-14-006-01: Poll every **5s** with **backoff when tab hidden** (EPIC-12 AC pattern); **no toast** on each successful poll. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-006-01` |
| **Secondary / negative test ID** | `TC-DG-14-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-006-01") or Xray/TestRail key == AC-DG-14-006-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-006` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | **404** → dedicated empty state card (“Scan not found”) + link back to Scans hub. |
| **Objective** | Verify AC-DG-14-006-02: **404** → dedicated empty state card (“Scan not found”) + link back to Scans hub. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-006-02` |
| **Secondary / negative test ID** | `TC-DG-14-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-006-02") or Xray/TestRail key == AC-DG-14-006-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-006-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-006` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `job_config` viewer is **read-only**; expand/collapse with **accessible** button (`aria-expanded`). |
| **Objective** | Verify AC-DG-14-006-03: `job_config` viewer is **read-only**; expand/collapse with **accessible** button (`aria-expanded`). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-006-03` |
| **Secondary / negative test ID** | `TC-DG-14-006-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-006-03") or Xray/TestRail key == AC-DG-14-006-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-007 — Cancel scan (`POST /v1/scans/{id}/cancel`)

**As a** user, **I want** to **request cancellation** with confirmation, **so that** `cancellation_requested` is set via the API.

**Wireframe — confirm modal (max 560px)**

```text
┌──────── Cancel scan? ────────────────────────────────────────┐
│ This requests cooperative cancel. Running work may stop soon.  │
│              [ Keep scan ]  [ Request cancel ]  (destructive)  │
└────────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-14-007-01:** **202** response → **toast** success + refresh row; **404** → error toast + message body.
- **AC-DG-14-007-02:** Modal obeys **focus trap** and **Escape** behaviour per style guide §12 (Escape blocked if dirty — N/A here).

---

### AC test specifications (US-DG-14-007)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-007` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | **202** response → **toast** success + refresh row; **404** → error toast + message body. |
| **Objective** | Verify AC-DG-14-007-01: **202** response → **toast** success + refresh row; **404** → error toast + message body. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-007-01` |
| **Secondary / negative test ID** | `TC-DG-14-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-007-01") or Xray/TestRail key == AC-DG-14-007-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-007-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-007` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Modal obeys **focus trap** and **Escape** behaviour per style guide §12 (Escape blocked if dirty — N/A here). |
| **Objective** | Verify AC-DG-14-007-02: Modal obeys **focus trap** and **Escape** behaviour per style guide §12 (Escape blocked if dirty — N/A here). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-007-02` |
| **Secondary / negative test ID** | `TC-DG-14-007-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-007-02") or Xray/TestRail key == AC-DG-14-007-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-008 — Recent scans without `GET /v1/scans` (client registry)

**As a** user, **I want** a **local list** of scans I created in this browser, **so that** I can reopen them without a list API.

**Wireframe — scans hub**

```text
┌──────── Scans ─────────────────────────────────────────────────┐
│ [ + New scan ]          Open by ID: [uuid________] [ Open ]    │
│ Recent (this browser)                                          │
│ ├ 3fa2…  QUEUED   2m ago    [View]                             │
│ └ 91ab…  FAILED   1d ago    [View]                             │
│ Empty: “No scans yet.” [ Create scan ]  (primary CTA)          │
└────────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-14-008-01:** Persist last **50** `scan_id` + `updated_at` + optional label in **`localStorage`**; **clear list** control with destructive confirm.
- **AC-DG-14-008-02:** **Open by ID** validates UUID before GET.

---

### AC test specifications (US-DG-14-008)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-008` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P2` / `Post-MVP` |
| **MoSCoW** | `Could` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `2` |
| **Requirement (verbatim)** | Persist last **50** `scan_id` + `updated_at` + optional label in **`localStorage`**; **clear list** control with destructive confirm. |
| **Objective** | Verify AC-DG-14-008-01: Persist last **50** `scan_id` + `updated_at` + optional label in **`localStorage`**; **clear list** control with destructive confirm. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-14-008-01` |
| **Secondary / negative test ID** | `TC-DG-14-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-008-01") or Xray/TestRail key == AC-DG-14-008-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-008` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | **Open by ID** validates UUID before GET. |
| **Objective** | Verify AC-DG-14-008-02: **Open by ID** validates UUID before GET. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-008-02` |
| **Secondary / negative test ID** | `TC-DG-14-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-008-02") or Xray/TestRail key == AC-DG-14-008-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-009 — Status badges and progress semantics

**As a** user, **I want** **status chips** that match API `status` / `current_stage`, **so that** I can scan visually.

**Acceptance criteria**

- **AC-DG-14-009-01:** Map `QUEUED`, `INGESTING`, `ANALYZING`, … to **badge** colours: use **`status.*`** tokens; pair **dot + label** (style guide §13), not colour alone.
- **AC-DG-14-009-02:** `percent_complete` uses **tabular nums**; right-align in tables (`font-variant-numeric: tabular-nums`).

---

### AC test specifications (US-DG-14-009)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-009` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Map `QUEUED`, `INGESTING`, `ANALYZING`, … to **badge** colours: use **`status.*`** tokens; pair **dot + label** (style guide §13), not colour alone. |
| **Objective** | Verify AC-DG-14-009-01: Map `QUEUED`, `INGESTING`, `ANALYZING`, … to **badge** colours: use **`status.*`** tokens; pair **dot + label** (style guide §13), not colour alone. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-009-01` |
| **Secondary / negative test ID** | `TC-DG-14-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-009-01") or Xray/TestRail key == AC-DG-14-009-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-009` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `percent_complete` uses **tabular nums**; right-align in tables (`font-variant-numeric: tabular-nums`). |
| **Objective** | Verify AC-DG-14-009-02: `percent_complete` uses **tabular nums**; right-align in tables (`font-variant-numeric: tabular-nums`). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-009-02` |
| **Secondary / negative test ID** | `TC-DG-14-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-009-02") or Xray/TestRail key == AC-DG-14-009-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-010 — Responsive layout and mobile navigation

**As a** user on **mobile**, **I want** usable forms and nav, **so that** I can trigger scans from a phone.

**Acceptance criteria**

- **AC-DG-14-010-01:** At `<lg`, sidebar becomes **drawer** with overlay **z-index** per `reference.md` §6; **no hamburger-only** critical actions on desktop (style guide §16).
- **AC-DG-14-010-02:** Page padding **16px** on small breakpoints (style guide §4).

---

### AC test specifications (US-DG-14-010)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-010` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | At `<lg`, sidebar becomes **drawer** with overlay **z-index** per `reference.md` §6; **no hamburger-only** critical actions on desktop (style guide §16). |
| **Objective** | Verify AC-DG-14-010-01: At `<lg`, sidebar becomes **drawer** with overlay **z-index** per `reference.md` §6; **no hamburger-only** critical actions on desktop (style guide §16). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-010-01` |
| **Secondary / negative test ID** | `TC-DG-14-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-010-01") or Xray/TestRail key == AC-DG-14-010-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-010` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Page padding **16px** on small breakpoints (style guide §4). |
| **Objective** | Verify AC-DG-14-010-02: Page padding **16px** on small breakpoints (style guide §4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-010-02` |
| **Secondary / negative test ID** | `TC-DG-14-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-010-02") or Xray/TestRail key == AC-DG-14-010-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-011 — Accessibility (WCAG 2.2 AA baseline)

**As a** keyboard user, **I want** full operability, **so that** the console is enterprise-acceptable.

**Acceptance criteria**

- **AC-DG-14-011-01:** Meet checklist **§15** of the UI skill (contrast, focus ring `brand.primary` 2px offset 2px, targets ≥24px / 40px icon-only, `aria-*` on tables/modals/forms).
- **AC-DG-14-011-02:** **`prefers-reduced-motion`** removes non-essential motion (skill §14).

---

### AC test specifications (US-DG-14-011)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-011-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-011` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Meet checklist **§15** of the UI skill (contrast, focus ring `brand.primary` 2px offset 2px, targets ≥24px / 40px icon-only, `aria-*` on tables/modals/forms). |
| **Objective** | Verify AC-DG-14-011-01: Meet checklist **§15** of the UI skill (contrast, focus ring `brand.primary` 2px offset 2px, targets ≥24px / 40px icon-only, `aria-*` on tables/modals/forms). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-011-01` |
| **Secondary / negative test ID** | `TC-DG-14-011-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-011-01") or Xray/TestRail key == AC-DG-14-011-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-011-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-011` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | **`prefers-reduced-motion`** removes non-essential motion (skill §14). |
| **Objective** | Verify AC-DG-14-011-02: **`prefers-reduced-motion`** removes non-essential motion (skill §14). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-011-02` |
| **Secondary / negative test ID** | `TC-DG-14-011-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-011-02") or Xray/TestRail key == AC-DG-14-011-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-012 — Dark mode (optional, Should)

**As a** user, **I want** **dark mode**, **so that** long sessions are comfortable.

**Acceptance criteria**

- **AC-DG-14-012-01:** Toggle persists; all screens use **dark** column from `reference.md` §1.
- **AC-DG-14-012-02:** No **pure #000 on #fff** large fields (skill §2).

---

### AC test specifications (US-DG-14-012)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-012-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-012` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Toggle persists; all screens use **dark** column from `reference.md` §1. |
| **Objective** | Verify AC-DG-14-012-01: Toggle persists; all screens use **dark** column from `reference.md` §1. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-012-01` |
| **Secondary / negative test ID** | `TC-DG-14-012-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-012-01") or Xray/TestRail key == AC-DG-14-012-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-14-012-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-012` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | No **pure #000 on #fff** large fields (skill §2). |
| **Objective** | Verify AC-DG-14-012-02: No **pure #000 on #fff** large fields (skill §2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-012-02` |
| **Secondary / negative test ID** | `TC-DG-14-012-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-012-02") or Xray/TestRail key == AC-DG-14-012-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-013 — Playwright smoke (BDD-ready)

**As a** QA engineer, **I want** **Playwright** tests against **mocked or dockerised API**, **so that** regressions in the MVP console are caught in CI.

**Acceptance criteria**

- **AC-DG-14-013-01:** At minimum: **health** → **create scan (git stub)** → **GET detail** → assert visible `scan_id` (align with `deepguard-delivery-quality` skill: BDD after unit tests for this slice).

---

### AC test specifications (US-DG-14-013)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-013-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-013` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | At minimum: **health** → **create scan (git stub)** → **GET detail** → assert visible `scan_id` (align with `deepguard-delivery-quality` skill: BDD after unit tests for this slice). |
| **Objective** | Verify AC-DG-14-013-01: At minimum: **health** → **create scan (git stub)** → **GET detail** → assert visible `scan_id` (align with `deepguard-delivery-quality` skill: BDD after unit tests for this slice). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-013-01` |
| **Secondary / negative test ID** | `TC-DG-14-013-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-013-01") or Xray/TestRail key == AC-DG-14-013-01 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-14-014 — Documentation handoff

**As a** new contributor, **I want** **README** links to run the web app, **so that** I can develop locally.

**Acceptance criteria**

- **AC-DG-14-014-01:** `apps/web` (or chosen path) **README** documents `NEXT_PUBLIC_*` env vars, API base URL, and points to **`docs/design/frontend-console-mvp-wireframes-and-mockups.md`**.

---

### Traceability notes

- Maps to **EPIC-DG-02** (`POST/GET/cancel` scans, `repo-uploads`), **EPIC-DG-04** (git vs archive, presign path), **EPIC-DG-12** (future superset UI).
- Visual rules: **`.cursor/skills/deepguard-ui-style-guide/SKILL.md`** + **`reference.md`**.

### AC test specifications (US-DG-14-014)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-14-014-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-14-014` |
| **Parent EPIC** | `EPIC-DG-14` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4/L5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `apps/web` (or chosen path) **README** documents `NEXT_PUBLIC_*` env vars, API base URL, and points to **`docs/design/frontend-console-mvp-wireframes-and-mockups.md`**. |
| **Objective** | Verify AC-DG-14-014-01: `apps/web` (or chosen path) **README** documents `NEXT_PUBLIC_*` env vars, API base URL, and points to **`docs/design/frontend-console-mvp-wireframes-and-mockups.md`**. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-14-014-01` |
| **Secondary / negative test ID** | `TC-DG-14-014-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-14-014-01") or Xray/TestRail key == AC-DG-14-014-01 |
| **Spec references** | Architecture_Design.md (see product spec) |


## Epic Definition of Done checklist

- [ ] All in-scope ACs for `EPIC-DG-14` implemented by `frontend` and linked to automated tests (`TC-DG-*`).
- [ ] Unit coverage on touched packages is >=80%.
- [ ] Integration tests pass for all required ACs.
- [ ] Playwright BDD updated where `test_layer_required` includes `bdd`.
- [ ] Observability hooks and stable `error_code` behaviour validated.
- [ ] Security/data-sovereignty constraints verified (no secret leaks, tenant isolation).
- [ ] Design spec for slice exists under `docs/design/` with approved status.
