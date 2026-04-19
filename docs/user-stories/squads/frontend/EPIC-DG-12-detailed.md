> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-12-console-ui.md`](../EPIC-12-console-ui.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-12 — Web console & operator experience (Next.js)

> **AC-level test specifications (generated):** Squad copy [`squads/frontend/EPIC-DG-12-detailed.md`](squads/frontend/EPIC-DG-12-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then `python3 scripts/validate_user_stories_traceability.py`.


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

### AC test specifications (US-DG-12-001)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-001` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-03`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | OIDC login establishes session; JWT forwarded to API on each request (maps EPIC-DG-03). |
| **Objective** | Verify AC-DG-12-001-01: OIDC login establishes session; JWT forwarded to API on each request (maps EPIC-DG-03). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-001-01` |
| **Secondary / negative test ID** | `TC-DG-12-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-001-01") or Xray/TestRail key == AC-DG-12-001-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-001` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Tenant switcher (if permitted) only lists authorised tenants; default from token `tenant_id`. |
| **Objective** | Verify AC-DG-12-001-02: Tenant switcher (if permitted) only lists authorised tenants; default from token `tenant_id`. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-001-02` |
| **Secondary / negative test ID** | `TC-DG-12-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-001-02") or Xray/TestRail key == AC-DG-12-001-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


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

### AC test specifications (US-DG-12-002)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-002` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Table columns include `scan_id`, `repo`, `status`, `current_stage`, `percent_complete`, `updated_at`. |
| **Objective** | Verify AC-DG-12-002-01: Table columns include `scan_id`, `repo`, `status`, `current_stage`, `percent_complete`, `updated_at`. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-002-01` |
| **Secondary / negative test ID** | `TC-DG-12-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-002-01") or Xray/TestRail key == AC-DG-12-002-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-002-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-002` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Row actions deep-link to scan detail (`/scans/:id`). |
| **Objective** | Verify AC-DG-12-002-02: Row actions deep-link to scan detail (`/scans/:id`). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-002-02` |
| **Secondary / negative test ID** | `TC-DG-12-002-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-002-02") or Xray/TestRail key == AC-DG-12-002-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-002-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-002` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Polling interval backs off when tab inactive (performance NFR). |
| **Objective** | Verify AC-DG-12-002-03: Polling interval backs off when tab inactive (performance NFR). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-002-03` |
| **Secondary / negative test ID** | `TC-DG-12-002-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-002-03") or Xray/TestRail key == AC-DG-12-002-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


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

### AC test specifications (US-DG-12-003)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-003` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `5` |
| **Requirement (verbatim)** | Timeline binds to `GET /v1/scans/{id}` fields; handles `AWAITING_REVIEW` with resume CTA for authorised roles. |
| **Objective** | Verify AC-DG-12-003-01: Timeline binds to `GET /v1/scans/{id}` fields; handles `AWAITING_REVIEW` with resume CTA for authorised roles. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-003-01` |
| **Secondary / negative test ID** | `TC-DG-12-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-003-01") or Xray/TestRail key == AC-DG-12-003-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-003` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-01`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Cancel button calls `POST …/cancel` and disables when terminal (EPIC-DG-01/02). |
| **Objective** | Verify AC-DG-12-003-02: Cancel button calls `POST …/cancel` and disables when terminal (EPIC-DG-01/02). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-003-02` |
| **Secondary / negative test ID** | `TC-DG-12-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-003-02") or Xray/TestRail key == AC-DG-12-003-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


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

### AC test specifications (US-DG-12-004)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-004` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Uses paginated findings API with cursor preservation in URL query. |
| **Objective** | Verify AC-DG-12-004-01: Uses paginated findings API with cursor preservation in URL query. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-004-01` |
| **Secondary / negative test ID** | `TC-DG-12-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-004-01") or Xray/TestRail key == AC-DG-12-004-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-004-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-004` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Evidence opens read-only code viewer; never exposes raw presigned URL in logs. |
| **Objective** | Verify AC-DG-12-004-02: Evidence opens read-only code viewer; never exposes raw presigned URL in logs. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-004-02` |
| **Secondary / negative test ID** | `TC-DG-12-004-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-004-02") or Xray/TestRail key == AC-DG-12-004-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-004-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-004` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Bulk select exports minimal JSON/CSV schema versioned `v1`. |
| **Objective** | Verify AC-DG-12-004-03: Bulk select exports minimal JSON/CSV schema versioned `v1`. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-004-03` |
| **Secondary / negative test ID** | `TC-DG-12-004-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-004-03") or Xray/TestRail key == AC-DG-12-004-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


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

### AC test specifications (US-DG-12-005)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-005` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Download uses artefact endpoint; handles `302` redirect transparently to browser. |
| **Objective** | Verify AC-DG-12-005-01: Download uses artefact endpoint; handles `302` redirect transparently to browser. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-005-01` |
| **Secondary / negative test ID** | `TC-DG-12-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-005-01") or Xray/TestRail key == AC-DG-12-005-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-005-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-005` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-02`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | UI displays checksum from API metadata (EPIC-DG-02/10). |
| **Objective** | Verify AC-DG-12-005-02: UI displays checksum from API metadata (EPIC-DG-02/10). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-005-02` |
| **Secondary / negative test ID** | `TC-DG-12-005-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-005-02") or Xray/TestRail key == AC-DG-12-005-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


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

### AC test specifications (US-DG-12-006)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-006` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-05`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Upload flow maps to `POST /v1/policies:upload` (EPIC-DG-05). |
| **Objective** | Verify AC-DG-12-006-01: Upload flow maps to `POST /v1/policies:upload` (EPIC-DG-05). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-006-01` |
| **Secondary / negative test ID** | `TC-DG-12-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-006-01") or Xray/TestRail key == AC-DG-12-006-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-006` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Error states show sanitised server messages; no stack traces to end users. |
| **Objective** | Verify AC-DG-12-006-02: Error states show sanitised server messages; no stack traces to end users. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-006-02` |
| **Secondary / negative test ID** | `TC-DG-12-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-006-02") or Xray/TestRail key == AC-DG-12-006-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-12-007 — Runtime flags read-only for auditors

**As an** auditor, **I want** to view effective runtime flags, **so that** I can verify safety settings during examination.

**Acceptance criteria**

- **AC-DG-12-007-01:** `auditor` role sees read-only merged JSON; cannot edit (EPIC-DG-03).

---

### AC test specifications (US-DG-12-007)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-007` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-03`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `auditor` role sees read-only merged JSON; cannot edit (EPIC-DG-03). |
| **Objective** | Verify AC-DG-12-007-01: `auditor` role sees read-only merged JSON; cannot edit (EPIC-DG-03). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-007-01` |
| **Secondary / negative test ID** | `TC-DG-12-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-007-01") or Xray/TestRail key == AC-DG-12-007-01 |
| **Spec references** | Architecture_Design.md (see product spec) |


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

