# Auto-generated from docs/user-stories/traceability-ac-detail-matrix.csv
# Edit AC text in EPIC-*.md, then regenerate.

@epic_EPIC_DG_14
Feature: EPIC-DG-14 acceptance criteria traceability stubs

  These scenarios are placeholders for BDD mapping.
  Replace Given/When/Then with executable step definitions.

  @ac_AC_DG_14_001_01 @us_US_DG_14_001 @squad_frontend
  Scenario: AC-DG-14-001-01 — CSS variables (or Tailwind theme) map to **semantic tokens** in `reference.md` §1 (`surface.page`, `surface.card`, `text.primary`, `brand.primary` `#4f46e5` light, `#818cf8` dark,…
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-001-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_001_02 @us_US_DG_14_001 @squad_frontend
  Scenario: AC-DG-14-001-02 — **One primary** button per viewport (style guide §6); destructive actions use **destructive** variant + confirm modal.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-001-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_001_03 @us_US_DG_14_001 @squad_frontend
  Scenario: AC-DG-14-001-03 — Sidebar order matches style guide: logo, tenant, **Scans**, then **disabled/placeholder** entries (Findings, Policies, Reports) with tooltip “Not available in API yet” until EPIC-…
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-001-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_001_04 @us_US_DG_14_001 @squad_frontend
  Scenario: AC-DG-14-001-04 — Footer shows app **version** + **environment** pill (`surface.subtle`, `text.muted`).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-001-04"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_002_01 @us_US_DG_14_002 @squad_frontend
  Scenario: AC-DG-14-002-01 — **Test connection** calls `GET /v1/healthz` (no auth); success shows **toast** “Saved” / “Connected” per `reference.md` §3.1.
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-002-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_002_02 @us_US_DG_14_002 @squad_frontend
  Scenario: AC-DG-14-002-02 — All authenticated requests send **`X-API-Key`** header; optional toggle to send **`Authorization: Bearer`** instead (mutually exclusive).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-002-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_002_03 @us_US_DG_14_002 @squad_frontend
  Scenario: AC-DG-14-002-03 — On **401**, show **inline alert** (`status.error.bg`, `role="alert"`) with copy deck error “You don’t have access” variant where applicable.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-002-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_003_01 @us_US_DG_14_003 @squad_frontend
  Scenario: AC-DG-14-003-01 — **Refresh** triggers `GET /v1/healthz`; loading state uses **skeleton** or spinner on card only (no global success toast on poll — style guide §11).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-003-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_003_02 @us_US_DG_14_003 @squad_frontend
  Scenario: AC-DG-14-003-02 — If health fails, **sticky error toast** until dismissed (`reference.md` §3.2).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-003-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_004_01 @us_US_DG_14_004 @squad_frontend
  Scenario: AC-DG-14-004-01 — Client-side validation mirrors **Pydantic** rules: at least one layer; cloud requires repo and/or profiles; code/IaC requires repo; `policy_ids` min 1; **archive** requires `stora…
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-004-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_004_02 @us_US_DG_14_004 @squad_frontend
  Scenario: AC-DG-14-004-02 — Successful **201** → **toast** “Scan queued” (`reference.md` §3.1) + navigate to **Scan detail** + append `scan_id` to **recent scans** (US-DG-14-008).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-004-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_004_03 @us_US_DG_14_004 @squad_frontend
  Scenario: AC-DG-14-004-03 — **422** maps field errors to **inline** `role="alert"` per field (style guide §8).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-004-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_005_01 @us_US_DG_14_005 @squad_frontend
  Scenario: AC-DG-14-005-01 — On **503** with `REPO_UPLOAD_S3_UNCONFIGURED`, show **inline alert** + link to docs (`.env.example` S3 vars); do not crash.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-005-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_005_02 @us_US_DG_14_005 @squad_frontend
  Scenario: AC-DG-14-005-02 — On success, **auto-fill** `storage_uri` on create-scan form (`sentence case` labels).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-005-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_005_03 @us_US_DG_14_005 @squad_frontend
  Scenario: AC-DG-14-005-03 — PUT uses **`upload_headers`** from API response; CORS failures show error deck “Something went wrong” with optional **request id** if exposed by future middleware.
    # phase: L3 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-005-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_006_01 @us_US_DG_14_006 @squad_frontend
  Scenario: AC-DG-14-006-01 — Poll every **5s** with **backoff when tab hidden** (EPIC-12 AC pattern); **no toast** on each successful poll.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-006-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_006_02 @us_US_DG_14_006 @squad_frontend
  Scenario: AC-DG-14-006-02 — **404** → dedicated empty state card (“Scan not found”) + link back to Scans hub.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-006-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_006_03 @us_US_DG_14_006 @squad_frontend
  Scenario: AC-DG-14-006-03 — `job_config` viewer is **read-only**; expand/collapse with **accessible** button (`aria-expanded`).
    # phase: L3 / priority: P0
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-006-03"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_007_01 @us_US_DG_14_007 @squad_frontend
  Scenario: AC-DG-14-007-01 — **202** response → **toast** success + refresh row; **404** → error toast + message body.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-007-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_007_02 @us_US_DG_14_007 @squad_frontend
  Scenario: AC-DG-14-007-02 — Modal obeys **focus trap** and **Escape** behaviour per style guide §12 (Escape blocked if dirty — N/A here).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-007-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_008_01 @us_US_DG_14_008 @squad_frontend
  Scenario: AC-DG-14-008-01 — Persist last **50** `scan_id` + `updated_at` + optional label in **`localStorage`**; **clear list** control with destructive confirm.
    # phase: L3 / priority: P2
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-008-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_008_02 @us_US_DG_14_008 @squad_frontend
  Scenario: AC-DG-14-008-02 — **Open by ID** validates UUID before GET.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-008-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_009_01 @us_US_DG_14_009 @squad_frontend
  Scenario: AC-DG-14-009-01 — Map `QUEUED`, `INGESTING`, `ANALYZING`, … to **badge** colours: use **`status.*`** tokens; pair **dot + label** (style guide §13), not colour alone.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-009-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_009_02 @us_US_DG_14_009 @squad_frontend
  Scenario: AC-DG-14-009-02 — `percent_complete` uses **tabular nums**; right-align in tables (`font-variant-numeric: tabular-nums`).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-009-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_010_01 @us_US_DG_14_010 @squad_frontend
  Scenario: AC-DG-14-010-01 — At `<lg`, sidebar becomes **drawer** with overlay **z-index** per `reference.md` §6; **no hamburger-only** critical actions on desktop (style guide §16).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-010-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_010_02 @us_US_DG_14_010 @squad_frontend
  Scenario: AC-DG-14-010-02 — Page padding **16px** on small breakpoints (style guide §4).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-010-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_011_01 @us_US_DG_14_011 @squad_frontend
  Scenario: AC-DG-14-011-01 — Meet checklist **§15** of the UI skill (contrast, focus ring `brand.primary` 2px offset 2px, targets ≥24px / 40px icon-only, `aria-*` on tables/modals/forms).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-011-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_011_02 @us_US_DG_14_011 @squad_frontend
  Scenario: AC-DG-14-011-02 — **`prefers-reduced-motion`** removes non-essential motion (skill §14).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-011-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_012_01 @us_US_DG_14_012 @squad_frontend
  Scenario: AC-DG-14-012-01 — Toggle persists; all screens use **dark** column from `reference.md` §1.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-012-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_012_02 @us_US_DG_14_012 @squad_frontend
  Scenario: AC-DG-14-012-02 — No **pure #000 on #fff** large fields (skill §2).
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-012-02"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_013_01 @us_US_DG_14_013 @squad_frontend
  Scenario: AC-DG-14-013-01 — At minimum: **health** → **create scan (git stub)** → **GET detail** → assert visible `scan_id` (align with `deepguard-delivery-quality` skill: BDD after unit tests for this slice…
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-013-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.

  @ac_AC_DG_14_014_01 @us_US_DG_14_014 @squad_frontend
  Scenario: AC-DG-14-014-01 — `apps/web` (or chosen path) **README** documents `NEXT_PUBLIC_*` env vars, API base URL, and points to **`docs/design/frontend-console-mvp-wireframes-and-mockups.md`**.
    # phase: L3 / priority: P1
    Given Tenant and scan fixtures exist; services healthy per test environment bootstrap.
    When the system executes behavior for "AC-DG-14-014-01"
    Then Assertions pass; no secret material in logs; stable machine-readable error_code on failures; tenant isolation preserved for EPIC-DG-14.
