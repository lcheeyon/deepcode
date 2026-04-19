# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_08
Feature: EPIC-DG-08 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_08_001_01 @us_US_DG_08_001 @squad_compliance_engine
  Scenario: AC-DG-08-001-01 — Findings include `control_id`, `severity`, `evidence_refs`, `reasoning_summary`, `confidence_score`, `status` (Architecture §3.1, §29.1).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_001_02 @us_US_DG_08_001 @squad_compliance_engine
  Scenario: AC-DG-08-001-02 — Low confidence after max iterations marks `UNCERTAIN` + `should_escalate` behaviours per thresholds (Architecture §3.2).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_002_01 @us_US_DG_08_002 @squad_compliance_engine
  Scenario: AC-DG-08-002-01 — Two-pass Athena emits separate trace spans `athena_generator_pass`, `athena_critic_pass` (Architecture §3.3, §23.1 Q5).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_002_02 @us_US_DG_08_002 @squad_compliance_engine
  Scenario: AC-DG-08-002-02 — Disagreements resolve to `UNCERTAIN` per reconcile rules (Architecture §3.3).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_003_01 @us_US_DG_08_003 @squad_compliance_engine
  Scenario: AC-DG-08-003-01 — `cross_layer_findings` list includes mapped frameworks + composite severity rationale (Architecture §3.4, §4.2).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_003_02 @us_US_DG_08_003 @squad_compliance_engine
  Scenario: AC-DG-08-003-02 — Executive report section highlights top cross-layer items (Architecture §18.1 item 7).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_004_01 @us_US_DG_08_004 @squad_compliance_engine
  Scenario: AC-DG-08-004-01 — Batch size target 8–12 controls with clustering on `scope_tags` + embedding similarity (Architecture §31.3).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_004_02 @us_US_DG_08_004 @squad_compliance_engine
  Scenario: AC-DG-08-004-02 — Feature flag `ATHENA_PER_CONTROL_SEND` defaults off (Architecture §23.1 Q1).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-004-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_005_01 @us_US_DG_08_005 @squad_compliance_engine
  Scenario: AC-DG-08-005-01 — Evidence segments use boundary markers in prompts (Architecture §20.2).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_005_02 @us_US_DG_08_005 @squad_compliance_engine
  Scenario: AC-DG-08-005-02 — Outputs parsed strictly to Pydantic models; free-form discarded (Architecture §6.4, §20.2).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-005-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_006_01 @us_US_DG_08_006 @squad_compliance_engine
  Scenario: AC-DG-08-006-01 — `compliance_summary` persisted with per-framework pass/fail/partial/NA counts (Architecture §4.2).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_006_02 @us_US_DG_08_006 @squad_compliance_engine
  Scenario: AC-DG-08-006-02 — Scoring weights honour `severity_weight` on controls (Architecture §16.2).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_006_03 @us_US_DG_08_006 @squad_compliance_engine
  Scenario: AC-DG-08-006-03 — UNCERTAIN ratio >30% triggers report banner + optional webhook (Architecture §8.4).
    # phase: L10 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-006-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_007_01 @us_US_DG_08_007 @squad_compliance_engine
  Scenario: AC-DG-08-007-01 — `job_config.locale` or tenant default selects `zh`, `en`, `bilingual` modes (product schema).
    # phase: L10 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_007_02 @us_US_DG_08_007 @squad_compliance_engine
  Scenario: AC-DG-08-007-02 — Bilingual mode renders primary + secondary column in finding tables (EPIC-DG-10).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_007_03 @us_US_DG_08_007 @squad_compliance_engine
  Scenario: AC-DG-08-007-03 — LLM routing prefers Qwen/DeepSeek for Chinese narrative when deployment requires (Architecture §13.1; Business doc §12).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-007-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_008_01 @us_US_DG_08_008 @squad_compliance_engine
  Scenario: AC-DG-08-008-01 — Athena code path uses MMR with documented lambda; falls back to plain top-K if disabled by flag.
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_008_02 @us_US_DG_08_008 @squad_compliance_engine
  Scenario: AC-DG-08-008-02 — Retrieved chunk ids logged in reasoning trace redacted excerpt metadata only (EPIC-DG-11).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_008_03 @us_US_DG_08_008 @squad_compliance_engine
  Scenario: AC-DG-08-008-03 — Deterministic tie-break on chunk id ordering when scores tie (`temperature=0` path).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_009_01 @us_US_DG_08_009 @squad_compliance_engine
  Scenario: AC-DG-08-009-01 — Failed batch increments `error_log` and can retry batch only without re-running completed batches (Architecture §31.3–31.4).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_009_02 @us_US_DG_08_009 @squad_compliance_engine
  Scenario: AC-DG-08-009-02 — After max batch retries, remaining controls marked `UNCERTAIN` with explicit reason code.
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_009_03 @us_US_DG_08_009 @squad_compliance_engine
  Scenario: AC-DG-08-009-03 — Checkpoint state after each successful batch is durable (EPIC-DG-01).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-009-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_010_01 @us_US_DG_08_010 @squad_compliance_engine
  Scenario: AC-DG-08-010-01 — NA requires `na_reason` enum + short text; empty NA rejected by schema.
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_010_02 @us_US_DG_08_010 @squad_compliance_engine
  Scenario: AC-DG-08-010-02 — Layer relevance from `PolicyControl` respected — e.g. pure cloud control skips code-only evidence requirement (Architecture §16.2).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_010_03 @us_US_DG_08_010 @squad_compliance_engine
  Scenario: AC-DG-08-010-03 — NA rate anomalies (>40% in a framework) flagged for product review dataset (eval hook).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-010-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_011_01 @us_US_DG_08_011 @squad_compliance_engine
  Scenario: AC-DG-08-011-01 — Finding schema includes machine-readable evidence grade (e.g. `direct_code_ref`, `config_only`, `heuristic`).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-011-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_011_02 @us_US_DG_08_011 @squad_compliance_engine
  Scenario: AC-DG-08-011-02 — Cross-layer findings require ≥2 layers’ evidence refs or downgrade severity (Architecture §3.4 spirit).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-011-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_011_03 @us_US_DG_08_011 @squad_compliance_engine
  Scenario: AC-DG-08-011-03 — UI and API expose same field (EPIC-DG-12).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-011-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_012_01 @us_US_DG_08_012 @squad_compliance_engine
  Scenario: AC-DG-08-012-01 — On `ContextLengthError`, compactor reduces prior steps per §10.3 and retries bounded times.
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-012-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_012_02 @us_US_DG_08_012 @squad_compliance_engine
  Scenario: AC-DG-08-012-02 — Compaction events logged with before/after token counts (redacted trace).
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-012-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.

  @ac_AC_DG_08_012_03 @us_US_DG_08_012 @squad_compliance_engine
  Scenario: AC-DG-08-012-03 — If still failing, control marked `UNCERTAIN` with `error_code=CONTEXT_LIMIT`.
    # phase: L10 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-08-012-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-08.
