> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-05-policy-tiresias.md`](../EPIC-05-policy-tiresias.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-05 — Policy catalogue & parsing (Tiresias)

> **AC-level test specifications (generated):** Squad copy [`squads/policy/EPIC-DG-05-detailed.md`](squads/policy/EPIC-DG-05-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py`.


**Goal:** Maintain installed compliance frameworks, parse uploaded policies into atomic controls, and version them for reproducible scans per `Architecture_Design.md` §16, §28.3.

**Primary personas:** Compliance lead, Tenant admin.

---


## US-DG-05-001 — List installed frameworks & versions

**As a** compliance lead, **I want** `GET /v1/policies`, **so that** I can pick valid `policy_ids` for scans.

**Wireframe — policy picker**

```text
┌──────── Policies ───────────────────────────┐
│ Search: [等保________]                      │
│  ISO-27001-2022    v2026-01-15   [info]    │
│  GB-T-22239-2019   v2025-11-01   [info]    │
│  SOC2-Type2        draft         [info]    │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-05-001-01:** Response lists `policy_id`, human title, `policy_version`, framework family (Architecture §28.3; registry §16.1).
- **AC-DG-05-001-02:** Deprecated policies flagged but still listable for historical scans.

---

### AC test specifications (US-DG-05-001)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-05-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-001` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Response lists `policy_id`, human title, `policy_version`, framework family (Architecture §28.3; registry §16.1). |
| **Objective** | Verify the behaviour described in AC-DG-05-001-01: Response lists `policy_id`, human title, `policy_version`, framework family (Architecture §28.3; registry §16.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-001-01` |
| **Secondary / negative test ID** | `TC-DG-05-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-001-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §28.3; registry §16.1 |

#### Test specification — AC-DG-05-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-001` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Deprecated policies flagged but still listable for historical scans. |
| **Objective** | Verify the behaviour described in AC-DG-05-001-02: Deprecated policies flagged but still listable for historical scans. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-001-02` |
| **Secondary / negative test ID** | `TC-DG-05-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-001-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-05-002 — Upload custom policy (admin)

**As a** tenant admin, **I want** `POST /v1/policies:upload` with PDF/YAML, **so that** internal security policies become testable controls.

**Wireframe — upload**

```text
┌──────── Upload policy ─────────────────────┐
│ File: [ Choose PDF/YAML ]                  │
│ Display name: [ACME Secure SDLC]          │
│                     [ Upload & parse ]      │
│ Progress: [=====>    ] Tiresias running     │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-05-002-01:** Multipart upload accepted only for `admin` role (Architecture §28.3).
- **AC-DG-05-002-02:** Successful parse returns `policy_id` + `policy_version` immutably stored.
- **AC-DG-05-002-03:** Parsed controls include `control_id`, `framework`, `scope_tags`, `layer_relevance`, `test_procedures` (Architecture §16.2).

---

### AC test specifications (US-DG-05-002)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-05-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-002` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Multipart upload accepted only for `admin` role (Architecture §28.3). |
| **Objective** | Verify the behaviour described in AC-DG-05-002-01: Multipart upload accepted only for `admin` role (Architecture §28.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-002-01` |
| **Secondary / negative test ID** | `TC-DG-05-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-002-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §28.3 |

#### Test specification — AC-DG-05-002-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-002` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Successful parse returns `policy_id` + `policy_version` immutably stored. |
| **Objective** | Verify the behaviour described in AC-DG-05-002-02: Successful parse returns `policy_id` + `policy_version` immutably stored. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-002-02` |
| **Secondary / negative test ID** | `TC-DG-05-002-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-002-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-05-002-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-002` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Parsed controls include `control_id`, `framework`, `scope_tags`, `layer_relevance`, `test_procedures` (Architecture §16.2). |
| **Objective** | Verify the behaviour described in AC-DG-05-002-03: Parsed controls include `control_id`, `framework`, `scope_tags`, `layer_relevance`, `test_procedures` (Architecture §16.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-002-03` |
| **Secondary / negative test ID** | `TC-DG-05-002-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-002-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §16.2 |


## US-DG-05-003 — Policy parse cache invalidation

**As a** platform engineer, **I want** cache entries invalidated on version bump, **so that** scans never reuse stale controls.

**Acceptance criteria**

- **AC-DG-05-003-01:** Redis policy parse cache key includes `policy_id` + `policy_version` TTL until version change (Architecture §9.4).
- **AC-DG-05-003-02:** Repo fingerprint / delta logic respects policy version changes (Architecture §23.1 Q7).

---

### AC test specifications (US-DG-05-003)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-05-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-003` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Redis policy parse cache key includes `policy_id` + `policy_version` TTL until version change (Architecture §9.4). |
| **Objective** | Verify the behaviour described in AC-DG-05-003-01: Redis policy parse cache key includes `policy_id` + `policy_version` TTL until version change (Architecture §9.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-003-01` |
| **Secondary / negative test ID** | `TC-DG-05-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-003-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §9.4 |

#### Test specification — AC-DG-05-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-003` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Repo fingerprint / delta logic respects policy version changes (Architecture §23.1 Q7). |
| **Objective** | Verify the behaviour described in AC-DG-05-003-02: Repo fingerprint / delta logic respects policy version changes (Architecture §23.1 Q7). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-003-02` |
| **Secondary / negative test ID** | `TC-DG-05-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-003-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §23.1 Q7 |


## US-DG-05-004 — Chinese framework fields

**As a** China-regulated customer, **I want** controls to carry Chinese titles where applicable, **so that** reports align to local assessor expectations.

**Acceptance criteria**

- **AC-DG-05-004-01:** For frameworks flagged as Chinese regulatory, `chinese_title` populated when source document provides it (Architecture §16.2; Business doc §15).

---

### AC test specifications (US-DG-05-004)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-05-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-004` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | For frameworks flagged as Chinese regulatory, `chinese_title` populated when source document provides it (Architecture §16.2; Business doc §15). |
| **Objective** | Verify the behaviour described in AC-DG-05-004-01: For frameworks flagged as Chinese regulatory, `chinese_title` populated when source document provides it (Architecture §16.2; Business doc §15). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-05-004-01` |
| **Secondary / negative test ID** | `TC-DG-05-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-004-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §16.2; Business doc §15 |


## US-DG-05-005 — Ingest structured JSON / YAML policy packs

**As a** compliance engineer, **I want** to upload versioned YAML/JSON control packs, **so that** parsing is deterministic without LLM for structure.

**Acceptance criteria**

- **AC-DG-05-005-01:** Schema validates control list: required fields match `PolicyControl` subset before Tiresias enrichment pass (Architecture §16.2).
- **AC-DG-05-005-02:** Invalid file returns field-level validation errors (EPIC-DG-02 problem JSON).
- **AC-DG-05-005-03:** Pack upload assigns monotonic `policy_version` string immutable after publish.

---

### AC test specifications (US-DG-05-005)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-05-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-005` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Schema validates control list: required fields match `PolicyControl` subset before Tiresias enrichment pass (Architecture §16.2). |
| **Objective** | Verify the behaviour described in AC-DG-05-005-01: Schema validates control list: required fields match `PolicyControl` subset before Tiresias enrichment pass (Architecture §16.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-005-01` |
| **Secondary / negative test ID** | `TC-DG-05-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-005-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §16.2 |

#### Test specification — AC-DG-05-005-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-005` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Invalid file returns field-level validation errors (EPIC-DG-02 problem JSON). |
| **Objective** | Verify the behaviour described in AC-DG-05-005-02: Invalid file returns field-level validation errors (EPIC-DG-02 problem JSON). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. \| 4. Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-005-02` |
| **Secondary / negative test ID** | `TC-DG-05-005-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-005-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-05-005-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-005` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Pack upload assigns monotonic `policy_version` string immutable after publish. |
| **Objective** | Verify the behaviour described in AC-DG-05-005-03: Pack upload assigns monotonic `policy_version` string immutable after publish. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-005-03` |
| **Secondary / negative test ID** | `TC-DG-05-005-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-005-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-05-006 — Tiresias LLM pass for unstructured PDF policies

**As a** customer, **I want** PDF policies split into atomic controls, **so that** scanning can map each clause.

**Acceptance criteria**

- **AC-DG-05-006-01:** PDF text extraction handles multi-column layouts where possible; OCR path documented for scanned PDFs (quality warning).
- **AC-DG-05-006-02:** Each extracted control gets `scope_tags` and `layer_relevance` inferred with confidence; low confidence flagged for human review list.
- **AC-DG-05-006-03:** Token usage for parse attributed to tenant cost (EPIC-DG-11).

---

### AC test specifications (US-DG-05-006)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-05-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-006` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | PDF text extraction handles multi-column layouts where possible; OCR path documented for scanned PDFs (quality warning). |
| **Objective** | Verify the behaviour described in AC-DG-05-006-01: PDF text extraction handles multi-column layouts where possible; OCR path documented for scanned PDFs (quality warning). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-006-01` |
| **Secondary / negative test ID** | `TC-DG-05-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-006-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-05-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-006` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Each extracted control gets `scope_tags` and `layer_relevance` inferred with confidence; low confidence flagged for human review list. |
| **Objective** | Verify the behaviour described in AC-DG-05-006-02: Each extracted control gets `scope_tags` and `layer_relevance` inferred with confidence; low confidence flagged for human review list. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-006-02` |
| **Secondary / negative test ID** | `TC-DG-05-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-006-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-05-006-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-006` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Token usage for parse attributed to tenant cost (EPIC-DG-11). |
| **Objective** | Verify the behaviour described in AC-DG-05-006-03: Token usage for parse attributed to tenant cost (EPIC-DG-11). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-006-03` |
| **Secondary / negative test ID** | `TC-DG-05-006-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-006-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-05-007 — Policy chunk embeddings for RAG

**As a** retrieval engineer, **I want** `policy_chunks` embedded per version, **so that** Argus/Athena retrieve relevant clauses.

**Acceptance criteria**

- **AC-DG-05-007-01:** After parse, batch embed policy chunks into `policy_chunks` with `policy_version` and `framework` (Architecture §12.1–12.2).
- **AC-DG-05-007-02:** Re-embedding skipped when version unchanged and `force_reindex=false`.
- **AC-DG-05-007-03:** Embedding model id stored on policy version metadata for reproducibility (EPIC-DG-10).

---

### AC test specifications (US-DG-05-007)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-05-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-007` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | After parse, batch embed policy chunks into `policy_chunks` with `policy_version` and `framework` (Architecture §12.1–12.2). |
| **Objective** | Verify the behaviour described in AC-DG-05-007-01: After parse, batch embed policy chunks into `policy_chunks` with `policy_version` and `framework` (Architecture §12.1–12.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-007-01` |
| **Secondary / negative test ID** | `TC-DG-05-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-007-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §12.1–12.2 |

#### Test specification — AC-DG-05-007-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-007` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Re-embedding skipped when version unchanged and `force_reindex=false`. |
| **Objective** | Verify the behaviour described in AC-DG-05-007-02: Re-embedding skipped when version unchanged and `force_reindex=false`. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-05-007-02` |
| **Secondary / negative test ID** | `TC-DG-05-007-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-007-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-05-007-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-007` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Embedding model id stored on policy version metadata for reproducibility (EPIC-DG-10). |
| **Objective** | Verify the behaviour described in AC-DG-05-007-03: Embedding model id stored on policy version metadata for reproducibility (EPIC-DG-10). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-007-03` |
| **Secondary / negative test ID** | `TC-DG-05-007-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-007-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-05-008 — Framework registry extensibility

**As a** product manager, **I want** new framework codes registered without forked binaries, **so that** ISO 42001 / GenAI packs ship as data.

**Acceptance criteria**

- **AC-DG-05-008-01:** `COMPLIANCE_FRAMEWORKS` loader reads from DB or packaged YAML list; adding row enables `policy_ids` selection (Architecture §16.1).
- **AC-DG-05-008-02:** Unknown `policy_id` on `CreateScanRequest` rejected at validation with list of valid ids.
- **AC-DG-05-008-03:** Framework metadata includes jurisdiction tags (`EU`, `CN`, `SG`) for UI filtering (Business doc §15).

---

### AC test specifications (US-DG-05-008)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-05-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-008` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | `COMPLIANCE_FRAMEWORKS` loader reads from DB or packaged YAML list; adding row enables `policy_ids` selection (Architecture §16.1). |
| **Objective** | Verify the behaviour described in AC-DG-05-008-01: `COMPLIANCE_FRAMEWORKS` loader reads from DB or packaged YAML list; adding row enables `policy_ids` selection (Architecture §16.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-008-01` |
| **Secondary / negative test ID** | `TC-DG-05-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-008-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §16.1 |

#### Test specification — AC-DG-05-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-008` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Unknown `policy_id` on `CreateScanRequest` rejected at validation with list of valid ids. |
| **Objective** | Verify the behaviour described in AC-DG-05-008-02: Unknown `policy_id` on `CreateScanRequest` rejected at validation with list of valid ids. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. \| 4. Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-008-02` |
| **Secondary / negative test ID** | `TC-DG-05-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-008-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-05-008-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-008` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Framework metadata includes jurisdiction tags (`EU`, `CN`, `SG`) for UI filtering (Business doc §15). |
| **Objective** | Verify the behaviour described in AC-DG-05-008-03: Framework metadata includes jurisdiction tags (`EU`, `CN`, `SG`) for UI filtering (Business doc §15). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-008-03` |
| **Secondary / negative test ID** | `TC-DG-05-008-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-008-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-05-009 — Policy diff between versions

**As a** compliance lead, **I want** API or UI to diff control sets between `policy_version` A and B, **so that** I understand scan impact.

**Acceptance criteria**

- **AC-DG-05-009-01:** `GET /v1/policies/{policy_id}/diff?from=&to=` returns added/removed/changed `control_id` list.
- **AC-DG-05-009-02:** Changed text highlights truncated to safe size; full text via signed URL if needed.
- **AC-DG-05-009-03:** Diff accessible to `admin` and `auditor`; not to unauthenticated callers.

---

### AC test specifications (US-DG-05-009)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-05-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-009` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | `GET /v1/policies/{policy_id}/diff?from=&to=` returns added/removed/changed `control_id` list. |
| **Objective** | Verify the behaviour described in AC-DG-05-009-01: `GET /v1/policies/{policy_id}/diff?from=&to=` returns added/removed/changed `control_id` list. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-009-01` |
| **Secondary / negative test ID** | `TC-DG-05-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-009-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-05-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-009` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Changed text highlights truncated to safe size; full text via signed URL if needed. |
| **Objective** | Verify the behaviour described in AC-DG-05-009-02: Changed text highlights truncated to safe size; full text via signed URL if needed. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-009-02` |
| **Secondary / negative test ID** | `TC-DG-05-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-009-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-05-009-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-009` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Diff accessible to `admin` and `auditor`; not to unauthenticated callers. |
| **Objective** | Verify the behaviour described in AC-DG-05-009-03: Diff accessible to `admin` and `auditor`; not to unauthenticated callers. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-009-03` |
| **Secondary / negative test ID** | `TC-DG-05-009-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-009-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-05-010 — Control test procedures exposed to Athena prompts

**As a** false-positive owner, **I want** `test_procedures` on each control, **so that** generator prompts look for concrete evidence types.

**Acceptance criteria**

- **AC-DG-05-010-01:** `PolicyControl.test_procedures` non-empty for catalog controls ≥90% (NFR target; document exceptions).
- **AC-DG-05-010-02:** Athena batching clusters by `scope_tags` using procedures hash in metadata (Architecture §31.3).
- **AC-DG-05-010-03:** Missing procedures downgrade control to “manual review recommended” banner in report (EPIC-DG-10).

### AC test specifications (US-DG-05-010)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-05-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-010` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | `PolicyControl.test_procedures` non-empty for catalog controls ≥90% (NFR target; document exceptions). |
| **Objective** | Verify the behaviour described in AC-DG-05-010-01: `PolicyControl.test_procedures` non-empty for catalog controls ≥90% (NFR target; document exceptions). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-010-01` |
| **Secondary / negative test ID** | `TC-DG-05-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-010-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-05-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-010` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Athena batching clusters by `scope_tags` using procedures hash in metadata (Architecture §31.3). |
| **Objective** | Verify the behaviour described in AC-DG-05-010-02: Athena batching clusters by `scope_tags` using procedures hash in metadata (Architecture §31.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-010-02` |
| **Secondary / negative test ID** | `TC-DG-05-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-010-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §31.3 |

#### Test specification — AC-DG-05-010-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-05-010` |
| **Parent EPIC** | `EPIC-DG-05` |
| **Owning squad** | `policy` |
| **Requirement (verbatim)** | Missing procedures downgrade control to “manual review recommended” banner in report (EPIC-DG-10). |
| **Objective** | Verify the behaviour described in AC-DG-05-010-03: Missing procedures downgrade control to “manual review recommended” banner in report (EPIC-DG-10). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-05. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-05-010-03` |
| **Secondary / negative test ID** | `TC-DG-05-010-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-05-010-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |
