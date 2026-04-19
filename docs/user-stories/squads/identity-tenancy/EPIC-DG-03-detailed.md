> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-03-identity-tenancy-rbac.md`](../EPIC-03-identity-tenancy-rbac.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-03 — Identity, tenancy & RBAC (Eumaeus)

> **AC-level test specifications (generated):** Squad copy [`squads/identity-tenancy/EPIC-DG-03-detailed.md`](squads/identity-tenancy/EPIC-DG-03-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py`.


**Goal:** Enforce tenant isolation and role capabilities across API and data paths per `Architecture_Design.md` §28.2, §29, §24.

**Primary personas:** Tenant admin, Scanner, Auditor.

---


## US-DG-03-001 — OIDC JWT authentication (SaaS / enterprise)

**As a** tenant admin, **I want** users to authenticate via OIDC JWT, **so that** roles and `tenant_id` are cryptographically bound.

**Wireframe — login / token flow (simplified)**

```text
  User                IdP                DeepGuard API
   |-- login -------->|                   |
   |<-- id_token -----|                   |
   |--- Authorization: Bearer <JWT> ---->|  /v1/scans
```

**Acceptance criteria**

- **AC-DG-03-001-01:** JWT validates issuer/audience configured by `JWT_ISSUER`, `JWT_AUDIENCE` (Architecture §27.1, §28.2).
- **AC-DG-03-001-02:** Claim `tenant_id` (UUID) is mandatory for authorisation context.
- **AC-DG-03-001-03:** Roles `scanner`, `admin`, `auditor` constrain verbs (e.g. auditors read-only; policy upload admin-only) (Architecture §28.2).

---

