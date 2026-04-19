> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-02-control-plane-api.md`](../EPIC-02-control-plane-api.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-02 — Control plane HTTP API (FastAPI)

> **AC-level test specifications (generated):** Squad copy [`squads/control-plane/EPIC-DG-02-detailed.md`](squads/control-plane/EPIC-DG-02-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then `python3 scripts/validate_user_stories_traceability.py`.


**Goal:** Expose a versioned, tenant-safe HTTP API for creating and observing scans, retrieving findings and artefacts, and managing policies per `Architecture_Design.md` §28.

**Primary personas:** CI pipeline, Back-end integrator, Auditor (read-only).

---


## US-DG-02-001 — Create scan job with layered configuration

**As a** CI integrator, **I want** to `POST /v1/scans` with repo, policies, layers, optional cloud profiles and budgets, **so that** the engine analyses the correct scope.

**Wireframe — “Create scan” request builder (conceptual UI or API client)**

```text
┌──────── New Scan ─────────────────────────────┐
│ Repo URL: [https://gitlab…/svc.git    ]     │
│ Ref: [main]  Commit: [optional SHA]         │
│ Policies: [x] ISO-27001  [x] GB-T-22239     │
│ Layers:  (x) Code  (x) IaC  ( ) Cloud       │
│ Cloud profiles: [ + Add profile ]           │
│ Budget: max LLM USD [ 12.5 ]  wall [3600s]  │
│           [ Start Scan ]                    │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-02-001-01:** Request body validates `CreateScanRequest` shape including `repo`, `policy_ids`, `scan_layers`, optional `cloud_profiles`, `notifications`, `budget` (Architecture §28.4).
- **AC-DG-02-001-02:** Validation rejects jobs where `scan_layers.cloud=true` but neither `repo` nor `cloud_profiles` satisfy minimum inputs per normative rules (Architecture §28.4).
- **AC-DG-02-001-03:** Validation rejects `scan_layers.code=true` or `iac=true` without `repo` when required (Architecture §28.4).
- **AC-DG-02-001-04:** Response `201` returns `scan_id` and initial `status` in {`PENDING`,`QUEUED`}.

---

### AC test specifications (US-DG-02-001)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-001` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P2` / `Post-MVP` |
| **MoSCoW** | `Could` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `2` |
| **Requirement (verbatim)** | Request body validates `CreateScanRequest` shape including `repo`, `policy_ids`, `scan_layers`, optional `cloud_profiles`, `notifications`, `budget` (Architecture §28.4). |
| **Objective** | Verify AC-DG-02-001-01: Request body validates `CreateScanRequest` shape including `repo`, `policy_ids`, `scan_layers`, optional `cloud_profiles`, `notifications`, `budget` (Architecture §28.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-02-001-01` |
| **Secondary / negative test ID** | `TC-DG-02-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-001-01") or Xray/TestRail key == AC-DG-02-001-01 |
| **Spec references** | Architecture §28.4 |

#### Test specification — AC-DG-02-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-001` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Validation rejects jobs where `scan_layers.cloud=true` but neither `repo` nor `cloud_profiles` satisfy minimum inputs per normative rules (Architecture §28.4). |
| **Objective** | Verify AC-DG-02-001-02: Validation rejects jobs where `scan_layers.cloud=true` but neither `repo` nor `cloud_profiles` satisfy minimum inputs per normative rules (Architecture §28.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. \| 4. Execute negative path and assert stable error_code with no side effects. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-001-02` |
| **Secondary / negative test ID** | `TC-DG-02-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-001-02") or Xray/TestRail key == AC-DG-02-001-02 |
| **Spec references** | Architecture §28.4 |

#### Test specification — AC-DG-02-001-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-001` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Validation rejects `scan_layers.code=true` or `iac=true` without `repo` when required (Architecture §28.4). |
| **Objective** | Verify AC-DG-02-001-03: Validation rejects `scan_layers.code=true` or `iac=true` without `repo` when required (Architecture §28.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. \| 4. Execute negative path and assert stable error_code with no side effects. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-001-03` |
| **Secondary / negative test ID** | `TC-DG-02-001-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-001-03") or Xray/TestRail key == AC-DG-02-001-03 |
| **Spec references** | Architecture §28.4 |

#### Test specification — AC-DG-02-001-04

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-001` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Response `201` returns `scan_id` and initial `status` in {`PENDING`,`QUEUED`}. |
| **Objective** | Verify AC-DG-02-001-04: Response `201` returns `scan_id` and initial `status` in {`PENDING`,`QUEUED`}. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-001-04` |
| **Secondary / negative test ID** | `TC-DG-02-001-04.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-001-04") or Xray/TestRail key == AC-DG-02-001-04 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-02-002 — Idempotent scan creation

**As a** CI pipeline, **I want** duplicate submissions with the same idempotency key to return the same scan, **so that** retries do not fork jobs.

**Acceptance criteria**

- **AC-DG-02-002-01:** `Idempotency-Key` header optional; duplicates within 24h return same `scan_id` with `201` or documented idempotent success code (Architecture §28.3).
- **AC-DG-02-002-02:** DB uniqueness on `(tenant_id, idempotency_key)` enforced (Architecture §29.1).

---

### AC test specifications (US-DG-02-002)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-002` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P2` / `Post-MVP` |
| **MoSCoW** | `Could` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `2` |
| **Requirement (verbatim)** | `Idempotency-Key` header optional; duplicates within 24h return same `scan_id` with `201` or documented idempotent success code (Architecture §28.3). |
| **Objective** | Verify AC-DG-02-002-01: `Idempotency-Key` header optional; duplicates within 24h return same `scan_id` with `201` or documented idempotent success code (Architecture §28.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-02-002-01` |
| **Secondary / negative test ID** | `TC-DG-02-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-002-01") or Xray/TestRail key == AC-DG-02-002-01 |
| **Spec references** | Architecture §28.3 |

#### Test specification — AC-DG-02-002-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-002` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | DB uniqueness on `(tenant_id, idempotency_key)` enforced (Architecture §29.1). |
| **Objective** | Verify AC-DG-02-002-02: DB uniqueness on `(tenant_id, idempotency_key)` enforced (Architecture §29.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-002-02` |
| **Secondary / negative test ID** | `TC-DG-02-002-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-002-02") or Xray/TestRail key == AC-DG-02-002-02 |
| **Spec references** | Architecture §29.1 |


## US-DG-02-003 — Poll scan status with stage granularity

**As an** operator, **I want** `GET /v1/scans/{scan_id}`, **so that** I can surface progress and errors.

**Wireframe — status card**

```text
┌──────── Scan 3fa2… ────────────────────────┐
│ Status: MAPPING (72%)                       │
│ Stage started: 2026-04-18T10:21:05Z         │
│ Policies: ISO-27001-2022 @ 2026-03-01      │
│ Error code: (empty)                         │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-02-003-01:** Response includes `current_stage`, `stage_started_at`, `percent_complete`, `error_code`, `error_message` (sanitised) per §28.5.
- **AC-DG-02-003-02:** Terminal states `COMPLETE`, `FAILED`, `CANCELLED`, `AWAITING_REVIEW` behave as documented (Architecture §28.5).
- **AC-DG-02-003-03:** Cross-tenant access returns `404` or `403` without leaking existence (security baseline).

---

### AC test specifications (US-DG-02-003)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-003` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Response includes `current_stage`, `stage_started_at`, `percent_complete`, `error_code`, `error_message` (sanitised) per §28.5. |
| **Objective** | Verify AC-DG-02-003-01: Response includes `current_stage`, `stage_started_at`, `percent_complete`, `error_code`, `error_message` (sanitised) per §28.5. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-003-01` |
| **Secondary / negative test ID** | `TC-DG-02-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-003-01") or Xray/TestRail key == AC-DG-02-003-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-02-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-003` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Terminal states `COMPLETE`, `FAILED`, `CANCELLED`, `AWAITING_REVIEW` behave as documented (Architecture §28.5). |
| **Objective** | Verify AC-DG-02-003-02: Terminal states `COMPLETE`, `FAILED`, `CANCELLED`, `AWAITING_REVIEW` behave as documented (Architecture §28.5). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-003-02` |
| **Secondary / negative test ID** | `TC-DG-02-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-003-02") or Xray/TestRail key == AC-DG-02-003-02 |
| **Spec references** | Architecture §28.5 |

#### Test specification — AC-DG-02-003-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-003` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Cross-tenant access returns `404` or `403` without leaking existence (security baseline). |
| **Objective** | Verify AC-DG-02-003-03: Cross-tenant access returns `404` or `403` without leaking existence (security baseline). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-003-03` |
| **Secondary / negative test ID** | `TC-DG-02-003-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-003-03") or Xray/TestRail key == AC-DG-02-003-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-02-004 — Paginated findings export

**As an** auditor, **I want** `GET /v1/scans/{scan_id}/findings` with filters, **so that** I can export evidence for control testing.

**Acceptance criteria**

- **AC-DG-02-004-01:** Supports `severity`, `framework`, `cursor` pagination (Architecture §28.3).
- **AC-DG-02-004-02:** Each finding includes stable identifiers: `framework`, `control_id`, `status`, `severity`, `evidence_refs`, `confidence_score`, `policy_version` (Architecture §29.1 fields / §3 model).

---

### AC test specifications (US-DG-02-004)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-004` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Supports `severity`, `framework`, `cursor` pagination (Architecture §28.3). |
| **Objective** | Verify AC-DG-02-004-01: Supports `severity`, `framework`, `cursor` pagination (Architecture §28.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-004-01` |
| **Secondary / negative test ID** | `TC-DG-02-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-004-01") or Xray/TestRail key == AC-DG-02-004-01 |
| **Spec references** | Architecture §28.3 |

#### Test specification — AC-DG-02-004-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-004` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Each finding includes stable identifiers: `framework`, `control_id`, `status`, `severity`, `evidence_refs`, `confidence_score`, `policy_version` (Architecture §29.1 fields / §3 model). |
| **Objective** | Verify AC-DG-02-004-02: Each finding includes stable identifiers: `framework`, `control_id`, `status`, `severity`, `evidence_refs`, `confidence_score`, `policy_version` (Architecture §29.1 fields / §3 model). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-004-02` |
| **Secondary / negative test ID** | `TC-DG-02-004-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-004-02") or Xray/TestRail key == AC-DG-02-004-02 |
| **Spec references** | Architecture §29.1 fields / §3 model |


## US-DG-02-005 — Secure artefact download

**As a** user, **I want** presigned or proxied artefact access, **so that** reports are not publicly enumerable.

**Acceptance criteria**

- **AC-DG-02-005-01:** `GET /v1/scans/{scan_id}/artifacts/{artifact_id}` returns `302` to short-TTL presigned URL or streams via authenticated proxy (Architecture §28.3).
- **AC-DG-02-005-02:** Artefact row stores `checksum_sha256`, `size_bytes`, `encryption` mode (Architecture §29.1).

---

### AC test specifications (US-DG-02-005)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-005` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `GET /v1/scans/{scan_id}/artifacts/{artifact_id}` returns `302` to short-TTL presigned URL or streams via authenticated proxy (Architecture §28.3). |
| **Objective** | Verify AC-DG-02-005-01: `GET /v1/scans/{scan_id}/artifacts/{artifact_id}` returns `302` to short-TTL presigned URL or streams via authenticated proxy (Architecture §28.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-005-01` |
| **Secondary / negative test ID** | `TC-DG-02-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-005-01") or Xray/TestRail key == AC-DG-02-005-01 |
| **Spec references** | Architecture §28.3 |

#### Test specification — AC-DG-02-005-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-005` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `5` |
| **Requirement (verbatim)** | Artefact row stores `checksum_sha256`, `size_bytes`, `encryption` mode (Architecture §29.1). |
| **Objective** | Verify AC-DG-02-005-02: Artefact row stores `checksum_sha256`, `size_bytes`, `encryption` mode (Architecture §29.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-005-02` |
| **Secondary / negative test ID** | `TC-DG-02-005-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-005-02") or Xray/TestRail key == AC-DG-02-005-02 |
| **Spec references** | Architecture §29.1 |


## US-DG-02-006 — Signed webhooks

**As a** SecOps integrator, **I want** signed `scan.completed` / `scan.failed` webhooks, **so that** my SOAR can trust events.

**Acceptance criteria**

- **AC-DG-02-006-01:** Payload includes `event`, `scan_id`, `tenant_id`, `report_artifact_id` when completed (Architecture §28.6).
- **AC-DG-02-006-02:** `X-DeepGuard-Signature: sha256=<hex>` verifies raw body with shared secret (Architecture §28.6).
- **AC-DG-02-006-03:** Retries with exponential backoff and DLQ rows in `webhook_deliveries` (Architecture §28.6, §29.4).

---

### AC test specifications (US-DG-02-006)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-006` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Payload includes `event`, `scan_id`, `tenant_id`, `report_artifact_id` when completed (Architecture §28.6). |
| **Objective** | Verify AC-DG-02-006-01: Payload includes `event`, `scan_id`, `tenant_id`, `report_artifact_id` when completed (Architecture §28.6). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-006-01` |
| **Secondary / negative test ID** | `TC-DG-02-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-006-01") or Xray/TestRail key == AC-DG-02-006-01 |
| **Spec references** | Architecture §28.6 |

#### Test specification — AC-DG-02-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-006` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `X-DeepGuard-Signature: sha256=<hex>` verifies raw body with shared secret (Architecture §28.6). |
| **Objective** | Verify AC-DG-02-006-02: `X-DeepGuard-Signature: sha256=<hex>` verifies raw body with shared secret (Architecture §28.6). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-006-02` |
| **Secondary / negative test ID** | `TC-DG-02-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-006-02") or Xray/TestRail key == AC-DG-02-006-02 |
| **Spec references** | Architecture §28.6 |

#### Test specification — AC-DG-02-006-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-006` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Retries with exponential backoff and DLQ rows in `webhook_deliveries` (Architecture §28.6, §29.4). |
| **Objective** | Verify AC-DG-02-006-03: Retries with exponential backoff and DLQ rows in `webhook_deliveries` (Architecture §28.6, §29.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-006-03` |
| **Secondary / negative test ID** | `TC-DG-02-006-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-006-03") or Xray/TestRail key == AC-DG-02-006-03 |
| **Spec references** | Architecture §28.6, §29.4 |


## US-DG-02-007 — API versioning and deprecation headers

**As an** API consumer, **I want** stable `/v1` paths and sunset notices, **so that** I can plan breaking migrations.

**Acceptance criteria**

- **AC-DG-02-007-01:** All documented resources live under base path `/v1` (Architecture §28.1).
- **AC-DG-02-007-02:** Deprecated endpoints return `Sunset` header per RFC 8594 when applicable (Architecture §28.1).
- **AC-DG-02-007-03:** Breaking changes require `/v2` path prefix; changelog references story IDs where maintained.

---

### AC test specifications (US-DG-02-007)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-007` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | All documented resources live under base path `/v1` (Architecture §28.1). |
| **Objective** | Verify AC-DG-02-007-01: All documented resources live under base path `/v1` (Architecture §28.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-007-01` |
| **Secondary / negative test ID** | `TC-DG-02-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-007-01") or Xray/TestRail key == AC-DG-02-007-01 |
| **Spec references** | Architecture §28.1 |

#### Test specification — AC-DG-02-007-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-007` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Deprecated endpoints return `Sunset` header per RFC 8594 when applicable (Architecture §28.1). |
| **Objective** | Verify AC-DG-02-007-02: Deprecated endpoints return `Sunset` header per RFC 8594 when applicable (Architecture §28.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-007-02` |
| **Secondary / negative test ID** | `TC-DG-02-007-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-007-02") or Xray/TestRail key == AC-DG-02-007-02 |
| **Spec references** | Architecture §28.1 |

#### Test specification — AC-DG-02-007-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-007` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Breaking changes require `/v2` path prefix; changelog references story IDs where maintained. |
| **Objective** | Verify AC-DG-02-007-03: Breaking changes require `/v2` path prefix; changelog references story IDs where maintained. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-007-03` |
| **Secondary / negative test ID** | `TC-DG-02-007-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-007-03") or Xray/TestRail key == AC-DG-02-007-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-02-008 — Resume human-in-the-loop scan

**As a** reviewer, **I want** `POST /v1/scans/{scan_id}/resume` with annotations JSON, **so that** Athena receives reviewer context.

**Acceptance criteria**

- **AC-DG-02-008-01:** Resume returns `202` when graph was interrupted and credentials still valid (Architecture §28.3).
- **AC-DG-02-008-02:** Resume rejected with clear error when scan not in `AWAITING_REVIEW` or user lacks role (Architecture §28.3, EPIC-DG-03).
- **AC-DG-02-008-03:** Annotations merge into `ScanState` fields documented for HITL (Architecture §4.7).

---

### AC test specifications (US-DG-02-008)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-008` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `5` |
| **Requirement (verbatim)** | Resume returns `202` when graph was interrupted and credentials still valid (Architecture §28.3). |
| **Objective** | Verify AC-DG-02-008-01: Resume returns `202` when graph was interrupted and credentials still valid (Architecture §28.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-008-01` |
| **Secondary / negative test ID** | `TC-DG-02-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-008-01") or Xray/TestRail key == AC-DG-02-008-01 |
| **Spec references** | Architecture §28.3 |

#### Test specification — AC-DG-02-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-008` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-03`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `5` |
| **Requirement (verbatim)** | Resume rejected with clear error when scan not in `AWAITING_REVIEW` or user lacks role (Architecture §28.3, EPIC-DG-03). |
| **Objective** | Verify AC-DG-02-008-02: Resume rejected with clear error when scan not in `AWAITING_REVIEW` or user lacks role (Architecture §28.3, EPIC-DG-03). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. \| 4. Execute negative path and assert stable error_code with no side effects. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-008-02` |
| **Secondary / negative test ID** | `TC-DG-02-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-008-02") or Xray/TestRail key == AC-DG-02-008-02 |
| **Spec references** | Architecture §28.3, EPIC-DG-03 |

#### Test specification — AC-DG-02-008-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-008` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Annotations merge into `ScanState` fields documented for HITL (Architecture §4.7). |
| **Objective** | Verify AC-DG-02-008-03: Annotations merge into `ScanState` fields documented for HITL (Architecture §4.7). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-008-03` |
| **Secondary / negative test ID** | `TC-DG-02-008-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-008-03") or Xray/TestRail key == AC-DG-02-008-03 |
| **Spec references** | Architecture §4.7 |


## US-DG-02-009 — List scans for tenant (cursor pagination)

**As a** dashboard user, **I want** `GET /v1/scans` with filters and cursor, **so that** I can page history without loading full tables.

**Wireframe — list API consumer**

```text
GET /v1/scans?status=FAILED&cursor=eyJ…
→ 200 { items: [...], next_cursor: "…" | null }
```

**Acceptance criteria**

- **AC-DG-02-009-01:** Endpoint exists and returns only current tenant’s scans (Architecture §28.2).
- **AC-DG-02-009-02:** Supports filter by `status`, optional `repo` substring, sort by `updated_at` desc default.
- **AC-DG-02-009-03:** Cursor is opaque, stable, and documented max page size (e.g. ≤100).

---

### AC test specifications (US-DG-02-009)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-009` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Endpoint exists and returns only current tenant’s scans (Architecture §28.2). |
| **Objective** | Verify AC-DG-02-009-01: Endpoint exists and returns only current tenant’s scans (Architecture §28.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-009-01` |
| **Secondary / negative test ID** | `TC-DG-02-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-009-01") or Xray/TestRail key == AC-DG-02-009-01 |
| **Spec references** | Architecture §28.2 |

#### Test specification — AC-DG-02-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-009` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P2` / `Post-MVP` |
| **MoSCoW** | `Could` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `2` |
| **Requirement (verbatim)** | Supports filter by `status`, optional `repo` substring, sort by `updated_at` desc default. |
| **Objective** | Verify AC-DG-02-009-02: Supports filter by `status`, optional `repo` substring, sort by `updated_at` desc default. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-02-009-02` |
| **Secondary / negative test ID** | `TC-DG-02-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-009-02") or Xray/TestRail key == AC-DG-02-009-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-02-009-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-009` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Cursor is opaque, stable, and documented max page size (e.g. ≤100). |
| **Objective** | Verify AC-DG-02-009-03: Cursor is opaque, stable, and documented max page size (e.g. ≤100). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-009-03` |
| **Secondary / negative test ID** | `TC-DG-02-009-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-009-03") or Xray/TestRail key == AC-DG-02-009-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-02-010 — Service health and readiness

**As a** k8s operator, **I want** liveness/readiness endpoints, **so that** rollouts do not send traffic to broken API pods.

**Acceptance criteria**

- **AC-DG-02-010-01:** `/healthz` (or `/livez`) returns 200 if process up (no DB required).
- **AC-DG-02-010-02:** `/readyz` returns 200 only when DB, Redis, and object store connectivity checks pass (configurable strictness).
- **AC-DG-02-010-03:** Readiness failure includes stable `error_code` body for logs, not secrets.

---

### AC test specifications (US-DG-02-010)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-010` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `/healthz` (or `/livez`) returns 200 if process up (no DB required). |
| **Objective** | Verify AC-DG-02-010-01: `/healthz` (or `/livez`) returns 200 if process up (no DB required). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-010-01` |
| **Secondary / negative test ID** | `TC-DG-02-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-010-01") or Xray/TestRail key == AC-DG-02-010-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-02-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-010` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `/readyz` returns 200 only when DB, Redis, and object store connectivity checks pass (configurable strictness). |
| **Objective** | Verify AC-DG-02-010-02: `/readyz` returns 200 only when DB, Redis, and object store connectivity checks pass (configurable strictness). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-010-02` |
| **Secondary / negative test ID** | `TC-DG-02-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-010-02") or Xray/TestRail key == AC-DG-02-010-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-02-010-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-010` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Readiness failure includes stable `error_code` body for logs, not secrets. |
| **Objective** | Verify AC-DG-02-010-03: Readiness failure includes stable `error_code` body for logs, not secrets. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-010-03` |
| **Secondary / negative test ID** | `TC-DG-02-010-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-010-03") or Xray/TestRail key == AC-DG-02-010-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-02-011 — OpenAPI schema publication

**As a** integrator, **I want** machine-readable OpenAPI 3.x, **so that** I can generate SDKs.

**Acceptance criteria**

- **AC-DG-02-011-01:** `GET /openapi.json` (or `/v1/openapi.json`) serves schema matching implemented routes (Architecture §28).
- **AC-DG-02-011-02:** Schemas include `CreateScanRequest`, `Scan`, `Finding`, error models with `error_code`.
- **AC-DG-02-011-03:** CI fails if routes drift from committed OpenAPI snapshot (optional gate).

---

### AC test specifications (US-DG-02-011)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-011-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-011` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `GET /openapi.json` (or `/v1/openapi.json`) serves schema matching implemented routes (Architecture §28). |
| **Objective** | Verify AC-DG-02-011-01: `GET /openapi.json` (or `/v1/openapi.json`) serves schema matching implemented routes (Architecture §28). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-011-01` |
| **Secondary / negative test ID** | `TC-DG-02-011-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-011-01") or Xray/TestRail key == AC-DG-02-011-01 |
| **Spec references** | Architecture §28 |

#### Test specification — AC-DG-02-011-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-011` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Schemas include `CreateScanRequest`, `Scan`, `Finding`, error models with `error_code`. |
| **Objective** | Verify AC-DG-02-011-02: Schemas include `CreateScanRequest`, `Scan`, `Finding`, error models with `error_code`. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-011-02` |
| **Secondary / negative test ID** | `TC-DG-02-011-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-011-02") or Xray/TestRail key == AC-DG-02-011-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-02-011-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-011` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P2` / `Post-MVP` |
| **MoSCoW** | `Could` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `2` |
| **Requirement (verbatim)** | CI fails if routes drift from committed OpenAPI snapshot (optional gate). |
| **Objective** | Verify AC-DG-02-011-03: CI fails if routes drift from committed OpenAPI snapshot (optional gate). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-02-011-03` |
| **Secondary / negative test ID** | `TC-DG-02-011-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-011-03") or Xray/TestRail key == AC-DG-02-011-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-02-012 — Structured problem details on errors

**As a** client developer, **I want** RFC 7807-style problem JSON, **so that** I can branch logic on `error_code` without parsing prose.

**Acceptance criteria**

- **AC-DG-02-012-01:** 4xx/5xx responses include `application/problem+json` or documented JSON with `type`, `title`, `status`, `error_code`, `detail` (sanitised).
- **AC-DG-02-012-02:** Validation errors list field-level issues for `CreateScanRequest` without echoing secrets.
- **AC-DG-02-012-03:** Rate limit responses include `Retry-After` when applicable (Architecture §35.2, EPIC-DG-03).

---

### AC test specifications (US-DG-02-012)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-012-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-012` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | 4xx/5xx responses include `application/problem+json` or documented JSON with `type`, `title`, `status`, `error_code`, `detail` (sanitised). |
| **Objective** | Verify AC-DG-02-012-01: 4xx/5xx responses include `application/problem+json` or documented JSON with `type`, `title`, `status`, `error_code`, `detail` (sanitised). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-012-01` |
| **Secondary / negative test ID** | `TC-DG-02-012-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-012-01") or Xray/TestRail key == AC-DG-02-012-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-02-012-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-012` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Validation errors list field-level issues for `CreateScanRequest` without echoing secrets. |
| **Objective** | Verify AC-DG-02-012-02: Validation errors list field-level issues for `CreateScanRequest` without echoing secrets. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-012-02` |
| **Secondary / negative test ID** | `TC-DG-02-012-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-012-02") or Xray/TestRail key == AC-DG-02-012-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-02-012-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-012` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-03`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Rate limit responses include `Retry-After` when applicable (Architecture §35.2, EPIC-DG-03). |
| **Objective** | Verify AC-DG-02-012-03: Rate limit responses include `Retry-After` when applicable (Architecture §35.2, EPIC-DG-03). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-012-03` |
| **Secondary / negative test ID** | `TC-DG-02-012-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-012-03") or Xray/TestRail key == AC-DG-02-012-03 |
| **Spec references** | Architecture §35.2, EPIC-DG-03 |


## US-DG-02-013 — Correlation IDs across API and workers

**As an** SRE, **I want** `X-Request-Id` propagated to logs and traces, **so that** I can tie HTTP to graph spans.

**Acceptance criteria**

- **AC-DG-02-013-01:** API accepts client `X-Request-Id` or generates UUID; returns same in response header.
- **AC-DG-02-013-02:** Request ID stored on `scans` row or child correlation table and passed in `ScanJobMessage` / worker logs.
- **AC-DG-02-013-03:** LangFuse/LangSmith sessions remain joinable by `scan_id` + request id (EPIC-DG-11).

---

### AC test specifications (US-DG-02-013)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-013-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-013` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | API accepts client `X-Request-Id` or generates UUID; returns same in response header. |
| **Objective** | Verify AC-DG-02-013-01: API accepts client `X-Request-Id` or generates UUID; returns same in response header. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-013-01` |
| **Secondary / negative test ID** | `TC-DG-02-013-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-013-01") or Xray/TestRail key == AC-DG-02-013-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-02-013-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-013` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Request ID stored on `scans` row or child correlation table and passed in `ScanJobMessage` / worker logs. |
| **Objective** | Verify AC-DG-02-013-02: Request ID stored on `scans` row or child correlation table and passed in `ScanJobMessage` / worker logs. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-013-02` |
| **Secondary / negative test ID** | `TC-DG-02-013-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-013-02") or Xray/TestRail key == AC-DG-02-013-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-02-013-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-013` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-11`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | LangFuse/LangSmith sessions remain joinable by `scan_id` + request id (EPIC-DG-11). |
| **Objective** | Verify AC-DG-02-013-03: LangFuse/LangSmith sessions remain joinable by `scan_id` + request id (EPIC-DG-11). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-013-03` |
| **Secondary / negative test ID** | `TC-DG-02-013-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-013-03") or Xray/TestRail key == AC-DG-02-013-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-02-014 — Export findings as JSONL for SIEM

**As a** SOC engineer, **I want** bulk export of findings for a scan, **so that** I can load them into Splunk/Databricks.

**Acceptance criteria**

- **AC-DG-02-014-01:** `GET /v1/scans/{scan_id}/findings:export?format=jsonl` (or POST async job) streams newline-delimited JSON with stable field names.
- **AC-DG-02-014-02:** Export respects tenant RBAC; rate limited to prevent abuse.
- **AC-DG-02-014-03:** Each line includes `finding_id`, `scan_id`, `framework`, `control_id`, `severity`, `evidence_refs` (Architecture §29.1).

### AC test specifications (US-DG-02-014)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-02-014-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-014` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `GET /v1/scans/{scan_id}/findings:export?format=jsonl` (or POST async job) streams newline-delimited JSON with stable field names. |
| **Objective** | Verify AC-DG-02-014-01: `GET /v1/scans/{scan_id}/findings:export?format=jsonl` (or POST async job) streams newline-delimited JSON with stable field names. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-014-01` |
| **Secondary / negative test ID** | `TC-DG-02-014-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-014-01") or Xray/TestRail key == AC-DG-02-014-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-02-014-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-014` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Export respects tenant RBAC; rate limited to prevent abuse. |
| **Objective** | Verify AC-DG-02-014-02: Export respects tenant RBAC; rate limited to prevent abuse. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-014-02` |
| **Secondary / negative test ID** | `TC-DG-02-014-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-014-02") or Xray/TestRail key == AC-DG-02-014-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-02-014-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-02-014` |
| **Parent EPIC** | `EPIC-DG-02` |
| **Owning squad / role** | `control-plane` / `backend_engineer` |
| **Phase mapping** | primary `L3`; secondary `L12/C5` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Each line includes `finding_id`, `scan_id`, `framework`, `control_id`, `severity`, `evidence_refs` (Architecture §29.1). |
| **Objective** | Verify AC-DG-02-014-03: Each line includes `finding_id`, `scan_id`, `framework`, `control_id`, `severity`, `evidence_refs` (Architecture §29.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-02-014-03` |
| **Secondary / negative test ID** | `TC-DG-02-014-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-02-014-03") or Xray/TestRail key == AC-DG-02-014-03 |
| **Spec references** | Architecture §29.1 |


## Epic Definition of Done checklist

- [ ] All in-scope ACs for `EPIC-DG-02` implemented by `control-plane` and linked to automated tests (`TC-DG-*`).
- [ ] Unit coverage on touched packages is >=80%.
- [ ] Integration tests pass for all required ACs.
- [ ] Playwright BDD updated where `test_layer_required` includes `bdd`.
- [ ] Observability hooks and stable `error_code` behaviour validated.
- [ ] Security/data-sovereignty constraints verified (no secret leaks, tenant isolation).
- [ ] Design spec for slice exists under `docs/design/` with approved status.
