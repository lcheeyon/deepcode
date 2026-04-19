> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-10-reporting-penelope.md`](../EPIC-10-reporting-penelope.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-10 — Report assembly & PDF (Penelope)

> **AC-level test specifications (generated):** Squad copy [`squads/remediation-reporting/EPIC-DG-10-detailed.md`](squads/remediation-reporting/EPIC-DG-10-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then `python3 scripts/validate_user_stories_traceability.py`.


**Goal:** Deterministically assemble audit-grade PDFs with CJK support, structured sections, and encrypted object storage per `Architecture_Design.md` §18, §32.

**Primary personas:** Auditor, Executive sponsor.

---


## US-DG-10-001 — Generate full report outline

**As an** auditor, **I want** the PDF to follow the mandated section order, **so that** my firm’s review checklist maps cleanly.

**Wireframe — report TOC preview (HTML/PDF)**

```text
┌──────── Report preview ──────────────────────┐
│ 1 Executive summary                        │
│ 2 Scan metadata                            │
│ 3 Compliance score dashboard               │
│ … Cross-layer correlation …                │
│ 9 Remediation roadmap                      │
│ Appendix B Evidence references             │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-10-001-01:** Sections 1–13 from §18.1 appear with stable ordering and anchors.
- **AC-DG-10-001-02:** Same inputs + policy version yield structurally identical skeleton (determinism goal Architecture §2.3) — allow bounded LLM variance only in narrative blocks explicitly flagged “LLM-polished”.

---

### AC test specifications (US-DG-10-001)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-10-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-001` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Sections 1–13 from §18.1 appear with stable ordering and anchors. |
| **Objective** | Verify AC-DG-10-001-01: Sections 1–13 from §18.1 appear with stable ordering and anchors. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-001-01` |
| **Secondary / negative test ID** | `TC-DG-10-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-001-01") or Xray/TestRail key == AC-DG-10-001-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-10-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-001` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Same inputs + policy version yield structurally identical skeleton (determinism goal Architecture §2.3) — allow bounded LLM variance only in narrative blocks explicitly flagged “LLM-polished”. |
| **Objective** | Verify AC-DG-10-001-02: Same inputs + policy version yield structurally identical skeleton (determinism goal Architecture §2.3) — allow bounded LLM variance only in narrative blocks explicitly flagged “LLM-polished”. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-001-02` |
| **Secondary / negative test ID** | `TC-DG-10-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-001-02") or Xray/TestRail key == AC-DG-10-001-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-10-002 — CJK font embedding for Chinese reports

**As a** China assessor, **I want** Chinese text rendered correctly, **so that** submissions are accepted.

**Acceptance criteria**

- **AC-DG-10-002-01:** ReportLab pipeline bundles CJK fonts (STHeiti/Songti) in image layer (Architecture §18.2; Business doc §16).

---

### AC test specifications (US-DG-10-002)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-10-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-002` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | ReportLab pipeline bundles CJK fonts (STHeiti/Songti) in image layer (Architecture §18.2; Business doc §16). |
| **Objective** | Verify AC-DG-10-002-01: ReportLab pipeline bundles CJK fonts (STHeiti/Songti) in image layer (Architecture §18.2; Business doc §16). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-002-01` |
| **Secondary / negative test ID** | `TC-DG-10-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-002-01") or Xray/TestRail key == AC-DG-10-002-01 |
| **Spec references** | Architecture §18.2; Business doc §16 |


## US-DG-10-003 — Encrypted PDF artefact with checksum

**As a** security officer, **I want** encrypted PDF stored in tenant object namespace, **so that** confidentiality matches contract.

**Acceptance criteria**

- **AC-DG-10-003-01:** Final `report.pdf` registered in `artifacts` with `checksum_sha256`, encryption mode, optional `expires_at` for presigned flows (Architecture §29.1, §32.1).
- **AC-DG-10-003-02:** Default retention aligns to 7-year audit requirement where configured (Architecture §14.2, §32.2).

---

