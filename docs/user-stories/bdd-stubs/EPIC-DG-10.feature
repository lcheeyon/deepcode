# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_10
Feature: EPIC-DG-10 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_10_001_01 @us_US_DG_10_001 @squad_remediation_reporting
  Scenario: AC-DG-10-001-01 — Sections 1–13 from §18.1 appear with stable ordering and anchors.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_001_02 @us_US_DG_10_001 @squad_remediation_reporting
  Scenario: AC-DG-10-001-02 — Same inputs + policy version yield structurally identical skeleton (determinism goal Architecture §2.3) — allow bounded LLM variance only in narrative blocks explicitly flagged “L…
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_002_01 @us_US_DG_10_002 @squad_remediation_reporting
  Scenario: AC-DG-10-002-01 — ReportLab pipeline bundles CJK fonts (STHeiti/Songti) in image layer (Architecture §18.2; Business doc §16).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_003_01 @us_US_DG_10_003 @squad_remediation_reporting
  Scenario: AC-DG-10-003-01 — Final `report.pdf` registered in `artifacts` with `checksum_sha256`, encryption mode, optional `expires_at` for presigned flows (Architecture §29.1, §32.1).
    # phase: L11 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_003_02 @us_US_DG_10_003 @squad_remediation_reporting
  Scenario: AC-DG-10-003-02 — Default retention aligns to 7-year audit requirement where configured (Architecture §14.2, §32.2).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_004_01 @us_US_DG_10_004 @squad_remediation_reporting
  Scenario: AC-DG-10-004-01 — Appendix B lists `file_path:line` or cloud ARN references matching DB `evidence_refs` JSON (Architecture §18.1; §29.1).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_005_01 @us_US_DG_10_005 @squad_remediation_reporting
  Scenario: AC-DG-10-005-01 — Appendix documents tool versions, LLM models, cache thresholds, known truncation warnings (Architecture §18.1 item 11).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_006_01 @us_US_DG_10_006 @squad_remediation_reporting
  Scenario: AC-DG-10-006-01 — Charts generated via matplotlib or equivalent; embedded as vector or high-DPI raster in PDF.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_006_02 @us_US_DG_10_006 @squad_remediation_reporting
  Scenario: AC-DG-10-006-02 — Chart data JSON archived alongside PDF for reproducibility.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_006_03 @us_US_DG_10_006 @squad_remediation_reporting
  Scenario: AC-DG-10-006-03 — Failure to render chart downgrades to table without failing scan.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-006-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_007_01 @us_US_DG_10_007 @squad_remediation_reporting
  Scenario: AC-DG-10-007-01 — Jinja → Markdown stage stored as artifact kind `report_md` with checksum (Architecture §18.2).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_007_02 @us_US_DG_10_007 @squad_remediation_reporting
  Scenario: AC-DG-10-007-02 — Markdown excludes raw secrets; same redaction rules as PDF (Architecture §20.3).
    # phase: L11 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_007_03 @us_US_DG_10_007 @squad_remediation_reporting
  Scenario: AC-DG-10-007-03 — Download path mirrors PDF artefact API pattern (EPIC-DG-02).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-007-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_008_01 @us_US_DG_10_008 @squad_remediation_reporting
  Scenario: AC-DG-10-008-01 — Tenant settings supply `logo_url`, `classification_label`, `footer_text` with size limits.
    # phase: L11 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_008_02 @us_US_DG_10_008 @squad_remediation_reporting
  Scenario: AC-DG-10-008-02 — Broken logo URL does not fail PDF; placeholder used.
    # phase: L11 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_008_03 @us_US_DG_10_008 @squad_remediation_reporting
  Scenario: AC-DG-10-008-03 — Classification appears on every page footer when configured.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_009_01 @us_US_DG_10_009 @squad_remediation_reporting
  Scenario: AC-DG-10-009-01 — Printed hash matches `artifacts.checksum_sha256` for stored object.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_009_02 @us_US_DG_10_009 @squad_remediation_reporting
  Scenario: AC-DG-10-009-02 — Optional PGP signing is deployment-specific (document if supported).
    # phase: L11 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_009_03 @us_US_DG_10_009 @squad_remediation_reporting
  Scenario: AC-DG-10-009-03 — UI displays same hash next to download (EPIC-DG-12).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-009-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_010_01 @us_US_DG_10_010 @squad_remediation_reporting
  Scenario: AC-DG-10-010-01 — Re-invoking Penelope after success returns same `report_artifact_id` or supersedes with version pointer (document).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_010_02 @us_US_DG_10_010 @squad_remediation_reporting
  Scenario: AC-DG-10-010-02 — Partial PDF write never exposes corrupt download; atomic rename pattern.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_010_03 @us_US_DG_10_010 @squad_remediation_reporting
  Scenario: AC-DG-10-010-03 — Failed PDF render sets `error_code` on scan and retains logs.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-010-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_011_01 @us_US_DG_10_011 @squad_remediation_reporting
  Scenario: AC-DG-10-011-01 — Secrets and credential refs replaced with `[REDACTED]` literal (Architecture §20.3).
    # phase: L11 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-011-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_011_02 @us_US_DG_10_011 @squad_remediation_reporting
  Scenario: AC-DG-10-011-02 — Includes `policy_versions` map used for the run (Architecture §29.1).
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-011-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.

  @ac_AC_DG_10_011_03 @us_US_DG_10_011 @squad_remediation_reporting
  Scenario: AC-DG-10-011-03 — Includes model routing summary (which providers invoked) without API keys.
    # phase: L11 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-10-011-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-10.