### AC test specifications (US-DG-12-008)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-008` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Form maps 1:1 to `CreateScanRequest.notifications` and `budget` (Architecture §28.4). |
| **Objective** | Verify AC-DG-12-008-01: Form maps 1:1 to `CreateScanRequest.notifications` and `budget` (Architecture §28.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-008-01` |
| **Secondary / negative test ID** | `TC-DG-12-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-008-01") or Xray/TestRail key == AC-DG-12-008-01 |
| **Spec references** | Architecture §28.4 |

#### Test specification — AC-DG-12-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-008` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Webhook URL validated as HTTPS only in production (configurable exception for dev). |
| **Objective** | Verify AC-DG-12-008-02: Webhook URL validated as HTTPS only in production (configurable exception for dev). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-008-02` |
| **Secondary / negative test ID** | `TC-DG-12-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-008-02") or Xray/TestRail key == AC-DG-12-008-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-008-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-008` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-02`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Test webhook button sends signed sample event (EPIC-DG-02). |
| **Objective** | Verify AC-DG-12-008-03: Test webhook button sends signed sample event (EPIC-DG-02). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-008-03` |
| **Secondary / negative test ID** | `TC-DG-12-008-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-008-03") or Xray/TestRail key == AC-DG-12-008-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-12-009 — Cross-layer insight page

**As an** analyst, **I want** dedicated view for `cross_layer_findings`, **so that** composite risks are not buried in flat tables.

**Acceptance criteria**

- **AC-DG-12-009-01:** Page lists composite title, severity, participating layers, evidence links.
- **AC-DG-12-009-02:** Visual diagram export PNG optional from same data (reuse EPIC-DG-10 chart components if shared).
- **AC-DG-12-009-03:** Empty state explains when layer flags prevented correlation.

---

### AC test specifications (US-DG-12-009)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-009` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Page lists composite title, severity, participating layers, evidence links. |
| **Objective** | Verify AC-DG-12-009-01: Page lists composite title, severity, participating layers, evidence links. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-009-01` |
| **Secondary / negative test ID** | `TC-DG-12-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-009-01") or Xray/TestRail key == AC-DG-12-009-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-009` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P2` / `Post-MVP` |
| **MoSCoW** | `Could` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-10`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `2` |
| **Requirement (verbatim)** | Visual diagram export PNG optional from same data (reuse EPIC-DG-10 chart components if shared). |
| **Objective** | Verify AC-DG-12-009-02: Visual diagram export PNG optional from same data (reuse EPIC-DG-10 chart components if shared). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-12-009-02` |
| **Secondary / negative test ID** | `TC-DG-12-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-009-02") or Xray/TestRail key == AC-DG-12-009-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-009-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-009` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Empty state explains when layer flags prevented correlation. |
| **Objective** | Verify AC-DG-12-009-03: Empty state explains when layer flags prevented correlation. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-009-03` |
| **Secondary / negative test ID** | `TC-DG-12-009-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-009-03") or Xray/TestRail key == AC-DG-12-009-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-12-010 — Accessibility and i18n baseline

**As a** enterprise buyer, **I want** WCAG 2.1 AA targets for core flows, **so that** procurement passes.

**Acceptance criteria**

- **AC-DG-12-010-01:** Keyboard navigable scan list and findings table; focus traps in modals.
- **AC-DG-12-010-02:** Colour contrast meets AA for default theme; high-contrast theme optional.
- **AC-DG-12-010-03:** UI strings externalised for `en` + `zh` bundles at minimum.

---

### AC test specifications (US-DG-12-010)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-010` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Keyboard navigable scan list and findings table; focus traps in modals. |
| **Objective** | Verify AC-DG-12-010-01: Keyboard navigable scan list and findings table; focus traps in modals. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-010-01` |
| **Secondary / negative test ID** | `TC-DG-12-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-010-01") or Xray/TestRail key == AC-DG-12-010-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-010` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P2` / `Post-MVP` |
| **MoSCoW** | `Could` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `2` |
| **Requirement (verbatim)** | Colour contrast meets AA for default theme; high-contrast theme optional. |
| **Objective** | Verify AC-DG-12-010-02: Colour contrast meets AA for default theme; high-contrast theme optional. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-12-010-02` |
| **Secondary / negative test ID** | `TC-DG-12-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-010-02") or Xray/TestRail key == AC-DG-12-010-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-010-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-010` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | UI strings externalised for `en` + `zh` bundles at minimum. |
| **Objective** | Verify AC-DG-12-010-03: UI strings externalised for `en` + `zh` bundles at minimum. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-010-03` |
| **Secondary / negative test ID** | `TC-DG-12-010-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-010-03") or Xray/TestRail key == AC-DG-12-010-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-12-011 — API key management page (optional SaaS)

**As a** tenant admin, **I want** to rotate API keys for automation, **so that** leaked keys can be revoked.

**Acceptance criteria**

- **AC-DG-12-011-01:** Aligns with EPIC-DG-03 service account stories; UI never shows full key twice.
- **AC-DG-12-011-02:** Key usage last_seen updated on authenticated API calls.
- **AC-DG-12-011-03:** mTLS-only tenants hide API key UI entirely.

---

### AC test specifications (US-DG-12-011)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-011-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-011` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-03`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Aligns with EPIC-DG-03 service account stories; UI never shows full key twice. |
| **Objective** | Verify AC-DG-12-011-01: Aligns with EPIC-DG-03 service account stories; UI never shows full key twice. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-011-01` |
| **Secondary / negative test ID** | `TC-DG-12-011-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-011-01") or Xray/TestRail key == AC-DG-12-011-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-011-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-011` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Key usage last_seen updated on authenticated API calls. |
| **Objective** | Verify AC-DG-12-011-02: Key usage last_seen updated on authenticated API calls. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-011-02` |
| **Secondary / negative test ID** | `TC-DG-12-011-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-011-02") or Xray/TestRail key == AC-DG-12-011-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-011-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-011` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | mTLS-only tenants hide API key UI entirely. |
| **Objective** | Verify AC-DG-12-011-03: mTLS-only tenants hide API key UI entirely. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-011-03` |
| **Secondary / negative test ID** | `TC-DG-12-011-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-011-03") or Xray/TestRail key == AC-DG-12-011-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-12-012 — Embedded reasoning excerpt (auditor)

**As an** auditor, **I want** to view redacted reasoning excerpt per finding, **so that** I sample LLM logic without raw payload.

**Acceptance criteria**

- **AC-DG-12-012-01:** UI calls documented endpoint returning `redacted_excerpt` ≤4KiB policy (Architecture §23.1 Q9).
- **AC-DG-12-012-02:** Full trace export gated behind admin break-glass (EPIC-DG-11).
- **AC-DG-12-012-03:** Copy-to-clipboard strips HTML and limits size.

---

### AC test specifications (US-DG-12-012)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-012-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-012` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | UI calls documented endpoint returning `redacted_excerpt` ≤4KiB policy (Architecture §23.1 Q9). |
| **Objective** | Verify AC-DG-12-012-01: UI calls documented endpoint returning `redacted_excerpt` ≤4KiB policy (Architecture §23.1 Q9). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-012-01` |
| **Secondary / negative test ID** | `TC-DG-12-012-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-012-01") or Xray/TestRail key == AC-DG-12-012-01 |
| **Spec references** | Architecture §23.1 Q9 |

#### Test specification — AC-DG-12-012-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-012` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-11`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Full trace export gated behind admin break-glass (EPIC-DG-11). |
| **Objective** | Verify AC-DG-12-012-02: Full trace export gated behind admin break-glass (EPIC-DG-11). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-012-02` |
| **Secondary / negative test ID** | `TC-DG-12-012-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-012-02") or Xray/TestRail key == AC-DG-12-012-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-012-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-012` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Copy-to-clipboard strips HTML and limits size. |
| **Objective** | Verify AC-DG-12-012-03: Copy-to-clipboard strips HTML and limits size. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-012-03` |
| **Secondary / negative test ID** | `TC-DG-12-012-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-012-03") or Xray/TestRail key == AC-DG-12-012-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-12-013 — Mobile-friendly scan status view

**As an** on-call engineer, **I want** readable scan status on phone, **so that** I can approve cancel/resume away from desk.

**Acceptance criteria**

- **AC-DG-12-013-01:** Scan detail timeline stacks vertically <768px width without horizontal scroll.
- **AC-DG-12-013-02:** Critical actions reachable in ≤2 taps from home.
- **AC-DG-12-013-03:** Performance: LCP <2.5s on 4G for scan list page (NFR).

---

### AC test specifications (US-DG-12-013)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-013-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-013` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Scan detail timeline stacks vertically <768px width without horizontal scroll. |
| **Objective** | Verify AC-DG-12-013-01: Scan detail timeline stacks vertically <768px width without horizontal scroll. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-013-01` |
| **Secondary / negative test ID** | `TC-DG-12-013-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-013-01") or Xray/TestRail key == AC-DG-12-013-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-013-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-013` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Critical actions reachable in ≤2 taps from home. |
| **Objective** | Verify AC-DG-12-013-02: Critical actions reachable in ≤2 taps from home. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-013-02` |
| **Secondary / negative test ID** | `TC-DG-12-013-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-013-02") or Xray/TestRail key == AC-DG-12-013-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-013-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-013` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `Hardening` |
| **MoSCoW** | `Should` |
| **Requirement type** | `NFR` |
| **NFR metric / target** | `lcp / Defined in AC statement` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `4` |
| **Requirement (verbatim)** | Performance: LCP <2.5s on 4G for scan list page (NFR). |
| **Objective** | Verify AC-DG-12-013-03: Performance: LCP <2.5s on 4G for scan list page (NFR). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-013-03` |
| **Secondary / negative test ID** | `TC-DG-12-013-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-013-03") or Xray/TestRail key == AC-DG-12-013-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-12-014 — Tenant settings: retention and classification defaults

**As a** tenant admin, **I want** to set default report classification and artefact retention, **so that** every scan inherits policy.

**Acceptance criteria**

- **AC-DG-12-014-01:** Settings persist in `tenants.runtime_config` or dedicated columns per ADR.
- **AC-DG-12-014-02:** Overrides on single scan allowed only where EPIC-DG-03 permits.
- **AC-DG-12-014-03:** Dangerous retention below legal minimum blocked with validation error.

### AC test specifications (US-DG-12-014)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-12-014-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-014` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Settings persist in `tenants.runtime_config` or dedicated columns per ADR. |
| **Objective** | Verify AC-DG-12-014-01: Settings persist in `tenants.runtime_config` or dedicated columns per ADR. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-014-01` |
| **Secondary / negative test ID** | `TC-DG-12-014-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-014-01") or Xray/TestRail key == AC-DG-12-014-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-014-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-014` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-03`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Overrides on single scan allowed only where EPIC-DG-03 permits. |
| **Objective** | Verify AC-DG-12-014-02: Overrides on single scan allowed only where EPIC-DG-03 permits. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-014-02` |
| **Secondary / negative test ID** | `TC-DG-12-014-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-014-02") or Xray/TestRail key == AC-DG-12-014-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-12-014-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-12-014` |
| **Parent EPIC** | `EPIC-DG-12` |
| **Owning squad / role** | `frontend` / `frontend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L4-C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `bdd+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Dangerous retention below legal minimum blocked with validation error. |
| **Objective** | Verify AC-DG-12-014-03: Dangerous retention below legal minimum blocked with validation error. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-12-014-03` |
| **Secondary / negative test ID** | `TC-DG-12-014-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-12-014-03") or Xray/TestRail key == AC-DG-12-014-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## Epic Definition of Done checklist

- [ ] All in-scope ACs for `EPIC-DG-12` implemented by `frontend` and linked to automated tests (`TC-DG-*`).
- [ ] Unit coverage on touched packages is >=80%.
- [ ] Integration tests pass for all required ACs.
- [ ] Playwright BDD updated where `test_layer_required` includes `bdd`.
- [ ] Observability hooks and stable `error_code` behaviour validated.
- [ ] Security/data-sovereignty constraints verified (no secret leaks, tenant isolation).
- [ ] Design spec for slice exists under `docs/design/` with approved status.
