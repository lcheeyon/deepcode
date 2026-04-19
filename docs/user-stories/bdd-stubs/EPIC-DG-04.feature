# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_04
Feature: EPIC-DG-04 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_04_001_01 @us_US_DG_04_001 @squad_ingestion_codeintel
  Scenario: AC-DG-04-001-01 — Supports HTTPS/SSH clone paths documented for GitHub/GitLab/Gitee/Bitbucket (Architecture §11.1; Business doc §4).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_001_02 @us_US_DG_04_001 @squad_ingestion_codeintel
  Scenario: AC-DG-04-001-02 — `REPO_CLONE_DEPTH` default applied unless overridden by allowed job config (Architecture §27.2).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_001_03 @us_US_DG_04_001 @squad_ingestion_codeintel
  Scenario: AC-DG-04-001-03 — On success, `repo_local_path` and `repo_metadata` populated in `ScanState` (Architecture §4.2, §5.4).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-001-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_002_01 @us_US_DG_04_002 @squad_ingestion_codeintel
  Scenario: AC-DG-04-002-01 — `REPO_MAX_BYTES` soft cap enforced with clear `ScanAbortError` / `error_code` (Architecture §27.2, §19.1).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_002_02 @us_US_DG_04_002 @squad_ingestion_codeintel
  Scenario: AC-DG-04-002-02 — ZIP/tarball uploads respect max compressed size policy (2GB in Architecture §11.1).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_003_01 @us_US_DG_04_003 @squad_ingestion_codeintel
  Scenario: AC-DG-04-003-01 — Object key layout `…/scans/{scan_id}/repo.tar.zst` (or equivalent) per §32.1.
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_003_02 @us_US_DG_04_003 @squad_ingestion_codeintel
  Scenario: AC-DG-04-003-02 — Default deletion of repo archive 24h after `COMPLETE` unless tenant override `retention_repo_archive_hours` (Architecture §32.2, §24.1).
    # phase: L6 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_004_01 @us_US_DG_04_004 @squad_ingestion_codeintel
  Scenario: AC-DG-04-004-01 — Cloud credentials resolved via Calypso pattern with ≤15m TTL; secrets never persisted in `ScanState` (Architecture §20.1).
    # phase: L6 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_004_02 @us_US_DG_04_004 @squad_ingestion_codeintel
  Scenario: AC-DG-04-004-02 — `cloud_snapshots` map keyed by `profile_id` stored as artifact refs when large (Architecture §5.3, §23.1 Q4).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-004-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_005_01 @us_US_DG_04_005 @squad_ingestion_codeintel
  Scenario: AC-DG-04-005-01 — IaC-only path accepts Terraform plan JSON / templates per ingestion table (Architecture §11.1).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_005_02 @us_US_DG_04_005 @squad_ingestion_codeintel
  Scenario: AC-DG-04-005-02 — Cloud-only path permitted when `repo` absent but `cloud_profiles` present and `scan_layers.cloud=true` (Architecture §28.4).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-005-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_006_01 @us_US_DG_04_006 @squad_ingestion_codeintel
  Scenario: AC-DG-04-006-01 — SSH key or PAT never logged or persisted in `job_config` plaintext; only `connector_credential_ref` style refs (Architecture §20.1).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_006_02 @us_US_DG_04_006 @squad_ingestion_codeintel
  Scenario: AC-DG-04-006-02 — Clone failure surfaces `error_code` distinguishing auth vs network vs missing ref.
    # phase: L6 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_006_03 @us_US_DG_04_006 @squad_ingestion_codeintel
  Scenario: AC-DG-04-006-03 — Known-hosts or strict host key policy configurable for enterprise Git (document default).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-006-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_007_01 @us_US_DG_04_007 @squad_ingestion_codeintel
  Scenario: AC-DG-04-007-01 — When `sub_path` set, Hermes stages only that subtree; path normalisation blocks `../` escape.
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_007_02 @us_US_DG_04_007 @squad_ingestion_codeintel
  Scenario: AC-DG-04-007-02 — Argus indexing honours same root for embeddings and tools (EPIC-DG-06).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_007_03 @us_US_DG_04_007 @squad_ingestion_codeintel
  Scenario: AC-DG-04-007-03 — Report metadata records `sub_path` for audit (EPIC-DG-10).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-007-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_008_01 @us_US_DG_04_008 @squad_ingestion_codeintel
  Scenario: AC-DG-04-008-01 — Multipart or pre-signed PUT flow documented; max size aligns `REPO_MAX_BYTES` (Architecture §11.1, §27.2).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_008_02 @us_US_DG_04_008 @squad_ingestion_codeintel
  Scenario: AC-DG-04-008-02 — Checksum verification (`checksum_sha256`) optional but recommended; mismatch fails fast.
    # phase: L6 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_008_03 @us_US_DG_04_008 @squad_ingestion_codeintel
  Scenario: AC-DG-04-008-03 — Uploaded artefact lands under tenant-scoped object prefix before worker extract (Architecture §32.1).
    # phase: L6 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_009_01 @us_US_DG_04_009 @squad_ingestion_codeintel
  Scenario: AC-DG-04-009-01 — `job_config` flag requests depth=full; default remains shallow (Architecture §11.1).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_009_02 @us_US_DG_04_009 @squad_ingestion_codeintel
  Scenario: AC-DG-04-009-02 — Full clone wall time surfaced in scan metadata; timeout participates in budget (EPIC-DG-01).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_009_03 @us_US_DG_04_009 @squad_ingestion_codeintel
  Scenario: AC-DG-04-009-03 — If history unused by graph, feature is no-op aside from clone cost (document).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-009-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_010_01 @us_US_DG_04_010 @squad_ingestion_codeintel
  Scenario: AC-DG-04-010-01 — After clone, `repo_commit_sha` persisted on `scans` even when request sent only `ref` (Architecture §29.1).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_010_02 @us_US_DG_04_010 @squad_ingestion_codeintel
  Scenario: AC-DG-04-010-02 — Detached HEAD state recorded correctly.
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_010_03 @us_US_DG_04_010 @squad_ingestion_codeintel
  Scenario: AC-DG-04-010-03 — Mismatch between requested `commit_sha` and resolved head fails with clear `error_code` when strict mode enabled.
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-010-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_011_01 @us_US_DG_04_011 @squad_ingestion_codeintel
  Scenario: AC-DG-04-011-01 — `repo_metadata` includes total files, ignored paths summary, binary-skipped count (fields documented in schema).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-011-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_011_02 @us_US_DG_04_011 @squad_ingestion_codeintel
  Scenario: AC-DG-04-011-02 — Extremely large file list truncation flagged for report appendix (Architecture §11.6).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-011-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_011_03 @us_US_DG_04_011 @squad_ingestion_codeintel
  Scenario: AC-DG-04-011-03 — Metadata serialisable size bounded; spill to artifact ref if huge (Architecture §5.3).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-011-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_012_01 @us_US_DG_04_012 @squad_ingestion_codeintel
  Scenario: AC-DG-04-012-01 — `cloud_profiles[].regions` array honoured; failures per region recorded in snapshot metadata (EPIC-DG-07).
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-012-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_012_02 @us_US_DG_04_012 @squad_ingestion_codeintel
  Scenario: AC-DG-04-012-02 — Snapshots stored compressed (`*.json.zst`) under object layout §32.1.
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-012-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.

  @ac_AC_DG_04_012_03 @us_US_DG_04_012 @squad_ingestion_codeintel
  Scenario: AC-DG-04-012-03 — Partial regional success still produces snapshot with `coverage_percent` field.
    # phase: L6 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-04-012-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-04.
