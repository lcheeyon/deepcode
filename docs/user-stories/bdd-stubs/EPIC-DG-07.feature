# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_07
Feature: EPIC-DG-07 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_07_001_01 @us_US_DG_07_001 @squad_connectors
  Scenario: AC-DG-07-001-01 — Parser registry includes backends listed in §15.1 for GA targets (Terraform, CFN, K8s, Ali ROS, Huawei template).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_001_02 @us_US_DG_07_001 @squad_connectors
  Scenario: AC-DG-07-001-02 — Tool execution uses `safe_read` sandbox — no path traversal (Architecture §6.5, §20.3).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_002_01 @us_US_DG_07_002 @squad_connectors
  Scenario: AC-DG-07-002-01 — `max_iterations` default 5 per agent configuration (Architecture §3.1).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_002_02 @us_US_DG_07_002 @squad_connectors
  Scenario: AC-DG-07-002-02 — Tool failures append `AgentError`, mark resource `SKIPPED`, continue when non-fatal (Architecture §31.4).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_003_01 @us_US_DG_07_003 @squad_connectors
  Scenario: AC-DG-07-003-01 — Interface methods include IAM/network/storage/compute/encryption/audit accessors (Architecture §15.2).
    # phase: L9 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_003_02 @us_US_DG_07_003 @squad_connectors
  Scenario: AC-DG-07-003-02 — AWS + Alibaba + Tencent + Huawei connectors enumerated in Chinese business doc map to same `ResourceSnapshot` canonical model (Business doc §13–§14).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_004_01 @us_US_DG_07_004 @squad_connectors
  Scenario: AC-DG-07-004-01 — Cloud credentials documented as read-only IAM/CAM policies (Architecture §2.3; Business doc §13.x).
    # phase: L9 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_004_02 @us_US_DG_07_004 @squad_connectors
  Scenario: AC-DG-07-004-02 — No write APIs invoked in connector code paths (static analysis / contract tests).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-004-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_005_01 @us_US_DG_07_005 @squad_connectors
  Scenario: AC-DG-07-005-01 — `CloudConnectorError` triggers degraded snapshot with explicit coverage gaps in report appendix (Architecture §19.1).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_006_01 @us_US_DG_07_006 @squad_connectors
  Scenario: AC-DG-07-006-01 — `kubernetes-validate` (or successor) integrated; invalid manifests produce `SKIPPED` with reason (Architecture §15.1).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_006_02 @us_US_DG_07_006 @squad_connectors
  Scenario: AC-DG-07-006-02 — Findings reference `namespace/kind/name` keys in evidence.
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_006_03 @us_US_DG_07_006 @squad_connectors
  Scenario: AC-DG-07-006-03 — Helm charts expanded with `helm template` when `scan_layers.iac` includes helm (beta documented Architecture §11.2).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-006-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_007_01 @us_US_DG_07_007 @squad_connectors
  Scenario: AC-DG-07-007-01 — Parser extracts module tree to max depth configurable; truncates with warning (Architecture §11.6 spirit).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_007_02 @us_US_DG_07_007 @squad_connectors
  Scenario: AC-DG-07-007-02 — Provider `required_version` and `terraform` block constraints appear in structured summary passed to Athena.
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_007_03 @us_US_DG_07_007 @squad_connectors
  Scenario: AC-DG-07-007-03 — Remote modules referenced by git URL recorded as third-party risk flag (Business doc supply chain).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-007-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_008_01 @us_US_DG_07_008 @squad_connectors
  Scenario: AC-DG-07-008-01 — Each connector has `pytest-recording` cassette suite with secrets redacted (Architecture §33.1).
    # phase: L9 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_008_02 @us_US_DG_07_008 @squad_connectors
  Scenario: AC-DG-07-008-02 — CI runs contract suite on provider SDK upgrades gated by maintainer approval.
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_008_03 @us_US_DG_07_008 @squad_connectors
  Scenario: AC-DG-07-008-03 — Recorded responses versioned with `schema_ver` bump when normaliser changes.
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_009_01 @us_US_DG_07_009 @squad_connectors
  Scenario: AC-DG-07-009-01 — Every snapshot JSON includes `schema_ver` and `provider` and `captured_at`.
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_009_02 @us_US_DG_07_009 @squad_connectors
  Scenario: AC-DG-07-009-02 — Breaking normaliser changes bump `schema_ver` and trigger regression evals (EPIC-DG-11).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_009_03 @us_US_DG_07_009 @squad_connectors
  Scenario: AC-DG-07-009-03 — Unknown resource types preserved as raw blob under typed envelope for forward compatibility.
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-009-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_010_01 @us_US_DG_07_010 @squad_connectors
  Scenario: AC-DG-07-010-01 — Alibaba: ActionTrail multi-region, OSS public access, ACK API exposure checks present in connector output mapping table (Business doc §13.1).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_010_02 @us_US_DG_07_010 @squad_connectors
  Scenario: AC-DG-07-010-02 — Tencent: CloudAudit, COS public ACL, CWP coverage signals present (Business doc §13.2).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_010_03 @us_US_DG_07_010 @squad_connectors
  Scenario: AC-DG-07-010-03 — Huawei: CTS, DEW/SM4 encryption flags, CBH presence captured where API allows (Business doc §13.3).
    # phase: L9 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-010-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_011_01 @us_US_DG_07_011 @squad_connectors
  Scenario: AC-DG-07-011-01 — Throttling uses jittered backoff; max retry count documented per SDK call site.
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-011-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_011_02 @us_US_DG_07_011 @squad_connectors
  Scenario: AC-DG-07-011-02 — Pagination cursors for massive IAM policy sets do not OOM; spill to artifact ref (Architecture §5.3).
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-011-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_011_03 @us_US_DG_07_011 @squad_connectors
  Scenario: AC-DG-07-011-03 — Partial completion sets `cloud_findings` metadata `coverage=partial` with reasons.
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-011-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_012_01 @us_US_DG_07_012 @squad_connectors
  Scenario: AC-DG-07-012-01 — Feature flag gates CDK/Bicep/Pulumi parsers listed Architecture §15.1; disabled by default in MVP if unstable.
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-012-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_012_02 @us_US_DG_07_012 @squad_connectors
  Scenario: AC-DG-07-012-02 — When disabled, scan does not fail; stage skipped with user-visible notice.
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-012-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.

  @ac_AC_DG_07_012_03 @us_US_DG_07_012 @squad_connectors
  Scenario: AC-DG-07-012-03 — When enabled, findings tagged `layer=IAC` and `parser_version` set for audit.
    # phase: L9 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-07-012-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-07.
