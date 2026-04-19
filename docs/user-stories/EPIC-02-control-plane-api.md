# EPIC-DG-02 — Control plane HTTP API (FastAPI)

> **AC-level test specifications (generated):** Squad copy [`squads/control-plane/EPIC-DG-02-detailed.md`](squads/control-plane/EPIC-DG-02-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then `python3 scripts/validate_user_stories_traceability.py`.


**Goal:** Expose a versioned, tenant-safe HTTP API for creating and observing scans, retrieving findings and artefacts, and managing policies per `Architecture_Design.md` §28.

**Primary personas:** CI pipeline, Back-end integrator, Auditor (read-only).

---

## US-DG-02-001 — Create scan job with layered configuration

**As a** CI integrator, **I want** to `POST /v1/scans` with repo, policies, layers, optional cloud profiles and budgets, **so that** the engine analyses the correct scope.

**Wireframe — “Create scan” request builder (conceptual UI or API client)**

```text
┌──────── New Scan ─────────────────────────────┐
│ Repo URL: [https://gitlab…/svc.git    ]     │
│ Ref: [main]  Commit: [optional SHA]         │
│ Policies: [x] ISO-27001  [x] GB-T-22239     │
│ Layers:  (x) Code  (x) IaC  ( ) Cloud       │
│ Cloud profiles: [ + Add profile ]           │
│ Budget: max LLM USD [ 12.5 ]  wall [3600s]  │
│           [ Start Scan ]                    │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-02-001-01:** Request body validates `CreateScanRequest` shape including `repo`, `policy_ids`, `scan_layers`, optional `cloud_profiles`, `notifications`, `budget` (Architecture §28.4).
- **AC-DG-02-001-02:** Validation rejects jobs where `scan_layers.cloud=true` but neither `repo` nor `cloud_profiles` satisfy minimum inputs per normative rules (Architecture §28.4).
- **AC-DG-02-001-03:** Validation rejects `scan_layers.code=true` or `iac=true` without `repo` when required (Architecture §28.4).
- **AC-DG-02-001-04:** Response `201` returns `scan_id` and initial `status` in {`PENDING`,`QUEUED`}.

---

## US-DG-02-002 — Idempotent scan creation

**As a** CI pipeline, **I want** duplicate submissions with the same idempotency key to return the same scan, **so that** retries do not fork jobs.

**Acceptance criteria**

- **AC-DG-02-002-01:** `Idempotency-Key` header optional; duplicates within 24h return same `scan_id` with `201` or documented idempotent success code (Architecture §28.3).
- **AC-DG-02-002-02:** DB uniqueness on `(tenant_id, idempotency_key)` enforced (Architecture §29.1).

---

## US-DG-02-003 — Poll scan status with stage granularity

**As an** operator, **I want** `GET /v1/scans/{scan_id}`, **so that** I can surface progress and errors.

**Wireframe — status card**

```text
┌──────── Scan 3fa2… ────────────────────────┐
│ Status: MAPPING (72%)                       │
│ Stage started: 2026-04-18T10:21:05Z         │
│ Policies: ISO-27001-2022 @ 2026-03-01      │
│ Error code: (empty)                         │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-02-003-01:** Response includes `current_stage`, `stage_started_at`, `percent_complete`, `error_code`, `error_message` (sanitised) per §28.5.
- **AC-DG-02-003-02:** Terminal states `COMPLETE`, `FAILED`, `CANCELLED`, `AWAITING_REVIEW` behave as documented (Architecture §28.5).
- **AC-DG-02-003-03:** Cross-tenant access returns `404` or `403` without leaking existence (security baseline).

---

## US-DG-02-004 — Paginated findings export

**As an** auditor, **I want** `GET /v1/scans/{scan_id}/findings` with filters, **so that** I can export evidence for control testing.

**Acceptance criteria**

- **AC-DG-02-004-01:** Supports `severity`, `framework`, `cursor` pagination (Architecture §28.3).
- **AC-DG-02-004-02:** Each finding includes stable identifiers: `framework`, `control_id`, `status`, `severity`, `evidence_refs`, `confidence_score`, `policy_version` (Architecture §29.1 fields / §3 model).

---

## US-DG-02-005 — Secure artefact download

**As a** user, **I want** presigned or proxied artefact access, **so that** reports are not publicly enumerable.

**Acceptance criteria**

- **AC-DG-02-005-01:** `GET /v1/scans/{scan_id}/artifacts/{artifact_id}` returns `302` to short-TTL presigned URL or streams via authenticated proxy (Architecture §28.3).
- **AC-DG-02-005-02:** Artefact row stores `checksum_sha256`, `size_bytes`, `encryption` mode (Architecture §29.1).

---

## US-DG-02-006 — Signed webhooks

**As a** SecOps integrator, **I want** signed `scan.completed` / `scan.failed` webhooks, **so that** my SOAR can trust events.

**Acceptance criteria**

- **AC-DG-02-006-01:** Payload includes `event`, `scan_id`, `tenant_id`, `report_artifact_id` when completed (Architecture §28.6).
- **AC-DG-02-006-02:** `X-DeepGuard-Signature: sha256=<hex>` verifies raw body with shared secret (Architecture §28.6).
- **AC-DG-02-006-03:** Retries with exponential backoff and DLQ rows in `webhook_deliveries` (Architecture §28.6, §29.4).

---

## US-DG-02-007 — API versioning and deprecation headers

**As an** API consumer, **I want** stable `/v1` paths and sunset notices, **so that** I can plan breaking migrations.

**Acceptance criteria**

- **AC-DG-02-007-01:** All documented resources live under base path `/v1` (Architecture §28.1).
- **AC-DG-02-007-02:** Deprecated endpoints return `Sunset` header per RFC 8594 when applicable (Architecture §28.1).
- **AC-DG-02-007-03:** Breaking changes require `/v2` path prefix; changelog references story IDs where maintained.

---

## US-DG-02-008 — Resume human-in-the-loop scan

**As a** reviewer, **I want** `POST /v1/scans/{scan_id}/resume` with annotations JSON, **so that** Athena receives reviewer context.

**Acceptance criteria**

- **AC-DG-02-008-01:** Resume returns `202` when graph was interrupted and credentials still valid (Architecture §28.3).
- **AC-DG-02-008-02:** Resume rejected with clear error when scan not in `AWAITING_REVIEW` or user lacks role (Architecture §28.3, EPIC-DG-03).
- **AC-DG-02-008-03:** Annotations merge into `ScanState` fields documented for HITL (Architecture §4.7).

---

## US-DG-02-009 — List scans for tenant (cursor pagination)

**As a** dashboard user, **I want** `GET /v1/scans` with filters and cursor, **so that** I can page history without loading full tables.

**Wireframe — list API consumer**

```text
GET /v1/scans?status=FAILED&cursor=eyJ…
→ 200 { items: [...], next_cursor: "…" | null }
```

**Acceptance criteria**

- **AC-DG-02-009-01:** Endpoint exists and returns only current tenant’s scans (Architecture §28.2).
- **AC-DG-02-009-02:** Supports filter by `status`, optional `repo` substring, sort by `updated_at` desc default.
- **AC-DG-02-009-03:** Cursor is opaque, stable, and documented max page size (e.g. ≤100).

---

## US-DG-02-010 — Service health and readiness

**As a** k8s operator, **I want** liveness/readiness endpoints, **so that** rollouts do not send traffic to broken API pods.

**Acceptance criteria**

- **AC-DG-02-010-01:** `/healthz` (or `/livez`) returns 200 if process up (no DB required).
- **AC-DG-02-010-02:** `/readyz` returns 200 only when DB, Redis, and object store connectivity checks pass (configurable strictness).
- **AC-DG-02-010-03:** Readiness failure includes stable `error_code` body for logs, not secrets.

---

## US-DG-02-011 — OpenAPI schema publication

**As a** integrator, **I want** machine-readable OpenAPI 3.x, **so that** I can generate SDKs.

**Acceptance criteria**

- **AC-DG-02-011-01:** `GET /openapi.json` (or `/v1/openapi.json`) serves schema matching implemented routes (Architecture §28).
- **AC-DG-02-011-02:** Schemas include `CreateScanRequest`, `Scan`, `Finding`, error models with `error_code`.
- **AC-DG-02-011-03:** CI fails if routes drift from committed OpenAPI snapshot (optional gate).

---

## US-DG-02-012 — Structured problem details on errors

**As a** client developer, **I want** RFC 7807-style problem JSON, **so that** I can branch logic on `error_code` without parsing prose.

**Acceptance criteria**

- **AC-DG-02-012-01:** 4xx/5xx responses include `application/problem+json` or documented JSON with `type`, `title`, `status`, `error_code`, `detail` (sanitised).
- **AC-DG-02-012-02:** Validation errors list field-level issues for `CreateScanRequest` without echoing secrets.
- **AC-DG-02-012-03:** Rate limit responses include `Retry-After` when applicable (Architecture §35.2, EPIC-DG-03).

---

## US-DG-02-013 — Correlation IDs across API and workers

**As an** SRE, **I want** `X-Request-Id` propagated to logs and traces, **so that** I can tie HTTP to graph spans.

**Acceptance criteria**

- **AC-DG-02-013-01:** API accepts client `X-Request-Id` or generates UUID; returns same in response header.
- **AC-DG-02-013-02:** Request ID stored on `scans` row or child correlation table and passed in `ScanJobMessage` / worker logs.
- **AC-DG-02-013-03:** LangFuse/LangSmith sessions remain joinable by `scan_id` + request id (EPIC-DG-11).

---

## US-DG-02-014 — Export findings as JSONL for SIEM

**As a** SOC engineer, **I want** bulk export of findings for a scan, **so that** I can load them into Splunk/Databricks.

**Acceptance criteria**

- **AC-DG-02-014-01:** `GET /v1/scans/{scan_id}/findings:export?format=jsonl` (or POST async job) streams newline-delimited JSON with stable field names.
- **AC-DG-02-014-02:** Export respects tenant RBAC; rate limited to prevent abuse.
- **AC-DG-02-014-03:** Each line includes `finding_id`, `scan_id`, `framework`, `control_id`, `severity`, `evidence_refs` (Architecture §29.1).
