# Supplement — ingestion & scan-create contracts (precedes full EPIC-02/04 automation)

> **Traceability:** This file is **not** parsed by `scripts/generate_ac_details_and_squad_docs.py` (filename does not match `EPIC-*.md`). When promoting a story into a canonical epic, add it to `EPIC-02-control-plane-api.md` or `EPIC-04-ingestion-hermes.md` and regenerate the CSV.

Canonical backlog remains in `EPIC-02-control-plane-api.md` and `EPIC-04-ingestion-hermes.md`. The following items were **not spelled as separate US rows** in those files but are **required** for a safe, testable implementation of **US-DG-02-001**, **US-DG-04-001**, **04-002**, **04-003**, and **04-008**.

---

## US-DG-02-015 — Presigned repo artefact upload (feeds archive scans)

**As a** CI integrator, **I want** a **server-issued presigned `PUT`** targeting a tenant-scoped staging key, **so that** I can upload a tarball without sharing long-lived object-store credentials with browsers or runners.

**Acceptance criteria**

- **AC-DG-02-015-01:** `POST /v1/repo-uploads` (authenticated, tenant-scoped) returns `upload_id`, `upload_url`, optional `upload_headers`, and a **`storage_uri`** (`s3://bucket/…`) suitable for `CreateScanRequest.repo` when `source=archive`.
- **AC-DG-02-015-02:** When object-store env is not configured, the endpoint returns **503** with a stable `error_code` (no partial credentials in the response body).

---

## US-DG-04-015 — Hermes outcome persisted on the scan row

**As a** mapper, **I want** `repo_commit_sha` (git) and a **`hermes` JSON fragment** merged into `job_config` after ingestion, **so that** Argus / Athena can read `repo_archive` metadata without re-querying object inventory.

**Acceptance criteria**

- **AC-DG-04-015-01:** After successful Hermes, `scans.repo_commit_sha` is set for **git** sources when `git rev-parse` succeeds.
- **AC-DG-04-015-02:** `job_config` gains `hermes.repo_archive` with `storage_uri`, `checksum_sha256`, `size_bytes` (when known), `format` (e.g. `tar_gz`).

---

## US-DG-04-016 — Opt-in Hermes execution on workers

**As a** platform operator, **I want** Hermes **disabled by default** until `DEEPGUARD_HERMES_ENABLED` and S3 credentials are set, **so that** local unit tests and laptops without MinIO keep today’s fast stub path.

**Acceptance criteria**

- **AC-DG-04-016-01:** When Hermes is **disabled**, the worker skips clone/upload and proceeds to the existing graph/report stages unchanged.
- **AC-DG-04-016-02:** When Hermes is **enabled** but S3 is **misconfigured**, the scan transitions to **FAILED** with `error_code=HERMES_S3_UNCONFIGURED` (or equivalent stable string).

---

## US-DG-04-017 — Server-side checksum verification for archive scans (optional hardening)

**As a** security analyst, **I want** the worker to **verify `checksum_sha256`** after downloading a customer-staged archive when the client supplied it, **so that** tampered uploads fail before graph execution.

**Acceptance criteria**

- **AC-DG-04-017-01:** If `repo.checksum_sha256` is present on an `archive` source, Hermes **compares** the digest of staged bytes and fails with `HERMES_CHECKSUM_MISMATCH` on mismatch.

*Implementation note:* Initial slice may ship **04-017** as a no-op when checksum omitted; mismatch detection is required only when the field is populated.

---

## Deferred — SSE-KMS / tenant CMK for repo archives

**As a** enterprise security officer, **I want** repo archives encrypted with **tenant-managed keys**, **so that** object-store operators cannot read source code.

**Status:** **Deferred** — current implementation uses **SSE-S3** style metadata (`encryption` field on artefacts) and plain `put_object` for dev parity with MinIO. Track as a future epic when Calypso/KMS integration is scheduled.
