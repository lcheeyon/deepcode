# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_05
Feature: EPIC-DG-05 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_05_001_01 @us_US_DG_05_001 @squad_policy
  Scenario: AC-DG-05-001-01 — Response lists `policy_id`, human title, `policy_version`, framework family (Architecture §28.3; registry §16.1).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_001_02 @us_US_DG_05_001 @squad_policy
  Scenario: AC-DG-05-001-02 — Deprecated policies flagged but still listable for historical scans.
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_002_01 @us_US_DG_05_002 @squad_policy
  Scenario: AC-DG-05-002-01 — Multipart upload accepted only for `admin` role (Architecture §28.3).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_002_02 @us_US_DG_05_002 @squad_policy
  Scenario: AC-DG-05-002-02 — Successful parse returns `policy_id` + `policy_version` immutably stored.
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_002_03 @us_US_DG_05_002 @squad_policy
  Scenario: AC-DG-05-002-03 — Parsed controls include `control_id`, `framework`, `scope_tags`, `layer_relevance`, `test_procedures` (Architecture §16.2).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-002-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_003_01 @us_US_DG_05_003 @squad_policy
  Scenario: AC-DG-05-003-01 — Redis policy parse cache key includes `policy_id` + `policy_version` TTL until version change (Architecture §9.4).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_003_02 @us_US_DG_05_003 @squad_policy
  Scenario: AC-DG-05-003-02 — Repo fingerprint / delta logic respects policy version changes (Architecture §23.1 Q7).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_004_01 @us_US_DG_05_004 @squad_policy
  Scenario: AC-DG-05-004-01 — For frameworks flagged as Chinese regulatory, `chinese_title` populated when source document provides it (Architecture §16.2; Business doc §15).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_005_01 @us_US_DG_05_005 @squad_policy
  Scenario: AC-DG-05-005-01 — Schema validates control list: required fields match `PolicyControl` subset before Tiresias enrichment pass (Architecture §16.2).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_005_02 @us_US_DG_05_005 @squad_policy
  Scenario: AC-DG-05-005-02 — Invalid file returns field-level validation errors (EPIC-DG-02 problem JSON).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-005-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_005_03 @us_US_DG_05_005 @squad_policy
  Scenario: AC-DG-05-005-03 — Pack upload assigns monotonic `policy_version` string immutable after publish.
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-005-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_006_01 @us_US_DG_05_006 @squad_policy
  Scenario: AC-DG-05-006-01 — PDF text extraction handles multi-column layouts where possible; OCR path documented for scanned PDFs (quality warning).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_006_02 @us_US_DG_05_006 @squad_policy
  Scenario: AC-DG-05-006-02 — Each extracted control gets `scope_tags` and `layer_relevance` inferred with confidence; low confidence flagged for human review list.
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_006_03 @us_US_DG_05_006 @squad_policy
  Scenario: AC-DG-05-006-03 — Token usage for parse attributed to tenant cost (EPIC-DG-11).
    # phase: L7 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-006-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_007_01 @us_US_DG_05_007 @squad_policy
  Scenario: AC-DG-05-007-01 — After parse, batch embed policy chunks into `policy_chunks` with `policy_version` and `framework` (Architecture §12.1–12.2).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_007_02 @us_US_DG_05_007 @squad_policy
  Scenario: AC-DG-05-007-02 — Re-embedding skipped when version unchanged and `force_reindex=false`.
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_007_03 @us_US_DG_05_007 @squad_policy
  Scenario: AC-DG-05-007-03 — Embedding model id stored on policy version metadata for reproducibility (EPIC-DG-10).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-007-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_008_01 @us_US_DG_05_008 @squad_policy
  Scenario: AC-DG-05-008-01 — `COMPLIANCE_FRAMEWORKS` loader reads from DB or packaged YAML list; adding row enables `policy_ids` selection (Architecture §16.1).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_008_02 @us_US_DG_05_008 @squad_policy
  Scenario: AC-DG-05-008-02 — Unknown `policy_id` on `CreateScanRequest` rejected at validation with list of valid ids.
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_008_03 @us_US_DG_05_008 @squad_policy
  Scenario: AC-DG-05-008-03 — Framework metadata includes jurisdiction tags (`EU`, `CN`, `SG`) for UI filtering (Business doc §15).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_009_01 @us_US_DG_05_009 @squad_policy
  Scenario: AC-DG-05-009-01 — `GET /v1/policies/{policy_id}/diff?from=&to=` returns added/removed/changed `control_id` list.
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_009_02 @us_US_DG_05_009 @squad_policy
  Scenario: AC-DG-05-009-02 — Changed text highlights truncated to safe size; full text via signed URL if needed.
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_009_03 @us_US_DG_05_009 @squad_policy
  Scenario: AC-DG-05-009-03 — Diff accessible to `admin` and `auditor`; not to unauthenticated callers.
    # phase: L7 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-009-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_010_01 @us_US_DG_05_010 @squad_policy
  Scenario: AC-DG-05-010-01 — `PolicyControl.test_procedures` non-empty for catalog controls ≥90% (NFR target; document exceptions).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_010_02 @us_US_DG_05_010 @squad_policy
  Scenario: AC-DG-05-010-02 — Athena batching clusters by `scope_tags` using procedures hash in metadata (Architecture §31.3).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.

  @ac_AC_DG_05_010_03 @us_US_DG_05_010 @squad_policy
  Scenario: AC-DG-05-010-03 — Missing procedures downgrade control to “manual review recommended” banner in report (EPIC-DG-10).
    # phase: L7 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-05-010-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-05.
