# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_11
Feature: EPIC-DG-11 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_11_001_01 @us_US_DG_11_001 @squad_observability
  Scenario: AC-DG-11-001-01 — Callback list includes LangFuse when enabled and LangSmith when enabled (Architecture §8.2).
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_001_02 @us_US_DG_11_001 @squad_observability
  Scenario: AC-DG-11-001-02 — Raw LLM output persisted only in tenant PostgreSQL; external sinks capped to 4KiB excerpt (Architecture §23.1 Q9).
    # phase: L13 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_001_03 @us_US_DG_11_001 @squad_observability
  Scenario: AC-DG-11-001-03 — `SECRET`-classified fields never exported to traces (Architecture §20.3).
    # phase: L13 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-001-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_002_01 @us_US_DG_11_002 @squad_observability
  Scenario: AC-DG-11-002-01 — LangFuse observations of type `GENERATION` feed documented aggregation query pattern (Architecture §8.3).
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_002_02 @us_US_DG_11_002 @squad_observability
  Scenario: AC-DG-11-002-02 — Budget alert triggers when single scan exceeds threshold and can abort scan (Architecture §8.4; job `budget.max_llm_usd` §28.4).
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_003_01 @us_US_DG_11_003 @squad_observability
  Scenario: AC-DG-11-003-01 — `false-positive-registry` eval cannot regress >2% absolute vs baseline on `main` (Architecture §33.2).
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_003_02 @us_US_DG_11_003 @squad_observability
  Scenario: AC-DG-11-003-02 — Datasets enumerated in §7.3 exist in `eval/datasets` with documented ownership.
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_004_01 @us_US_DG_11_004 @squad_observability
  Scenario: AC-DG-11-004-01 — P95 total scan <10 min for reference ≤500k LOC tracked as SLO (Architecture §21.1, §35.1).
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_004_02 @us_US_DG_11_004 @squad_observability
  Scenario: AC-DG-11-004-02 — Queue depth >500 pending >15m raises alert (Architecture §35.2).
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-004-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_005_01 @us_US_DG_11_005 @squad_observability
  Scenario: AC-DG-11-005-01 — API emits spans for `POST /v1/scans`, DB queries as child spans where practical (Architecture §26.2, §35).
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_005_02 @us_US_DG_11_005 @squad_observability
  Scenario: AC-DG-11-005-02 — Worker emits spans per LangGraph node name matching Architecture trace hierarchy §7.1.
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-005-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_005_03 @us_US_DG_11_005 @squad_observability
  Scenario: AC-DG-11-005-03 — Trace context propagates `scan_id`, `tenant_id` attributes (non-secret).
    # phase: L13 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-005-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_006_01 @us_US_DG_11_006 @squad_observability
  Scenario: AC-DG-11-006-01 — Startup or first-use logs resolved prompt revision for `deepguard/athena-*` style keys.
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_006_02 @us_US_DG_11_006 @squad_observability
  Scenario: AC-DG-11-006-02 — Offline mode uses bundled prompt pack with version file (EPIC-DG-13).
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_006_03 @us_US_DG_11_006 @squad_observability
  Scenario: AC-DG-11-006-03 — Prompt change triggers cache invalidation per §9.4 semantic cache rules.
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-006-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_007_01 @us_US_DG_11_007 @squad_observability
  Scenario: AC-DG-11-007-01 — Metrics exported: `cache_l1_hit_total`, `semantic_cache_hit_total`, etc. (names documented).
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_007_02 @us_US_DG_11_007 @squad_observability
  Scenario: AC-DG-11-007-02 — Per-tenant labels on cost metrics but not on raw code content metrics (privacy).
    # phase: L13 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_007_03 @us_US_DG_11_007 @squad_observability
  Scenario: AC-DG-11-007-03 — Dashboard template JSON checked into `infra/` or `docs/` (optional).
    # phase: L13 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-007-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_008_01 @us_US_DG_11_008 @squad_observability
  Scenario: AC-DG-11-008-01 — Retention job deletes or archives traces per tenant policy default 1y with legal hold override.
    # phase: L13 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_008_02 @us_US_DG_11_008 @squad_observability
  Scenario: AC-DG-11-008-02 — Encryption uses app-level AES-256 or pgcrypto as decided in ADR (Architecture §23.1 Q9).
    # phase: L13 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_008_03 @us_US_DG_11_008 @squad_observability
  Scenario: AC-DG-11-008-03 — Export of raw traces requires `admin` + break-glass logging (EPIC-DG-03).
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_009_01 @us_US_DG_11_009 @squad_observability
  Scenario: AC-DG-11-009-01 — When `LANGCHAIN_TRACING_V2=false`, no LangSmith network calls occur (verified by integration test with network deny).
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_009_02 @us_US_DG_11_009 @squad_observability
  Scenario: AC-DG-11-009-02 — LangFuse host configurable; missing keys disable handler without error on startup.
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_009_03 @us_US_DG_11_009 @squad_observability
  Scenario: AC-DG-11-009-03 — Dual-sink order documented if both enabled (Architecture §8.2).
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-009-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_010_01 @us_US_DG_11_010 @squad_observability
  Scenario: AC-DG-11-010-01 — Retry rate computed per scan and aggregated per tenant hourly.
    # phase: L13 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_010_02 @us_US_DG_11_010 @squad_observability
  Scenario: AC-DG-11-010-02 — Alert includes top contributing `agent_id` and `error_code` histogram.
    # phase: L13 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.

  @ac_AC_DG_11_010_03 @us_US_DG_11_010 @squad_observability
  Scenario: AC-DG-11-010-03 — Silencing / maintenance window supported via standard alertmanager pattern (optional).
    # phase: L13 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-11-010-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-11.
