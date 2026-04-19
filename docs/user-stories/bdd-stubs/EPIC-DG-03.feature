# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_03
Feature: EPIC-DG-03 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_03_001_01 @us_US_DG_03_001 @squad_identity_tenancy
  Scenario: AC-DG-03-001-01 — JWT validates issuer/audience configured by `JWT_ISSUER`, `JWT_AUDIENCE` (Architecture §27.1, §28.2).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_001_02 @us_US_DG_03_001 @squad_identity_tenancy
  Scenario: AC-DG-03-001-02 — Claim `tenant_id` (UUID) is mandatory for authorisation context.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_001_03 @us_US_DG_03_001 @squad_identity_tenancy
  Scenario: AC-DG-03-001-03 — Roles `scanner`, `admin`, `auditor` constrain verbs (e.g. auditors read-only; policy upload admin-only) (Architecture §28.2).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-001-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_002_01 @us_US_DG_03_002 @squad_identity_tenancy
  Scenario: AC-DG-03-002-01 — Every persisted row carries `tenant_id` and API middleware rejects mismatched paths (Architecture §28.2, §29.1).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_002_02 @us_US_DG_03_002 @squad_identity_tenancy
  Scenario: AC-DG-03-002-02 — Object storage keys are namespaced by `tenant_id` / `scan_id` (Architecture §32.1).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_003_01 @us_US_DG_03_003 @squad_identity_tenancy
  Scenario: AC-DG-03-003-01 — Effective config = `deep_merge(DEFAULT_RUNTIME_CONFIG, tenants.runtime_config[, scan_job_overrides])` per §24.2.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_003_02 @us_US_DG_03_003 @squad_identity_tenancy
  Scenario: AC-DG-03-003-02 — Scan-level overrides allowed only for `budget.*` and `notifications.*` unless role `admin` (Architecture §24.2).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_003_03 @us_US_DG_03_003 @squad_identity_tenancy
  Scenario: AC-DG-03-003-03 — Safety flags such as `semantic_cache_threshold` cannot be overridden by non-admin (Architecture §24.2).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-003-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_004_01 @us_US_DG_03_004 @squad_identity_tenancy
  Scenario: AC-DG-03-004-01 — When `max_concurrent_scans` / `MAX_CONCURRENT_SCANS_PER_TENANT` exceeded, API returns `429` with `Retry-After` (Architecture §35.2, §24.1).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_005_01 @us_US_DG_03_005 @squad_identity_tenancy
  Scenario: AC-DG-03-005-01 — When mTLS enabled, API verifies client cert chain and maps certificate to `tenant_id` / service identity (Architecture §28.2).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_005_02 @us_US_DG_03_005 @squad_identity_tenancy
  Scenario: AC-DG-03-005-02 — mTLS identities cannot impersonate human JWT roles unless explicitly granted service role.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-005-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_005_03 @us_US_DG_03_005 @squad_identity_tenancy
  Scenario: AC-DG-03-005-03 — Misconfigured cert returns `403` without leaking tenant existence.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-005-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_006_01 @us_US_DG_03_006 @squad_identity_tenancy
  Scenario: AC-DG-03-006-01 — Events capture actor, action, target id, IP (if available), outcome (success/fail).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_006_02 @us_US_DG_03_006 @squad_identity_tenancy
  Scenario: AC-DG-03-006-02 — Audit store is append-only from API perspective (no delete via public API).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_006_03 @us_US_DG_03_006 @squad_identity_tenancy
  Scenario: AC-DG-03-006-03 — Retention period configurable per deployment (align §14.2).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-006-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_007_01 @us_US_DG_03_007 @squad_identity_tenancy
  Scenario: AC-DG-03-007-01 — Matrix covers `POST /v1/scans`, `POST …/cancel`, `POST …/resume`, `POST /v1/policies:upload`, findings export (EPIC-DG-02).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_007_02 @us_US_DG_03_007 @squad_identity_tenancy
  Scenario: AC-DG-03-007-02 — Missing role returns `403` with `error_code=FORBIDDEN`.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_007_03 @us_US_DG_03_007 @squad_identity_tenancy
  Scenario: AC-DG-03-007-03 — Automated contract tests assert matrix for each route template.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-007-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_008_01 @us_US_DG_03_008 @squad_identity_tenancy
  Scenario: AC-DG-03-008-01 — Suspended tenant receives `403` on mutating endpoints; read access policy documented (e.g. allow auditors read-only).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_008_02 @us_US_DG_03_008 @squad_identity_tenancy
  Scenario: AC-DG-03-008-02 — In-flight scans behaviour on suspend: cooperative cancel or run-to-completion (document single chosen behaviour).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_008_03 @us_US_DG_03_008 @squad_identity_tenancy
  Scenario: AC-DG-03-008-03 — Delete tenant is soft-delete with retention schedule or hard-delete behind break-glass (document).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_009_01 @us_US_DG_03_009 @squad_identity_tenancy
  Scenario: AC-DG-03-009-01 — Console uses PKCE for SPA OAuth where applicable; no long-lived API keys in browser storage by default.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_009_02 @us_US_DG_03_009 @squad_identity_tenancy
  Scenario: AC-DG-03-009-02 — Logout clears client session and invalidates refresh if server-side session store used.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_009_03 @us_US_DG_03_009 @squad_identity_tenancy
  Scenario: AC-DG-03-009-03 — CORS rules restrict console origin per tenant deployment config.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-009-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_010_01 @us_US_DG_03_010 @squad_identity_tenancy
  Scenario: AC-DG-03-010-01 — Service account creation requires `admin`; token lists show prefix + created_at only (never full secret twice).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_010_02 @us_US_DG_03_010 @squad_identity_tenancy
  Scenario: AC-DG-03-010-02 — Token revocation is immediate for new requests; in-flight scan policy documented.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.

  @ac_AC_DG_03_010_03 @us_US_DG_03_010 @squad_identity_tenancy
  Scenario: AC-DG-03-010-03 — Tokens are hashed at rest; compare using constant-time compare.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-03-010-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-03.