### AC test specifications (US-DG-03-001)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-03-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-001` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | JWT validates issuer/audience configured by `JWT_ISSUER`, `JWT_AUDIENCE` (Architecture §27.1, §28.2). |
| **Objective** | Verify the behaviour described in AC-DG-03-001-01: JWT validates issuer/audience configured by `JWT_ISSUER`, `JWT_AUDIENCE` (Architecture §27.1, §28.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-001-01` |
| **Secondary / negative test ID** | `TC-DG-03-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-001-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §27.1, §28.2 |

#### Test specification — AC-DG-03-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-001` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Claim `tenant_id` (UUID) is mandatory for authorisation context. |
| **Objective** | Verify the behaviour described in AC-DG-03-001-02: Claim `tenant_id` (UUID) is mandatory for authorisation context. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-001-02` |
| **Secondary / negative test ID** | `TC-DG-03-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-001-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-001-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-001` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Roles `scanner`, `admin`, `auditor` constrain verbs (e.g. auditors read-only; policy upload admin-only) (Architecture §28.2). |
| **Objective** | Verify the behaviour described in AC-DG-03-001-03: Roles `scanner`, `admin`, `auditor` constrain verbs (e.g. auditors read-only; policy upload admin-only) (Architecture §28.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-001-03` |
| **Secondary / negative test ID** | `TC-DG-03-001-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-001-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §28.2 |


## US-DG-03-002 — Hard tenant isolation on all resources

**As a** security officer, **I want** no cross-tenant reads/writes, **so that** customer data never leaks across logical boundaries.

**Acceptance criteria**

- **AC-DG-03-002-01:** Every persisted row carries `tenant_id` and API middleware rejects mismatched paths (Architecture §28.2, §29.1).
- **AC-DG-03-002-02:** Object storage keys are namespaced by `tenant_id` / `scan_id` (Architecture §32.1).

---

### AC test specifications (US-DG-03-002)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-03-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-002` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Every persisted row carries `tenant_id` and API middleware rejects mismatched paths (Architecture §28.2, §29.1). |
| **Objective** | Verify the behaviour described in AC-DG-03-002-01: Every persisted row carries `tenant_id` and API middleware rejects mismatched paths (Architecture §28.2, §29.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. \| 4. Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-002-01` |
| **Secondary / negative test ID** | `TC-DG-03-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-002-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §28.2, §29.1 |

#### Test specification — AC-DG-03-002-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-002` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Object storage keys are namespaced by `tenant_id` / `scan_id` (Architecture §32.1). |
| **Objective** | Verify the behaviour described in AC-DG-03-002-02: Object storage keys are namespaced by `tenant_id` / `scan_id` (Architecture §32.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-002-02` |
| **Secondary / negative test ID** | `TC-DG-03-002-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-002-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §32.1 |


## US-DG-03-003 — Runtime configuration merge

**As a** platform admin, **I want** tenant-level `runtime_config` merged with safe defaults, **so that** features can be toggled without code deploy.

**Wireframe — tenant settings (admin)**

```text
┌──── Tenant runtime flags ────────────────────┐
│ semantic_cache_enabled: [on|off]            │
│ semantic_cache_threshold: [0.97] (0.95–0.99)│
│ delta_skip_analysis: [ ]                    │
│ max_concurrent_scans: [3]                   │
│                        [ Save ]             │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-03-003-01:** Effective config = `deep_merge(DEFAULT_RUNTIME_CONFIG, tenants.runtime_config[, scan_job_overrides])` per §24.2.
- **AC-DG-03-003-02:** Scan-level overrides allowed only for `budget.*` and `notifications.*` unless role `admin` (Architecture §24.2).
- **AC-DG-03-003-03:** Safety flags such as `semantic_cache_threshold` cannot be overridden by non-admin (Architecture §24.2).

---

### AC test specifications (US-DG-03-003)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-03-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-003` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Effective config = `deep_merge(DEFAULT_RUNTIME_CONFIG, tenants.runtime_config[, scan_job_overrides])` per §24.2. |
| **Objective** | Verify the behaviour described in AC-DG-03-003-01: Effective config = `deep_merge(DEFAULT_RUNTIME_CONFIG, tenants.runtime_config[, scan_job_overrides])` per §24.2. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-003-01` |
| **Secondary / negative test ID** | `TC-DG-03-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-003-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-003` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Scan-level overrides allowed only for `budget.*` and `notifications.*` unless role `admin` (Architecture §24.2). |
| **Objective** | Verify the behaviour described in AC-DG-03-003-02: Scan-level overrides allowed only for `budget.*` and `notifications.*` unless role `admin` (Architecture §24.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-003-02` |
| **Secondary / negative test ID** | `TC-DG-03-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-003-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §24.2 |

#### Test specification — AC-DG-03-003-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-003` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Safety flags such as `semantic_cache_threshold` cannot be overridden by non-admin (Architecture §24.2). |
| **Objective** | Verify the behaviour described in AC-DG-03-003-03: Safety flags such as `semantic_cache_threshold` cannot be overridden by non-admin (Architecture §24.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-003-03` |
| **Secondary / negative test ID** | `TC-DG-03-003-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-003-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §24.2 |


## US-DG-03-004 — Backpressure for concurrent scans

**As a** SaaS operator, **I want** per-tenant concurrency caps, **so that** noisy neighbours cannot exhaust workers.

**Acceptance criteria**

- **AC-DG-03-004-01:** When `max_concurrent_scans` / `MAX_CONCURRENT_SCANS_PER_TENANT` exceeded, API returns `429` with `Retry-After` (Architecture §35.2, §24.1).

---

### AC test specifications (US-DG-03-004)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-03-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-004` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | When `max_concurrent_scans` / `MAX_CONCURRENT_SCANS_PER_TENANT` exceeded, API returns `429` with `Retry-After` (Architecture §35.2, §24.1). |
| **Objective** | Verify the behaviour described in AC-DG-03-004-01: When `max_concurrent_scans` / `MAX_CONCURRENT_SCANS_PER_TENANT` exceeded, API returns `429` with `Retry-After` (Architecture §35.2, §24.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. \| 4. Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-03-004-01` |
| **Secondary / negative test ID** | `TC-DG-03-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-004-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §35.2, §24.1 |


## US-DG-03-005 — Machine-to-machine authentication (optional mTLS)

**As a** platform engineer, **I want** worker ↔ internal API authentication via mTLS, **so that** only enrolled workers enqueue or claim work.

**Acceptance criteria**

- **AC-DG-03-005-01:** When mTLS enabled, API verifies client cert chain and maps certificate to `tenant_id` / service identity (Architecture §28.2).
- **AC-DG-03-005-02:** mTLS identities cannot impersonate human JWT roles unless explicitly granted service role.
- **AC-DG-03-005-03:** Misconfigured cert returns `403` without leaking tenant existence.

---

### AC test specifications (US-DG-03-005)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-03-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-005` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | When mTLS enabled, API verifies client cert chain and maps certificate to `tenant_id` / service identity (Architecture §28.2). |
| **Objective** | Verify the behaviour described in AC-DG-03-005-01: When mTLS enabled, API verifies client cert chain and maps certificate to `tenant_id` / service identity (Architecture §28.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-03-005-01` |
| **Secondary / negative test ID** | `TC-DG-03-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-005-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §28.2 |

#### Test specification — AC-DG-03-005-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-005` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | mTLS identities cannot impersonate human JWT roles unless explicitly granted service role. |
| **Objective** | Verify the behaviour described in AC-DG-03-005-02: mTLS identities cannot impersonate human JWT roles unless explicitly granted service role. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-005-02` |
| **Secondary / negative test ID** | `TC-DG-03-005-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-005-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-005-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-005` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Misconfigured cert returns `403` without leaking tenant existence. |
| **Objective** | Verify the behaviour described in AC-DG-03-005-03: Misconfigured cert returns `403` without leaking tenant existence. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. \| 4. Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-005-03` |
| **Secondary / negative test ID** | `TC-DG-03-005-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-005-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-03-006 — Immutable audit log for security-relevant actions

**As an** auditor, **I want** append-only audit events for policy upload, resume, runtime flag change, **so that** investigations are trustworthy.

**Wireframe — audit trail (UI)**

```text
┌──────── Audit log ──────────────────────────────────────────┐
│ 10:22Z  admin@…  policy.upload  policy_id=acme-sdlc v3    │
│ 10:05Z  svc-ci     scan.create    scan_id=… idem=build-442  │
└─────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-03-006-01:** Events capture actor, action, target id, IP (if available), outcome (success/fail).
- **AC-DG-03-006-02:** Audit store is append-only from API perspective (no delete via public API).
- **AC-DG-03-006-03:** Retention period configurable per deployment (align §14.2).

---

### AC test specifications (US-DG-03-006)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-03-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-006` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Events capture actor, action, target id, IP (if available), outcome (success/fail). |
| **Objective** | Verify the behaviour described in AC-DG-03-006-01: Events capture actor, action, target id, IP (if available), outcome (success/fail). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-006-01` |
| **Secondary / negative test ID** | `TC-DG-03-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-006-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-006` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Audit store is append-only from API perspective (no delete via public API). |
| **Objective** | Verify the behaviour described in AC-DG-03-006-02: Audit store is append-only from API perspective (no delete via public API). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-006-02` |
| **Secondary / negative test ID** | `TC-DG-03-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-006-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-006-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-006` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Retention period configurable per deployment (align §14.2). |
| **Objective** | Verify the behaviour described in AC-DG-03-006-03: Retention period configurable per deployment (align §14.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-006-03` |
| **Secondary / negative test ID** | `TC-DG-03-006-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-006-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-03-007 — Role matrix documented and enforced in middleware

**As a** security architect, **I want** a single role→permission matrix, **so that** new routes do not ship without authz.

**Acceptance criteria**

- **AC-DG-03-007-01:** Matrix covers `POST /v1/scans`, `POST …/cancel`, `POST …/resume`, `POST /v1/policies:upload`, findings export (EPIC-DG-02).
- **AC-DG-03-007-02:** Missing role returns `403` with `error_code=FORBIDDEN`.
- **AC-DG-03-007-03:** Automated contract tests assert matrix for each route template.

---

### AC test specifications (US-DG-03-007)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-03-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-007` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Matrix covers `POST /v1/scans`, `POST …/cancel`, `POST …/resume`, `POST /v1/policies:upload`, findings export (EPIC-DG-02). |
| **Objective** | Verify the behaviour described in AC-DG-03-007-01: Matrix covers `POST /v1/scans`, `POST …/cancel`, `POST …/resume`, `POST /v1/policies:upload`, findings export (EPIC-DG-02). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-007-01` |
| **Secondary / negative test ID** | `TC-DG-03-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-007-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-007-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-007` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Missing role returns `403` with `error_code=FORBIDDEN`. |
| **Objective** | Verify the behaviour described in AC-DG-03-007-02: Missing role returns `403` with `error_code=FORBIDDEN`. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. \| 4. Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-007-02` |
| **Secondary / negative test ID** | `TC-DG-03-007-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-007-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-007-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-007` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Automated contract tests assert matrix for each route template. |
| **Objective** | Verify the behaviour described in AC-DG-03-007-03: Automated contract tests assert matrix for each route template. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-007-03` |
| **Secondary / negative test ID** | `TC-DG-03-007-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-007-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-03-008 — Tenant lifecycle (create, suspend, delete)

**As a** SaaS operator, **I want** to suspend a tenant, **so that** billing abuse or legal hold stops new scans immediately.

**Acceptance criteria**

- **AC-DG-03-008-01:** Suspended tenant receives `403` on mutating endpoints; read access policy documented (e.g. allow auditors read-only).
- **AC-DG-03-008-02:** In-flight scans behaviour on suspend: cooperative cancel or run-to-completion (document single chosen behaviour).
- **AC-DG-03-008-03:** Delete tenant is soft-delete with retention schedule or hard-delete behind break-glass (document).

---

### AC test specifications (US-DG-03-008)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-03-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-008` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Suspended tenant receives `403` on mutating endpoints; read access policy documented (e.g. allow auditors read-only). |
| **Objective** | Verify the behaviour described in AC-DG-03-008-01: Suspended tenant receives `403` on mutating endpoints; read access policy documented (e.g. allow auditors read-only). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. \| 4. Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-008-01` |
| **Secondary / negative test ID** | `TC-DG-03-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-008-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-008` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | In-flight scans behaviour on suspend: cooperative cancel or run-to-completion (document single chosen behaviour). |
| **Objective** | Verify the behaviour described in AC-DG-03-008-02: In-flight scans behaviour on suspend: cooperative cancel or run-to-completion (document single chosen behaviour). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-008-02` |
| **Secondary / negative test ID** | `TC-DG-03-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-008-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-008-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-008` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Delete tenant is soft-delete with retention schedule or hard-delete behind break-glass (document). |
| **Objective** | Verify the behaviour described in AC-DG-03-008-03: Delete tenant is soft-delete with retention schedule or hard-delete behind break-glass (document). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-008-03` |
| **Secondary / negative test ID** | `TC-DG-03-008-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-008-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-03-009 — OIDC refresh and session binding for console

**As a** end user, **I want** short access token + refresh via IdP, **so that** stolen tokens expire quickly.

**Acceptance criteria**

- **AC-DG-03-009-01:** Console uses PKCE for SPA OAuth where applicable; no long-lived API keys in browser storage by default.
- **AC-DG-03-009-02:** Logout clears client session and invalidates refresh if server-side session store used.
- **AC-DG-03-009-03:** CORS rules restrict console origin per tenant deployment config.

---

### AC test specifications (US-DG-03-009)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-03-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-009` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Console uses PKCE for SPA OAuth where applicable; no long-lived API keys in browser storage by default. |
| **Objective** | Verify the behaviour described in AC-DG-03-009-01: Console uses PKCE for SPA OAuth where applicable; no long-lived API keys in browser storage by default. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-009-01` |
| **Secondary / negative test ID** | `TC-DG-03-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-009-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-009` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Logout clears client session and invalidates refresh if server-side session store used. |
| **Objective** | Verify the behaviour described in AC-DG-03-009-02: Logout clears client session and invalidates refresh if server-side session store used. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. \| 4. Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-009-02` |
| **Secondary / negative test ID** | `TC-DG-03-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-009-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-009-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-009` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | CORS rules restrict console origin per tenant deployment config. |
| **Objective** | Verify the behaviour described in AC-DG-03-009-03: CORS rules restrict console origin per tenant deployment config. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-009-03` |
| **Secondary / negative test ID** | `TC-DG-03-009-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-009-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-03-010 — Service accounts for CI with scoped tokens

**As a** DevOps lead, **I want** CI-scoped tokens limited to `scanner` on one tenant, **so that** pipeline leaks are blast-radius limited.

**Acceptance criteria**

- **AC-DG-03-010-01:** Service account creation requires `admin`; token lists show prefix + created_at only (never full secret twice).
- **AC-DG-03-010-02:** Token revocation is immediate for new requests; in-flight scan policy documented.
- **AC-DG-03-010-03:** Tokens are hashed at rest; compare using constant-time compare.

### AC test specifications (US-DG-03-010)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-03-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-010` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Service account creation requires `admin`; token lists show prefix + created_at only (never full secret twice). |
| **Objective** | Verify the behaviour described in AC-DG-03-010-01: Service account creation requires `admin`; token lists show prefix + created_at only (never full secret twice). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-010-01` |
| **Secondary / negative test ID** | `TC-DG-03-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-010-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-010` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Token revocation is immediate for new requests; in-flight scan policy documented. |
| **Objective** | Verify the behaviour described in AC-DG-03-010-02: Token revocation is immediate for new requests; in-flight scan policy documented. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-010-02` |
| **Secondary / negative test ID** | `TC-DG-03-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-010-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-03-010-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-03-010` |
| **Parent EPIC** | `EPIC-DG-03` |
| **Owning squad** | `identity-tenancy` |
| **Requirement (verbatim)** | Tokens are hashed at rest; compare using constant-time compare. |
| **Objective** | Verify the behaviour described in AC-DG-03-010-03: Tokens are hashed at rest; compare using constant-time compare. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-03. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-03-010-03` |
| **Secondary / negative test ID** | `TC-DG-03-010-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-03-010-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |
