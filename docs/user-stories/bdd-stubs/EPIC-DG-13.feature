# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_13
Feature: EPIC-DG-13 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_13_001_01 @us_US_DG_13_001 @squad_security_deployment
  Scenario: AC-DG-13-001-01 — Default configuration blocks remote LLM calls when `deployment=private_cloud|air_gapped` (Architecture §2.3, §13.2).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_001_02 @us_US_DG_13_001 @squad_security_deployment
  Scenario: AC-DG-13-001-02 — Opt-in SaaS LLM tier requires explicit tenant contract flag recorded in audit log (product requirement; implementation-specific storage).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_002_01 @us_US_DG_13_002 @squad_security_deployment
  Scenario: AC-DG-13-002-01 — `CALYPSO_BACKEND` supports documented backends; short TTL tokens only (Architecture §20.1, §27.3).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_002_02 @us_US_DG_13_002 @squad_security_deployment
  Scenario: AC-DG-13-002-02 — Secrets never written to `ScanState` or reasoning traces (Architecture §20.1, §20.3).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_003_01 @us_US_DG_13_003 @squad_security_deployment
  Scenario: AC-DG-13-003-01 — Router obeys task-to-model matrix defaults (Architecture §13.1–13.3).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_003_02 @us_US_DG_13_003 @squad_security_deployment
  Scenario: AC-DG-13-003-02 — Circuit breaker opens after threshold failures and switches provider (Architecture §19.2).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_004_01 @us_US_DG_13_004 @squad_security_deployment
  Scenario: AC-DG-13-004-01 — Default threshold `0.97` with tenant-configurable range `0.95–0.99` for admins only (Architecture §9.2, §24.1–24.2).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_004_02 @us_US_DG_13_004 @squad_security_deployment
  Scenario: AC-DG-13-004-02 — Cache invalidates on prompt template version change (Architecture §9.4).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-004-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_005_01 @us_US_DG_13_005 @squad_security_deployment
  Scenario: AC-DG-13-005-01 — Air-gap profile disables LangSmith; mandates self-hosted LangFuse (Architecture §22.2, §8.1).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_005_02 @us_US_DG_13_005 @squad_security_deployment
  Scenario: AC-DG-13-005-02 — Huawei deployment documents SM2/SM3/SM4 where applicable (Business doc §13.3, §17 Phase 3).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-005-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_005_03 @us_US_DG_13_005 @squad_security_deployment
  Scenario: AC-DG-13-005-03 — Image pull sources restricted to domestic registries when `deployment=xinchuang` (Architecture §22.2).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-005-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_006_01 @us_US_DG_13_006 @squad_security_deployment
  Scenario: AC-DG-13-006-01 — Path traversal attempts raise `ToolExecutionError` without crashing graph (Architecture §6.5, §20.2).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_006_02 @us_US_DG_13_006 @squad_security_deployment
  Scenario: AC-DG-13-006-02 — `TOOL_SANDBOX_ROOT` enforced for all tool I/O (Architecture §27.2).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_007_01 @us_US_DG_13_007 @squad_security_deployment
  Scenario: AC-DG-13-007-01 — Cache key `sha256(repo_url + commit_sha + policy_version)` documented; value is prior `ScanResult` reference or artifact pointer.
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_007_02 @us_US_DG_13_007 @squad_security_deployment
  Scenario: AC-DG-13-007-02 — Skip path still writes new `scan_id` row with `status=COMPLETE` and link to prior result OR returns same id per product decision (document one).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_007_03 @us_US_DG_13_007 @squad_security_deployment
  Scenario: AC-DG-13-007-03 — Skip disabled when any `scan_layers` differ from cached run.
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-007-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_008_01 @us_US_DG_13_008 @squad_security_deployment
  Scenario: AC-DG-13-008-01 — Tool cache key includes `tool_impl_version` semver from package build.
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_008_02 @us_US_DG_13_008 @squad_security_deployment
  Scenario: AC-DG-13-008-02 — Toggle to disable L3 per tenant for debugging (runtime_config).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_008_03 @us_US_DG_13_008 @squad_security_deployment
  Scenario: AC-DG-13-008-03 — Cache poisoning tests ensure different args never return wrong value.
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_009_01 @us_US_DG_13_009 @squad_security_deployment
  Scenario: AC-DG-13-009-01 — Build flavour `fips` documented in Dockerfile/Helm values; uses approved OpenSSL provider where applicable.
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_009_02 @us_US_DG_13_009 @squad_security_deployment
  Scenario: AC-DG-13-009-02 — Non-FIPS and FIPS images not mixed in same StatefulSet without node labels (k8s constraint doc).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_009_03 @us_US_DG_13_009 @squad_security_deployment
  Scenario: AC-DG-13-009-03 — Automated check fails if FIPS image links non-FIPS sidecar (optional).
    # phase: L14 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-009-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_010_01 @us_US_DG_13_010 @squad_security_deployment
  Scenario: AC-DG-13-010-01 — Documented egress list per deployment mode (SaaS vs VPC vs air-gap).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_010_02 @us_US_DG_13_010 @squad_security_deployment
  Scenario: AC-DG-13-010-02 — Egress proxy support for `HTTPS_PROXY` with TLS MITM **disallowed** by default (document).
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_010_03 @us_US_DG_13_010 @squad_security_deployment
  Scenario: AC-DG-13-010-03 — Integration test with network policy denies unexpected destinations.
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-010-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_011_01 @us_US_DG_13_011 @squad_security_deployment
  Scenario: AC-DG-13-011-01 — Release pipeline generates SPDX or CycloneDX SBOM for api/worker images.
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-011-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_011_02 @us_US_DG_13_011 @squad_security_deployment
  Scenario: AC-DG-13-011-02 — Signature verification steps documented for Helm install.
    # phase: L14 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-011-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.

  @ac_AC_DG_13_011_03 @us_US_DG_13_011 @squad_security_deployment
  Scenario: AC-DG-13-011-03 — Critical CVEs in SBOM gate release per policy table (optional CI gate).
    # phase: L14 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-13-011-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-13.
