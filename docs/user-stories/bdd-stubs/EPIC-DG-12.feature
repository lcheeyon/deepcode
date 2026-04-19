# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_12
Feature: EPIC-DG-12 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_12_001_01 @us_US_DG_12_001 @squad_frontend
  Scenario: AC-DG-12-001-01 — OIDC login establishes session; JWT forwarded to API on each request (maps EPIC-DG-03).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_001_02 @us_US_DG_12_001 @squad_frontend
  Scenario: AC-DG-12-001-02 — Tenant switcher (if permitted) only lists authorised tenants; default from token `tenant_id`.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_002_01 @us_US_DG_12_002 @squad_frontend
  Scenario: AC-DG-12-002-01 — Table columns include `scan_id`, `repo`, `status`, `current_stage`, `percent_complete`, `updated_at`.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_002_02 @us_US_DG_12_002 @squad_frontend
  Scenario: AC-DG-12-002-02 — Row actions deep-link to scan detail (`/scans/:id`).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_002_03 @us_US_DG_12_002 @squad_frontend
  Scenario: AC-DG-12-002-03 — Polling interval backs off when tab inactive (performance NFR).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-002-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_003_01 @us_US_DG_12_003 @squad_frontend
  Scenario: AC-DG-12-003-01 — Timeline binds to `GET /v1/scans/{id}` fields; handles `AWAITING_REVIEW` with resume CTA for authorised roles.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_003_02 @us_US_DG_12_003 @squad_frontend
  Scenario: AC-DG-12-003-02 — Cancel button calls `POST …/cancel` and disables when terminal (EPIC-DG-01/02).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_004_01 @us_US_DG_12_004 @squad_frontend
  Scenario: AC-DG-12-004-01 — Uses paginated findings API with cursor preservation in URL query.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_004_02 @us_US_DG_12_004 @squad_frontend
  Scenario: AC-DG-12-004-02 — Evidence opens read-only code viewer; never exposes raw presigned URL in logs.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-004-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_004_03 @us_US_DG_12_004 @squad_frontend
  Scenario: AC-DG-12-004-03 — Bulk select exports minimal JSON/CSV schema versioned `v1`.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-004-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_005_01 @us_US_DG_12_005 @squad_frontend
  Scenario: AC-DG-12-005-01 — Download uses artefact endpoint; handles `302` redirect transparently to browser.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_005_02 @us_US_DG_12_005 @squad_frontend
  Scenario: AC-DG-12-005-02 — UI displays checksum from API metadata (EPIC-DG-02/10).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-005-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_006_01 @us_US_DG_12_006 @squad_frontend
  Scenario: AC-DG-12-006-01 — Upload flow maps to `POST /v1/policies:upload` (EPIC-DG-05).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_006_02 @us_US_DG_12_006 @squad_frontend
  Scenario: AC-DG-12-006-02 — Error states show sanitised server messages; no stack traces to end users.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_007_01 @us_US_DG_12_007 @squad_frontend
  Scenario: AC-DG-12-007-01 — `auditor` role sees read-only merged JSON; cannot edit (EPIC-DG-03).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_008_01 @us_US_DG_12_008 @squad_frontend
  Scenario: AC-DG-12-008-01 — Form maps 1:1 to `CreateScanRequest.notifications` and `budget` (Architecture §28.4).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_008_02 @us_US_DG_12_008 @squad_frontend
  Scenario: AC-DG-12-008-02 — Webhook URL validated as HTTPS only in production (configurable exception for dev).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_008_03 @us_US_DG_12_008 @squad_frontend
  Scenario: AC-DG-12-008-03 — Test webhook button sends signed sample event (EPIC-DG-02).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_009_01 @us_US_DG_12_009 @squad_frontend
  Scenario: AC-DG-12-009-01 — Page lists composite title, severity, participating layers, evidence links.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_009_02 @us_US_DG_12_009 @squad_frontend
  Scenario: AC-DG-12-009-02 — Visual diagram export PNG optional from same data (reuse EPIC-DG-10 chart components if shared).
    # phase: L3 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_009_03 @us_US_DG_12_009 @squad_frontend
  Scenario: AC-DG-12-009-03 — Empty state explains when layer flags prevented correlation.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-009-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_010_01 @us_US_DG_12_010 @squad_frontend
  Scenario: AC-DG-12-010-01 — Keyboard navigable scan list and findings table; focus traps in modals.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_010_02 @us_US_DG_12_010 @squad_frontend
  Scenario: AC-DG-12-010-02 — Colour contrast meets AA for default theme; high-contrast theme optional.
    # phase: L3 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_010_03 @us_US_DG_12_010 @squad_frontend
  Scenario: AC-DG-12-010-03 — UI strings externalised for `en` + `zh` bundles at minimum.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-010-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_011_01 @us_US_DG_12_011 @squad_frontend
  Scenario: AC-DG-12-011-01 — Aligns with EPIC-DG-03 service account stories; UI never shows full key twice.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-011-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_011_02 @us_US_DG_12_011 @squad_frontend
  Scenario: AC-DG-12-011-02 — Key usage last_seen updated on authenticated API calls.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-011-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_011_03 @us_US_DG_12_011 @squad_frontend
  Scenario: AC-DG-12-011-03 — mTLS-only tenants hide API key UI entirely.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-011-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_012_01 @us_US_DG_12_012 @squad_frontend
  Scenario: AC-DG-12-012-01 — UI calls documented endpoint returning `redacted_excerpt` ≤4KiB policy (Architecture §23.1 Q9).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-012-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_012_02 @us_US_DG_12_012 @squad_frontend
  Scenario: AC-DG-12-012-02 — Full trace export gated behind admin break-glass (EPIC-DG-11).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-012-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_012_03 @us_US_DG_12_012 @squad_frontend
  Scenario: AC-DG-12-012-03 — Copy-to-clipboard strips HTML and limits size.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-012-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_013_01 @us_US_DG_12_013 @squad_frontend
  Scenario: AC-DG-12-013-01 — Scan detail timeline stacks vertically <768px width without horizontal scroll.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-013-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_013_02 @us_US_DG_12_013 @squad_frontend
  Scenario: AC-DG-12-013-02 — Critical actions reachable in ≤2 taps from home.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-013-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_013_03 @us_US_DG_12_013 @squad_frontend
  Scenario: AC-DG-12-013-03 — Performance: LCP <2.5s on 4G for scan list page (NFR).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-013-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_014_01 @us_US_DG_12_014 @squad_frontend
  Scenario: AC-DG-12-014-01 — Settings persist in `tenants.runtime_config` or dedicated columns per ADR.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-014-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_014_02 @us_US_DG_12_014 @squad_frontend
  Scenario: AC-DG-12-014-02 — Overrides on single scan allowed only where EPIC-DG-03 permits.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-014-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.

  @ac_AC_DG_12_014_03 @us_US_DG_12_014 @squad_frontend
  Scenario: AC-DG-12-014-03 — Dangerous retention below legal minimum blocked with validation error.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-12-014-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-12.
