> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-07-iac-cloud-analyzers.md`](../EPIC-07-iac-cloud-analyzers.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-07 — IaC & live cloud analysers (Laocoon + Cassandra)

> **AC-level test specifications (generated):** Squad copy [`squads/connectors/EPIC-DG-07-detailed.md`](squads/connectors/EPIC-DG-07-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then `python3 scripts/validate_user_stories_traceability.py`.


**Goal:** Produce normalised IaC findings and cloud posture findings using read-only connectors and typed tool calls per `Architecture_Design.md` §15–§16, product multi-cloud claims.

**Primary personas:** Cloud security engineer, DevOps.

---


## US-DG-07-001 — IaC parser registry coverage

**As a** DevOps engineer, **I want** Terraform/CFN/K8s/ROS/Huawei templates parsed, **so that** misconfigurations become evidence-backed findings.

**Wireframe — IaC inventory**

```text
┌──────── IaC files detected ─────────────────┐
│ ./infra/main.tf          Terraform  [view] │
│ ./k8s/prod/deploy.yaml   Kubernetes [view]│
│ Filters: [provider ▼] [severity ▼]         │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-07-001-01:** Parser registry includes backends listed in §15.1 for GA targets (Terraform, CFN, K8s, Ali ROS, Huawei template).
- **AC-DG-07-001-02:** Tool execution uses `safe_read` sandbox — no path traversal (Architecture §6.5, §20.3).

---

