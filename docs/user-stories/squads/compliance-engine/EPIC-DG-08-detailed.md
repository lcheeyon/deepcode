> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-08-compliance-athena.md`](../EPIC-08-compliance-athena.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-08 — Compliance mapping & cross-layer reasoning (Athena)

> **AC-level test specifications (generated):** Squad copy [`squads/compliance-engine/EPIC-DG-08-detailed.md`](squads/compliance-engine/EPIC-DG-08-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py`.


**Goal:** Map controls to PASS/FAIL/PARTIAL/NA with evidence, run generator–critic reconciliation, emit cross-layer composite findings, and expose confidence for governance per `Architecture_Design.md` §3, §16, §18.

**Primary personas:** Compliance officer, Security architect.

---


## US-DG-08-001 — Per-control structured findings

**As a** compliance officer, **I want** each control mapped with severity and evidence refs, **so that** audits are traceable.

**Wireframe — control detail drawer**

```text
┌──────── Finding: ISO27001-A.10.1.1 ────────┐
│ Status: FAIL   Severity: HIGH              │
│ Confidence: 0.82                         │
│ Evidence:                                   │
│  • src/crypto/tls.ts:L42-L58               │
│  • iac/modules/s3/main.tf:L12             │
│ Reasoning summary: [expand/collapse]      │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-08-001-01:** Findings include `control_id`, `severity`, `evidence_refs`, `reasoning_summary`, `confidence_score`, `status` (Architecture §3.1, §29.1).
- **AC-DG-08-001-02:** Low confidence after max iterations marks `UNCERTAIN` + `should_escalate` behaviours per thresholds (Architecture §3.2).

---

### AC test specifications (US-DG-08-001)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-08-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-001` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Findings include `control_id`, `severity`, `evidence_refs`, `reasoning_summary`, `confidence_score`, `status` (Architecture §3.1, §29.1). |
| **Objective** | Verify the behaviour described in AC-DG-08-001-01: Findings include `control_id`, `severity`, `evidence_refs`, `reasoning_summary`, `confidence_score`, `status` (Architecture §3.1, §29.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-001-01` |
| **Secondary / negative test ID** | `TC-DG-08-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-001-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §3.1, §29.1 |

#### Test specification — AC-DG-08-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-001` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Low confidence after max iterations marks `UNCERTAIN` + `should_escalate` behaviours per thresholds (Architecture §3.2). |
| **Objective** | Verify the behaviour described in AC-DG-08-001-02: Low confidence after max iterations marks `UNCERTAIN` + `should_escalate` behaviours per thresholds (Architecture §3.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-001-02` |
| **Secondary / negative test ID** | `TC-DG-08-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-001-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §3.2 |


## US-DG-08-002 — Generator + critic reconciliation

**As a** false-positive champion, **I want** critic pass to challenge generator output, **so that** over-claiming FAIL is reduced.

**Acceptance criteria**

- **AC-DG-08-002-01:** Two-pass Athena emits separate trace spans `athena_generator_pass`, `athena_critic_pass` (Architecture §3.3, §23.1 Q5).
- **AC-DG-08-002-02:** Disagreements resolve to `UNCERTAIN` per reconcile rules (Architecture §3.3).

---

### AC test specifications (US-DG-08-002)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-08-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-002` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Two-pass Athena emits separate trace spans `athena_generator_pass`, `athena_critic_pass` (Architecture §3.3, §23.1 Q5). |
| **Objective** | Verify the behaviour described in AC-DG-08-002-01: Two-pass Athena emits separate trace spans `athena_generator_pass`, `athena_critic_pass` (Architecture §3.3, §23.1 Q5). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-002-01` |
| **Secondary / negative test ID** | `TC-DG-08-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-002-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §3.3, §23.1 Q5 |

#### Test specification — AC-DG-08-002-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-002` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Disagreements resolve to `UNCERTAIN` per reconcile rules (Architecture §3.3). |
| **Objective** | Verify the behaviour described in AC-DG-08-002-02: Disagreements resolve to `UNCERTAIN` per reconcile rules (Architecture §3.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-002-02` |
| **Secondary / negative test ID** | `TC-DG-08-002-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-002-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §3.3 |


## US-DG-08-003 — Cross-layer correlation findings

**As a** security architect, **I want** composite findings linking code + IaC + cloud, **so that** I see “policy on paper vs reality” gaps.

**Wireframe — correlation timeline**

```text
Code ────────● mis-use of presigned URL (Argus)
IaC  ────● bucket encryption ON (Laocoon)
Cloud ─● bucket policy s3:GetObject * (Cassandra)
        └─► Composite: HIGH — access path defeats encryption intent
```

**Acceptance criteria**

- **AC-DG-08-003-01:** `cross_layer_findings` list includes mapped frameworks + composite severity rationale (Architecture §3.4, §4.2).
- **AC-DG-08-003-02:** Executive report section highlights top cross-layer items (Architecture §18.1 item 7).

---

### AC test specifications (US-DG-08-003)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-08-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-003` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | `cross_layer_findings` list includes mapped frameworks + composite severity rationale (Architecture §3.4, §4.2). |
| **Objective** | Verify the behaviour described in AC-DG-08-003-01: `cross_layer_findings` list includes mapped frameworks + composite severity rationale (Architecture §3.4, §4.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-003-01` |
| **Secondary / negative test ID** | `TC-DG-08-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-003-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §3.4, §4.2 |

#### Test specification — AC-DG-08-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-003` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Executive report section highlights top cross-layer items (Architecture §18.1 item 7). |
| **Objective** | Verify the behaviour described in AC-DG-08-003-02: Executive report section highlights top cross-layer items (Architecture §18.1 item 7). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-003-02` |
| **Secondary / negative test ID** | `TC-DG-08-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-003-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §18.1 item 7 |


## US-DG-08-004 — Batched control processing (MVP)

**As a** performance owner, **I want** controls processed in semantic batches, **so that** P95 mapping stays within SLO.

**Acceptance criteria**

- **AC-DG-08-004-01:** Batch size target 8–12 controls with clustering on `scope_tags` + embedding similarity (Architecture §31.3).
- **AC-DG-08-004-02:** Feature flag `ATHENA_PER_CONTROL_SEND` defaults off (Architecture §23.1 Q1).

---

### AC test specifications (US-DG-08-004)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-08-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-004` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Batch size target 8–12 controls with clustering on `scope_tags` + embedding similarity (Architecture §31.3). |
| **Objective** | Verify the behaviour described in AC-DG-08-004-01: Batch size target 8–12 controls with clustering on `scope_tags` + embedding similarity (Architecture §31.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-004-01` |
| **Secondary / negative test ID** | `TC-DG-08-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-004-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §31.3 |

#### Test specification — AC-DG-08-004-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-004` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Feature flag `ATHENA_PER_CONTROL_SEND` defaults off (Architecture §23.1 Q1). |
| **Objective** | Verify the behaviour described in AC-DG-08-004-02: Feature flag `ATHENA_PER_CONTROL_SEND` defaults off (Architecture §23.1 Q1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-004-02` |
| **Secondary / negative test ID** | `TC-DG-08-004-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-004-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §23.1 Q1 |


## US-DG-08-005 — Prompt injection hardening in evidence path

**As a** security reviewer, **I want** evidence wrapped and structured outputs enforced, **so that** malicious repo content cannot hijack tools.

**Acceptance criteria**

- **AC-DG-08-005-01:** Evidence segments use boundary markers in prompts (Architecture §20.2).
- **AC-DG-08-005-02:** Outputs parsed strictly to Pydantic models; free-form discarded (Architecture §6.4, §20.2).

---

### AC test specifications (US-DG-08-005)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-08-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-005` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Evidence segments use boundary markers in prompts (Architecture §20.2). |
| **Objective** | Verify the behaviour described in AC-DG-08-005-01: Evidence segments use boundary markers in prompts (Architecture §20.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-005-01` |
| **Secondary / negative test ID** | `TC-DG-08-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-005-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §20.2 |

#### Test specification — AC-DG-08-005-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-005` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Outputs parsed strictly to Pydantic models; free-form discarded (Architecture §6.4, §20.2). |
| **Objective** | Verify the behaviour described in AC-DG-08-005-02: Outputs parsed strictly to Pydantic models; free-form discarded (Architecture §6.4, §20.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-005-02` |
| **Secondary / negative test ID** | `TC-DG-08-005-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-005-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §6.4, §20.2 |


## US-DG-08-006 — Compliance summary and per-framework scores

**As an** executive, **I want** `ComplianceSummary` with radar-friendly scores, **so that** board packs are one glance.

**Wireframe — score strip**

```text
┌──────── Compliance summary ────────────────────────────────┐
│ ISO 27001:  78%   等保三级: 64%   SOC2: 81%                 │
│ Cross-layer HIGH: 3   UNCERTAIN: 4   (review queue)         │
└──────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-08-006-01:** `compliance_summary` persisted with per-framework pass/fail/partial/NA counts (Architecture §4.2).
- **AC-DG-08-006-02:** Scoring weights honour `severity_weight` on controls (Architecture §16.2).
- **AC-DG-08-006-03:** UNCERTAIN ratio >30% triggers report banner + optional webhook (Architecture §8.4).

---

### AC test specifications (US-DG-08-006)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-08-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-006` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | `compliance_summary` persisted with per-framework pass/fail/partial/NA counts (Architecture §4.2). |
| **Objective** | Verify the behaviour described in AC-DG-08-006-01: `compliance_summary` persisted with per-framework pass/fail/partial/NA counts (Architecture §4.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-006-01` |
| **Secondary / negative test ID** | `TC-DG-08-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-006-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §4.2 |

#### Test specification — AC-DG-08-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-006` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Scoring weights honour `severity_weight` on controls (Architecture §16.2). |
| **Objective** | Verify the behaviour described in AC-DG-08-006-02: Scoring weights honour `severity_weight` on controls (Architecture §16.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-006-02` |
| **Secondary / negative test ID** | `TC-DG-08-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-006-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §16.2 |

#### Test specification — AC-DG-08-006-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-006` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | UNCERTAIN ratio >30% triggers report banner + optional webhook (Architecture §8.4). |
| **Objective** | Verify the behaviour described in AC-DG-08-006-03: UNCERTAIN ratio >30% triggers report banner + optional webhook (Architecture §8.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-08-006-03` |
| **Secondary / negative test ID** | `TC-DG-08-006-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-006-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §8.4 |


## US-DG-08-007 — Bilingual output for MAS / 等保 reports

**As a** regional customer, **I want** Chinese + English finding titles where configured, **so that** mixed audit teams can read reports.

**Acceptance criteria**

- **AC-DG-08-007-01:** `job_config.locale` or tenant default selects `zh`, `en`, `bilingual` modes (product schema).
- **AC-DG-08-007-02:** Bilingual mode renders primary + secondary column in finding tables (EPIC-DG-10).
- **AC-DG-08-007-03:** LLM routing prefers Qwen/DeepSeek for Chinese narrative when deployment requires (Architecture §13.1; Business doc §12).

---

### AC test specifications (US-DG-08-007)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-08-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-007` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | `job_config.locale` or tenant default selects `zh`, `en`, `bilingual` modes (product schema). |
| **Objective** | Verify the behaviour described in AC-DG-08-007-01: `job_config.locale` or tenant default selects `zh`, `en`, `bilingual` modes (product schema). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-007-01` |
| **Secondary / negative test ID** | `TC-DG-08-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-007-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-08-007-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-007` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Bilingual mode renders primary + secondary column in finding tables (EPIC-DG-10). |
| **Objective** | Verify the behaviour described in AC-DG-08-007-02: Bilingual mode renders primary + secondary column in finding tables (EPIC-DG-10). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-007-02` |
| **Secondary / negative test ID** | `TC-DG-08-007-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-007-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-08-007-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-007` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | LLM routing prefers Qwen/DeepSeek for Chinese narrative when deployment requires (Architecture §13.1; Business doc §12). |
| **Objective** | Verify the behaviour described in AC-DG-08-007-03: LLM routing prefers Qwen/DeepSeek for Chinese narrative when deployment requires (Architecture §13.1; Business doc §12). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-08-007-03` |
| **Secondary / negative test ID** | `TC-DG-08-007-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-007-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §13.1; Business doc §12 |


## US-DG-08-008 — MMR re-ranking for diverse code evidence

**As a** mapper engineer, **I want** MMR on Athena code retrieval, **so that** top-K chunks are not near-duplicates (Architecture §12.2).

**Acceptance criteria**

- **AC-DG-08-008-01:** Athena code path uses MMR with documented lambda; falls back to plain top-K if disabled by flag.
- **AC-DG-08-008-02:** Retrieved chunk ids logged in reasoning trace redacted excerpt metadata only (EPIC-DG-11).
- **AC-DG-08-008-03:** Deterministic tie-break on chunk id ordering when scores tie (`temperature=0` path).

---

### AC test specifications (US-DG-08-008)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-08-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-008` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Athena code path uses MMR with documented lambda; falls back to plain top-K if disabled by flag. |
| **Objective** | Verify the behaviour described in AC-DG-08-008-01: Athena code path uses MMR with documented lambda; falls back to plain top-K if disabled by flag. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-008-01` |
| **Secondary / negative test ID** | `TC-DG-08-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-008-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-08-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-008` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Retrieved chunk ids logged in reasoning trace redacted excerpt metadata only (EPIC-DG-11). |
| **Objective** | Verify the behaviour described in AC-DG-08-008-02: Retrieved chunk ids logged in reasoning trace redacted excerpt metadata only (EPIC-DG-11). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-008-02` |
| **Secondary / negative test ID** | `TC-DG-08-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-008-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-08-008-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-008` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Deterministic tie-break on chunk id ordering when scores tie (`temperature=0` path). |
| **Objective** | Verify the behaviour described in AC-DG-08-008-03: Deterministic tie-break on chunk id ordering when scores tie (`temperature=0` path). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-08-008-03` |
| **Secondary / negative test ID** | `TC-DG-08-008-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-008-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-08-009 — Batch failure isolation and retry

**As a** reliability engineer, **I want** one Athena batch failure not to lose prior batches’ findings, **so that** resume cost is bounded.

**Acceptance criteria**

- **AC-DG-08-009-01:** Failed batch increments `error_log` and can retry batch only without re-running completed batches (Architecture §31.3–31.4).
- **AC-DG-08-009-02:** After max batch retries, remaining controls marked `UNCERTAIN` with explicit reason code.
- **AC-DG-08-009-03:** Checkpoint state after each successful batch is durable (EPIC-DG-01).

---

### AC test specifications (US-DG-08-009)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-08-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-009` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Failed batch increments `error_log` and can retry batch only without re-running completed batches (Architecture §31.3–31.4). |
| **Objective** | Verify the behaviour described in AC-DG-08-009-01: Failed batch increments `error_log` and can retry batch only without re-running completed batches (Architecture §31.3–31.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-009-01` |
| **Secondary / negative test ID** | `TC-DG-08-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-009-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §31.3–31.4 |

#### Test specification — AC-DG-08-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-009` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | After max batch retries, remaining controls marked `UNCERTAIN` with explicit reason code. |
| **Objective** | Verify the behaviour described in AC-DG-08-009-02: After max batch retries, remaining controls marked `UNCERTAIN` with explicit reason code. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-009-02` |
| **Secondary / negative test ID** | `TC-DG-08-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-009-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-08-009-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-009` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Checkpoint state after each successful batch is durable (EPIC-DG-01). |
| **Objective** | Verify the behaviour described in AC-DG-08-009-03: Checkpoint state after each successful batch is durable (EPIC-DG-01). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-009-03` |
| **Secondary / negative test ID** | `TC-DG-08-009-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-009-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-08-010 — Control applicability (NA) with justification

**As an** auditor, **I want** explicit NA with reason, **so that** frameworks do not show false gaps.

**Acceptance criteria**

- **AC-DG-08-010-01:** NA requires `na_reason` enum + short text; empty NA rejected by schema.
- **AC-DG-08-010-02:** Layer relevance from `PolicyControl` respected — e.g. pure cloud control skips code-only evidence requirement (Architecture §16.2).
- **AC-DG-08-010-03:** NA rate anomalies (>40% in a framework) flagged for product review dataset (eval hook).

---

### AC test specifications (US-DG-08-010)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-08-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-010` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | NA requires `na_reason` enum + short text; empty NA rejected by schema. |
| **Objective** | Verify the behaviour described in AC-DG-08-010-01: NA requires `na_reason` enum + short text; empty NA rejected by schema. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. \| 4. Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-010-01` |
| **Secondary / negative test ID** | `TC-DG-08-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-010-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-08-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-010` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Layer relevance from `PolicyControl` respected — e.g. pure cloud control skips code-only evidence requirement (Architecture §16.2). |
| **Objective** | Verify the behaviour described in AC-DG-08-010-02: Layer relevance from `PolicyControl` respected — e.g. pure cloud control skips code-only evidence requirement (Architecture §16.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-010-02` |
| **Secondary / negative test ID** | `TC-DG-08-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-010-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §16.2 |

#### Test specification — AC-DG-08-010-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-010` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | NA rate anomalies (>40% in a framework) flagged for product review dataset (eval hook). |
| **Objective** | Verify the behaviour described in AC-DG-08-010-03: NA rate anomalies (>40% in a framework) flagged for product review dataset (eval hook). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-010-03` |
| **Secondary / negative test ID** | `TC-DG-08-010-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-010-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-08-011 — Evidence strength scoring in finding object

**As a** triage analyst, **I want** `evidence_strength` or equivalent, **so that** I sort by corroboration depth.

**Acceptance criteria**

- **AC-DG-08-011-01:** Finding schema includes machine-readable evidence grade (e.g. `direct_code_ref`, `config_only`, `heuristic`).
- **AC-DG-08-011-02:** Cross-layer findings require ≥2 layers’ evidence refs or downgrade severity (Architecture §3.4 spirit).
- **AC-DG-08-011-03:** UI and API expose same field (EPIC-DG-12).

---

### AC test specifications (US-DG-08-011)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-08-011-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-011` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Finding schema includes machine-readable evidence grade (e.g. `direct_code_ref`, `config_only`, `heuristic`). |
| **Objective** | Verify the behaviour described in AC-DG-08-011-01: Finding schema includes machine-readable evidence grade (e.g. `direct_code_ref`, `config_only`, `heuristic`). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-011-01` |
| **Secondary / negative test ID** | `TC-DG-08-011-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-011-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-08-011-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-011` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Cross-layer findings require ≥2 layers’ evidence refs or downgrade severity (Architecture §3.4 spirit). |
| **Objective** | Verify the behaviour described in AC-DG-08-011-02: Cross-layer findings require ≥2 layers’ evidence refs or downgrade severity (Architecture §3.4 spirit). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-011-02` |
| **Secondary / negative test ID** | `TC-DG-08-011-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-011-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §3.4 spirit |

#### Test specification — AC-DG-08-011-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-011` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | UI and API expose same field (EPIC-DG-12). |
| **Objective** | Verify the behaviour described in AC-DG-08-011-03: UI and API expose same field (EPIC-DG-12). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-011-03` |
| **Secondary / negative test ID** | `TC-DG-08-011-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-011-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-08-012 — Trace compaction before context overflow

**As a** graph engineer, **I want** trace compaction when token budget exceeded, **so that** `ContextLengthError` triggers recovery (Architecture §10.3–10.5, §19.1).

**Acceptance criteria**

- **AC-DG-08-012-01:** On `ContextLengthError`, compactor reduces prior steps per §10.3 and retries bounded times.
- **AC-DG-08-012-02:** Compaction events logged with before/after token counts (redacted trace).
- **AC-DG-08-012-03:** If still failing, control marked `UNCERTAIN` with `error_code=CONTEXT_LIMIT`.

### AC test specifications (US-DG-08-012)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-08-012-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-012` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | On `ContextLengthError`, compactor reduces prior steps per §10.3 and retries bounded times. |
| **Objective** | Verify the behaviour described in AC-DG-08-012-01: On `ContextLengthError`, compactor reduces prior steps per §10.3 and retries bounded times. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-012-01` |
| **Secondary / negative test ID** | `TC-DG-08-012-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-012-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-08-012-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-012` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | Compaction events logged with before/after token counts (redacted trace). |
| **Objective** | Verify the behaviour described in AC-DG-08-012-02: Compaction events logged with before/after token counts (redacted trace). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-012-02` |
| **Secondary / negative test ID** | `TC-DG-08-012-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-012-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-08-012-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-08-012` |
| **Parent EPIC** | `EPIC-DG-08` |
| **Owning squad** | `compliance-engine` |
| **Requirement (verbatim)** | If still failing, control marked `UNCERTAIN` with `error_code=CONTEXT_LIMIT`. |
| **Objective** | Verify the behaviour described in AC-DG-08-012-03: If still failing, control marked `UNCERTAIN` with `error_code=CONTEXT_LIMIT`. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-08. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-08-012-03` |
| **Secondary / negative test ID** | `TC-DG-08-012-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-08-012-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |
