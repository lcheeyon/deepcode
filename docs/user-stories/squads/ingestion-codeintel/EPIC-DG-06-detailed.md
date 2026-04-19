> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-06-code-indexing-argus.md`](../EPIC-06-code-indexing-argus.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-06 — Code indexing & retrieval (Argus)

> **AC-level test specifications (generated):** Squad copy [`squads/ingestion-codeintel/EPIC-DG-06-detailed.md`](squads/ingestion-codeintel/EPIC-DG-06-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then `python3 scripts/validate_user_stories_traceability.py`.


**Goal:** Parse multi-language code, build dependency signals, chunk semantically, embed into pgvector, and support hybrid retrieval per `Architecture_Design.md` §11–§12.

**Primary personas:** Security engineer, ML engineer (tuning).

---


## US-DG-06-001 — Language-aware AST parse & chunking

**As a** security engineer, **I want** AST-boundary chunking, **so that** embeddings preserve semantic units.

**Wireframe — language coverage dashboard**

```text
┌──────── Repo language breakdown ────────────┐
│ Python   ████████████  62%                │
│ TypeScript ██████      28%                │
│ Go       ██            10%                │
│ [ View excluded files ]                    │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-06-001-01:** GA languages from support matrix use tree-sitter path (Architecture §11.2–11.4).
- **AC-DG-06-001-02:** Chunker never splits mid-function/class for configured node types (Architecture §11.4).
- **AC-DG-06-001-03:** `language_breakdown` populated in `ScanState` (Architecture §4.2).

---

