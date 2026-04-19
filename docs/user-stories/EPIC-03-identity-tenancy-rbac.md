# EPIC-DG-03 — Identity, tenancy & RBAC (Eumaeus)

> **AC-level test specifications (generated):** Squad copy [`squads/identity-tenancy/EPIC-DG-03-detailed.md`](squads/identity-tenancy/EPIC-DG-03-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py`.


**Goal:** Enforce tenant isolation and role capabilities across API and data paths per `Architecture_Design.md` §28.2, §29, §24.

**Primary personas:** Tenant admin, Scanner, Auditor.

---

## US-DG-03-001 — OIDC JWT authentication (SaaS / enterprise)

**As a** tenant admin, **I want** users to authenticate via OIDC JWT, **so that** roles and `tenant_id` are cryptographically bound.

**Wireframe — login / token flow (simplified)**

```text
  User                IdP                DeepGuard API
   |-- login -------->|                   |
   |<-- id_token -----|                   |
   |--- Authorization: Bearer <JWT> ---->|  /v1/scans
```

**Acceptance criteria**

- **AC-DG-03-001-01:** JWT validates issuer/audience configured by `JWT_ISSUER`, `JWT_AUDIENCE` (Architecture §27.1, §28.2).
- **AC-DG-03-001-02:** Claim `tenant_id` (UUID) is mandatory for authorisation context.
- **AC-DG-03-001-03:** Roles `scanner`, `admin`, `auditor` constrain verbs (e.g. auditors read-only; policy upload admin-only) (Architecture §28.2).

---

## US-DG-03-002 — Hard tenant isolation on all resources

**As a** security officer, **I want** no cross-tenant reads/writes, **so that** customer data never leaks across logical boundaries.

**Acceptance criteria**

- **AC-DG-03-002-01:** Every persisted row carries `tenant_id` and API middleware rejects mismatched paths (Architecture §28.2, §29.1).
- **AC-DG-03-002-02:** Object storage keys are namespaced by `tenant_id` / `scan_id` (Architecture §32.1).

---

## US-DG-03-003 — Runtime configuration merge

**As a** platform admin, **I want** tenant-level `runtime_config` merged with safe defaults, **so that** features can be toggled without code deploy.

**Wireframe — tenant settings (admin)**

```text
┌──── Tenant runtime flags ────────────────────┐
│ semantic_cache_enabled: [on|off]            │
│ semantic_cache_threshold: [0.97] (0.95–0.99)│
│ delta_skip_analysis: [ ]                    │
│ max_concurrent_scans: [3]                   │
│                        [ Save ]             │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-03-003-01:** Effective config = `deep_merge(DEFAULT_RUNTIME_CONFIG, tenants.runtime_config[, scan_job_overrides])` per §24.2.
- **AC-DG-03-003-02:** Scan-level overrides allowed only for `budget.*` and `notifications.*` unless role `admin` (Architecture §24.2).
- **AC-DG-03-003-03:** Safety flags such as `semantic_cache_threshold` cannot be overridden by non-admin (Architecture §24.2).

---

## US-DG-03-004 — Backpressure for concurrent scans

**As a** SaaS operator, **I want** per-tenant concurrency caps, **so that** noisy neighbours cannot exhaust workers.

**Acceptance criteria**

- **AC-DG-03-004-01:** When `max_concurrent_scans` / `MAX_CONCURRENT_SCANS_PER_TENANT` exceeded, API returns `429` with `Retry-After` (Architecture §35.2, §24.1).

---

## US-DG-03-005 — Machine-to-machine authentication (optional mTLS)

**As a** platform engineer, **I want** worker ↔ internal API authentication via mTLS, **so that** only enrolled workers enqueue or claim work.

**Acceptance criteria**

- **AC-DG-03-005-01:** When mTLS enabled, API verifies client cert chain and maps certificate to `tenant_id` / service identity (Architecture §28.2).
- **AC-DG-03-005-02:** mTLS identities cannot impersonate human JWT roles unless explicitly granted service role.
- **AC-DG-03-005-03:** Misconfigured cert returns `403` without leaking tenant existence.

---

## US-DG-03-006 — Immutable audit log for security-relevant actions

**As an** auditor, **I want** append-only audit events for policy upload, resume, runtime flag change, **so that** investigations are trustworthy.

**Wireframe — audit trail (UI)**

```text
┌──────── Audit log ──────────────────────────────────────────┐
│ 10:22Z  admin@…  policy.upload  policy_id=acme-sdlc v3    │
│ 10:05Z  svc-ci     scan.create    scan_id=… idem=build-442  │
└─────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-03-006-01:** Events capture actor, action, target id, IP (if available), outcome (success/fail).
- **AC-DG-03-006-02:** Audit store is append-only from API perspective (no delete via public API).
- **AC-DG-03-006-03:** Retention period configurable per deployment (align §14.2).

---

## US-DG-03-007 — Role matrix documented and enforced in middleware

**As a** security architect, **I want** a single role→permission matrix, **so that** new routes do not ship without authz.

**Acceptance criteria**

- **AC-DG-03-007-01:** Matrix covers `POST /v1/scans`, `POST …/cancel`, `POST …/resume`, `POST /v1/policies:upload`, findings export (EPIC-DG-02).
- **AC-DG-03-007-02:** Missing role returns `403` with `error_code=FORBIDDEN`.
- **AC-DG-03-007-03:** Automated contract tests assert matrix for each route template.

---

## US-DG-03-008 — Tenant lifecycle (create, suspend, delete)

**As a** SaaS operator, **I want** to suspend a tenant, **so that** billing abuse or legal hold stops new scans immediately.

**Acceptance criteria**

- **AC-DG-03-008-01:** Suspended tenant receives `403` on mutating endpoints; read access policy documented (e.g. allow auditors read-only).
- **AC-DG-03-008-02:** In-flight scans behaviour on suspend: cooperative cancel or run-to-completion (document single chosen behaviour).
- **AC-DG-03-008-03:** Delete tenant is soft-delete with retention schedule or hard-delete behind break-glass (document).

---

## US-DG-03-009 — OIDC refresh and session binding for console

**As a** end user, **I want** short access token + refresh via IdP, **so that** stolen tokens expire quickly.

**Acceptance criteria**

- **AC-DG-03-009-01:** Console uses PKCE for SPA OAuth where applicable; no long-lived API keys in browser storage by default.
- **AC-DG-03-009-02:** Logout clears client session and invalidates refresh if server-side session store used.
- **AC-DG-03-009-03:** CORS rules restrict console origin per tenant deployment config.

---

## US-DG-03-010 — Service accounts for CI with scoped tokens

**As a** DevOps lead, **I want** CI-scoped tokens limited to `scanner` on one tenant, **so that** pipeline leaks are blast-radius limited.

**Acceptance criteria**

- **AC-DG-03-010-01:** Service account creation requires `admin`; token lists show prefix + created_at only (never full secret twice).
- **AC-DG-03-010-02:** Token revocation is immediate for new requests; in-flight scan policy documented.
- **AC-DG-03-010-03:** Tokens are hashed at rest; compare using constant-time compare.
