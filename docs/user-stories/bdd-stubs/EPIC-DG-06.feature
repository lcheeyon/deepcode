# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_06
Feature: EPIC-DG-06 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_06_001_01 @us_US_DG_06_001 @squad_ingestion_codeintel
  Scenario: AC-DG-06-001-01 — GA languages from support matrix use tree-sitter path (Architecture §11.2–11.4).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_001_02 @us_US_DG_06_001 @squad_ingestion_codeintel
  Scenario: AC-DG-06-001-02 — Chunker never splits mid-function/class for configured node types (Architecture §11.4).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_001_03 @us_US_DG_06_001 @squad_ingestion_codeintel
  Scenario: AC-DG-06-001-03 — `language_breakdown` populated in `ScanState` (Architecture §4.2).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-001-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_002_01 @us_US_DG_06_002 @squad_ingestion_codeintel
  Scenario: AC-DG-06-002-01 — Graph includes external deps and vulnerable deps cross-ref hooks (Architecture §11.5–11.6).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_002_02 @us_US_DG_06_002 @squad_ingestion_codeintel
  Scenario: AC-DG-06-002-02 — When exceeding `max_nodes` / `max_depth`, status `TRUNCATED` recorded and warning surfaces in report (Architecture §23.1 Q6).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_003_01 @us_US_DG_06_003 @squad_ingestion_codeintel
  Scenario: AC-DG-06-003-01 — Ensemble retriever weights documented default (0.3 BM25 / 0.7 vector) configurable within bounds (Architecture §12.3).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_003_02 @us_US_DG_06_003 @squad_ingestion_codeintel
  Scenario: AC-DG-06-003-02 — `code_chunks` rows include `tenant_id`, `scan_id`, metadata JSON for file/line span (Architecture §12.1).
    # phase: L8 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_004_01 @us_US_DG_06_004 @squad_ingestion_codeintel
  Scenario: AC-DG-06-004-01 — Strategies per size tier applied (Architecture §11.6).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_004_02 @us_US_DG_06_004 @squad_ingestion_codeintel
  Scenario: AC-DG-06-004-02 — For >2M LOC, scan requires explicit sub-path scoping or async batch mode flag (Architecture §11.6).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-004-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_005_01 @us_US_DG_06_005 @squad_ingestion_codeintel
  Scenario: AC-DG-06-005-01 — Security pattern scanner outputs feed Athena context as structured signals (Architecture §11.3).
    # phase: L8 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_006_01 @us_US_DG_06_006 @squad_ingestion_codeintel
  Scenario: AC-DG-06-006-01 — Ignore file grammar documented; default excludes `node_modules/`, `.git/`, large `dist/` unless overridden.
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_006_02 @us_US_DG_06_006 @squad_ingestion_codeintel
  Scenario: AC-DG-06-006-02 — Excluded path count and total bytes skipped recorded in `repo_metadata` / scan summary.
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_006_03 @us_US_DG_06_006 @squad_ingestion_codeintel
  Scenario: AC-DG-06-006-03 — Explicit `include_paths` in job config overrides ignore for emergency audits (admin only).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-006-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_007_01 @us_US_DG_06_007 @squad_ingestion_codeintel
  Scenario: AC-DG-06-007-01 — Cache key and TTL 7d default; invalidation on embedding model version change (Architecture §9.4).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_007_02 @us_US_DG_06_007 @squad_ingestion_codeintel
  Scenario: AC-DG-06-007-02 — Cache miss path records latency metric per batch (EPIC-DG-11).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_007_03 @us_US_DG_06_007 @squad_ingestion_codeintel
  Scenario: AC-DG-06-007-03 — Tenant flag can disable shared embedding cache for paranoid mode (document trade-off).
    # phase: L8 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-007-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_008_01 @us_US_DG_06_008 @squad_ingestion_codeintel
  Scenario: AC-DG-06-008-01 — When `DELTA_SKIP_ANALYSIS` / `delta_skip_analysis` true and fingerprint matches, behaviour matches MVP decision §23.1 Q7 (re-run Athena+Circe+Penelope on policy bump; optional ski…
    # phase: L8 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_008_02 @us_US_DG_06_008 @squad_ingestion_codeintel
  Scenario: AC-DG-06-008-02 — Delta fingerprint includes `repo_commit_sha` + `policy_version` + `scan_layers` (Architecture §23.1 Q7).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_008_03 @us_US_DG_06_008 @squad_ingestion_codeintel
  Scenario: AC-DG-06-008-03 — Carry-forward findings list references prior `scan_id` for audit trail.
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_009_01 @us_US_DG_06_009 @squad_ingestion_codeintel
  Scenario: AC-DG-06-009-01 — BM25 documents deleted or tombstoned when scan artefacts expire (align retention §14.2).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_009_02 @us_US_DG_06_009 @squad_ingestion_codeintel
  Scenario: AC-DG-06-009-02 — No cross-tenant BM25 query possible at API/SQL layer.
    # phase: L8 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_009_03 @us_US_DG_06_009 @squad_ingestion_codeintel
  Scenario: AC-DG-06-009-03 — Reindex job idempotent if worker retries Argus node.
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-009-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_010_01 @us_US_DG_06_010 @squad_ingestion_codeintel
  Scenario: AC-DG-06-010-01 — linguist-style heuristics + size cap classify binaries; list surfaced in report appendix.
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_010_02 @us_US_DG_06_010 @squad_ingestion_codeintel
  Scenario: AC-DG-06-010-02 — Misclassified text-as-binary override API for path glob (admin).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_010_03 @us_US_DG_06_010 @squad_ingestion_codeintel
  Scenario: AC-DG-06-010-03 — Skipped files do not appear as false “missing coverage” without explicit control mapping (Athena prompt guidance).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-010-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_011_01 @us_US_DG_06_011 @squad_ingestion_codeintel
  Scenario: AC-DG-06-011-01 — Lockfile parsers for npm, pip, go mod, Maven documented; graceful skip if absent (Architecture §11.5–11.6).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-011-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_011_02 @us_US_DG_06_011 @squad_ingestion_codeintel
  Scenario: AC-DG-06-011-02 — Advisory feed version pinned; air-gap mode uses bundled snapshot (EPIC-DG-13).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-011-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_011_03 @us_US_DG_06_011 @squad_ingestion_codeintel
  Scenario: AC-DG-06-011-03 — Each vulnerable dep links to dependency graph node ids for evidence (Architecture §11.5).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-011-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_012_01 @us_US_DG_06_012 @squad_ingestion_codeintel
  Scenario: AC-DG-06-012-01 — Index creation runs in migration or async job; documented for `lists` / M values (Architecture §12.1).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-012-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_012_02 @us_US_DG_06_012 @squad_ingestion_codeintel
  Scenario: AC-DG-06-012-02 — Vacuum/reindex playbook linked from ops doc (Architecture §35.3).
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-012-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.

  @ac_AC_DG_06_012_03 @us_US_DG_06_012 @squad_ingestion_codeintel
  Scenario: AC-DG-06-012-03 — Embedding dimension mismatch fails fast at index time with `error_code`.
    # phase: L8 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-06-012-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-06.