### AC test specifications (US-DG-10-003)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-10-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-003` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P0` / `Post-MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `4` |
| **Requirement (verbatim)** | Final `report.pdf` registered in `artifacts` with `checksum_sha256`, encryption mode, optional `expires_at` for presigned flows (Architecture §29.1, §32.1). |
| **Objective** | Verify AC-DG-10-003-01: Final `report.pdf` registered in `artifacts` with `checksum_sha256`, encryption mode, optional `expires_at` for presigned flows (Architecture §29.1, §32.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-10-003-01` |
| **Secondary / negative test ID** | `TC-DG-10-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-003-01") or Xray/TestRail key == AC-DG-10-003-01 |
| **Spec references** | Architecture §29.1, §32.1 |

#### Test specification — AC-DG-10-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-003` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Default retention aligns to 7-year audit requirement where configured (Architecture §14.2, §32.2). |
| **Objective** | Verify AC-DG-10-003-02: Default retention aligns to 7-year audit requirement where configured (Architecture §14.2, §32.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-003-02` |
| **Secondary / negative test ID** | `TC-DG-10-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-003-02") or Xray/TestRail key == AC-DG-10-003-02 |
| **Spec references** | Architecture §14.2, §32.2 |


## US-DG-10-004 — Evidence appendix with file:line citations

**As an** external auditor, **I want** appendix B to enumerate evidence pointers, **so that** sampling is efficient.

**Acceptance criteria**

- **AC-DG-10-004-01:** Appendix B lists `file_path:line` or cloud ARN references matching DB `evidence_refs` JSON (Architecture §18.1; §29.1).

---

### AC test specifications (US-DG-10-004)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-10-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-004` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Appendix B lists `file_path:line` or cloud ARN references matching DB `evidence_refs` JSON (Architecture §18.1; §29.1). |
| **Objective** | Verify AC-DG-10-004-01: Appendix B lists `file_path:line` or cloud ARN references matching DB `evidence_refs` JSON (Architecture §18.1; §29.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-004-01` |
| **Secondary / negative test ID** | `TC-DG-10-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-004-01") or Xray/TestRail key == AC-DG-10-004-01 |
| **Spec references** | Architecture §18.1; §29.1 |


## US-DG-10-005 — Methodology & limitations transparency

**As a** risk committee member, **I want** explicit methodology including model versions, **so that** we understand residual risk.

**Acceptance criteria**

- **AC-DG-10-005-01:** Appendix documents tool versions, LLM models, cache thresholds, known truncation warnings (Architecture §18.1 item 11).

---

### AC test specifications (US-DG-10-005)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-10-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-005` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Appendix documents tool versions, LLM models, cache thresholds, known truncation warnings (Architecture §18.1 item 11). |
| **Objective** | Verify AC-DG-10-005-01: Appendix documents tool versions, LLM models, cache thresholds, known truncation warnings (Architecture §18.1 item 11). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-005-01` |
| **Secondary / negative test ID** | `TC-DG-10-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-005-01") or Xray/TestRail key == AC-DG-10-005-01 |
| **Spec references** | Architecture §18.1 item 11 |


## US-DG-10-006 — Radar / heatmap charts for framework domains

**As a** risk committee member, **I want** visual radar of control domains, **so that** weak domains stand out (Architecture §18.1 item 3; Business doc §16).

**Acceptance criteria**

- **AC-DG-10-006-01:** Charts generated via matplotlib or equivalent; embedded as vector or high-DPI raster in PDF.
- **AC-DG-10-006-02:** Chart data JSON archived alongside PDF for reproducibility.
- **AC-DG-10-006-03:** Failure to render chart downgrades to table without failing scan.

---

### AC test specifications (US-DG-10-006)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-10-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-006` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Charts generated via matplotlib or equivalent; embedded as vector or high-DPI raster in PDF. |
| **Objective** | Verify AC-DG-10-006-01: Charts generated via matplotlib or equivalent; embedded as vector or high-DPI raster in PDF. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-006-01` |
| **Secondary / negative test ID** | `TC-DG-10-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-006-01") or Xray/TestRail key == AC-DG-10-006-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-10-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-006` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Chart data JSON archived alongside PDF for reproducibility. |
| **Objective** | Verify AC-DG-10-006-02: Chart data JSON archived alongside PDF for reproducibility. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-006-02` |
| **Secondary / negative test ID** | `TC-DG-10-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-006-02") or Xray/TestRail key == AC-DG-10-006-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-10-006-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-006` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Failure to render chart downgrades to table without failing scan. |
| **Objective** | Verify AC-DG-10-006-03: Failure to render chart downgrades to table without failing scan. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-006-03` |
| **Secondary / negative test ID** | `TC-DG-10-006-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-006-03") or Xray/TestRail key == AC-DG-10-006-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-10-007 — Markdown intermediate artefact

**As a** integrator, **I want** optional `report.md` artefact, **so that** I can publish to Confluence or Git.

**Acceptance criteria**

- **AC-DG-10-007-01:** Jinja → Markdown stage stored as artifact kind `report_md` with checksum (Architecture §18.2).
- **AC-DG-10-007-02:** Markdown excludes raw secrets; same redaction rules as PDF (Architecture §20.3).
- **AC-DG-10-007-03:** Download path mirrors PDF artefact API pattern (EPIC-DG-02).

---

### AC test specifications (US-DG-10-007)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-10-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-007` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Jinja → Markdown stage stored as artifact kind `report_md` with checksum (Architecture §18.2). |
| **Objective** | Verify AC-DG-10-007-01: Jinja → Markdown stage stored as artifact kind `report_md` with checksum (Architecture §18.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-007-01` |
| **Secondary / negative test ID** | `TC-DG-10-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-007-01") or Xray/TestRail key == AC-DG-10-007-01 |
| **Spec references** | Architecture §18.2 |

#### Test specification — AC-DG-10-007-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-007` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Markdown excludes raw secrets; same redaction rules as PDF (Architecture §20.3). |
| **Objective** | Verify AC-DG-10-007-02: Markdown excludes raw secrets; same redaction rules as PDF (Architecture §20.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-007-02` |
| **Secondary / negative test ID** | `TC-DG-10-007-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-007-02") or Xray/TestRail key == AC-DG-10-007-02 |
| **Spec references** | Architecture §20.3 |

#### Test specification — AC-DG-10-007-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-007` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-02`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Download path mirrors PDF artefact API pattern (EPIC-DG-02). |
| **Objective** | Verify AC-DG-10-007-03: Download path mirrors PDF artefact API pattern (EPIC-DG-02). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-007-03` |
| **Secondary / negative test ID** | `TC-DG-10-007-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-007-03") or Xray/TestRail key == AC-DG-10-007-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-10-008 — Cover page branding and classification

**As a** enterprise customer, **I want** logo, classification banner (`Confidential`), **so that** PDFs meet policy (Business doc §16 cover).

**Acceptance criteria**

- **AC-DG-10-008-01:** Tenant settings supply `logo_url`, `classification_label`, `footer_text` with size limits.
- **AC-DG-10-008-02:** Broken logo URL does not fail PDF; placeholder used.
- **AC-DG-10-008-03:** Classification appears on every page footer when configured.

---

### AC test specifications (US-DG-10-008)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-10-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-008` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Tenant settings supply `logo_url`, `classification_label`, `footer_text` with size limits. |
| **Objective** | Verify AC-DG-10-008-01: Tenant settings supply `logo_url`, `classification_label`, `footer_text` with size limits. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-008-01` |
| **Secondary / negative test ID** | `TC-DG-10-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-008-01") or Xray/TestRail key == AC-DG-10-008-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-10-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-008` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P2` / `MVP` |
| **MoSCoW** | `Could` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Broken logo URL does not fail PDF; placeholder used. |
| **Objective** | Verify AC-DG-10-008-02: Broken logo URL does not fail PDF; placeholder used. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-008-02` |
| **Secondary / negative test ID** | `TC-DG-10-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-008-02") or Xray/TestRail key == AC-DG-10-008-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-10-008-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-008` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Classification appears on every page footer when configured. |
| **Objective** | Verify AC-DG-10-008-03: Classification appears on every page footer when configured. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-008-03` |
| **Secondary / negative test ID** | `TC-DG-10-008-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-008-03") or Xray/TestRail key == AC-DG-10-008-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-10-009 — Digital fingerprint / hash page for integrity

**As a** recipient, **I want** SHA-256 of PDF printed on appendix, **so that** I can verify file integrity out-of-band.

**Acceptance criteria**

- **AC-DG-10-009-01:** Printed hash matches `artifacts.checksum_sha256` for stored object.
- **AC-DG-10-009-02:** Optional PGP signing is deployment-specific (document if supported).
- **AC-DG-10-009-03:** UI displays same hash next to download (EPIC-DG-12).

---

### AC test specifications (US-DG-10-009)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-10-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-009` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Printed hash matches `artifacts.checksum_sha256` for stored object. |
| **Objective** | Verify AC-DG-10-009-01: Printed hash matches `artifacts.checksum_sha256` for stored object. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-009-01` |
| **Secondary / negative test ID** | `TC-DG-10-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-009-01") or Xray/TestRail key == AC-DG-10-009-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-10-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-009` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P2` / `Post-MVP` |
| **MoSCoW** | `Could` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `2` |
| **Requirement (verbatim)** | Optional PGP signing is deployment-specific (document if supported). |
| **Objective** | Verify AC-DG-10-009-02: Optional PGP signing is deployment-specific (document if supported). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-10-009-02` |
| **Secondary / negative test ID** | `TC-DG-10-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-009-02") or Xray/TestRail key == AC-DG-10-009-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-10-009-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-009` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-12`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | UI displays same hash next to download (EPIC-DG-12). |
| **Objective** | Verify AC-DG-10-009-03: UI displays same hash next to download (EPIC-DG-12). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-009-03` |
| **Secondary / negative test ID** | `TC-DG-10-009-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-009-03") or Xray/TestRail key == AC-DG-10-009-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-10-010 — Report generation idempotency on retry

**As a** worker, **I want** Penelope retries not to duplicate PDFs with different ids, **so that** artefact inventory stays clean.

**Acceptance criteria**

- **AC-DG-10-010-01:** Re-invoking Penelope after success returns same `report_artifact_id` or supersedes with version pointer (document).
- **AC-DG-10-010-02:** Partial PDF write never exposes corrupt download; atomic rename pattern.
- **AC-DG-10-010-03:** Failed PDF render sets `error_code` on scan and retains logs.

---

### AC test specifications (US-DG-10-010)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-10-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-010` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Re-invoking Penelope after success returns same `report_artifact_id` or supersedes with version pointer (document). |
| **Objective** | Verify AC-DG-10-010-01: Re-invoking Penelope after success returns same `report_artifact_id` or supersedes with version pointer (document). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-010-01` |
| **Secondary / negative test ID** | `TC-DG-10-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-010-01") or Xray/TestRail key == AC-DG-10-010-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-10-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-010` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Partial PDF write never exposes corrupt download; atomic rename pattern. |
| **Objective** | Verify AC-DG-10-010-02: Partial PDF write never exposes corrupt download; atomic rename pattern. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-010-02` |
| **Secondary / negative test ID** | `TC-DG-10-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-010-02") or Xray/TestRail key == AC-DG-10-010-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-10-010-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-010` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Failed PDF render sets `error_code` on scan and retains logs. |
| **Objective** | Verify AC-DG-10-010-03: Failed PDF render sets `error_code` on scan and retains logs. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-010-03` |
| **Secondary / negative test ID** | `TC-DG-10-010-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-010-03") or Xray/TestRail key == AC-DG-10-010-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-10-011 — Appendix C scan configuration dump

**As an** assessor, **I want** redacted `job_config` JSON in appendix, **so that** methodology reviewers see scope.

**Acceptance criteria**

- **AC-DG-10-011-01:** Secrets and credential refs replaced with `[REDACTED]` literal (Architecture §20.3).
- **AC-DG-10-011-02:** Includes `policy_versions` map used for the run (Architecture §29.1).
- **AC-DG-10-011-03:** Includes model routing summary (which providers invoked) without API keys.

### AC test specifications (US-DG-10-011)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-10-011-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-011` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Secrets and credential refs replaced with `[REDACTED]` literal (Architecture §20.3). |
| **Objective** | Verify AC-DG-10-011-01: Secrets and credential refs replaced with `[REDACTED]` literal (Architecture §20.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-011-01` |
| **Secondary / negative test ID** | `TC-DG-10-011-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-011-01") or Xray/TestRail key == AC-DG-10-011-01 |
| **Spec references** | Architecture §20.3 |

#### Test specification — AC-DG-10-011-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-011` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Includes `policy_versions` map used for the run (Architecture §29.1). |
| **Objective** | Verify AC-DG-10-011-02: Includes `policy_versions` map used for the run (Architecture §29.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-011-02` |
| **Secondary / negative test ID** | `TC-DG-10-011-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-011-02") or Xray/TestRail key == AC-DG-10-011-02 |
| **Spec references** | Architecture §29.1 |

#### Test specification — AC-DG-10-011-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-10-011` |
| **Parent EPIC** | `EPIC-DG-10` |
| **Owning squad / role** | `remediation-reporting` / `security_engineer` |
| **Phase mapping** | primary `L11`; secondary `L12` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Includes model routing summary (which providers invoked) without API keys. |
| **Objective** | Verify AC-DG-10-011-03: Includes model routing summary (which providers invoked) without API keys. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-10-011-03` |
| **Secondary / negative test ID** | `TC-DG-10-011-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-10-011-03") or Xray/TestRail key == AC-DG-10-011-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## Epic Definition of Done checklist

- [ ] All in-scope ACs for `EPIC-DG-10` implemented by `remediation-reporting` and linked to automated tests (`TC-DG-*`).
- [ ] Unit coverage on touched packages is >=80%.
- [ ] Integration tests pass for all required ACs.
- [ ] Playwright BDD updated where `test_layer_required` includes `bdd`.
- [ ] Observability hooks and stable `error_code` behaviour validated.
- [ ] Security/data-sovereignty constraints verified (no secret leaks, tenant isolation).
- [ ] Design spec for slice exists under `docs/design/` with approved status.
