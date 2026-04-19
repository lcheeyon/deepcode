> **Generated** — AC test specifications for QA/traceability. **Canonical backlog (edit here):** [`EPIC-04-ingestion-hermes.md`](../EPIC-04-ingestion-hermes.md). **Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.

# EPIC-DG-04 — Ingestion gateway (Hermes)

> **AC-level test specifications (generated):** Squad copy [`squads/ingestion-codeintel/EPIC-DG-04-detailed.md`](squads/ingestion-codeintel/EPIC-DG-04-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then `python3 scripts/validate_user_stories_traceability.py`.


**Goal:** Acquire source artefacts, optional IaC bundles, and read-only cloud snapshots into the secure work area and object store per `Architecture_Design.md` §11.1, §32 and product docs (Git/ZIP/CI).

**Primary personas:** Developer, CI system, Cloud admin.

---


## US-DG-04-001 — Clone Git repository (shallow by default)

**As a** developer, **I want** Hermes to clone my repo ref, **so that** downstream agents analyse the intended revision.

**Wireframe — repo picker**

```text
┌──────── Repository source ──────────────────┐
│ Provider: ( ) GitHub (x) GitLab ( ) Gitee   │
│ URL: [https://gitlab.com/acme/api.git]     │
│ Ref: [main]   Depth: [50 ▼]                │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-04-001-01:** Supports HTTPS/SSH clone paths documented for GitHub/GitLab/Gitee/Bitbucket (Architecture §11.1; Business doc §4).
- **AC-DG-04-001-02:** `REPO_CLONE_DEPTH` default applied unless overridden by allowed job config (Architecture §27.2).
- **AC-DG-04-001-03:** On success, `repo_local_path` and `repo_metadata` populated in `ScanState` (Architecture §4.2, §5.4).

---

### AC test specifications (US-DG-04-001)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-04-001-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-001` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Supports HTTPS/SSH clone paths documented for GitHub/GitLab/Gitee/Bitbucket (Architecture §11.1; Business doc §4). |
| **Objective** | Verify AC-DG-04-001-01: Supports HTTPS/SSH clone paths documented for GitHub/GitLab/Gitee/Bitbucket (Architecture §11.1; Business doc §4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-001-01` |
| **Secondary / negative test ID** | `TC-DG-04-001-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-001-01") or Xray/TestRail key == AC-DG-04-001-01 |
| **Spec references** | Architecture §11.1; Business doc §4 |

#### Test specification — AC-DG-04-001-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-001` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `REPO_CLONE_DEPTH` default applied unless overridden by allowed job config (Architecture §27.2). |
| **Objective** | Verify AC-DG-04-001-02: `REPO_CLONE_DEPTH` default applied unless overridden by allowed job config (Architecture §27.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-001-02` |
| **Secondary / negative test ID** | `TC-DG-04-001-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-001-02") or Xray/TestRail key == AC-DG-04-001-02 |
| **Spec references** | Architecture §27.2 |

#### Test specification — AC-DG-04-001-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-001` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | On success, `repo_local_path` and `repo_metadata` populated in `ScanState` (Architecture §4.2, §5.4). |
| **Objective** | Verify AC-DG-04-001-03: On success, `repo_local_path` and `repo_metadata` populated in `ScanState` (Architecture §4.2, §5.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-001-03` |
| **Secondary / negative test ID** | `TC-DG-04-001-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-001-03") or Xray/TestRail key == AC-DG-04-001-03 |
| **Spec references** | Architecture §4.2, §5.4 |


## US-DG-04-002 — Enforce repository size limits

**As a** platform operator, **I want** ingestion to abort oversized archives, **so that** workers are protected from OOM.

**Acceptance criteria**

- **AC-DG-04-002-01:** `REPO_MAX_BYTES` soft cap enforced with clear `ScanAbortError` / `error_code` (Architecture §27.2, §19.1).
- **AC-DG-04-002-02:** ZIP/tarball uploads respect max compressed size policy (2GB in Architecture §11.1).

---

### AC test specifications (US-DG-04-002)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-04-002-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-002` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `REPO_MAX_BYTES` soft cap enforced with clear `ScanAbortError` / `error_code` (Architecture §27.2, §19.1). |
| **Objective** | Verify AC-DG-04-002-01: `REPO_MAX_BYTES` soft cap enforced with clear `ScanAbortError` / `error_code` (Architecture §27.2, §19.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-002-01` |
| **Secondary / negative test ID** | `TC-DG-04-002-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-002-01") or Xray/TestRail key == AC-DG-04-002-01 |
| **Spec references** | Architecture §27.2, §19.1 |

#### Test specification — AC-DG-04-002-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-002` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | ZIP/tarball uploads respect max compressed size policy (2GB in Architecture §11.1). |
| **Objective** | Verify AC-DG-04-002-02: ZIP/tarball uploads respect max compressed size policy (2GB in Architecture §11.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-002-02` |
| **Secondary / negative test ID** | `TC-DG-04-002-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-002-02") or Xray/TestRail key == AC-DG-04-002-02 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-04-003 — Stage encrypted repo archive to object store

**As a** compliance officer, **I want** raw artefacts stored encrypted with lifecycle, **so that** evidence handling matches retention policy.

**Acceptance criteria**

- **AC-DG-04-003-01:** Object key layout `…/scans/{scan_id}/repo.tar.zst` (or equivalent) per §32.1.
- **AC-DG-04-003-02:** Default deletion of repo archive 24h after `COMPLETE` unless tenant override `retention_repo_archive_hours` (Architecture §32.2, §24.1).

---

### AC test specifications (US-DG-04-003)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-04-003-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-003` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Object key layout `…/scans/{scan_id}/repo.tar.zst` (or equivalent) per §32.1. |
| **Objective** | Verify AC-DG-04-003-01: Object key layout `…/scans/{scan_id}/repo.tar.zst` (or equivalent) per §32.1. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-003-01` |
| **Secondary / negative test ID** | `TC-DG-04-003-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-003-01") or Xray/TestRail key == AC-DG-04-003-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-04-003-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-003` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Default deletion of repo archive 24h after `COMPLETE` unless tenant override `retention_repo_archive_hours` (Architecture §32.2, §24.1). |
| **Objective** | Verify AC-DG-04-003-02: Default deletion of repo archive 24h after `COMPLETE` unless tenant override `retention_repo_archive_hours` (Architecture §32.2, §24.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-003-02` |
| **Secondary / negative test ID** | `TC-DG-04-003-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-003-02") or Xray/TestRail key == AC-DG-04-003-02 |
| **Spec references** | Architecture §32.2, §24.1 |


## US-DG-04-004 — Capture read-only cloud snapshots

**As a** cloud admin, **I want** Hermes to invoke connectors with short-lived creds, **so that** Cassandra analyses current posture.

**Wireframe — cloud profile card**

```text
┌──────── Cloud profile: aws-prod-ro ────────┐
│ Provider: AWS   Regions: ap-southeast-1      │
│ Credential ref: calypso://secret/aws-ro    │
│ [ Test connectivity ]   Status: OK         │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-04-004-01:** Cloud credentials resolved via Calypso pattern with ≤15m TTL; secrets never persisted in `ScanState` (Architecture §20.1).
- **AC-DG-04-004-02:** `cloud_snapshots` map keyed by `profile_id` stored as artifact refs when large (Architecture §5.3, §23.1 Q4).

---

### AC test specifications (US-DG-04-004)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-04-004-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-004` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Cloud credentials resolved via Calypso pattern with ≤15m TTL; secrets never persisted in `ScanState` (Architecture §20.1). |
| **Objective** | Verify AC-DG-04-004-01: Cloud credentials resolved via Calypso pattern with ≤15m TTL; secrets never persisted in `ScanState` (Architecture §20.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-004-01` |
| **Secondary / negative test ID** | `TC-DG-04-004-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-004-01") or Xray/TestRail key == AC-DG-04-004-01 |
| **Spec references** | Architecture §20.1 |

#### Test specification — AC-DG-04-004-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-004` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `cloud_snapshots` map keyed by `profile_id` stored as artifact refs when large (Architecture §5.3, §23.1 Q4). |
| **Objective** | Verify AC-DG-04-004-02: `cloud_snapshots` map keyed by `profile_id` stored as artifact refs when large (Architecture §5.3, §23.1 Q4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-004-02` |
| **Secondary / negative test ID** | `TC-DG-04-004-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-004-02") or Xray/TestRail key == AC-DG-04-004-02 |
| **Spec references** | Architecture §5.3, §23.1 Q4 |


## US-DG-04-005 — IaC-only / cloud-only scan entry points

**As a** solutions architect, **I want** to run scans without all three layers, **so that** I can scope PoCs.

**Acceptance criteria**

- **AC-DG-04-005-01:** IaC-only path accepts Terraform plan JSON / templates per ingestion table (Architecture §11.1).
- **AC-DG-04-005-02:** Cloud-only path permitted when `repo` absent but `cloud_profiles` present and `scan_layers.cloud=true` (Architecture §28.4).

---

### AC test specifications (US-DG-04-005)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-04-005-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-005` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | IaC-only path accepts Terraform plan JSON / templates per ingestion table (Architecture §11.1). |
| **Objective** | Verify AC-DG-04-005-01: IaC-only path accepts Terraform plan JSON / templates per ingestion table (Architecture §11.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-005-01` |
| **Secondary / negative test ID** | `TC-DG-04-005-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-005-01") or Xray/TestRail key == AC-DG-04-005-01 |
| **Spec references** | Architecture §11.1 |

#### Test specification — AC-DG-04-005-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-005` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Cloud-only path permitted when `repo` absent but `cloud_profiles` present and `scan_layers.cloud=true` (Architecture §28.4). |
| **Objective** | Verify AC-DG-04-005-02: Cloud-only path permitted when `repo` absent but `cloud_profiles` present and `scan_layers.cloud=true` (Architecture §28.4). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-005-02` |
| **Secondary / negative test ID** | `TC-DG-04-005-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-005-02") or Xray/TestRail key == AC-DG-04-005-02 |
| **Spec references** | Architecture §28.4 |


## US-DG-04-006 — Private Git over SSH or deploy keys

**As an** enterprise developer, **I want** Hermes to clone private repos using Calypso-backed credentials, **so that** internal code is scannable.

**Wireframe — credential binding**

```text
┌──────── Repo access ────────────────────────────────────────┐
│ Method: (x) SSH deploy key  ( ) HTTPS PAT (vault ref)       │
│ Secret ref: [calypso://secret/gitlab-deploy-acme]           │
│ [ Test clone ]   Last OK: 2026-04-18                         │
└──────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-04-006-01:** SSH key or PAT never logged or persisted in `job_config` plaintext; only `connector_credential_ref` style refs (Architecture §20.1).
- **AC-DG-04-006-02:** Clone failure surfaces `error_code` distinguishing auth vs network vs missing ref.
- **AC-DG-04-006-03:** Known-hosts or strict host key policy configurable for enterprise Git (document default).

---

### AC test specifications (US-DG-04-006)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-04-006-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-006` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | SSH key or PAT never logged or persisted in `job_config` plaintext; only `connector_credential_ref` style refs (Architecture §20.1). |
| **Objective** | Verify AC-DG-04-006-01: SSH key or PAT never logged or persisted in `job_config` plaintext; only `connector_credential_ref` style refs (Architecture §20.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-006-01` |
| **Secondary / negative test ID** | `TC-DG-04-006-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-006-01") or Xray/TestRail key == AC-DG-04-006-01 |
| **Spec references** | Architecture §20.1 |

#### Test specification — AC-DG-04-006-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-006` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Clone failure surfaces `error_code` distinguishing auth vs network vs missing ref. |
| **Objective** | Verify AC-DG-04-006-02: Clone failure surfaces `error_code` distinguishing auth vs network vs missing ref. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. \| 4. Execute negative path and assert stable error_code with no side effects. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-006-02` |
| **Secondary / negative test ID** | `TC-DG-04-006-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-006-02") or Xray/TestRail key == AC-DG-04-006-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-04-006-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-006` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Known-hosts or strict host key policy configurable for enterprise Git (document default). |
| **Objective** | Verify AC-DG-04-006-03: Known-hosts or strict host key policy configurable for enterprise Git (document default). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-006-03` |
| **Secondary / negative test ID** | `TC-DG-04-006-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-006-03") or Xray/TestRail key == AC-DG-04-006-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-04-007 — Monorepo sub-path scoping

**As a** repo owner, **I want** optional `repo.sub_path`, **so that** scans target `services/payments/` only.

**Acceptance criteria**

- **AC-DG-04-007-01:** When `sub_path` set, Hermes stages only that subtree; path normalisation blocks `../` escape.
- **AC-DG-04-007-02:** Argus indexing honours same root for embeddings and tools (EPIC-DG-06).
- **AC-DG-04-007-03:** Report metadata records `sub_path` for audit (EPIC-DG-10).

---

### AC test specifications (US-DG-04-007)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-04-007-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-007` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | When `sub_path` set, Hermes stages only that subtree; path normalisation blocks `../` escape. |
| **Objective** | Verify AC-DG-04-007-01: When `sub_path` set, Hermes stages only that subtree; path normalisation blocks `../` escape. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-007-01` |
| **Secondary / negative test ID** | `TC-DG-04-007-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-007-01") or Xray/TestRail key == AC-DG-04-007-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-04-007-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-007` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-06`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Argus indexing honours same root for embeddings and tools (EPIC-DG-06). |
| **Objective** | Verify AC-DG-04-007-02: Argus indexing honours same root for embeddings and tools (EPIC-DG-06). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-007-02` |
| **Secondary / negative test ID** | `TC-DG-04-007-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-007-02") or Xray/TestRail key == AC-DG-04-007-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-04-007-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-007` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-10`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Report metadata records `sub_path` for audit (EPIC-DG-10). |
| **Objective** | Verify AC-DG-04-007-03: Report metadata records `sub_path` for audit (EPIC-DG-10). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-007-03` |
| **Secondary / negative test ID** | `TC-DG-04-007-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-007-03") or Xray/TestRail key == AC-DG-04-007-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-04-008 — CI pipeline artifact ingestion

**As a** CI author, **I want** to push tarball or OCI layer digest to Hermes, **so that** I can scan build outputs without exposing full monorepo.

**Acceptance criteria**

- **AC-DG-04-008-01:** Multipart or pre-signed PUT flow documented; max size aligns `REPO_MAX_BYTES` (Architecture §11.1, §27.2).
- **AC-DG-04-008-02:** Checksum verification (`checksum_sha256`) optional but recommended; mismatch fails fast.
- **AC-DG-04-008-03:** Uploaded artefact lands under tenant-scoped object prefix before worker extract (Architecture §32.1).

---

### AC test specifications (US-DG-04-008)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-04-008-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-008` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `5` |
| **Requirement (verbatim)** | Multipart or pre-signed PUT flow documented; max size aligns `REPO_MAX_BYTES` (Architecture §11.1, §27.2). |
| **Objective** | Verify AC-DG-04-008-01: Multipart or pre-signed PUT flow documented; max size aligns `REPO_MAX_BYTES` (Architecture §11.1, §27.2). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-008-01` |
| **Secondary / negative test ID** | `TC-DG-04-008-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-008-01") or Xray/TestRail key == AC-DG-04-008-01 |
| **Spec references** | Architecture §11.1, §27.2 |

#### Test specification — AC-DG-04-008-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-008` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P2` / `Post-MVP` |
| **MoSCoW** | `Could` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `2` |
| **Requirement (verbatim)** | Checksum verification (`checksum_sha256`) optional but recommended; mismatch fails fast. |
| **Objective** | Verify AC-DG-04-008-02: Checksum verification (`checksum_sha256`) optional but recommended; mismatch fails fast. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. Feature-disabled path yields explicit skip/no-op behaviour. |
| **Primary automated test ID** | `TC-DG-04-008-02` |
| **Secondary / negative test ID** | `TC-DG-04-008-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-008-02") or Xray/TestRail key == AC-DG-04-008-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-04-008-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-008` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P0` / `MVP` |
| **MoSCoW** | `Must` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Uploaded artefact lands under tenant-scoped object prefix before worker extract (Architecture §32.1). |
| **Objective** | Verify AC-DG-04-008-03: Uploaded artefact lands under tenant-scoped object prefix before worker extract (Architecture §32.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-008-03` |
| **Secondary / negative test ID** | `TC-DG-04-008-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-008-03") or Xray/TestRail key == AC-DG-04-008-03 |
| **Spec references** | Architecture §32.1 |


## US-DG-04-009 — Full clone option for blame / history signals

**As a** security analyst, **I want** optional full clone, **so that** future agents can use git history where product enables it.

**Acceptance criteria**

- **AC-DG-04-009-01:** `job_config` flag requests depth=full; default remains shallow (Architecture §11.1).
- **AC-DG-04-009-02:** Full clone wall time surfaced in scan metadata; timeout participates in budget (EPIC-DG-01).
- **AC-DG-04-009-03:** If history unused by graph, feature is no-op aside from clone cost (document).

---

### AC test specifications (US-DG-04-009)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-04-009-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-009` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `job_config` flag requests depth=full; default remains shallow (Architecture §11.1). |
| **Objective** | Verify AC-DG-04-009-01: `job_config` flag requests depth=full; default remains shallow (Architecture §11.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-009-01` |
| **Secondary / negative test ID** | `TC-DG-04-009-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-009-01") or Xray/TestRail key == AC-DG-04-009-01 |
| **Spec references** | Architecture §11.1 |

#### Test specification — AC-DG-04-009-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-009` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-01`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Full clone wall time surfaced in scan metadata; timeout participates in budget (EPIC-DG-01). |
| **Objective** | Verify AC-DG-04-009-02: Full clone wall time surfaced in scan metadata; timeout participates in budget (EPIC-DG-01). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-009-02` |
| **Secondary / negative test ID** | `TC-DG-04-009-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-009-02") or Xray/TestRail key == AC-DG-04-009-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-04-009-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-009` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `Hardening` |
| **MoSCoW** | `Should` |
| **Requirement type** | `NFR` |
| **NFR metric / target** | `scan_cost / TBD` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `4` |
| **Requirement (verbatim)** | If history unused by graph, feature is no-op aside from clone cost (document). |
| **Objective** | Verify AC-DG-04-009-03: If history unused by graph, feature is no-op aside from clone cost (document). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-009-03` |
| **Secondary / negative test ID** | `TC-DG-04-009-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-009-03") or Xray/TestRail key == AC-DG-04-009-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-04-010 — Record resolved `repo_commit_sha` on scan

**As an** auditor, **I want** immutable commit SHA on the scan row, **so that** evidence ties to exact revision.

**Acceptance criteria**

- **AC-DG-04-010-01:** After clone, `repo_commit_sha` persisted on `scans` even when request sent only `ref` (Architecture §29.1).
- **AC-DG-04-010-02:** Detached HEAD state recorded correctly.
- **AC-DG-04-010-03:** Mismatch between requested `commit_sha` and resolved head fails with clear `error_code` when strict mode enabled.

---

### AC test specifications (US-DG-04-010)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-04-010-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-010` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | After clone, `repo_commit_sha` persisted on `scans` even when request sent only `ref` (Architecture §29.1). |
| **Objective** | Verify AC-DG-04-010-01: After clone, `repo_commit_sha` persisted on `scans` even when request sent only `ref` (Architecture §29.1). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-010-01` |
| **Secondary / negative test ID** | `TC-DG-04-010-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-010-01") or Xray/TestRail key == AC-DG-04-010-01 |
| **Spec references** | Architecture §29.1 |

#### Test specification — AC-DG-04-010-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-010` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Detached HEAD state recorded correctly. |
| **Objective** | Verify AC-DG-04-010-02: Detached HEAD state recorded correctly. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-010-02` |
| **Secondary / negative test ID** | `TC-DG-04-010-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-010-02") or Xray/TestRail key == AC-DG-04-010-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-04-010-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-010` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Mismatch between requested `commit_sha` and resolved head fails with clear `error_code` when strict mode enabled. |
| **Objective** | Verify AC-DG-04-010-03: Mismatch between requested `commit_sha` and resolved head fails with clear `error_code` when strict mode enabled. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-010-03` |
| **Secondary / negative test ID** | `TC-DG-04-010-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-010-03") or Xray/TestRail key == AC-DG-04-010-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## US-DG-04-011 — Hermes metadata for languages and file counts

**As a** mapper, **I want** `RepoMetadata` with LOC estimates and excluded binary counts, **so that** Athena can tune retrieval.

**Acceptance criteria**

- **AC-DG-04-011-01:** `repo_metadata` includes total files, ignored paths summary, binary-skipped count (fields documented in schema).
- **AC-DG-04-011-02:** Extremely large file list truncation flagged for report appendix (Architecture §11.6).
- **AC-DG-04-011-03:** Metadata serialisable size bounded; spill to artifact ref if huge (Architecture §5.3).

---

### AC test specifications (US-DG-04-011)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-04-011-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-011` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `repo_metadata` includes total files, ignored paths summary, binary-skipped count (fields documented in schema). |
| **Objective** | Verify AC-DG-04-011-01: `repo_metadata` includes total files, ignored paths summary, binary-skipped count (fields documented in schema). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-011-01` |
| **Secondary / negative test ID** | `TC-DG-04-011-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-011-01") or Xray/TestRail key == AC-DG-04-011-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-04-011-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-011` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Extremely large file list truncation flagged for report appendix (Architecture §11.6). |
| **Objective** | Verify AC-DG-04-011-02: Extremely large file list truncation flagged for report appendix (Architecture §11.6). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-011-02` |
| **Secondary / negative test ID** | `TC-DG-04-011-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-011-02") or Xray/TestRail key == AC-DG-04-011-02 |
| **Spec references** | Architecture §11.6 |

#### Test specification — AC-DG-04-011-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-011` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Metadata serialisable size bounded; spill to artifact ref if huge (Architecture §5.3). |
| **Objective** | Verify AC-DG-04-011-03: Metadata serialisable size bounded; spill to artifact ref if huge (Architecture §5.3). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-011-03` |
| **Secondary / negative test ID** | `TC-DG-04-011-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-011-03") or Xray/TestRail key == AC-DG-04-011-03 |
| **Spec references** | Architecture §5.3 |


## US-DG-04-012 — Cloud snapshot per-region fan-out and compression

**As a** multi-region customer, **I want** multiple regions per profile, **so that** Cassandra sees full estate.

**Acceptance criteria**

- **AC-DG-04-012-01:** `cloud_profiles[].regions` array honoured; failures per region recorded in snapshot metadata (EPIC-DG-07).
- **AC-DG-04-012-02:** Snapshots stored compressed (`*.json.zst`) under object layout §32.1.
- **AC-DG-04-012-03:** Partial regional success still produces snapshot with `coverage_percent` field.

### AC test specifications (US-DG-04-012)

Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.

#### Test specification — AC-DG-04-012-01

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-012` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `EPIC-DG-07`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | `cloud_profiles[].regions` array honoured; failures per region recorded in snapshot metadata (EPIC-DG-07). |
| **Objective** | Verify AC-DG-04-012-01: `cloud_profiles[].regions` array honoured; failures per region recorded in snapshot metadata (EPIC-DG-07). |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-012-01` |
| **Secondary / negative test ID** | `TC-DG-04-012-01.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-012-01") or Xray/TestRail key == AC-DG-04-012-01 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-04-012-02

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-012` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Snapshots stored compressed (`*.json.zst`) under object layout §32.1. |
| **Objective** | Verify AC-DG-04-012-02: Snapshots stored compressed (`*.json.zst`) under object layout §32.1. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-012-02` |
| **Secondary / negative test ID** | `TC-DG-04-012-02.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-012-02") or Xray/TestRail key == AC-DG-04-012-02 |
| **Spec references** | Architecture_Design.md (see product spec) |

#### Test specification — AC-DG-04-012-03

| Attribute | Specification |
|-----------|---------------|
| **Parent US** | `US-DG-04-012` |
| **Parent EPIC** | `EPIC-DG-04` |
| **Owning squad / role** | `ingestion-codeintel` / `ml_platform_engineer` |
| **Phase mapping** | primary `L6`; secondary `L8/L9` |
| **Priority / release** | `P1` / `MVP` |
| **MoSCoW** | `Should` |
| **Requirement type** | `Functional` |
| **NFR metric / target** | `- / -` |
| **Dependencies** | epics `-`; stories `-`; ACs `-` |
| **Required test layer** | `unit+integration` (min automated tests: `1`) |
| **Framework / control tags** | `-` / `-` |
| **Estimate (story points hint)** | `3` |
| **Requirement (verbatim)** | Partial regional success still produces snapshot with `coverage_percent` field. |
| **Objective** | Verify AC-DG-04-012-03: Partial regional success still produces snapshot with `coverage_percent` field. |
| **Preconditions** | Tenant and scan fixtures exist; services healthy per test environment bootstrap. |
| **Verification procedure** | 1. Arrange test data and configuration to match preconditions. \| 2. Execute the operation or graph/API path under test. \| 3. Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces. |
| **Expected result** | Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04. |
| **Edge / negative focus** | Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states. |
| **Primary automated test ID** | `TC-DG-04-012-03` |
| **Secondary / negative test ID** | `TC-DG-04-012-03.2` |
| **Automation hints** | pytest marker @pytest.mark.req("AC-DG-04-012-03") or Xray/TestRail key == AC-DG-04-012-03 |
| **Spec references** | Architecture_Design.md (see product spec) |


## Epic Definition of Done checklist

- [ ] All in-scope ACs for `EPIC-DG-04` implemented by `ingestion-codeintel` and linked to automated tests (`TC-DG-*`).
- [ ] Unit coverage on touched packages is >=80%.
- [ ] Integration tests pass for all required ACs.
- [ ] Playwright BDD updated where `test_layer_required` includes `bdd`.
- [ ] Observability hooks and stable `error_code` behaviour validated.
- [ ] Security/data-sovereignty constraints verified (no secret leaks, tenant isolation).
- [ ] Design spec for slice exists under `docs/design/` with approved status.