### AC test specifications (US-DG-06-001)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-06-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-001` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | GA languages from support matrix use tree-sitter path (Architecture §11.2–11.4). |
| **Objective** | Verify AC-DG-06-001-01: GA languages from support matrix use tree-sitter path (Architecture §11.2–11.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-001-01` |
| **Secondary / negative test ID** | `TC-DG-06-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-001-01") or Xray/TestRail key == AC-DG-06-001-01 |
| **Spec references** | Architecture §11.2–11.4 |

#### Test specification — AC-DG-06-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-001` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Chunker never splits mid-function/class for configured node types (Architecture §11.4). |
| **Objective** | Verify AC-DG-06-001-02: Chunker never splits mid-function/class for configured node types (Architecture §11.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-001-02` |
| **Secondary / negative test ID** | `TC-DG-06-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-001-02") or Xray/TestRail key == AC-DG-06-001-02 |
| **Spec references** | Architecture §11.4 |

#### Test specification — AC-DG-06-001-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-001` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `language_breakdown` populated in `ScanState` (Architecture §4.2). |
| **Objective** | Verify AC-DG-06-001-03: `language_breakdown` populated in `ScanState` (Architecture §4.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-001-03` |
| **Secondary / negative test ID** | `TC-DG-06-001-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-001-03") or Xray/TestRail key == AC-DG-06-001-03 |
| **Spec references** | Architecture §4.2 |


## US-DG-06-002 — Build dependency graph with caps

**As a** engineer, **I want** dependency graph construction with truncation flags, **so that** monorepos remain tractable.

**Acceptance criteria**

- **AC-DG-06-002-01:** Graph includes external deps and vulnerable deps cross-ref hooks (Architecture §11.5–11.6).
- **AC-DG-06-002-02:** When exceeding `max_nodes` / `max_depth`, status `TRUNCATED` recorded and warning surfaces in report (Architecture §23.1 Q6).

---

### AC test specifications (US-DG-06-002)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-06-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-002` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Graph includes external deps and vulnerable deps cross-ref hooks (Architecture §11.5–11.6). |
| **Objective** | Verify AC-DG-06-002-01: Graph includes external deps and vulnerable deps cross-ref hooks (Architecture §11.5–11.6). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-002-01` |
| **Secondary / negative test ID** | `TC-DG-06-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-002-01") or Xray/TestRail key == AC-DG-06-002-01 |
| **Spec references** | Architecture §11.5–11.6 |

#### Test specification — AC-DG-06-002-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-002` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | When exceeding `max_nodes` / `max_depth`, status `TRUNCATED` recorded and warning surfaces in report (Architecture §23.1 Q6). |
| **Objective** | Verify AC-DG-06-002-02: When exceeding `max_nodes` / `max_depth`, status `TRUNCATED` recorded and warning surfaces in report (Architecture §23.1 Q6). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-002-02` |
| **Secondary / negative test ID** | `TC-DG-06-002-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-002-02") or Xray/TestRail key == AC-DG-06-002-02 |
| **Spec references** | Architecture §23.1 Q6 |


## US-DG-06-003 — Hybrid retrieval (BM25 + vector)

**As a** mapper author, **I want** hybrid retrieval for code, **so that** identifier-exact matches are not missed.

**Acceptance criteria**

- **AC-DG-06-003-01:** Ensemble retriever weights documented default (0.3 BM25 / 0.7 vector) configurable within bounds (Architecture §12.3).
- **AC-DG-06-003-02:** `code_chunks` rows include `tenant_id`, `scan_id`, metadata JSON for file/line span (Architecture §12.1).

---

### AC test specifications (US-DG-06-003)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-06-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-003` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Ensemble retriever weights documented default (0.3 BM25 / 0.7 vector) configurable within bounds (Architecture §12.3). |
| **Objective** | Verify AC-DG-06-003-01: Ensemble retriever weights documented default (0.3 BM25 / 0.7 vector) configurable within bounds (Architecture §12.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-003-01` |
| **Secondary / negative test ID** | `TC-DG-06-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-003-01") or Xray/TestRail key == AC-DG-06-003-01 |
| **Spec references** | Architecture §12.3 |

#### Test specification — AC-DG-06-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-003` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `code_chunks` rows include `tenant_id`, `scan_id`, metadata JSON for file/line span (Architecture §12.1). |
| **Objective** | Verify AC-DG-06-003-02: `code_chunks` rows include `tenant_id`, `scan_id`, metadata JSON for file/line span (Architecture §12.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-003-02` |
| **Secondary / negative test ID** | `TC-DG-06-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-003-02") or Xray/TestRail key == AC-DG-06-003-02 |
| **Spec references** | Architecture §12.1 |


## US-DG-06-004 — Large repository handling modes

**As a** enterprise customer, **I want** predictable behaviour beyond 500k LOC, **so that** scans complete within SLA targets.

**Acceptance criteria**

- **AC-DG-06-004-01:** Strategies per size tier applied (Architecture §11.6).
- **AC-DG-06-004-02:** For >2M LOC, scan requires explicit sub-path scoping or async batch mode flag (Architecture §11.6).

---

### AC test specifications (US-DG-06-004)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-06-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-004` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Strategies per size tier applied (Architecture §11.6). |
| **Objective** | Verify AC-DG-06-004-01: Strategies per size tier applied (Architecture §11.6). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-004-01` |
| **Secondary / negative test ID** | `TC-DG-06-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-004-01") or Xray/TestRail key == AC-DG-06-004-01 |
| **Spec references** | Architecture §11.6 |

#### Test specification — AC-DG-06-004-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-004` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | For >2M LOC, scan requires explicit sub-path scoping or async batch mode flag (Architecture §11.6). |
| **Objective** | Verify AC-DG-06-004-02: For >2M LOC, scan requires explicit sub-path scoping or async batch mode flag (Architecture §11.6). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-004-02` |
| **Secondary / negative test ID** | `TC-DG-06-004-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-004-02") or Xray/TestRail key == AC-DG-06-004-02 |
| **Spec references** | Architecture §11.6 |


## US-DG-06-005 — Security pattern signals (non-LLM layer)

**As a** false-positive owner, **I want** semgrep-style checks where configured, **so that** obvious issues have deterministic anchors.

**Acceptance criteria**

- **AC-DG-06-005-01:** Security pattern scanner outputs feed Athena context as structured signals (Architecture §11.3).

---

### AC test specifications (US-DG-06-005)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-06-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-005` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Security pattern scanner outputs feed Athena context as structured signals (Architecture §11.3). |
| **Objective** | Verify AC-DG-06-005-01: Security pattern scanner outputs feed Athena context as structured signals (Architecture §11.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-005-01` |
| **Secondary / negative test ID** | `TC-DG-06-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-005-01") or Xray/TestRail key == AC-DG-06-005-01 |
| **Spec references** | Architecture §11.3 |


## US-DG-06-006 — Respect `.deepguardignore` and repo ignore patterns

**As a** developer, **I want** vendor and generated dirs excluded, **so that** scans focus on first-party code.

**Acceptance criteria**

- **AC-DG-06-006-01:** Ignore file grammar documented; default excludes `node_modules/`, `.git/`, large `dist/` unless overridden.
- **AC-DG-06-006-02:** Excluded path count and total bytes skipped recorded in `repo_metadata` / scan summary.
- **AC-DG-06-006-03:** Explicit `include_paths` in job config overrides ignore for emergency audits (admin only).

---

### AC test specifications (US-DG-06-006)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-06-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-006` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Ignore file grammar documented; default excludes `node_modules/`, `.git/`, large `dist/` unless overridden. |
| **Objective** | Verify AC-DG-06-006-01: Ignore file grammar documented; default excludes `node_modules/`, `.git/`, large `dist/` unless overridden. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-006-01` |
| **Secondary / negative test ID** | `TC-DG-06-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-006-01") or Xray/TestRail key == AC-DG-06-006-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-06-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-006` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Excluded path count and total bytes skipped recorded in `repo_metadata` / scan summary. |
| **Objective** | Verify AC-DG-06-006-02: Excluded path count and total bytes skipped recorded in `repo_metadata` / scan summary. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-006-02` |
| **Secondary / negative test ID** | `TC-DG-06-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-006-02") or Xray/TestRail key == AC-DG-06-006-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-06-006-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-006` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Explicit `include_paths` in job config overrides ignore for emergency audits (admin only). |
| **Objective** | Verify AC-DG-06-006-03: Explicit `include_paths` in job config overrides ignore for emergency audits (admin only). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-006-03` |
| **Secondary / negative test ID** | `TC-DG-06-006-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-006-03") or Xray/TestRail key == AC-DG-06-006-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-06-007 — Embedding batch pipeline with L4 cache

**As a** cost owner, **I want** embedding cache hits by `sha256(text_chunk + model_id)`, **so that** re-scans avoid re-embedding unchanged chunks when policy allows (Architecture §9.1, §9.4 L4).

**Acceptance criteria**

- **AC-DG-06-007-01:** Cache key and TTL 7d default; invalidation on embedding model version change (Architecture §9.4).
- **AC-DG-06-007-02:** Cache miss path records latency metric per batch (EPIC-DG-11).
- **AC-DG-06-007-03:** Tenant flag can disable shared embedding cache for paranoid mode (document trade-off).

---

### AC test specifications (US-DG-06-007)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-06-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-007` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Cache key and TTL 7d default; invalidation on embedding model version change (Architecture §9.4). |
| **Objective** | Verify AC-DG-06-007-01: Cache key and TTL 7d default; invalidation on embedding model version change (Architecture §9.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. \| 4. Execute negative path and assert stable error_code with no side effects. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-007-01` |
| **Secondary / negative test ID** | `TC-DG-06-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-007-01") or Xray/TestRail key == AC-DG-06-007-01 |
| **Spec references** | Architecture §9.4 |

#### Test specification — AC-DG-06-007-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-007` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `Hardening` |
| **MoSCoW** | `Should` |
| **Requirement type** | `NFR` |
| **NFR metric / target** | `latency / TBD` |
| **Dependencies** | epics `EPIC-DG-11`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `4` |
| **Requirement (verbatim)** | Cache miss path records latency metric per batch (EPIC-DG-11). |
| **Objective** | Verify AC-DG-06-007-02: Cache miss path records latency metric per batch (EPIC-DG-11). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-007-02` |
| **Secondary / negative test ID** | `TC-DG-06-007-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-007-02") or Xray/TestRail key == AC-DG-06-007-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-06-007-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-007` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Tenant flag can disable shared embedding cache for paranoid mode (document trade-off). |
| **Objective** | Verify AC-DG-06-007-03: Tenant flag can disable shared embedding cache for paranoid mode (document trade-off). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-007-03` |
| **Secondary / negative test ID** | `TC-DG-06-007-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-007-03") or Xray/TestRail key == AC-DG-06-007-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-06-008 — Incremental / delta index when feature enabled

**As a** frequent CI user, **I want** delta scope between commits, **so that** token spend drops 60–80% when enabled (Architecture §9.3).

**Acceptance criteria**

- **AC-DG-06-008-01:** When `DELTA_SKIP_ANALYSIS` / `delta_skip_analysis` true and fingerprint matches, behaviour matches MVP decision §23.1 Q7 (re-run Athena+Circe+Penelope on policy bump; optional skip analysis layers).
- **AC-DG-06-008-02:** Delta fingerprint includes `repo_commit_sha` + `policy_version` + `scan_layers` (Architecture §23.1 Q7).
- **AC-DG-06-008-03:** Carry-forward findings list references prior `scan_id` for audit trail.

---

### AC test specifications (US-DG-06-008)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-06-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-008` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P2` / `Post-MVP` |
| **MoSCoW** | `Could` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `2` |
| **Requirement (verbatim)** | When `DELTA_SKIP_ANALYSIS` / `delta_skip_analysis` true and fingerprint matches, behaviour matches MVP decision §23.1 Q7 (re-run Athena+Circe+Penelope on policy bump; optional skip analysis layers). |
| **Objective** | Verify AC-DG-06-008-01: When `DELTA_SKIP_ANALYSIS` / `delta_skip_analysis` true and fingerprint matches, behaviour matches MVP decision §23.1 Q7 (re-run Athena+Circe+Penelope on policy bump; optional skip analysis layers). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-06-008-01` |
| **Secondary / negative test ID** | `TC-DG-06-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-008-01") or Xray/TestRail key == AC-DG-06-008-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-06-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-008` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Delta fingerprint includes `repo_commit_sha` + `policy_version` + `scan_layers` (Architecture §23.1 Q7). |
| **Objective** | Verify AC-DG-06-008-02: Delta fingerprint includes `repo_commit_sha` + `policy_version` + `scan_layers` (Architecture §23.1 Q7). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-008-02` |
| **Secondary / negative test ID** | `TC-DG-06-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-008-02") or Xray/TestRail key == AC-DG-06-008-02 |
| **Spec references** | Architecture §23.1 Q7 |

#### Test specification — AC-DG-06-008-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-008` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Carry-forward findings list references prior `scan_id` for audit trail. |
| **Objective** | Verify AC-DG-06-008-03: Carry-forward findings list references prior `scan_id` for audit trail. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-008-03` |
| **Secondary / negative test ID** | `TC-DG-06-008-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-008-03") or Xray/TestRail key == AC-DG-06-008-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-06-009 — BM25 index lifecycle per scan

**As a** search engineer, **I want** BM25 index built for `scan_id` tenant scope, **so that** hybrid retrieval is isolated.

**Acceptance criteria**

- **AC-DG-06-009-01:** BM25 documents deleted or tombstoned when scan artefacts expire (align retention §14.2).
- **AC-DG-06-009-02:** No cross-tenant BM25 query possible at API/SQL layer.
- **AC-DG-06-009-03:** Reindex job idempotent if worker retries Argus node.

---

### AC test specifications (US-DG-06-009)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-06-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-009` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | BM25 documents deleted or tombstoned when scan artefacts expire (align retention §14.2). |
| **Objective** | Verify AC-DG-06-009-01: BM25 documents deleted or tombstoned when scan artefacts expire (align retention §14.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-009-01` |
| **Secondary / negative test ID** | `TC-DG-06-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-009-01") or Xray/TestRail key == AC-DG-06-009-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-06-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-009` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | No cross-tenant BM25 query possible at API/SQL layer. |
| **Objective** | Verify AC-DG-06-009-02: No cross-tenant BM25 query possible at API/SQL layer. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-009-02` |
| **Secondary / negative test ID** | `TC-DG-06-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-009-02") or Xray/TestRail key == AC-DG-06-009-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-06-009-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-009` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Reindex job idempotent if worker retries Argus node. |
| **Objective** | Verify AC-DG-06-009-03: Reindex job idempotent if worker retries Argus node. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-009-03` |
| **Secondary / negative test ID** | `TC-DG-06-009-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-009-03") or Xray/TestRail key == AC-DG-06-009-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-06-010 — Binary and generated file detection

**As a** platform engineer, **I want** binaries skipped from embedding, **so that** pgvector is not polluted.

**Acceptance criteria**

- **AC-DG-06-010-01:** linguist-style heuristics + size cap classify binaries; list surfaced in report appendix.
- **AC-DG-06-010-02:** Misclassified text-as-binary override API for path glob (admin).
- **AC-DG-06-010-03:** Skipped files do not appear as false “missing coverage” without explicit control mapping (Athena prompt guidance).

---

### AC test specifications (US-DG-06-010)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-06-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-010` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | linguist-style heuristics + size cap classify binaries; list surfaced in report appendix. |
| **Objective** | Verify AC-DG-06-010-01: linguist-style heuristics + size cap classify binaries; list surfaced in report appendix. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-010-01` |
| **Secondary / negative test ID** | `TC-DG-06-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-010-01") or Xray/TestRail key == AC-DG-06-010-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-06-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-010` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Misclassified text-as-binary override API for path glob (admin). |
| **Objective** | Verify AC-DG-06-010-02: Misclassified text-as-binary override API for path glob (admin). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-010-02` |
| **Secondary / negative test ID** | `TC-DG-06-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-010-02") or Xray/TestRail key == AC-DG-06-010-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-06-010-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-010` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Skipped files do not appear as false “missing coverage” without explicit control mapping (Athena prompt guidance). |
| **Objective** | Verify AC-DG-06-010-03: Skipped files do not appear as false “missing coverage” without explicit control mapping (Athena prompt guidance). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. \| 4. Execute negative path and assert stable error_code with no side effects. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-010-03` |
| **Secondary / negative test ID** | `TC-DG-06-010-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-010-03") or Xray/TestRail key == AC-DG-06-010-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-06-011 — Vulnerable dependency enrichment (OSV/NVD)

**As a** AppSec lead, **I want** `vulnerable_deps` populated when lockfiles present, **so that** Athena correlates CVE with call paths.

**Acceptance criteria**

- **AC-DG-06-011-01:** Lockfile parsers for npm, pip, go mod, Maven documented; graceful skip if absent (Architecture §11.5–11.6).
- **AC-DG-06-011-02:** Advisory feed version pinned; air-gap mode uses bundled snapshot (EPIC-DG-13).
- **AC-DG-06-011-03:** Each vulnerable dep links to dependency graph node ids for evidence (Architecture §11.5).

---

### AC test specifications (US-DG-06-011)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-06-011-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-011` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Lockfile parsers for npm, pip, go mod, Maven documented; graceful skip if absent (Architecture §11.5–11.6). |
| **Objective** | Verify AC-DG-06-011-01: Lockfile parsers for npm, pip, go mod, Maven documented; graceful skip if absent (Architecture §11.5–11.6). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-011-01` |
| **Secondary / negative test ID** | `TC-DG-06-011-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-011-01") or Xray/TestRail key == AC-DG-06-011-01 |
| **Spec references** | Architecture §11.5–11.6 |

#### Test specification — AC-DG-06-011-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-011` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-13`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Advisory feed version pinned; air-gap mode uses bundled snapshot (EPIC-DG-13). |
| **Objective** | Verify AC-DG-06-011-02: Advisory feed version pinned; air-gap mode uses bundled snapshot (EPIC-DG-13). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-011-02` |
| **Secondary / negative test ID** | `TC-DG-06-011-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-011-02") or Xray/TestRail key == AC-DG-06-011-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-06-011-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-011` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Each vulnerable dep links to dependency graph node ids for evidence (Architecture §11.5). |
| **Objective** | Verify AC-DG-06-011-03: Each vulnerable dep links to dependency graph node ids for evidence (Architecture §11.5). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-011-03` |
| **Secondary / negative test ID** | `TC-DG-06-011-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-011-03") or Xray/TestRail key == AC-DG-06-011-03 |
| **Spec references** | Architecture §11.5 |


## US-DG-06-012 — pgvector index maintenance

**As a** DBA, **I want** IVFFlat/ HNSW parameters tunable per deployment, **so that** recall meets SLO.

**Acceptance criteria**

- **AC-DG-06-012-01:** Index creation runs in migration or async job; documented for `lists` / M values (Architecture §12.1).
- **AC-DG-06-012-02:** Vacuum/reindex playbook linked from ops doc (Architecture §35.3).
- **AC-DG-06-012-03:** Embedding dimension mismatch fails fast at index time with `error_code`.

### AC test specifications (US-DG-06-012)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-06-012-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-012` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Index creation runs in migration or async job; documented for `lists` / M values (Architecture §12.1). |
| **Objective** | Verify AC-DG-06-012-01: Index creation runs in migration or async job; documented for `lists` / M values (Architecture §12.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-012-01` |
| **Secondary / negative test ID** | `TC-DG-06-012-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-012-01") or Xray/TestRail key == AC-DG-06-012-01 |
| **Spec references** | Architecture §12.1 |

#### Test specification — AC-DG-06-012-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-012` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Vacuum/reindex playbook linked from ops doc (Architecture §35.3). |
| **Objective** | Verify AC-DG-06-012-02: Vacuum/reindex playbook linked from ops doc (Architecture §35.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-012-02` |
| **Secondary / negative test ID** | `TC-DG-06-012-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-012-02") or Xray/TestRail key == AC-DG-06-012-02 |
| **Spec references** | Architecture §35.3 |

#### Test specification — AC-DG-06-012-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-06-012` |
| **Parent EPIC** | `EPIC-DG-06` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L8`; secondary `L10` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Embedding dimension mismatch fails fast at index time with `error_code`. |
| **Objective** | Verify AC-DG-06-012-03: Embedding dimension mismatch fails fast at index time with `error_code`. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-06-012-03` |
| **Secondary / negative test ID** | `TC-DG-06-012-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-06-012-03") or Xray/TestRail key == AC-DG-06-012-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## Epic Definition of Done checklist

- [ ] All in-scope ACs for `EPIC-DG-06` implemented by `ingestion-codeintel` and linked to automated tests (`TC-DG-*`).
- [ ] Unit coverage on touched packages is >=80%.
- [ ] Integration tests pass for all required ACs.
- [ ] Playwright BDD updated where `test_layer_required` includes `bdd`.
- [ ] Observability hooks and stable `error_code` behaviour validated.
- [ ] Security/data-sovereignty constraints verified (no secret leaks, tenant isolation).
- [ ] Design spec for slice exists under `docs/design/` with approved status.