### AC test specifications (US-DG-07-001)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-07-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-001` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Parser registry includes backends listed in §15.1 for GA targets (Terraform, CFN, K8s, Ali ROS, Huawei template). |
| **Objective** | Verify AC-DG-07-001-01: Parser registry includes backends listed in §15.1 for GA targets (Terraform, CFN, K8s, Ali ROS, Huawei template). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-001-01` |
| **Secondary / negative test ID** | `TC-DG-07-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-001-01") or Xray/TestRail key == AC-DG-07-001-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-07-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-001` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Tool execution uses `safe_read` sandbox — no path traversal (Architecture §6.5, §20.3). |
| **Objective** | Verify AC-DG-07-001-02: Tool execution uses `safe_read` sandbox — no path traversal (Architecture §6.5, §20.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-001-02` |
| **Secondary / negative test ID** | `TC-DG-07-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-001-02") or Xray/TestRail key == AC-DG-07-001-02 |
| **Spec references** | Architecture §6.5, §20.3 |


## US-DG-07-002 — Structured tool-calling loop with caps

**As a** platform engineer, **I want** bounded ReAct iterations, **so that** runaway tool loops cannot burn tokens.

**Acceptance criteria**

- **AC-DG-07-002-01:** `max_iterations` default 5 per agent configuration (Architecture §3.1).
- **AC-DG-07-002-02:** Tool failures append `AgentError`, mark resource `SKIPPED`, continue when non-fatal (Architecture §31.4).

---

### AC test specifications (US-DG-07-002)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-07-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-002` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `max_iterations` default 5 per agent configuration (Architecture §3.1). |
| **Objective** | Verify AC-DG-07-002-01: `max_iterations` default 5 per agent configuration (Architecture §3.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-002-01` |
| **Secondary / negative test ID** | `TC-DG-07-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-002-01") or Xray/TestRail key == AC-DG-07-002-01 |
| **Spec references** | Architecture §3.1 |

#### Test specification — AC-DG-07-002-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-002` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Tool failures append `AgentError`, mark resource `SKIPPED`, continue when non-fatal (Architecture §31.4). |
| **Objective** | Verify AC-DG-07-002-02: Tool failures append `AgentError`, mark resource `SKIPPED`, continue when non-fatal (Architecture §31.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-002-02` |
| **Secondary / negative test ID** | `TC-DG-07-002-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-002-02") or Xray/TestRail key == AC-DG-07-002-02 |
| **Spec references** | Architecture §31.4 |


## US-DG-07-003 — Cloud connector abstraction

**As a** multi-cloud customer, **I want** provider-specific SDKs behind `CloudConnector`, **so that** adding a vendor does not fork core mapping.

**Acceptance criteria**

- **AC-DG-07-003-01:** Interface methods include IAM/network/storage/compute/encryption/audit accessors (Architecture §15.2).
- **AC-DG-07-003-02:** AWS + Alibaba + Tencent + Huawei connectors enumerated in Chinese business doc map to same `ResourceSnapshot` canonical model (Business doc §13–§14).

---

### AC test specifications (US-DG-07-003)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-07-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-003` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `5` |
| **Requirement (verbatim)** | Interface methods include IAM/network/storage/compute/encryption/audit accessors (Architecture §15.2). |
| **Objective** | Verify AC-DG-07-003-01: Interface methods include IAM/network/storage/compute/encryption/audit accessors (Architecture §15.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-003-01` |
| **Secondary / negative test ID** | `TC-DG-07-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-003-01") or Xray/TestRail key == AC-DG-07-003-01 |
| **Spec references** | Architecture §15.2 |

#### Test specification — AC-DG-07-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-003` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | AWS + Alibaba + Tencent + Huawei connectors enumerated in Chinese business doc map to same `ResourceSnapshot` canonical model (Business doc §13–§14). |
| **Objective** | Verify AC-DG-07-003-02: AWS + Alibaba + Tencent + Huawei connectors enumerated in Chinese business doc map to same `ResourceSnapshot` canonical model (Business doc §13–§14). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-003-02` |
| **Secondary / negative test ID** | `TC-DG-07-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-003-02") or Xray/TestRail key == AC-DG-07-003-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-07-004 — Read-only enforcement

**As a** CISO, **I want** guarantees connectors cannot mutate resources, **so that** production safety is preserved.

**Acceptance criteria**

- **AC-DG-07-004-01:** Cloud credentials documented as read-only IAM/CAM policies (Architecture §2.3; Business doc §13.x).
- **AC-DG-07-004-02:** No write APIs invoked in connector code paths (static analysis / contract tests).

---

### AC test specifications (US-DG-07-004)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-07-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-004` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Cloud credentials documented as read-only IAM/CAM policies (Architecture §2.3; Business doc §13.x). |
| **Objective** | Verify AC-DG-07-004-01: Cloud credentials documented as read-only IAM/CAM policies (Architecture §2.3; Business doc §13.x). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-004-01` |
| **Secondary / negative test ID** | `TC-DG-07-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-004-01") or Xray/TestRail key == AC-DG-07-004-01 |
| **Spec references** | Architecture §2.3; Business doc §13.x |

#### Test specification — AC-DG-07-004-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-004` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | No write APIs invoked in connector code paths (static analysis / contract tests). |
| **Objective** | Verify AC-DG-07-004-02: No write APIs invoked in connector code paths (static analysis / contract tests). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-004-02` |
| **Secondary / negative test ID** | `TC-DG-07-004-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-004-02") or Xray/TestRail key == AC-DG-07-004-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-07-005 — Partial cloud degradation

**As an** operator, **I want** scans to continue when a region API fails, **so that** I still receive partial coverage.

**Acceptance criteria**

- **AC-DG-07-005-01:** `CloudConnectorError` triggers degraded snapshot with explicit coverage gaps in report appendix (Architecture §19.1).

---

### AC test specifications (US-DG-07-005)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-07-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-005` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `CloudConnectorError` triggers degraded snapshot with explicit coverage gaps in report appendix (Architecture §19.1). |
| **Objective** | Verify AC-DG-07-005-01: `CloudConnectorError` triggers degraded snapshot with explicit coverage gaps in report appendix (Architecture §19.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-005-01` |
| **Secondary / negative test ID** | `TC-DG-07-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-005-01") or Xray/TestRail key == AC-DG-07-005-01 |
| **Spec references** | Architecture §19.1 |


## US-DG-07-006 — Kubernetes manifest validation findings

**As a** platform engineer, **I want** privileged containers, hostPath, and missing resource limits flagged, **so that** CIS/K8s controls map cleanly.

**Acceptance criteria**

- **AC-DG-07-006-01:** `kubernetes-validate` (or successor) integrated; invalid manifests produce `SKIPPED` with reason (Architecture §15.1).
- **AC-DG-07-006-02:** Findings reference `namespace/kind/name` keys in evidence.
- **AC-DG-07-006-03:** Helm charts expanded with `helm template` when `scan_layers.iac` includes helm (beta documented Architecture §11.2).

---

### AC test specifications (US-DG-07-006)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-07-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-006` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `kubernetes-validate` (or successor) integrated; invalid manifests produce `SKIPPED` with reason (Architecture §15.1). |
| **Objective** | Verify AC-DG-07-006-01: `kubernetes-validate` (or successor) integrated; invalid manifests produce `SKIPPED` with reason (Architecture §15.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. \| 4. Execute negative path and assert stable error_code with no side effects. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-006-01` |
| **Secondary / negative test ID** | `TC-DG-07-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-006-01") or Xray/TestRail key == AC-DG-07-006-01 |
| **Spec references** | Architecture §15.1 |

#### Test specification — AC-DG-07-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-006` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Findings reference `namespace/kind/name` keys in evidence. |
| **Objective** | Verify AC-DG-07-006-02: Findings reference `namespace/kind/name` keys in evidence. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-006-02` |
| **Secondary / negative test ID** | `TC-DG-07-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-006-02") or Xray/TestRail key == AC-DG-07-006-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-07-006-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-006` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `Post-MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Helm charts expanded with `helm template` when `scan_layers.iac` includes helm (beta documented Architecture §11.2). |
| **Objective** | Verify AC-DG-07-006-03: Helm charts expanded with `helm template` when `scan_layers.iac` includes helm (beta documented Architecture §11.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-006-03` |
| **Secondary / negative test ID** | `TC-DG-07-006-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-006-03") or Xray/TestRail key == AC-DG-07-006-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-07-007 — Terraform module graph and provider constraints

**As a** DevOps engineer, **I want** module depth and provider version constraints summarised, **so that** Athena reasons about blast radius.

**Acceptance criteria**

- **AC-DG-07-007-01:** Parser extracts module tree to max depth configurable; truncates with warning (Architecture §11.6 spirit).
- **AC-DG-07-007-02:** Provider `required_version` and `terraform` block constraints appear in structured summary passed to Athena.
- **AC-DG-07-007-03:** Remote modules referenced by git URL recorded as third-party risk flag (Business doc supply chain).

---

### AC test specifications (US-DG-07-007)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-07-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-007` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Parser extracts module tree to max depth configurable; truncates with warning (Architecture §11.6 spirit). |
| **Objective** | Verify AC-DG-07-007-01: Parser extracts module tree to max depth configurable; truncates with warning (Architecture §11.6 spirit). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-007-01` |
| **Secondary / negative test ID** | `TC-DG-07-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-007-01") or Xray/TestRail key == AC-DG-07-007-01 |
| **Spec references** | Architecture §11.6 spirit |

#### Test specification — AC-DG-07-007-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-007` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Provider `required_version` and `terraform` block constraints appear in structured summary passed to Athena. |
| **Objective** | Verify AC-DG-07-007-02: Provider `required_version` and `terraform` block constraints appear in structured summary passed to Athena. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-007-02` |
| **Secondary / negative test ID** | `TC-DG-07-007-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-007-02") or Xray/TestRail key == AC-DG-07-007-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-07-007-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-007` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Remote modules referenced by git URL recorded as third-party risk flag (Business doc supply chain). |
| **Objective** | Verify AC-DG-07-007-03: Remote modules referenced by git URL recorded as third-party risk flag (Business doc supply chain). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-007-03` |
| **Secondary / negative test ID** | `TC-DG-07-007-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-007-03") or Xray/TestRail key == AC-DG-07-007-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-07-008 — CloudConnector contract tests (VCR)

**As a** CI maintainer, **I want** sanitised VCR fixtures per provider, **so that** connectors do not regress.

**Acceptance criteria**

- **AC-DG-07-008-01:** Each connector has `pytest-recording` cassette suite with secrets redacted (Architecture §33.1).
- **AC-DG-07-008-02:** CI runs contract suite on provider SDK upgrades gated by maintainer approval.
- **AC-DG-07-008-03:** Recorded responses versioned with `schema_ver` bump when normaliser changes.

---

### AC test specifications (US-DG-07-008)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-07-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-008` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Each connector has `pytest-recording` cassette suite with secrets redacted (Architecture §33.1). |
| **Objective** | Verify AC-DG-07-008-01: Each connector has `pytest-recording` cassette suite with secrets redacted (Architecture §33.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-008-01` |
| **Secondary / negative test ID** | `TC-DG-07-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-008-01") or Xray/TestRail key == AC-DG-07-008-01 |
| **Spec references** | Architecture §33.1 |

#### Test specification — AC-DG-07-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-008` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | CI runs contract suite on provider SDK upgrades gated by maintainer approval. |
| **Objective** | Verify AC-DG-07-008-02: CI runs contract suite on provider SDK upgrades gated by maintainer approval. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-008-02` |
| **Secondary / negative test ID** | `TC-DG-07-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-008-02") or Xray/TestRail key == AC-DG-07-008-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-07-008-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-008` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Recorded responses versioned with `schema_ver` bump when normaliser changes. |
| **Objective** | Verify AC-DG-07-008-03: Recorded responses versioned with `schema_ver` bump when normaliser changes. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-008-03` |
| **Secondary / negative test ID** | `TC-DG-07-008-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-008-03") or Xray/TestRail key == AC-DG-07-008-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-07-009 — Normalised `ResourceSnapshot` schema versioning

**As a** mapper author, **I want** versioned canonical schema for cloud resources, **so that** Athena prompts stay stable across vendors.

**Acceptance criteria**

- **AC-DG-07-009-01:** Every snapshot JSON includes `schema_ver` and `provider` and `captured_at`.
- **AC-DG-07-009-02:** Breaking normaliser changes bump `schema_ver` and trigger regression evals (EPIC-DG-11).
- **AC-DG-07-009-03:** Unknown resource types preserved as raw blob under typed envelope for forward compatibility.

---

### AC test specifications (US-DG-07-009)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-07-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-009` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Every snapshot JSON includes `schema_ver` and `provider` and `captured_at`. |
| **Objective** | Verify AC-DG-07-009-01: Every snapshot JSON includes `schema_ver` and `provider` and `captured_at`. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-009-01` |
| **Secondary / negative test ID** | `TC-DG-07-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-009-01") or Xray/TestRail key == AC-DG-07-009-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-07-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-009` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-11`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Breaking normaliser changes bump `schema_ver` and trigger regression evals (EPIC-DG-11). |
| **Objective** | Verify AC-DG-07-009-02: Breaking normaliser changes bump `schema_ver` and trigger regression evals (EPIC-DG-11). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-009-02` |
| **Secondary / negative test ID** | `TC-DG-07-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-009-02") or Xray/TestRail key == AC-DG-07-009-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-07-009-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-009` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Unknown resource types preserved as raw blob under typed envelope for forward compatibility. |
| **Objective** | Verify AC-DG-07-009-03: Unknown resource types preserved as raw blob under typed envelope for forward compatibility. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-009-03` |
| **Secondary / negative test ID** | `TC-DG-07-009-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-009-03") or Xray/TestRail key == AC-DG-07-009-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-07-010 — Alibaba / Tencent / Huawei-specific checks (domestic clouds)

**As a** China-region customer, **I want** checks aligned to RAM/CAM/IAM and OSS/COS/OBS patterns, **so that** 等保 evidence is meaningful (Business doc §13).

**Acceptance criteria**

- **AC-DG-07-010-01:** Alibaba: ActionTrail multi-region, OSS public access, ACK API exposure checks present in connector output mapping table (Business doc §13.1).
- **AC-DG-07-010-02:** Tencent: CloudAudit, COS public ACL, CWP coverage signals present (Business doc §13.2).
- **AC-DG-07-010-03:** Huawei: CTS, DEW/SM4 encryption flags, CBH presence captured where API allows (Business doc §13.3).

---

### AC test specifications (US-DG-07-010)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-07-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-010` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `5` |
| **Requirement (verbatim)** | Alibaba: ActionTrail multi-region, OSS public access, ACK API exposure checks present in connector output mapping table (Business doc §13.1). |
| **Objective** | Verify AC-DG-07-010-01: Alibaba: ActionTrail multi-region, OSS public access, ACK API exposure checks present in connector output mapping table (Business doc §13.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-010-01` |
| **Secondary / negative test ID** | `TC-DG-07-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-010-01") or Xray/TestRail key == AC-DG-07-010-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-07-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-010` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Tencent: CloudAudit, COS public ACL, CWP coverage signals present (Business doc §13.2). |
| **Objective** | Verify AC-DG-07-010-02: Tencent: CloudAudit, COS public ACL, CWP coverage signals present (Business doc §13.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-010-02` |
| **Secondary / negative test ID** | `TC-DG-07-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-010-02") or Xray/TestRail key == AC-DG-07-010-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-07-010-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-010` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `5` |
| **Requirement (verbatim)** | Huawei: CTS, DEW/SM4 encryption flags, CBH presence captured where API allows (Business doc §13.3). |
| **Objective** | Verify AC-DG-07-010-03: Huawei: CTS, DEW/SM4 encryption flags, CBH presence captured where API allows (Business doc §13.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-010-03` |
| **Secondary / negative test ID** | `TC-DG-07-010-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-010-03") or Xray/TestRail key == AC-DG-07-010-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-07-011 — Cloud resource rate limiting and pagination

**As a** connector developer, **I want** exponential backoff on API throttles, **so that** large accounts complete without fatal error.

**Acceptance criteria**

- **AC-DG-07-011-01:** Throttling uses jittered backoff; max retry count documented per SDK call site.
- **AC-DG-07-011-02:** Pagination cursors for massive IAM policy sets do not OOM; spill to artifact ref (Architecture §5.3).
- **AC-DG-07-011-03:** Partial completion sets `cloud_findings` metadata `coverage=partial` with reasons.

---

### AC test specifications (US-DG-07-011)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-07-011-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-011` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Throttling uses jittered backoff; max retry count documented per SDK call site. |
| **Objective** | Verify AC-DG-07-011-01: Throttling uses jittered backoff; max retry count documented per SDK call site. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-011-01` |
| **Secondary / negative test ID** | `TC-DG-07-011-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-011-01") or Xray/TestRail key == AC-DG-07-011-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-07-011-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-011` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Pagination cursors for massive IAM policy sets do not OOM; spill to artifact ref (Architecture §5.3). |
| **Objective** | Verify AC-DG-07-011-02: Pagination cursors for massive IAM policy sets do not OOM; spill to artifact ref (Architecture §5.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-011-02` |
| **Secondary / negative test ID** | `TC-DG-07-011-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-011-02") or Xray/TestRail key == AC-DG-07-011-02 |
| **Spec references** | Architecture §5.3 |

#### Test specification — AC-DG-07-011-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-011` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Partial completion sets `cloud_findings` metadata `coverage=partial` with reasons. |
| **Objective** | Verify AC-DG-07-011-03: Partial completion sets `cloud_findings` metadata `coverage=partial` with reasons. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-011-03` |
| **Secondary / negative test ID** | `TC-DG-07-011-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-011-03") or Xray/TestRail key == AC-DG-07-011-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-07-012 — CDK / Pulumi / Bicep beta paths

**As a** modern IaC user, **I want** optional analysis for CDK TypeScript and Bicep, **so that** roadmap parity is visible in scan config.

**Acceptance criteria**

- **AC-DG-07-012-01:** Feature flag gates CDK/Bicep/Pulumi parsers listed Architecture §15.1; disabled by default in MVP if unstable.
- **AC-DG-07-012-02:** When disabled, scan does not fail; stage skipped with user-visible notice.
- **AC-DG-07-012-03:** When enabled, findings tagged `layer=IAC` and `parser_version` set for audit.

### AC test specifications (US-DG-07-012)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-07-012-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-012` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Feature flag gates CDK/Bicep/Pulumi parsers listed Architecture §15.1; disabled by default in MVP if unstable. |
| **Objective** | Verify AC-DG-07-012-01: Feature flag gates CDK/Bicep/Pulumi parsers listed Architecture §15.1; disabled by default in MVP if unstable. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-012-01` |
| **Secondary / negative test ID** | `TC-DG-07-012-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-012-01") or Xray/TestRail key == AC-DG-07-012-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-07-012-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-012` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | When disabled, scan does not fail; stage skipped with user-visible notice. |
| **Objective** | Verify AC-DG-07-012-02: When disabled, scan does not fail; stage skipped with user-visible notice. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-012-02` |
| **Secondary / negative test ID** | `TC-DG-07-012-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-012-02") or Xray/TestRail key == AC-DG-07-012-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-07-012-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-07-012` |
| **Parent EPIC** | `EPIC-DG-07` |
| **Owning squad / role** | `connectors` / `cloud_security_engineer` |
| **Phase mapping** | primary `L9`; secondary `C1-C4` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | When enabled, findings tagged `layer=IAC` and `parser_version` set for audit. |
| **Objective** | Verify AC-DG-07-012-03: When enabled, findings tagged `layer=IAC` and `parser_version` set for audit. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-07-012-03` |
| **Secondary / negative test ID** | `TC-DG-07-012-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-07-012-03") or Xray/TestRail key == AC-DG-07-012-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## Epic Definition of Done checklist

- [ ] All in-scope ACs for `EPIC-DG-07` implemented by `connectors` and linked to automated tests (`TC-DG-*`).
- [ ] Unit coverage on touched packages is >=80%.
- [ ] Integration tests pass for all required ACs.
- [ ] Playwright BDD updated where `test_layer_required` includes `bdd`.
- [ ] Observability hooks and stable `error_code` behaviour validated.
- [ ] Security/data-sovereignty constraints verified (no secret leaks, tenant isolation).
- [ ] Design spec for slice exists under `docs/design/` with approved status.
