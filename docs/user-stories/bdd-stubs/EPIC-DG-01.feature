# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_01
Feature: EPIC-DG-01 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_01_001_01 @us_US_DG_01_001 @squad_platform_runtime
  Scenario: AC-DG-01-001-01 — Given `scan_layers.iac=true` and `scan_layers.cloud=true`, Laocoon and Cassandra are dispatched per fan-out rules and Athena does not start until the convergence gate validates co…
    # phase: L4 / priority: P1
    Given `scan_layers.iac=true` and `scan_layers.cloud=true`, Laocoon and Cassandra are dispatched per fan-out rules and Athena does not start until the convergence gate validates completi…
    When the system executes behavior for "AC-DG-01-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_001_02 @us_US_DG_01_001 @squad_platform_runtime
  Scenario: AC-DG-01-001-02 — Given `scan_layers.iac=false`, Laocoon is skipped and the gate does not block indefinitely on IaC outputs.
    # phase: L4 / priority: P1
    Given `scan_layers.iac=false`, Laocoon is skipped and the gate does not block indefinitely on IaC outputs
    When the system executes behavior for "AC-DG-01-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_001_03 @us_US_DG_01_001 @squad_platform_runtime
  Scenario: AC-DG-01-001-03 — Given `scan_layers.cloud=false` or no snapshots, Cassandra is skipped per routing rules.
    # phase: L4 / priority: P1
    Given `scan_layers.cloud=false` or no snapshots, Cassandra is skipped per routing rules
    When the system executes behavior for "AC-DG-01-001-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_001_04 @us_US_DG_01_001 @squad_platform_runtime
  Scenario: AC-DG-01-001-04 — Graph compilation uses a stable `thread_id = scan_id` for checkpoint correlation (Architecture §31.1).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-001-04"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_002_01 @us_US_DG_01_002 @squad_platform_runtime
  Scenario: AC-DG-01-002-01 — Postgres-backed checkpointer is used in production topology (`LANGGRAPH_CHECKPOINT=postgres`) (Architecture §4.6, §27).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_002_02 @us_US_DG_01_002 @squad_platform_runtime
  Scenario: AC-DG-01-002-02 — Athena MVP batches checkpoint after each batch completion (Architecture §31.3).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_002_03 @us_US_DG_01_002 @squad_platform_runtime
  Scenario: AC-DG-01-002-03 — Resume invocation with `invoke(None, config)` continues from last successful checkpoint without duplicating persisted findings (Architecture §4.6).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-002-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_003_01 @us_US_DG_01_003 @squad_platform_runtime
  Scenario: AC-DG-01-003-01 — `POST /v1/scans/{id}/cancel` sets `cancellation_requested=true` and returns `202` (Architecture §28.3, §30.4).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_003_02 @us_US_DG_01_003 @squad_platform_runtime
  Scenario: AC-DG-01-003-02 — Worker observes cancel between LangGraph nodes and transitions to `CANCELLED` terminal state with partial artefacts retained per policy (Architecture §30.4).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_003_03 @us_US_DG_01_003 @squad_platform_runtime
  Scenario: AC-DG-01-003-03 — Cancelled scans never emit a `scan.completed` webhook (only `failed`/`completed` per configured events).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-003-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_004_01 @us_US_DG_01_004 @squad_platform_runtime
  Scenario: AC-DG-01-004-01 — When `graph_interrupt_before_athena` / `GRAPH_INTERRUPT_BEFORE_ATHENA` enabled, graph enters `AWAITING_REVIEW` and awaits `resume` with annotations (Architecture §4.7, §28.5).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_004_02 @us_US_DG_01_004 @squad_platform_runtime
  Scenario: AC-DG-01-004-02 — Resume clears interrupt only for authorised roles (`admin` or configured reviewer).
    # phase: L4 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-004-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_004_03 @us_US_DG_01_004 @squad_platform_runtime
  Scenario: AC-DG-01-004-03 — Audit log records who resumed and timestamp (stored alongside scan metadata).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-004-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_005_01 @us_US_DG_01_005 @squad_platform_runtime
  Scenario: AC-DG-01-005-01 — Worker renews `scan:{scan_id}:heartbeat` every ≤30s with TTL ≥120s (Architecture §30.3).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_005_02 @us_US_DG_01_005 @squad_platform_runtime
  Scenario: AC-DG-01-005-02 — Watchdog marks `FAILED` with `error_code=WORKER_LOST` when heartbeat missing for a non-terminal scan (Architecture §30.3).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-005-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_006_01 @us_US_DG_01_006 @squad_platform_runtime
  Scenario: AC-DG-01-006-01 — Worker verifies `scans.status == QUEUED` (or equivalent) before transitioning to in-flight processing (Architecture §30.2).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_006_02 @us_US_DG_01_006 @squad_platform_runtime
  Scenario: AC-DG-01-006-02 — Visibility timeout / pending entry stale after configurable duration (e.g. 15m) is reclaimable via `XCLAIM` pattern (Architecture §30.2).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_006_03 @us_US_DG_01_006 @squad_platform_runtime
  Scenario: AC-DG-01-006-03 — Duplicate delivery does not create duplicate `scan_id` rows or fork graph state when idempotency keys are in use (align with EPIC-DG-02).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-006-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_006_04 @us_US_DG_01_006 @squad_platform_runtime
  Scenario: AC-DG-01-006-04 — Optional Kafka deployment uses same `ScanJobMessage` schema version `schema_ver` (Architecture §30.1–30.2).
    # phase: L4 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-006-04"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_007_01 @us_US_DG_01_007 @squad_platform_runtime
  Scenario: AC-DG-01-007-01 — When `should_abort=true`, conditional edges route to `error_handler` which sets terminal `FAILED` and stable `error_code` (Architecture §4.4, §31.4).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_007_02 @us_US_DG_01_007 @squad_platform_runtime
  Scenario: AC-DG-01-007-02 — `error_message` is sanitised (no stack traces, no secret material) in API and DB (Architecture §28.5).
    # phase: L4 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_007_03 @us_US_DG_01_007 @squad_platform_runtime
  Scenario: AC-DG-01-007-03 — Non-fatal `ToolExecutionError` does not invoke `error_handler`; partial outputs remain (Architecture §31.4).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-007-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_008_01 @us_US_DG_01_008 @squad_platform_runtime
  Scenario: AC-DG-01-008-01 — When `max_wall_seconds` exceeded, cooperative abort triggers `CANCELLED` or `FAILED` with `error_code` documented for timeout (Architecture §28.4, §19.1 `ScanAbortError`).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_008_02 @us_US_DG_01_008 @squad_platform_runtime
  Scenario: AC-DG-01-008-02 — When `max_llm_usd` exceeded mid-graph, scan aborts and partial artefacts retained per retention policy (Architecture §28.4, §8.4).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_008_03 @us_US_DG_01_008 @squad_platform_runtime
  Scenario: AC-DG-01-008-03 — Budget checks occur at defined cooperative points between LangGraph nodes (Architecture §30.4).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_009_01 @us_US_DG_01_009 @squad_platform_runtime
  Scenario: AC-DG-01-009-01 — Optional streaming mode maps LangGraph events to `percent_complete` / sub-stage hints without breaking REST status contract (Architecture §31.2).
    # phase: L4 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_009_02 @us_US_DG_01_009 @squad_platform_runtime
  Scenario: AC-DG-01-009-02 — Streaming disconnect does not cancel scan; worker continues (resilience).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_009_03 @us_US_DG_01_009 @squad_platform_runtime
  Scenario: AC-DG-01-009-03 — Event stream excludes `SECRET`-classified state (Architecture §20.3).
    # phase: L4 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-009-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_010_01 @us_US_DG_01_010 @squad_platform_runtime
  Scenario: AC-DG-01-010-01 — Resume uses same `thread_id = scan_id` and does not duplicate findings on reducer merge (Architecture §4.6, §31.1).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_010_02 @us_US_DG_01_010 @squad_platform_runtime
  Scenario: AC-DG-01-010-02 — Resume is rejected or no-op when scan already terminal unless explicit product policy for `FAILED` retry (document behaviour).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_010_03 @us_US_DG_01_010 @squad_platform_runtime
  Scenario: AC-DG-01-010-03 — Resume path audited with `resumed_at`, `worker_instance_id` if available (observability alignment EPIC-DG-11).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-010-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_011_01 @us_US_DG_01_011 @squad_platform_runtime
  Scenario: AC-DG-01-011-01 — `ScanJobMessage` accepts `priority` integer; worker ordering respects documented algorithm (Architecture §30.1).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-011-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_011_02 @us_US_DG_01_011 @squad_platform_runtime
  Scenario: AC-DG-01-011-02 — Starvation test: low-priority jobs still start within configured max wait under load (NFR; document SLO).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-011-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_011_03 @us_US_DG_01_011 @squad_platform_runtime
  Scenario: AC-DG-01-011-03 — Abuse of priority requires `admin` tenant flag or plan tier (product guard).
    # phase: L4 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-011-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_012_01 @us_US_DG_01_012 @squad_platform_runtime
  Scenario: AC-DG-01-012-01 — Compiled graph reused for all scans in process; feature flags read at compile or documented refresh boundary (Architecture §31.1).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-012-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.

  @ac_AC_DG_01_012_02 @us_US_DG_01_012 @squad_platform_runtime
  Scenario: AC-DG-01-012-02 — Hot reload of graph requires worker restart in production (documented); dev may auto-reload (Architecture §34).
    # phase: L4 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-01-012-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-01.
