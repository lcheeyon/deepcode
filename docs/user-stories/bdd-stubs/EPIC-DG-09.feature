# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_09
Feature: EPIC-DG-09 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_09_001_01 @us_US_DG_09_001 @squad_remediation_reporting
  Scenario: AC-DG-09-001-01 — Patches never auto-apply; include `test_suggestion` field (Architecture §17.1–17.2).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_001_02 @us_US_DG_09_001 @squad_remediation_reporting
  Scenario: AC-DG-09-001-02 — Security-critical patches include `risk_of_fix` (Architecture §17.2).
    # phase: L11 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_001_03 @us_US_DG_09_001 @squad_remediation_reporting
  Scenario: AC-DG-09-001-03 — Multi-file patches include ordering metadata (Architecture §17.2).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-001-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_002_01 @us_US_DG_09_002 @squad_remediation_reporting
  Scenario: AC-DG-09-002-01 — When `circe_terraform_validation=true`, run fmt-check/validate/tflint where Terraform present (Architecture §23.1 Q10).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_002_02 @us_US_DG_09_002 @squad_remediation_reporting
  Scenario: AC-DG-09-002-02 — Record `remediation.validation_status` + stdout/stderr excerpts; failures do not fail entire scan (Architecture §23.1 Q10).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_003_01 @us_US_DG_09_003 @squad_remediation_reporting
  Scenario: AC-DG-09-003-01 — Remediation type `generate_cli_remediation` supported with provider tagging (Architecture §17.1; Business doc §11.3 examples).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_004_01 @us_US_DG_09_004 @squad_remediation_reporting
  Scenario: AC-DG-09-004-01 — `generate_iac_patch` tool produces diff with file path headers per resource block (Architecture §17.1).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_004_02 @us_US_DG_09_004 @squad_remediation_reporting
  Scenario: AC-DG-09-004-02 — Multi-file IaC patches include explicit file order metadata (Architecture §17.2).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-004-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_004_03 @us_US_DG_09_004 @squad_remediation_reporting
  Scenario: AC-DG-09-004-03 — Patches never include secrets or data values from live cloud — only template fixes (Architecture §2.3).
    # phase: L11 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-004-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_005_01 @us_US_DG_09_005 @squad_remediation_reporting
  Scenario: AC-DG-09-005-01 — Sorting uses severity, CVSS when present, exploitability hints, and estimated effort enum (Architecture §18.1 item 10).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_005_02 @us_US_DG_09_005 @squad_remediation_reporting
  Scenario: AC-DG-09-005-02 — Ordering dependencies between remediations validated acyclic; cycles broken with warning.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-005-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_005_03 @us_US_DG_09_005 @squad_remediation_reporting
  Scenario: AC-DG-09-005-03 — Export to CSV/JSON includes `remediation_id` joinable to `finding_id`.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-005-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_006_01 @us_US_DG_09_006 @squad_remediation_reporting
  Scenario: AC-DG-09-006-01 — Patch validator rejects hunks introducing new import statements unless `admin_override` flag on job (document risk).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_006_02 @us_US_DG_09_006 @squad_remediation_reporting
  Scenario: AC-DG-09-006-02 — Violations surface as `remediation.status=rejected_guardrail` with machine reason.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_006_03 @us_US_DG_09_006 @squad_remediation_reporting
  Scenario: AC-DG-09-006-03 — Report appendix lists skipped remediations with guardrail reason.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-006-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_007_01 @us_US_DG_09_007 @squad_remediation_reporting
  Scenario: AC-DG-09-007-01 — Output format `json_patch` or strategic merge documented per finding type.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_007_02 @us_US_DG_09_007 @squad_remediation_reporting
  Scenario: AC-DG-09-007-02 — Patches reference GVK + namespace + name in metadata (EPIC-DG-07).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_007_03 @us_US_DG_09_007 @squad_remediation_reporting
  Scenario: AC-DG-09-007-03 — Dry-run instructions included in `test_suggestion` field.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-007-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_008_01 @us_US_DG_09_008 @squad_remediation_reporting
  Scenario: AC-DG-09-008-01 — `Remediation` model includes `finding_id` + `control_id` + `framework` foreign keys or string ids matching findings table.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_008_02 @us_US_DG_09_008 @squad_remediation_reporting
  Scenario: AC-DG-09-008-02 — API `GET …/remediations` optional endpoint or embedded in findings export (EPIC-DG-02).
    # phase: L11 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.

  @ac_AC_DG_09_008_03 @us_US_DG_09_008 @squad_remediation_reporting
  Scenario: AC-DG-09-008-03 — PDF section cross-links finding number to remediation number (EPIC-DG-10).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-09-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-09.
