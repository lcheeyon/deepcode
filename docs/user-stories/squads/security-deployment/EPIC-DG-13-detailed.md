> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-13-security-deployment-modes.md`](../EPIC-13-security-deployment-modes.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-13 — Security, secrets & deployment topologies

> **AC-level test specifications (generated):** Squad copy [`squads/security-deployment/EPIC-DG-13-detailed.md`](squads/security-deployment/EPIC-DG-13-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py`.


**Goal:** Satisfy data-sovereignty, air-gap, caching safety, and LLM routing policies per `Architecture_Design.md` §2.3, §13, §20–§22, §27 and Chinese market requirements (`玄武合规引擎_商业计划书.md`).

**Primary personas:** CISO, SecOps, Field engineer.

---


## US-DG-13-001 — No code egress by default (VPC / private)

**As a** CISO, **I want** architectural guarantee that source fragments are not sent to external LLM APIs unless explicitly allowed, **so that** data residency contracts hold.

**Wireframe — deployment mode selector (install wizard)**

```text
┌──────── Deployment mode ────────────────────────────────────┐
│ (x) Private VPC — LLM endpoint inside VPC                   │
│ ( ) SaaS tier — allowlisted external models (contract add.) │
│ ( ) Air-gapped — local Ollama / vLLM only                  │
│                                                             │
│ Note: Code prompts never leave boundary in VPC/air-gap.     │
└─────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-13-001-01:** Default configuration blocks remote LLM calls when `deployment=private_cloud|air_gapped` (Architecture §2.3, §13.2).
- **AC-DG-13-001-02:** Opt-in SaaS LLM tier requires explicit tenant contract flag recorded in audit log (product requirement; implementation-specific storage).

---

### AC test specifications (US-DG-13-001)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-13-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-001` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Default configuration blocks remote LLM calls when `deployment=private_cloud\|air_gapped` (Architecture §2.3, §13.2). |
| **Objective** | Verify the behaviour described in AC-DG-13-001-01: Default configuration blocks remote LLM calls when `deployment=private_cloud\|air_gapped` (Architecture §2.3, §13.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-13-001-01` |
| **Secondary / negative test ID** | `TC-DG-13-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-001-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §2.3, §13.2 |

#### Test specification — AC-DG-13-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-001` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Opt-in SaaS LLM tier requires explicit tenant contract flag recorded in audit log (product requirement; implementation-specific storage). |
| **Objective** | Verify the behaviour described in AC-DG-13-001-02: Opt-in SaaS LLM tier requires explicit tenant contract flag recorded in audit log (product requirement; implementation-specific storage). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-001-02` |
| **Secondary / negative test ID** | `TC-DG-13-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-001-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-13-002 — Calypso secret resolution

**As a** SecOps engineer, **I want** secrets pulled from Vault/KMS/SM at runtime, **so that** long-lived keys are not in env files.

**Acceptance criteria**

- **AC-DG-13-002-01:** `CALYPSO_BACKEND` supports documented backends; short TTL tokens only (Architecture §20.1, §27.3).
- **AC-DG-13-002-02:** Secrets never written to `ScanState` or reasoning traces (Architecture §20.1, §20.3).

---

### AC test specifications (US-DG-13-002)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-13-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-002` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | `CALYPSO_BACKEND` supports documented backends; short TTL tokens only (Architecture §20.1, §27.3). |
| **Objective** | Verify the behaviour described in AC-DG-13-002-01: `CALYPSO_BACKEND` supports documented backends; short TTL tokens only (Architecture §20.1, §27.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-002-01` |
| **Secondary / negative test ID** | `TC-DG-13-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-002-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §20.1, §27.3 |

#### Test specification — AC-DG-13-002-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-002` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Secrets never written to `ScanState` or reasoning traces (Architecture §20.1, §20.3). |
| **Objective** | Verify the behaviour described in AC-DG-13-002-02: Secrets never written to `ScanState` or reasoning traces (Architecture §20.1, §20.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-002-02` |
| **Secondary / negative test ID** | `TC-DG-13-002-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-002-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §20.1, §20.3 |


## US-DG-13-003 — LLM router with fallbacks

**As a** platform engineer, **I want** provider fallback chain on rate limits, **so that** scans complete resiliently.

**Acceptance criteria**

- **AC-DG-13-003-01:** Router obeys task-to-model matrix defaults (Architecture §13.1–13.3).
- **AC-DG-13-003-02:** Circuit breaker opens after threshold failures and switches provider (Architecture §19.2).

---

### AC test specifications (US-DG-13-003)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-13-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-003` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Router obeys task-to-model matrix defaults (Architecture §13.1–13.3). |
| **Objective** | Verify the behaviour described in AC-DG-13-003-01: Router obeys task-to-model matrix defaults (Architecture §13.1–13.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-003-01` |
| **Secondary / negative test ID** | `TC-DG-13-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-003-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §13.1–13.3 |

#### Test specification — AC-DG-13-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-003` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Circuit breaker opens after threshold failures and switches provider (Architecture §19.2). |
| **Objective** | Verify the behaviour described in AC-DG-13-003-02: Circuit breaker opens after threshold failures and switches provider (Architecture §19.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-003-02` |
| **Secondary / negative test ID** | `TC-DG-13-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-003-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §19.2 |


## US-DG-13-004 — Semantic cache safety threshold

**As a** ML owner, **I want** conservative semantic cache similarity, **so that** dissimilar controls never share answers.

**Acceptance criteria**

- **AC-DG-13-004-01:** Default threshold `0.97` with tenant-configurable range `0.95–0.99` for admins only (Architecture §9.2, §24.1–24.2).
- **AC-DG-13-004-02:** Cache invalidates on prompt template version change (Architecture §9.4).

---

### AC test specifications (US-DG-13-004)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-13-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-004` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Default threshold `0.97` with tenant-configurable range `0.95–0.99` for admins only (Architecture §9.2, §24.1–24.2). |
| **Objective** | Verify the behaviour described in AC-DG-13-004-01: Default threshold `0.97` with tenant-configurable range `0.95–0.99` for admins only (Architecture §9.2, §24.1–24.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-004-01` |
| **Secondary / negative test ID** | `TC-DG-13-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-004-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §9.2, §24.1–24.2 |

#### Test specification — AC-DG-13-004-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-004` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Cache invalidates on prompt template version change (Architecture §9.4). |
| **Objective** | Verify the behaviour described in AC-DG-13-004-02: Cache invalidates on prompt template version change (Architecture §9.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. \| 4. Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-004-02` |
| **Secondary / negative test ID** | `TC-DG-13-004-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-004-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §9.4 |


## US-DG-13-005 — Xinchuang / 信创 deployment profile

**As a** government customer, **I want** domestic containers, SM crypto, and local models, **so that**目录认定路径可行.

**Acceptance criteria**

- **AC-DG-13-005-01:** Air-gap profile disables LangSmith; mandates self-hosted LangFuse (Architecture §22.2, §8.1).
- **AC-DG-13-005-02:** Huawei deployment documents SM2/SM3/SM4 where applicable (Business doc §13.3, §17 Phase 3).
- **AC-DG-13-005-03:** Image pull sources restricted to domestic registries when `deployment=xinchuang` (Architecture §22.2).

---

### AC test specifications (US-DG-13-005)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-13-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-005` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Air-gap profile disables LangSmith; mandates self-hosted LangFuse (Architecture §22.2, §8.1). |
| **Objective** | Verify the behaviour described in AC-DG-13-005-01: Air-gap profile disables LangSmith; mandates self-hosted LangFuse (Architecture §22.2, §8.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-005-01` |
| **Secondary / negative test ID** | `TC-DG-13-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-005-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §22.2, §8.1 |

#### Test specification — AC-DG-13-005-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-005` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Huawei deployment documents SM2/SM3/SM4 where applicable (Business doc §13.3, §17 Phase 3). |
| **Objective** | Verify the behaviour described in AC-DG-13-005-02: Huawei deployment documents SM2/SM3/SM4 where applicable (Business doc §13.3, §17 Phase 3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-005-02` |
| **Secondary / negative test ID** | `TC-DG-13-005-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-005-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-13-005-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-005` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Image pull sources restricted to domestic registries when `deployment=xinchuang` (Architecture §22.2). |
| **Objective** | Verify the behaviour described in AC-DG-13-005-03: Image pull sources restricted to domestic registries when `deployment=xinchuang` (Architecture §22.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-13-005-03` |
| **Secondary / negative test ID** | `TC-DG-13-005-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-005-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §22.2 |


## US-DG-13-006 — Tool sandbox filesystem boundary

**As a** security reviewer, **I want** `safe_read` chrooted to staged repo root, **so that** tools cannot read `/etc/passwd`.

**Acceptance criteria**

- **AC-DG-13-006-01:** Path traversal attempts raise `ToolExecutionError` without crashing graph (Architecture §6.5, §20.2).
- **AC-DG-13-006-02:** `TOOL_SANDBOX_ROOT` enforced for all tool I/O (Architecture §27.2).

---

### AC test specifications (US-DG-13-006)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-13-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-006` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Path traversal attempts raise `ToolExecutionError` without crashing graph (Architecture §6.5, §20.2). |
| **Objective** | Verify the behaviour described in AC-DG-13-006-01: Path traversal attempts raise `ToolExecutionError` without crashing graph (Architecture §6.5, §20.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-006-01` |
| **Secondary / negative test ID** | `TC-DG-13-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-006-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §6.5, §20.2 |

#### Test specification — AC-DG-13-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-006` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | `TOOL_SANDBOX_ROOT` enforced for all tool I/O (Architecture §27.2). |
| **Objective** | Verify the behaviour described in AC-DG-13-006-02: `TOOL_SANDBOX_ROOT` enforced for all tool I/O (Architecture §27.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-006-02` |
| **Secondary / negative test ID** | `TC-DG-13-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-006-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §27.2 |


## US-DG-13-007 — Repo fingerprint L1 cache (skip full rescan)

**As a** cost owner, **I want** optional full-result skip when repo+policy unchanged, **so that** CI noise drops (Architecture §9.1 L1).

**Acceptance criteria**

- **AC-DG-13-007-01:** Cache key `sha256(repo_url + commit_sha + policy_version)` documented; value is prior `ScanResult` reference or artifact pointer.
- **AC-DG-13-007-02:** Skip path still writes new `scan_id` row with `status=COMPLETE` and link to prior result OR returns same id per product decision (document one).
- **AC-DG-13-007-03:** Skip disabled when any `scan_layers` differ from cached run.

---

### AC test specifications (US-DG-13-007)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-13-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-007` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Cache key `sha256(repo_url + commit_sha + policy_version)` documented; value is prior `ScanResult` reference or artifact pointer. |
| **Objective** | Verify the behaviour described in AC-DG-13-007-01: Cache key `sha256(repo_url + commit_sha + policy_version)` documented; value is prior `ScanResult` reference or artifact pointer. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-007-01` |
| **Secondary / negative test ID** | `TC-DG-13-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-007-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-13-007-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-007` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Skip path still writes new `scan_id` row with `status=COMPLETE` and link to prior result OR returns same id per product decision (document one). |
| **Objective** | Verify the behaviour described in AC-DG-13-007-02: Skip path still writes new `scan_id` row with `status=COMPLETE` and link to prior result OR returns same id per product decision (document one). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-007-02` |
| **Secondary / negative test ID** | `TC-DG-13-007-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-007-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-13-007-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-007` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Skip disabled when any `scan_layers` differ from cached run. |
| **Objective** | Verify the behaviour described in AC-DG-13-007-03: Skip disabled when any `scan_layers` differ from cached run. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-13-007-03` |
| **Secondary / negative test ID** | `TC-DG-13-007-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-007-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-13-008 — L3 tool output cache correctness

**As a** security reviewer, **I want** tool cache invalidated on tool version bump, **so that** parser fixes apply immediately (Architecture §9.4).

**Acceptance criteria**

- **AC-DG-13-008-01:** Tool cache key includes `tool_impl_version` semver from package build.
- **AC-DG-13-008-02:** Toggle to disable L3 per tenant for debugging (runtime_config).
- **AC-DG-13-008-03:** Cache poisoning tests ensure different args never return wrong value.

---

### AC test specifications (US-DG-13-008)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-13-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-008` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Tool cache key includes `tool_impl_version` semver from package build. |
| **Objective** | Verify the behaviour described in AC-DG-13-008-01: Tool cache key includes `tool_impl_version` semver from package build. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-008-01` |
| **Secondary / negative test ID** | `TC-DG-13-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-008-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-13-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-008` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Toggle to disable L3 per tenant for debugging (runtime_config). |
| **Objective** | Verify the behaviour described in AC-DG-13-008-02: Toggle to disable L3 per tenant for debugging (runtime_config). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-008-02` |
| **Secondary / negative test ID** | `TC-DG-13-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-008-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-13-008-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-008` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Cache poisoning tests ensure different args never return wrong value. |
| **Objective** | Verify the behaviour described in AC-DG-13-008-03: Cache poisoning tests ensure different args never return wrong value. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-008-03` |
| **Secondary / negative test ID** | `TC-DG-13-008-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-008-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-13-009 — FIPS / compliance-hardened container image profile

**As a** US public sector customer, **I want** optional FIPS-enabled base image flag, **so that** crypto modules meet policy (Business doc Phase 6; Architecture §22).

**Acceptance criteria**

- **AC-DG-13-009-01:** Build flavour `fips` documented in Dockerfile/Helm values; uses approved OpenSSL provider where applicable.
- **AC-DG-13-009-02:** Non-FIPS and FIPS images not mixed in same StatefulSet without node labels (k8s constraint doc).
- **AC-DG-13-009-03:** Automated check fails if FIPS image links non-FIPS sidecar (optional).

---

### AC test specifications (US-DG-13-009)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-13-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-009` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Build flavour `fips` documented in Dockerfile/Helm values; uses approved OpenSSL provider where applicable. |
| **Objective** | Verify the behaviour described in AC-DG-13-009-01: Build flavour `fips` documented in Dockerfile/Helm values; uses approved OpenSSL provider where applicable. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-009-01` |
| **Secondary / negative test ID** | `TC-DG-13-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-009-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-13-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-009` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Non-FIPS and FIPS images not mixed in same StatefulSet without node labels (k8s constraint doc). |
| **Objective** | Verify the behaviour described in AC-DG-13-009-02: Non-FIPS and FIPS images not mixed in same StatefulSet without node labels (k8s constraint doc). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-009-02` |
| **Secondary / negative test ID** | `TC-DG-13-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-009-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-13-009-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-009` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Automated check fails if FIPS image links non-FIPS sidecar (optional). |
| **Objective** | Verify the behaviour described in AC-DG-13-009-03: Automated check fails if FIPS image links non-FIPS sidecar (optional). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-13-009-03` |
| **Secondary / negative test ID** | `TC-DG-13-009-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-009-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-13-010 — Network egress allowlist for workers

**As a** network admin, **I want** workers to reach only LLM, cloud APIs, and internal deps, **so that** data exfil paths are closed.

**Acceptance criteria**

- **AC-DG-13-010-01:** Documented egress list per deployment mode (SaaS vs VPC vs air-gap).
- **AC-DG-13-010-02:** Egress proxy support for `HTTPS_PROXY` with TLS MITM **disallowed** by default (document).
- **AC-DG-13-010-03:** Integration test with network policy denies unexpected destinations.

---

### AC test specifications (US-DG-13-010)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-13-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-010` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Documented egress list per deployment mode (SaaS vs VPC vs air-gap). |
| **Objective** | Verify the behaviour described in AC-DG-13-010-01: Documented egress list per deployment mode (SaaS vs VPC vs air-gap). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-010-01` |
| **Secondary / negative test ID** | `TC-DG-13-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-010-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-13-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-010` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Egress proxy support for `HTTPS_PROXY` with TLS MITM **disallowed** by default (document). |
| **Objective** | Verify the behaviour described in AC-DG-13-010-02: Egress proxy support for `HTTPS_PROXY` with TLS MITM **disallowed** by default (document). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-010-02` |
| **Secondary / negative test ID** | `TC-DG-13-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-010-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-13-010-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-010` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Integration test with network policy denies unexpected destinations. |
| **Objective** | Verify the behaviour described in AC-DG-13-010-03: Integration test with network policy denies unexpected destinations. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-010-03` |
| **Secondary / negative test ID** | `TC-DG-13-010-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-010-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-13-011 — Supply chain: signed images and SBOM

**As a** CISO, **I want** cosign-signed images and SBOM published per release, **so that** customer admission controllers can verify.

**Acceptance criteria**

- **AC-DG-13-011-01:** Release pipeline generates SPDX or CycloneDX SBOM for api/worker images.
- **AC-DG-13-011-02:** Signature verification steps documented for Helm install.
- **AC-DG-13-011-03:** Critical CVEs in SBOM gate release per policy table (optional CI gate).

### AC test specifications (US-DG-13-011)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-13-011-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-011` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Release pipeline generates SPDX or CycloneDX SBOM for api/worker images. |
| **Objective** | Verify the behaviour described in AC-DG-13-011-01: Release pipeline generates SPDX or CycloneDX SBOM for api/worker images. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-011-01` |
| **Secondary / negative test ID** | `TC-DG-13-011-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-011-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-13-011-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-011` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Signature verification steps documented for Helm install. |
| **Objective** | Verify the behaviour described in AC-DG-13-011-02: Signature verification steps documented for Helm install. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-13-011-02` |
| **Secondary / negative test ID** | `TC-DG-13-011-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-011-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-13-011-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-13-011` |
| **Parent EPIC** | `EPIC-DG-13` |
| **Owning squad** | `security-deployment` |
| **Requirement (verbatim)** | Critical CVEs in SBOM gate release per policy table (optional CI gate). |
| **Objective** | Verify the behaviour described in AC-DG-13-011-03: Critical CVEs in SBOM gate release per policy table (optional CI gate). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-13. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-13-011-03` |
| **Secondary / negative test ID** | `TC-DG-13-011-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-13-011-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |
