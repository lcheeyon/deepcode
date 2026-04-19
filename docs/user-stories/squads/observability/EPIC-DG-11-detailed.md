> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-11-observability-cost-governance.md`](../EPIC-11-observability-cost-governance.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-11 — Observability, evaluation & cost governance

> **AC-level test specifications (generated):** Squad copy [`squads/observability/EPIC-DG-11-detailed.md`](squads/observability/EPIC-DG-11-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py`.


**Goal:** Dual observability (LangSmith + LangFuse), per-tenant cost accounting, alerting, and evaluation gates per `Architecture_Design.md` §7–§8, §21, §33.

**Primary personas:** ML engineer, FinOps, SRE.

---


## US-DG-11-001 — Dual-sink tracing with redaction policy

**As a** regulated customer, **I want** traces in self-hosted LangFuse with redacted payloads, **so that** SaaS tracing is optional.

**Wireframe — trace explorer (LangFuse)**

```text
┌──────── Session: scan_id 3fa2… ─────────────┐
│ Span: athena_generator_pass                 │
│ Tokens: in 12.4k / out 1.1k   Cost: $0.03   │
│ Raw LLM: [REDACTED]  Excerpt: [4KiB max]   │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-11-001-01:** Callback list includes LangFuse when enabled and LangSmith when enabled (Architecture §8.2).
- **AC-DG-11-001-02:** Raw LLM output persisted only in tenant PostgreSQL; external sinks capped to 4KiB excerpt (Architecture §23.1 Q9).
- **AC-DG-11-001-03:** `SECRET`-classified fields never exported to traces (Architecture §20.3).

---

### AC test specifications (US-DG-11-001)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-11-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-001` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Callback list includes LangFuse when enabled and LangSmith when enabled (Architecture §8.2). |
| **Objective** | Verify the behaviour described in AC-DG-11-001-01: Callback list includes LangFuse when enabled and LangSmith when enabled (Architecture §8.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-11-001-01` |
| **Secondary / negative test ID** | `TC-DG-11-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-001-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §8.2 |

#### Test specification — AC-DG-11-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-001` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Raw LLM output persisted only in tenant PostgreSQL; external sinks capped to 4KiB excerpt (Architecture §23.1 Q9). |
| **Objective** | Verify the behaviour described in AC-DG-11-001-02: Raw LLM output persisted only in tenant PostgreSQL; external sinks capped to 4KiB excerpt (Architecture §23.1 Q9). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-001-02` |
| **Secondary / negative test ID** | `TC-DG-11-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-001-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §23.1 Q9 |

#### Test specification — AC-DG-11-001-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-001` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | `SECRET`-classified fields never exported to traces (Architecture §20.3). |
| **Objective** | Verify the behaviour described in AC-DG-11-001-03: `SECRET`-classified fields never exported to traces (Architecture §20.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-001-03` |
| **Secondary / negative test ID** | `TC-DG-11-001-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-001-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §20.3 |


## US-DG-11-002 — Per-tenant daily cost ledger

**As a** FinOps analyst, **I want** SQL aggregations of token/cost by tenant/day, **so that** I can invoice SaaS usage.

**Acceptance criteria**

- **AC-DG-11-002-01:** LangFuse observations of type `GENERATION` feed documented aggregation query pattern (Architecture §8.3).
- **AC-DG-11-002-02:** Budget alert triggers when single scan exceeds threshold and can abort scan (Architecture §8.4; job `budget.max_llm_usd` §28.4).

---

### AC test specifications (US-DG-11-002)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-11-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-002` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | LangFuse observations of type `GENERATION` feed documented aggregation query pattern (Architecture §8.3). |
| **Objective** | Verify the behaviour described in AC-DG-11-002-01: LangFuse observations of type `GENERATION` feed documented aggregation query pattern (Architecture §8.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-002-01` |
| **Secondary / negative test ID** | `TC-DG-11-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-002-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §8.3 |

#### Test specification — AC-DG-11-002-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-002` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Budget alert triggers when single scan exceeds threshold and can abort scan (Architecture §8.4; job `budget.max_llm_usd` §28.4). |
| **Objective** | Verify the behaviour described in AC-DG-11-002-02: Budget alert triggers when single scan exceeds threshold and can abort scan (Architecture §8.4; job `budget.max_llm_usd` §28.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-11-002-02` |
| **Secondary / negative test ID** | `TC-DG-11-002-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-002-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §8.4; job `budget.max_llm_usd` §28.4 |


## US-DG-11-003 — Evaluation CI gate on false positives

**As an** ML engineer, **I want** CI to block prompt regressions on gold sets, **so that** mapping quality stays bounded.

**Acceptance criteria**

- **AC-DG-11-003-01:** `false-positive-registry` eval cannot regress >2% absolute vs baseline on `main` (Architecture §33.2).
- **AC-DG-11-003-02:** Datasets enumerated in §7.3 exist in `eval/datasets` with documented ownership.

---

### AC test specifications (US-DG-11-003)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-11-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-003` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | `false-positive-registry` eval cannot regress >2% absolute vs baseline on `main` (Architecture §33.2). |
| **Objective** | Verify the behaviour described in AC-DG-11-003-01: `false-positive-registry` eval cannot regress >2% absolute vs baseline on `main` (Architecture §33.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-003-01` |
| **Secondary / negative test ID** | `TC-DG-11-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-003-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §33.2 |

#### Test specification — AC-DG-11-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-003` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Datasets enumerated in §7.3 exist in `eval/datasets` with documented ownership. |
| **Objective** | Verify the behaviour described in AC-DG-11-003-02: Datasets enumerated in §7.3 exist in `eval/datasets` with documented ownership. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-003-02` |
| **Secondary / negative test ID** | `TC-DG-11-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-003-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-11-004 — Operational SLO dashboards

**As an** SRE, **I want** alerts for P95 latency and queue depth, **so that** we scale workers proactively.

**Acceptance criteria**

- **AC-DG-11-004-01:** P95 total scan <10 min for reference ≤500k LOC tracked as SLO (Architecture §21.1, §35.1).
- **AC-DG-11-004-02:** Queue depth >500 pending >15m raises alert (Architecture §35.2).

---

### AC test specifications (US-DG-11-004)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-11-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-004` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | P95 total scan <10 min for reference ≤500k LOC tracked as SLO (Architecture §21.1, §35.1). |
| **Objective** | Verify the behaviour described in AC-DG-11-004-01: P95 total scan <10 min for reference ≤500k LOC tracked as SLO (Architecture §21.1, §35.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-004-01` |
| **Secondary / negative test ID** | `TC-DG-11-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-004-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §21.1, §35.1 |

#### Test specification — AC-DG-11-004-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-004` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Queue depth >500 pending >15m raises alert (Architecture §35.2). |
| **Objective** | Verify the behaviour described in AC-DG-11-004-02: Queue depth >500 pending >15m raises alert (Architecture §35.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-004-02` |
| **Secondary / negative test ID** | `TC-DG-11-004-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-004-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §35.2 |


## US-DG-11-005 — OpenTelemetry traces for API and worker

**As a** SRE, **I want** OTel spans bridged to Grafana, **so that** I unify metrics with other services.

**Acceptance criteria**

- **AC-DG-11-005-01:** API emits spans for `POST /v1/scans`, DB queries as child spans where practical (Architecture §26.2, §35).
- **AC-DG-11-005-02:** Worker emits spans per LangGraph node name matching Architecture trace hierarchy §7.1.
- **AC-DG-11-005-03:** Trace context propagates `scan_id`, `tenant_id` attributes (non-secret).

---

### AC test specifications (US-DG-11-005)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-11-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-005` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | API emits spans for `POST /v1/scans`, DB queries as child spans where practical (Architecture §26.2, §35). |
| **Objective** | Verify the behaviour described in AC-DG-11-005-01: API emits spans for `POST /v1/scans`, DB queries as child spans where practical (Architecture §26.2, §35). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-005-01` |
| **Secondary / negative test ID** | `TC-DG-11-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-005-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §26.2, §35 |

#### Test specification — AC-DG-11-005-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-005` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Worker emits spans per LangGraph node name matching Architecture trace hierarchy §7.1. |
| **Objective** | Verify the behaviour described in AC-DG-11-005-02: Worker emits spans per LangGraph node name matching Architecture trace hierarchy §7.1. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-005-02` |
| **Secondary / negative test ID** | `TC-DG-11-005-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-005-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-11-005-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-005` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Trace context propagates `scan_id`, `tenant_id` attributes (non-secret). |
| **Objective** | Verify the behaviour described in AC-DG-11-005-03: Trace context propagates `scan_id`, `tenant_id` attributes (non-secret). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-005-03` |
| **Secondary / negative test ID** | `TC-DG-11-005-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-005-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-11-006 — LangSmith Hub prompt pull audit

**As an** ML engineer, **I want** every hub pull to log commit hash / version label, **so that** regressions correlate to prompt changes (Architecture §6.3).

**Acceptance criteria**

- **AC-DG-11-006-01:** Startup or first-use logs resolved prompt revision for `deepguard/athena-*` style keys.
- **AC-DG-11-006-02:** Offline mode uses bundled prompt pack with version file (EPIC-DG-13).
- **AC-DG-11-006-03:** Prompt change triggers cache invalidation per §9.4 semantic cache rules.

---

### AC test specifications (US-DG-11-006)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-11-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-006` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Startup or first-use logs resolved prompt revision for `deepguard/athena-*` style keys. |
| **Objective** | Verify the behaviour described in AC-DG-11-006-01: Startup or first-use logs resolved prompt revision for `deepguard/athena-*` style keys. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-006-01` |
| **Secondary / negative test ID** | `TC-DG-11-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-006-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-11-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-006` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Offline mode uses bundled prompt pack with version file (EPIC-DG-13). |
| **Objective** | Verify the behaviour described in AC-DG-11-006-02: Offline mode uses bundled prompt pack with version file (EPIC-DG-13). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-006-02` |
| **Secondary / negative test ID** | `TC-DG-11-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-006-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-11-006-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-006` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Prompt change triggers cache invalidation per §9.4 semantic cache rules. |
| **Objective** | Verify the behaviour described in AC-DG-11-006-03: Prompt change triggers cache invalidation per §9.4 semantic cache rules. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. \| 4. Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-006-03` |
| **Secondary / negative test ID** | `TC-DG-11-006-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-006-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-11-007 — Cache hit ratio metrics per layer

**As a** performance analyst, **I want** L1–L5 cache hit/miss counters, **so that** I tune TTLs.

**Acceptance criteria**

- **AC-DG-11-007-01:** Metrics exported: `cache_l1_hit_total`, `semantic_cache_hit_total`, etc. (names documented).
- **AC-DG-11-007-02:** Per-tenant labels on cost metrics but not on raw code content metrics (privacy).
- **AC-DG-11-007-03:** Dashboard template JSON checked into `infra/` or `docs/` (optional).

---

### AC test specifications (US-DG-11-007)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-11-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-007` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Metrics exported: `cache_l1_hit_total`, `semantic_cache_hit_total`, etc. (names documented). |
| **Objective** | Verify the behaviour described in AC-DG-11-007-01: Metrics exported: `cache_l1_hit_total`, `semantic_cache_hit_total`, etc. (names documented). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-007-01` |
| **Secondary / negative test ID** | `TC-DG-11-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-007-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-11-007-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-007` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Per-tenant labels on cost metrics but not on raw code content metrics (privacy). |
| **Objective** | Verify the behaviour described in AC-DG-11-007-02: Per-tenant labels on cost metrics but not on raw code content metrics (privacy). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-007-02` |
| **Secondary / negative test ID** | `TC-DG-11-007-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-007-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-11-007-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-007` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Dashboard template JSON checked into `infra/` or `docs/` (optional). |
| **Objective** | Verify the behaviour described in AC-DG-11-007-03: Dashboard template JSON checked into `infra/` or `docs/` (optional). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-11-007-03` |
| **Secondary / negative test ID** | `TC-DG-11-007-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-007-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-11-008 — Reasoning trace storage and retention job

**As a** compliance officer, **I want** `reasoning_traces` rows with encrypted `raw_llm_payload`, **so that** audits survive 7y policy where required (Architecture §29.1, §14.2).

**Acceptance criteria**

- **AC-DG-11-008-01:** Retention job deletes or archives traces per tenant policy default 1y with legal hold override.
- **AC-DG-11-008-02:** Encryption uses app-level AES-256 or pgcrypto as decided in ADR (Architecture §23.1 Q9).
- **AC-DG-11-008-03:** Export of raw traces requires `admin` + break-glass logging (EPIC-DG-03).

---

### AC test specifications (US-DG-11-008)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-11-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-008` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Retention job deletes or archives traces per tenant policy default 1y with legal hold override. |
| **Objective** | Verify the behaviour described in AC-DG-11-008-01: Retention job deletes or archives traces per tenant policy default 1y with legal hold override. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-008-01` |
| **Secondary / negative test ID** | `TC-DG-11-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-008-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-11-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-008` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Encryption uses app-level AES-256 or pgcrypto as decided in ADR (Architecture §23.1 Q9). |
| **Objective** | Verify the behaviour described in AC-DG-11-008-02: Encryption uses app-level AES-256 or pgcrypto as decided in ADR (Architecture §23.1 Q9). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-008-02` |
| **Secondary / negative test ID** | `TC-DG-11-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-008-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §23.1 Q9 |

#### Test specification — AC-DG-11-008-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-008` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Export of raw traces requires `admin` + break-glass logging (EPIC-DG-03). |
| **Objective** | Verify the behaviour described in AC-DG-11-008-03: Export of raw traces requires `admin` + break-glass logging (EPIC-DG-03). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-008-03` |
| **Secondary / negative test ID** | `TC-DG-11-008-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-008-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-11-009 — LangSmith vs LangFuse feature matrix in run config

**As a** deployer, **I want** explicit env toggles, **so that** air-gap never accidentally enables LangSmith (Architecture §8.1, §27.1).

**Acceptance criteria**

- **AC-DG-11-009-01:** When `LANGCHAIN_TRACING_V2=false`, no LangSmith network calls occur (verified by integration test with network deny).
- **AC-DG-11-009-02:** LangFuse host configurable; missing keys disable handler without error on startup.
- **AC-DG-11-009-03:** Dual-sink order documented if both enabled (Architecture §8.2).

---

### AC test specifications (US-DG-11-009)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-11-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-009` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | When `LANGCHAIN_TRACING_V2=false`, no LangSmith network calls occur (verified by integration test with network deny). |
| **Objective** | Verify the behaviour described in AC-DG-11-009-01: When `LANGCHAIN_TRACING_V2=false`, no LangSmith network calls occur (verified by integration test with network deny). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-11-009-01` |
| **Secondary / negative test ID** | `TC-DG-11-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-009-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-11-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-009` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | LangFuse host configurable; missing keys disable handler without error on startup. |
| **Objective** | Verify the behaviour described in AC-DG-11-009-02: LangFuse host configurable; missing keys disable handler without error on startup. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-009-02` |
| **Secondary / negative test ID** | `TC-DG-11-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-009-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-11-009-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-009` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Dual-sink order documented if both enabled (Architecture §8.2). |
| **Objective** | Verify the behaviour described in AC-DG-11-009-03: Dual-sink order documented if both enabled (Architecture §8.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-009-03` |
| **Secondary / negative test ID** | `TC-DG-11-009-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-009-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §8.2 |


## US-DG-11-010 — Agent retry rate alert

**As an** on-call engineer, **I want** alert when agent retry rate >20%, **so that** I catch bad prompts or provider outages (Architecture §8.4).

**Acceptance criteria**

- **AC-DG-11-010-01:** Retry rate computed per scan and aggregated per tenant hourly.
- **AC-DG-11-010-02:** Alert includes top contributing `agent_id` and `error_code` histogram.
- **AC-DG-11-010-03:** Silencing / maintenance window supported via standard alertmanager pattern (optional).

### AC test specifications (US-DG-11-010)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-11-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-010` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Retry rate computed per scan and aggregated per tenant hourly. |
| **Objective** | Verify the behaviour described in AC-DG-11-010-01: Retry rate computed per scan and aggregated per tenant hourly. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-010-01` |
| **Secondary / negative test ID** | `TC-DG-11-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-010-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-11-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-010` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Alert includes top contributing `agent_id` and `error_code` histogram. |
| **Objective** | Verify the behaviour described in AC-DG-11-010-02: Alert includes top contributing `agent_id` and `error_code` histogram. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-11-010-02` |
| **Secondary / negative test ID** | `TC-DG-11-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-010-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-11-010-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-11-010` |
| **Parent EPIC** | `EPIC-DG-11` |
| **Owning squad** | `observability` |
| **Requirement (verbatim)** | Silencing / maintenance window supported via standard alertmanager pattern (optional). |
| **Objective** | Verify the behaviour described in AC-DG-11-010-03: Silencing / maintenance window supported via standard alertmanager pattern (optional). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-11. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-11-010-03` |
| **Secondary / negative test ID** | `TC-DG-11-010-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-11-010-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |
