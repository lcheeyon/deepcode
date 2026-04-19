> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-01-scan-job-orchestration.md`](../EPIC-01-scan-job-orchestration.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-01 — Scan job orchestration (Odysseus / LangGraph)

> **AC-level test specifications (generated):** Squad copy [`squads/platform-runtime/EPIC-DG-01-detailed.md`](squads/platform-runtime/EPIC-DG-01-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py`.


**Goal:** Reliably execute end-to-end compliance scans across ingestion → analysis → mapping → remediation → reporting, with resumability, cancellation, and clear lifecycle semantics aligned to `Architecture_Design.md` §4, §14, §28–§31.

**Primary personas:** Platform engineer, Worker runtime, Security auditor (read-only).

---


## US-DG-01-001 — Execute graph in documented order with convergence

**As a** platform engineer, **I want** the scan graph to follow the prescribed node order with a convergence gate before compliance mapping, **so that** IaC and cloud branches complete deterministically before Athena consumes combined context.

**Wireframe — high-level runtime (operator mental model)**

```text
┌──────────── Scan Job (scan_id) ────────────┐
│  [Hermes] → [Tiresias] → [Argus]           │
│                    ├──────────┬──────────┤ │
│                    v          v          │ │
│               [Laocoon]  [Cassandra]      │ │
│                    └────┬─────┘           │ │
│                         v                 │ │
│                 [Convergence Gate]        │ │
│                         v                 │ │
│         [Athena]→[Circe]→[Penelope]→ END │ │
└────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-01-001-01:** Given `scan_layers.iac=true` and `scan_layers.cloud=true`, Laocoon and Cassandra are dispatched per fan-out rules and Athena does not start until the convergence gate validates completion markers / artifact refs (Architecture §4.5–4.6, §23.1 Q4).
- **AC-DG-01-001-02:** Given `scan_layers.iac=false`, Laocoon is skipped and the gate does not block indefinitely on IaC outputs.
- **AC-DG-01-001-03:** Given `scan_layers.cloud=false` or no snapshots, Cassandra is skipped per routing rules.
- **AC-DG-01-001-04:** Graph compilation uses a stable `thread_id = scan_id` for checkpoint correlation (Architecture §31.1).

---

### AC test specifications (US-DG-01-001)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-01-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-001` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Given `scan_layers.iac=true` and `scan_layers.cloud=true`, Laocoon and Cassandra are dispatched per fan-out rules and Athena does not start until the convergence gate validates completion markers / artifact refs (Architecture §4.5–4.6, §23.1 Q4). |
| **Objective** | Verify the behaviour described in AC-DG-01-001-01: Given `scan_layers.iac=true` and `scan_layers.cloud=true`, Laocoon and Cassandra are dispatched per fan-out rules and Athena does not start until the convergence gate validates completion markers / artifact refs (Archite… |
| **Preconditions** | `scan_layers.iac=true` and `scan_layers.cloud=true`, Laocoon and Cassandra are dispatched per fan-out rules and Athena does not start until the convergence gate validates completion markers / artifact refs (Architecture §4.5–4.6, §23.1 Q4) |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-001-01` |
| **Secondary / negative test ID** | `TC-DG-01-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-001-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §4.5–4.6, §23.1 Q4 |

#### Test specification — AC-DG-01-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-001` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Given `scan_layers.iac=false`, Laocoon is skipped and the gate does not block indefinitely on IaC outputs. |
| **Objective** | Verify the behaviour described in AC-DG-01-001-02: Given `scan_layers.iac=false`, Laocoon is skipped and the gate does not block indefinitely on IaC outputs. |
| **Preconditions** | `scan_layers.iac=false`, Laocoon is skipped and the gate does not block indefinitely on IaC outputs |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-001-02` |
| **Secondary / negative test ID** | `TC-DG-01-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-001-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-01-001-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-001` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Given `scan_layers.cloud=false` or no snapshots, Cassandra is skipped per routing rules. |
| **Objective** | Verify the behaviour described in AC-DG-01-001-03: Given `scan_layers.cloud=false` or no snapshots, Cassandra is skipped per routing rules. |
| **Preconditions** | `scan_layers.cloud=false` or no snapshots, Cassandra is skipped per routing rules |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-001-03` |
| **Secondary / negative test ID** | `TC-DG-01-001-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-001-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-01-001-04

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-001` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Graph compilation uses a stable `thread_id = scan_id` for checkpoint correlation (Architecture §31.1). |
| **Objective** | Verify the behaviour described in AC-DG-01-001-04: Graph compilation uses a stable `thread_id = scan_id` for checkpoint correlation (Architecture §31.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-001-04` |
| **Secondary / negative test ID** | `TC-DG-01-001-04.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-001-04") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §31.1 |


## US-DG-01-002 — Persist checkpoints after each material stage

**As a** worker operator, **I want** checkpoints after node/batch boundaries, **so that** crashes resume without full rework.

**Acceptance criteria**

- **AC-DG-01-002-01:** Postgres-backed checkpointer is used in production topology (`LANGGRAPH_CHECKPOINT=postgres`) (Architecture §4.6, §27).
- **AC-DG-01-002-02:** Athena MVP batches checkpoint after each batch completion (Architecture §31.3).
- **AC-DG-01-002-03:** Resume invocation with `invoke(None, config)` continues from last successful checkpoint without duplicating persisted findings (Architecture §4.6).

---

### AC test specifications (US-DG-01-002)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-01-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-002` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Postgres-backed checkpointer is used in production topology (`LANGGRAPH_CHECKPOINT=postgres`) (Architecture §4.6, §27). |
| **Objective** | Verify the behaviour described in AC-DG-01-002-01: Postgres-backed checkpointer is used in production topology (`LANGGRAPH_CHECKPOINT=postgres`) (Architecture §4.6, §27). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-002-01` |
| **Secondary / negative test ID** | `TC-DG-01-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-002-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §4.6, §27 |

#### Test specification — AC-DG-01-002-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-002` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Athena MVP batches checkpoint after each batch completion (Architecture §31.3). |
| **Objective** | Verify the behaviour described in AC-DG-01-002-02: Athena MVP batches checkpoint after each batch completion (Architecture §31.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-002-02` |
| **Secondary / negative test ID** | `TC-DG-01-002-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-002-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §31.3 |

#### Test specification — AC-DG-01-002-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-002` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Resume invocation with `invoke(None, config)` continues from last successful checkpoint without duplicating persisted findings (Architecture §4.6). |
| **Objective** | Verify the behaviour described in AC-DG-01-002-03: Resume invocation with `invoke(None, config)` continues from last successful checkpoint without duplicating persisted findings (Architecture §4.6). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-002-03` |
| **Secondary / negative test ID** | `TC-DG-01-002-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-002-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §4.6 |


## US-DG-01-003 — Cooperative cancellation

**As a** scan requester, **I want** to cancel an in-flight scan, **so that** wasted LLM spend stops and the system records partial artefacts for audit.

**Wireframe — cancel control (API or UI)**

```text
┌──────── Job header ────────────────┐
│ scan_id: 3fa2…   Status: ANALYZING│
│  [ Cancel scan ]  (confirm modal)  │
└────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-01-003-01:** `POST /v1/scans/{id}/cancel` sets `cancellation_requested=true` and returns `202` (Architecture §28.3, §30.4).
- **AC-DG-01-003-02:** Worker observes cancel between LangGraph nodes and transitions to `CANCELLED` terminal state with partial artefacts retained per policy (Architecture §30.4).
- **AC-DG-01-003-03:** Cancelled scans never emit a `scan.completed` webhook (only `failed`/`completed` per configured events).

---

### AC test specifications (US-DG-01-003)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-01-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-003` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | `POST /v1/scans/{id}/cancel` sets `cancellation_requested=true` and returns `202` (Architecture §28.3, §30.4). |
| **Objective** | Verify the behaviour described in AC-DG-01-003-01: `POST /v1/scans/{id}/cancel` sets `cancellation_requested=true` and returns `202` (Architecture §28.3, §30.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-003-01` |
| **Secondary / negative test ID** | `TC-DG-01-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-003-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §28.3, §30.4 |

#### Test specification — AC-DG-01-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-003` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Worker observes cancel between LangGraph nodes and transitions to `CANCELLED` terminal state with partial artefacts retained per policy (Architecture §30.4). |
| **Objective** | Verify the behaviour described in AC-DG-01-003-02: Worker observes cancel between LangGraph nodes and transitions to `CANCELLED` terminal state with partial artefacts retained per policy (Architecture §30.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-003-02` |
| **Secondary / negative test ID** | `TC-DG-01-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-003-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §30.4 |

#### Test specification — AC-DG-01-003-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-003` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Cancelled scans never emit a `scan.completed` webhook (only `failed`/`completed` per configured events). |
| **Objective** | Verify the behaviour described in AC-DG-01-003-03: Cancelled scans never emit a `scan.completed` webhook (only `failed`/`completed` per configured events). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-003-03` |
| **Secondary / negative test ID** | `TC-DG-01-003-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-003-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-01-004 — Human-in-the-loop gate before Athena (optional)

**As a** security reviewer, **I want** optional pause before mapping, **so that** I can annotate state when upstream agents flag escalation.

**Acceptance criteria**

- **AC-DG-01-004-01:** When `graph_interrupt_before_athena` / `GRAPH_INTERRUPT_BEFORE_ATHENA` enabled, graph enters `AWAITING_REVIEW` and awaits `resume` with annotations (Architecture §4.7, §28.5).
- **AC-DG-01-004-02:** Resume clears interrupt only for authorised roles (`admin` or configured reviewer).
- **AC-DG-01-004-03:** Audit log records who resumed and timestamp (stored alongside scan metadata).

---

### AC test specifications (US-DG-01-004)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-01-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-004` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | When `graph_interrupt_before_athena` / `GRAPH_INTERRUPT_BEFORE_ATHENA` enabled, graph enters `AWAITING_REVIEW` and awaits `resume` with annotations (Architecture §4.7, §28.5). |
| **Objective** | Verify the behaviour described in AC-DG-01-004-01: When `graph_interrupt_before_athena` / `GRAPH_INTERRUPT_BEFORE_ATHENA` enabled, graph enters `AWAITING_REVIEW` and awaits `resume` with annotations (Architecture §4.7, §28.5). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-01-004-01` |
| **Secondary / negative test ID** | `TC-DG-01-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-004-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §4.7, §28.5 |

#### Test specification — AC-DG-01-004-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-004` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Resume clears interrupt only for authorised roles (`admin` or configured reviewer). |
| **Objective** | Verify the behaviour described in AC-DG-01-004-02: Resume clears interrupt only for authorised roles (`admin` or configured reviewer). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-004-02` |
| **Secondary / negative test ID** | `TC-DG-01-004-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-004-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-01-004-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-004` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Audit log records who resumed and timestamp (stored alongside scan metadata). |
| **Objective** | Verify the behaviour described in AC-DG-01-004-03: Audit log records who resumed and timestamp (stored alongside scan metadata). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-004-03` |
| **Secondary / negative test ID** | `TC-DG-01-004-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-004-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-01-005 — Heartbeat & worker-loss detection

**As a** SRE, **I want** heartbeat TTL for active scans, **so that** stuck workers are detected.

**Acceptance criteria**

- **AC-DG-01-005-01:** Worker renews `scan:{scan_id}:heartbeat` every ≤30s with TTL ≥120s (Architecture §30.3).
- **AC-DG-01-005-02:** Watchdog marks `FAILED` with `error_code=WORKER_LOST` when heartbeat missing for a non-terminal scan (Architecture §30.3).

---

### AC test specifications (US-DG-01-005)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-01-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-005` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Worker renews `scan:{scan_id}:heartbeat` every ≤30s with TTL ≥120s (Architecture §30.3). |
| **Objective** | Verify the behaviour described in AC-DG-01-005-01: Worker renews `scan:{scan_id}:heartbeat` every ≤30s with TTL ≥120s (Architecture §30.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-005-01` |
| **Secondary / negative test ID** | `TC-DG-01-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-005-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §30.3 |

#### Test specification — AC-DG-01-005-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-005` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Watchdog marks `FAILED` with `error_code=WORKER_LOST` when heartbeat missing for a non-terminal scan (Architecture §30.3). |
| **Objective** | Verify the behaviour described in AC-DG-01-005-02: Watchdog marks `FAILED` with `error_code=WORKER_LOST` when heartbeat missing for a non-terminal scan (Architecture §30.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-01-005-02` |
| **Secondary / negative test ID** | `TC-DG-01-005-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-005-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §30.3 |


## US-DG-01-006 — Queue claim, visibility timeout, and stale recovery

**As a** worker platform owner, **I want** Redis Streams (or Kafka) consumer semantics with reclaim, **so that** crashed workers do not permanently strand jobs.

**Wireframe — queue depth (ops)**

```text
┌──────── Scan queue (stream:scans) ─────────────────────────┐
│ Pending: 42   Consumers: workers (8)   Lag P95: 1.2m        │
│ [ View DLQ ]  [ XCLAIM stale >15m ]                         │
└─────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-01-006-01:** Worker verifies `scans.status == QUEUED` (or equivalent) before transitioning to in-flight processing (Architecture §30.2).
- **AC-DG-01-006-02:** Visibility timeout / pending entry stale after configurable duration (e.g. 15m) is reclaimable via `XCLAIM` pattern (Architecture §30.2).
- **AC-DG-01-006-03:** Duplicate delivery does not create duplicate `scan_id` rows or fork graph state when idempotency keys are in use (align with EPIC-DG-02).
- **AC-DG-01-006-04:** Optional Kafka deployment uses same `ScanJobMessage` schema version `schema_ver` (Architecture §30.1–30.2).

---

### AC test specifications (US-DG-01-006)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-01-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-006` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Worker verifies `scans.status == QUEUED` (or equivalent) before transitioning to in-flight processing (Architecture §30.2). |
| **Objective** | Verify the behaviour described in AC-DG-01-006-01: Worker verifies `scans.status == QUEUED` (or equivalent) before transitioning to in-flight processing (Architecture §30.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-006-01` |
| **Secondary / negative test ID** | `TC-DG-01-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-006-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §30.2 |

#### Test specification — AC-DG-01-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-006` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Visibility timeout / pending entry stale after configurable duration (e.g. 15m) is reclaimable via `XCLAIM` pattern (Architecture §30.2). |
| **Objective** | Verify the behaviour described in AC-DG-01-006-02: Visibility timeout / pending entry stale after configurable duration (e.g. 15m) is reclaimable via `XCLAIM` pattern (Architecture §30.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-006-02` |
| **Secondary / negative test ID** | `TC-DG-01-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-006-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §30.2 |

#### Test specification — AC-DG-01-006-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-006` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Duplicate delivery does not create duplicate `scan_id` rows or fork graph state when idempotency keys are in use (align with EPIC-DG-02). |
| **Objective** | Verify the behaviour described in AC-DG-01-006-03: Duplicate delivery does not create duplicate `scan_id` rows or fork graph state when idempotency keys are in use (align with EPIC-DG-02). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-006-03` |
| **Secondary / negative test ID** | `TC-DG-01-006-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-006-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-01-006-04

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-006` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Optional Kafka deployment uses same `ScanJobMessage` schema version `schema_ver` (Architecture §30.1–30.2). |
| **Objective** | Verify the behaviour described in AC-DG-01-006-04: Optional Kafka deployment uses same `ScanJobMessage` schema version `schema_ver` (Architecture §30.1–30.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-01-006-04` |
| **Secondary / negative test ID** | `TC-DG-01-006-04.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-006-04") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §30.1–30.2 |


## US-DG-01-007 — Centralised `error_handler` node and stable error codes

**As an** operator, **I want** fatal graph errors routed to a single handler, **so that** `FAILED` status and `error_code` are always persisted consistently.

**Acceptance criteria**

- **AC-DG-01-007-01:** When `should_abort=true`, conditional edges route to `error_handler` which sets terminal `FAILED` and stable `error_code` (Architecture §4.4, §31.4).
- **AC-DG-01-007-02:** `error_message` is sanitised (no stack traces, no secret material) in API and DB (Architecture §28.5).
- **AC-DG-01-007-03:** Non-fatal `ToolExecutionError` does not invoke `error_handler`; partial outputs remain (Architecture §31.4).

---

### AC test specifications (US-DG-01-007)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-01-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-007` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | When `should_abort=true`, conditional edges route to `error_handler` which sets terminal `FAILED` and stable `error_code` (Architecture §4.4, §31.4). |
| **Objective** | Verify the behaviour described in AC-DG-01-007-01: When `should_abort=true`, conditional edges route to `error_handler` which sets terminal `FAILED` and stable `error_code` (Architecture §4.4, §31.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-01-007-01` |
| **Secondary / negative test ID** | `TC-DG-01-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-007-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §4.4, §31.4 |

#### Test specification — AC-DG-01-007-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-007` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | `error_message` is sanitised (no stack traces, no secret material) in API and DB (Architecture §28.5). |
| **Objective** | Verify the behaviour described in AC-DG-01-007-02: `error_message` is sanitised (no stack traces, no secret material) in API and DB (Architecture §28.5). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-007-02` |
| **Secondary / negative test ID** | `TC-DG-01-007-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-007-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §28.5 |

#### Test specification — AC-DG-01-007-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-007` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Non-fatal `ToolExecutionError` does not invoke `error_handler`; partial outputs remain (Architecture §31.4). |
| **Objective** | Verify the behaviour described in AC-DG-01-007-03: Non-fatal `ToolExecutionError` does not invoke `error_handler`; partial outputs remain (Architecture §31.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-007-03` |
| **Secondary / negative test ID** | `TC-DG-01-007-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-007-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §31.4 |


## US-DG-01-008 — Enforce scan wall-clock and LLM budget

**As a** FinOps owner, **I want** `job_config.budget` honoured, **so that** runaway scans stop predictably.

**Acceptance criteria**

- **AC-DG-01-008-01:** When `max_wall_seconds` exceeded, cooperative abort triggers `CANCELLED` or `FAILED` with `error_code` documented for timeout (Architecture §28.4, §19.1 `ScanAbortError`).
- **AC-DG-01-008-02:** When `max_llm_usd` exceeded mid-graph, scan aborts and partial artefacts retained per retention policy (Architecture §28.4, §8.4).
- **AC-DG-01-008-03:** Budget checks occur at defined cooperative points between LangGraph nodes (Architecture §30.4).

---

### AC test specifications (US-DG-01-008)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-01-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-008` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | When `max_wall_seconds` exceeded, cooperative abort triggers `CANCELLED` or `FAILED` with `error_code` documented for timeout (Architecture §28.4, §19.1 `ScanAbortError`). |
| **Objective** | Verify the behaviour described in AC-DG-01-008-01: When `max_wall_seconds` exceeded, cooperative abort triggers `CANCELLED` or `FAILED` with `error_code` documented for timeout (Architecture §28.4, §19.1 `ScanAbortError`). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-01-008-01` |
| **Secondary / negative test ID** | `TC-DG-01-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-008-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §28.4, §19.1 `ScanAbortError` |

#### Test specification — AC-DG-01-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-008` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | When `max_llm_usd` exceeded mid-graph, scan aborts and partial artefacts retained per retention policy (Architecture §28.4, §8.4). |
| **Objective** | Verify the behaviour described in AC-DG-01-008-02: When `max_llm_usd` exceeded mid-graph, scan aborts and partial artefacts retained per retention policy (Architecture §28.4, §8.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-01-008-02` |
| **Secondary / negative test ID** | `TC-DG-01-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-008-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §28.4, §8.4 |

#### Test specification — AC-DG-01-008-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-008` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Budget checks occur at defined cooperative points between LangGraph nodes (Architecture §30.4). |
| **Objective** | Verify the behaviour described in AC-DG-01-008-03: Budget checks occur at defined cooperative points between LangGraph nodes (Architecture §30.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-008-03` |
| **Secondary / negative test ID** | `TC-DG-01-008-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-008-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §30.4 |


## US-DG-01-009 — Stream graph events for live progress (optional)

**As a** UI developer, **I want** `app.astream_events` translated to progress fields, **so that** consoles show sub-stage activity without polling DB only.

**Acceptance criteria**

- **AC-DG-01-009-01:** Optional streaming mode maps LangGraph events to `percent_complete` / sub-stage hints without breaking REST status contract (Architecture §31.2).
- **AC-DG-01-009-02:** Streaming disconnect does not cancel scan; worker continues (resilience).
- **AC-DG-01-009-03:** Event stream excludes `SECRET`-classified state (Architecture §20.3).

---

### AC test specifications (US-DG-01-009)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-01-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-009` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Optional streaming mode maps LangGraph events to `percent_complete` / sub-stage hints without breaking REST status contract (Architecture §31.2). |
| **Objective** | Verify the behaviour described in AC-DG-01-009-01: Optional streaming mode maps LangGraph events to `percent_complete` / sub-stage hints without breaking REST status contract (Architecture §31.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-01-009-01` |
| **Secondary / negative test ID** | `TC-DG-01-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-009-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §31.2 |

#### Test specification — AC-DG-01-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-009` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Streaming disconnect does not cancel scan; worker continues (resilience). |
| **Objective** | Verify the behaviour described in AC-DG-01-009-02: Streaming disconnect does not cancel scan; worker continues (resilience). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-009-02` |
| **Secondary / negative test ID** | `TC-DG-01-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-009-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-01-009-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-009` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Event stream excludes `SECRET`-classified state (Architecture §20.3). |
| **Objective** | Verify the behaviour described in AC-DG-01-009-03: Event stream excludes `SECRET`-classified state (Architecture §20.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-009-03` |
| **Secondary / negative test ID** | `TC-DG-01-009-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-009-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §20.3 |


## US-DG-01-010 — Resume after worker crash (checkpoint parity)

**As a** reliability engineer, **I want** a new worker process to resume from Postgres checkpoint, **so that** P95 SLA is recoverable after pod eviction.

**Acceptance criteria**

- **AC-DG-01-010-01:** Resume uses same `thread_id = scan_id` and does not duplicate findings on reducer merge (Architecture §4.6, §31.1).
- **AC-DG-01-010-02:** Resume is rejected or no-op when scan already terminal unless explicit product policy for `FAILED` retry (document behaviour).
- **AC-DG-01-010-03:** Resume path audited with `resumed_at`, `worker_instance_id` if available (observability alignment EPIC-DG-11).

---

### AC test specifications (US-DG-01-010)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-01-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-010` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Resume uses same `thread_id = scan_id` and does not duplicate findings on reducer merge (Architecture §4.6, §31.1). |
| **Objective** | Verify the behaviour described in AC-DG-01-010-01: Resume uses same `thread_id = scan_id` and does not duplicate findings on reducer merge (Architecture §4.6, §31.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-010-01` |
| **Secondary / negative test ID** | `TC-DG-01-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-010-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §4.6, §31.1 |

#### Test specification — AC-DG-01-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-010` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Resume is rejected or no-op when scan already terminal unless explicit product policy for `FAILED` retry (document behaviour). |
| **Objective** | Verify the behaviour described in AC-DG-01-010-02: Resume is rejected or no-op when scan already terminal unless explicit product policy for `FAILED` retry (document behaviour). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. \| 4. Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. \| Feature disabled path: behaviour is explicit no-op or skip with user-visible reason. |
| **Primary automated test ID** | `TC-DG-01-010-02` |
| **Secondary / negative test ID** | `TC-DG-01-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-010-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-01-010-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-010` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Resume path audited with `resumed_at`, `worker_instance_id` if available (observability alignment EPIC-DG-11). |
| **Objective** | Verify the behaviour described in AC-DG-01-010-03: Resume path audited with `resumed_at`, `worker_instance_id` if available (observability alignment EPIC-DG-11). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-010-03` |
| **Secondary / negative test ID** | `TC-DG-01-010-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-010-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-01-011 — Priority and fairness between tenants (queue)

**As a** SaaS operator, **I want** optional message `priority`, **so that** paid tiers can dequeue ahead without starving others below a fairness floor.

**Acceptance criteria**

- **AC-DG-01-011-01:** `ScanJobMessage` accepts `priority` integer; worker ordering respects documented algorithm (Architecture §30.1).
- **AC-DG-01-011-02:** Starvation test: low-priority jobs still start within configured max wait under load (NFR; document SLO).
- **AC-DG-01-011-03:** Abuse of priority requires `admin` tenant flag or plan tier (product guard).

---

### AC test specifications (US-DG-01-011)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-01-011-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-011` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | `ScanJobMessage` accepts `priority` integer; worker ordering respects documented algorithm (Architecture §30.1). |
| **Objective** | Verify the behaviour described in AC-DG-01-011-01: `ScanJobMessage` accepts `priority` integer; worker ordering respects documented algorithm (Architecture §30.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-011-01` |
| **Secondary / negative test ID** | `TC-DG-01-011-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-011-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §30.1 |

#### Test specification — AC-DG-01-011-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-011` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Starvation test: low-priority jobs still start within configured max wait under load (NFR; document SLO). |
| **Objective** | Verify the behaviour described in AC-DG-01-011-02: Starvation test: low-priority jobs still start within configured max wait under load (NFR; document SLO). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-011-02` |
| **Secondary / negative test ID** | `TC-DG-01-011-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-011-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-01-011-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-011` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Abuse of priority requires `admin` tenant flag or plan tier (product guard). |
| **Objective** | Verify the behaviour described in AC-DG-01-011-03: Abuse of priority requires `admin` tenant flag or plan tier (product guard). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-011-03` |
| **Secondary / negative test ID** | `TC-DG-01-011-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-011-03") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-01-012 — Graph compile once per worker process

**As a** performance engineer, **I want** `build_odysseus_graph().compile()` at worker startup, **so that** per-scan overhead is minimal.

**Acceptance criteria**

- **AC-DG-01-012-01:** Compiled graph reused for all scans in process; feature flags read at compile or documented refresh boundary (Architecture §31.1).
- **AC-DG-01-012-02:** Hot reload of graph requires worker restart in production (documented); dev may auto-reload (Architecture §34).

### AC test specifications (US-DG-01-012)

Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.

#### Test specification — AC-DG-01-012-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-012` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Compiled graph reused for all scans in process; feature flags read at compile or documented refresh boundary (Architecture §31.1). |
| **Objective** | Verify the behaviour described in AC-DG-01-012-01: Compiled graph reused for all scans in process; feature flags read at compile or documented refresh boundary (Architecture §31.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-012-01` |
| **Secondary / negative test ID** | `TC-DG-01-012-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-012-01") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §31.1 |

#### Test specification — AC-DG-01-012-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-01-012` |
| **Parent EPIC** | `EPIC-DG-01` |
| **Owning squad** | `platform-runtime` |
| **Requirement (verbatim)** | Hot reload of graph requires worker restart in production (documented); dev may auto-reload (Architecture §34). |
| **Objective** | Verify the behaviour described in AC-DG-01-012-02: Hot reload of graph requires worker restart in production (documented); dev may auto-reload (Architecture §34). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph path under test (single happy path unless AC implies negative). \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable. |
| **Expected result** | All assertions pass; no secret material in logs; stable machine-readable error_code on failures; state remains tenant-scoped for EPIC-DG-01. |
| **Edge / negative focus** | Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies. \| Timeout / partial failure: system reaches documented terminal or degraded state without data corruption. |
| **Primary automated test ID** | `TC-DG-01-012-02` |
| **Secondary / negative test ID** | `TC-DG-01-012-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-01-012-02") or Xray/TestRail key == ac_id |
| **Spec references** | Architecture §34 |
