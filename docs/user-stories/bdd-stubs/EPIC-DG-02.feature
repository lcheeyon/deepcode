# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_02
Feature: EPIC-DG-02 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_02_001_01 @us_US_DG_02_001 @squad_control_plane
  Scenario: AC-DG-02-001-01 — Request body validates `CreateScanRequest` shape including `repo`, `policy_ids`, `scan_layers`, optional `cloud_profiles`, `notifications`, `budget` (Architecture §28.4).
    # phase: L3 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_001_02 @us_US_DG_02_001 @squad_control_plane
  Scenario: AC-DG-02-001-02 — Validation rejects jobs where `scan_layers.cloud=true` but neither `repo` nor `cloud_profiles` satisfy minimum inputs per normative rules (Architecture §28.4).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_001_03 @us_US_DG_02_001 @squad_control_plane
  Scenario: AC-DG-02-001-03 — Validation rejects `scan_layers.code=true` or `iac=true` without `repo` when required (Architecture §28.4).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-001-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_001_04 @us_US_DG_02_001 @squad_control_plane
  Scenario: AC-DG-02-001-04 — Response `201` returns `scan_id` and initial `status` in {`PENDING`,`QUEUED`}.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-001-04"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_002_01 @us_US_DG_02_002 @squad_control_plane
  Scenario: AC-DG-02-002-01 — `Idempotency-Key` header optional; duplicates within 24h return same `scan_id` with `201` or documented idempotent success code (Architecture §28.3).
    # phase: L3 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_002_02 @us_US_DG_02_002 @squad_control_plane
  Scenario: AC-DG-02-002-02 — DB uniqueness on `(tenant_id, idempotency_key)` enforced (Architecture §29.1).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_003_01 @us_US_DG_02_003 @squad_control_plane
  Scenario: AC-DG-02-003-01 — Response includes `current_stage`, `stage_started_at`, `percent_complete`, `error_code`, `error_message` (sanitised) per §28.5.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_003_02 @us_US_DG_02_003 @squad_control_plane
  Scenario: AC-DG-02-003-02 — Terminal states `COMPLETE`, `FAILED`, `CANCELLED`, `AWAITING_REVIEW` behave as documented (Architecture §28.5).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_003_03 @us_US_DG_02_003 @squad_control_plane
  Scenario: AC-DG-02-003-03 — Cross-tenant access returns `404` or `403` without leaking existence (security baseline).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-003-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_004_01 @us_US_DG_02_004 @squad_control_plane
  Scenario: AC-DG-02-004-01 — Supports `severity`, `framework`, `cursor` pagination (Architecture §28.3).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_004_02 @us_US_DG_02_004 @squad_control_plane
  Scenario: AC-DG-02-004-02 — Each finding includes stable identifiers: `framework`, `control_id`, `status`, `severity`, `evidence_refs`, `confidence_score`, `policy_version` (Architecture §29.1 fields / §3 mo…
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-004-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_005_01 @us_US_DG_02_005 @squad_control_plane
  Scenario: AC-DG-02-005-01 — `GET /v1/scans/{scan_id}/artifacts/{artifact_id}` returns `302` to short-TTL presigned URL or streams via authenticated proxy (Architecture §28.3).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_005_02 @us_US_DG_02_005 @squad_control_plane
  Scenario: AC-DG-02-005-02 — Artefact row stores `checksum_sha256`, `size_bytes`, `encryption` mode (Architecture §29.1).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-005-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_006_01 @us_US_DG_02_006 @squad_control_plane
  Scenario: AC-DG-02-006-01 — Payload includes `event`, `scan_id`, `tenant_id`, `report_artifact_id` when completed (Architecture §28.6).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_006_02 @us_US_DG_02_006 @squad_control_plane
  Scenario: AC-DG-02-006-02 — `X-DeepGuard-Signature: sha256=<hex>` verifies raw body with shared secret (Architecture §28.6).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_006_03 @us_US_DG_02_006 @squad_control_plane
  Scenario: AC-DG-02-006-03 — Retries with exponential backoff and DLQ rows in `webhook_deliveries` (Architecture §28.6, §29.4).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-006-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_007_01 @us_US_DG_02_007 @squad_control_plane
  Scenario: AC-DG-02-007-01 — All documented resources live under base path `/v1` (Architecture §28.1).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_007_02 @us_US_DG_02_007 @squad_control_plane
  Scenario: AC-DG-02-007-02 — Deprecated endpoints return `Sunset` header per RFC 8594 when applicable (Architecture §28.1).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_007_03 @us_US_DG_02_007 @squad_control_plane
  Scenario: AC-DG-02-007-03 — Breaking changes require `/v2` path prefix; changelog references story IDs where maintained.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-007-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_008_01 @us_US_DG_02_008 @squad_control_plane
  Scenario: AC-DG-02-008-01 — Resume returns `202` when graph was interrupted and credentials still valid (Architecture §28.3).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_008_02 @us_US_DG_02_008 @squad_control_plane
  Scenario: AC-DG-02-008-02 — Resume rejected with clear error when scan not in `AWAITING_REVIEW` or user lacks role (Architecture §28.3, EPIC-DG-03).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_008_03 @us_US_DG_02_008 @squad_control_plane
  Scenario: AC-DG-02-008-03 — Annotations merge into `ScanState` fields documented for HITL (Architecture §4.7).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-008-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_009_01 @us_US_DG_02_009 @squad_control_plane
  Scenario: AC-DG-02-009-01 — Endpoint exists and returns only current tenant’s scans (Architecture §28.2).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_009_02 @us_US_DG_02_009 @squad_control_plane
  Scenario: AC-DG-02-009-02 — Supports filter by `status`, optional `repo` substring, sort by `updated_at` desc default.
    # phase: L3 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_009_03 @us_US_DG_02_009 @squad_control_plane
  Scenario: AC-DG-02-009-03 — Cursor is opaque, stable, and documented max page size (e.g. ≤100).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-009-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_010_01 @us_US_DG_02_010 @squad_control_plane
  Scenario: AC-DG-02-010-01 — `/healthz` (or `/livez`) returns 200 if process up (no DB required).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_010_02 @us_US_DG_02_010 @squad_control_plane
  Scenario: AC-DG-02-010-02 — `/readyz` returns 200 only when DB, Redis, and object store connectivity checks pass (configurable strictness).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_010_03 @us_US_DG_02_010 @squad_control_plane
  Scenario: AC-DG-02-010-03 — Readiness failure includes stable `error_code` body for logs, not secrets.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-010-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_011_01 @us_US_DG_02_011 @squad_control_plane
  Scenario: AC-DG-02-011-01 — `GET /openapi.json` (or `/v1/openapi.json`) serves schema matching implemented routes (Architecture §28).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-011-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_011_02 @us_US_DG_02_011 @squad_control_plane
  Scenario: AC-DG-02-011-02 — Schemas include `CreateScanRequest`, `Scan`, `Finding`, error models with `error_code`.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-011-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_011_03 @us_US_DG_02_011 @squad_control_plane
  Scenario: AC-DG-02-011-03 — CI fails if routes drift from committed OpenAPI snapshot (optional gate).
    # phase: L3 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-011-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_012_01 @us_US_DG_02_012 @squad_control_plane
  Scenario: AC-DG-02-012-01 — 4xx/5xx responses include `application/problem+json` or documented JSON with `type`, `title`, `status`, `error_code`, `detail` (sanitised).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-012-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_012_02 @us_US_DG_02_012 @squad_control_plane
  Scenario: AC-DG-02-012-02 — Validation errors list field-level issues for `CreateScanRequest` without echoing secrets.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-012-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_012_03 @us_US_DG_02_012 @squad_control_plane
  Scenario: AC-DG-02-012-03 — Rate limit responses include `Retry-After` when applicable (Architecture §35.2, EPIC-DG-03).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-012-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_013_01 @us_US_DG_02_013 @squad_control_plane
  Scenario: AC-DG-02-013-01 — API accepts client `X-Request-Id` or generates UUID; returns same in response header.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-013-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_013_02 @us_US_DG_02_013 @squad_control_plane
  Scenario: AC-DG-02-013-02 — Request ID stored on `scans` row or child correlation table and passed in `ScanJobMessage` / worker logs.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-013-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_013_03 @us_US_DG_02_013 @squad_control_plane
  Scenario: AC-DG-02-013-03 — LangFuse/LangSmith sessions remain joinable by `scan_id` + request id (EPIC-DG-11).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-013-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_014_01 @us_US_DG_02_014 @squad_control_plane
  Scenario: AC-DG-02-014-01 — `GET /v1/scans/{scan_id}/findings:export?format=jsonl` (or POST async job) streams newline-delimited JSON with stable field names.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-014-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_014_02 @us_US_DG_02_014 @squad_control_plane
  Scenario: AC-DG-02-014-02 — Export respects tenant RBAC; rate limited to prevent abuse.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-014-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.

  @ac_AC_DG_02_014_03 @us_US_DG_02_014 @squad_control_plane
  Scenario: AC-DG-02-014-03 — Each line includes `finding_id`, `scan_id`, `framework`, `control_id`, `severity`, `evidence_refs` (Architecture §29.1).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-02-014-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-02.
