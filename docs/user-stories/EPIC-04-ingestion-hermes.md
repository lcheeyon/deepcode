# EPIC-DG-04 — Ingestion gateway (Hermes)

> **AC-level test specifications (generated):** Squad copy [`squads/ingestion-codeintel/EPIC-DG-04-detailed.md`](squads/ingestion-codeintel/EPIC-DG-04-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then `python3 scripts/validate_user_stories_traceability.py`.


**Goal:** Acquire source artefacts, optional IaC bundles, and read-only cloud snapshots into the secure work area and object store per `Architecture_Design.md` §11.1, §32 and product docs (Git/ZIP/CI).

**Primary personas:** Developer, CI system, Cloud admin.

---

## US-DG-04-001 — Clone Git repository (shallow by default)

**As a** developer, **I want** Hermes to clone my repo ref, **so that** downstream agents analyse the intended revision.

**Wireframe — repo picker**

```text
┌──────── Repository source ──────────────────┐
│ Provider: ( ) GitHub (x) GitLab ( ) Gitee   │
│ URL: [https://gitlab.com/acme/api.git]     │
│ Ref: [main]   Depth: [50 ▼]                │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-04-001-01:** Supports HTTPS/SSH clone paths documented for GitHub/GitLab/Gitee/Bitbucket (Architecture §11.1; Business doc §4).
- **AC-DG-04-001-02:** `REPO_CLONE_DEPTH` default applied unless overridden by allowed job config (Architecture §27.2).
- **AC-DG-04-001-03:** On success, `repo_local_path` and `repo_metadata` populated in `ScanState` (Architecture §4.2, §5.4).

---

## US-DG-04-002 — Enforce repository size limits

**As a** platform operator, **I want** ingestion to abort oversized archives, **so that** workers are protected from OOM.

**Acceptance criteria**

- **AC-DG-04-002-01:** `REPO_MAX_BYTES` soft cap enforced with clear `ScanAbortError` / `error_code` (Architecture §27.2, §19.1).
- **AC-DG-04-002-02:** ZIP/tarball uploads respect max compressed size policy (2GB in Architecture §11.1).

---

## US-DG-04-003 — Stage encrypted repo archive to object store

**As a** compliance officer, **I want** raw artefacts stored encrypted with lifecycle, **so that** evidence handling matches retention policy.

**Acceptance criteria**

- **AC-DG-04-003-01:** Object key layout `…/scans/{scan_id}/repo.tar.zst` (or equivalent) per §32.1.
- **AC-DG-04-003-02:** Default deletion of repo archive 24h after `COMPLETE` unless tenant override `retention_repo_archive_hours` (Architecture §32.2, §24.1).

---

## US-DG-04-004 — Capture read-only cloud snapshots

**As a** cloud admin, **I want** Hermes to invoke connectors with short-lived creds, **so that** Cassandra analyses current posture.

**Wireframe — cloud profile card**

```text
┌──────── Cloud profile: aws-prod-ro ────────┐
│ Provider: AWS   Regions: ap-southeast-1      │
│ Credential ref: calypso://secret/aws-ro    │
│ [ Test connectivity ]   Status: OK         │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-04-004-01:** Cloud credentials resolved via Calypso pattern with ≤15m TTL; secrets never persisted in `ScanState` (Architecture §20.1).
- **AC-DG-04-004-02:** `cloud_snapshots` map keyed by `profile_id` stored as artifact refs when large (Architecture §5.3, §23.1 Q4).

---

## US-DG-04-005 — IaC-only / cloud-only scan entry points

**As a** solutions architect, **I want** to run scans without all three layers, **so that** I can scope PoCs.

**Acceptance criteria**

- **AC-DG-04-005-01:** IaC-only path accepts Terraform plan JSON / templates per ingestion table (Architecture §11.1).
- **AC-DG-04-005-02:** Cloud-only path permitted when `repo` absent but `cloud_profiles` present and `scan_layers.cloud=true` (Architecture §28.4).

---

## US-DG-04-006 — Private Git over SSH or deploy keys

**As an** enterprise developer, **I want** Hermes to clone private repos using Calypso-backed credentials, **so that** internal code is scannable.

**Wireframe — credential binding**

```text
┌──────── Repo access ────────────────────────────────────────┐
│ Method: (x) SSH deploy key  ( ) HTTPS PAT (vault ref)       │
│ Secret ref: [calypso://secret/gitlab-deploy-acme]           │
│ [ Test clone ]   Last OK: 2026-04-18                         │
└──────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-04-006-01:** SSH key or PAT never logged or persisted in `job_config` plaintext; only `connector_credential_ref` style refs (Architecture §20.1).
- **AC-DG-04-006-02:** Clone failure surfaces `error_code` distinguishing auth vs network vs missing ref.
- **AC-DG-04-006-03:** Known-hosts or strict host key policy configurable for enterprise Git (document default).

---

## US-DG-04-007 — Monorepo sub-path scoping

**As a** repo owner, **I want** optional `repo.sub_path`, **so that** scans target `services/payments/` only.

**Acceptance criteria**

- **AC-DG-04-007-01:** When `sub_path` set, Hermes stages only that subtree; path normalisation blocks `../` escape.
- **AC-DG-04-007-02:** Argus indexing honours same root for embeddings and tools (EPIC-DG-06).
- **AC-DG-04-007-03:** Report metadata records `sub_path` for audit (EPIC-DG-10).

---

## US-DG-04-008 — CI pipeline artifact ingestion

**As a** CI author, **I want** to push tarball or OCI layer digest to Hermes, **so that** I can scan build outputs without exposing full monorepo.

**Acceptance criteria**

- **AC-DG-04-008-01:** Multipart or pre-signed PUT flow documented; max size aligns `REPO_MAX_BYTES` (Architecture §11.1, §27.2).
- **AC-DG-04-008-02:** Checksum verification (`checksum_sha256`) optional but recommended; mismatch fails fast.
- **AC-DG-04-008-03:** Uploaded artefact lands under tenant-scoped object prefix before worker extract (Architecture §32.1).

---

## US-DG-04-009 — Full clone option for blame / history signals

**As a** security analyst, **I want** optional full clone, **so that** future agents can use git history where product enables it.

**Acceptance criteria**

- **AC-DG-04-009-01:** `job_config` flag requests depth=full; default remains shallow (Architecture §11.1).
- **AC-DG-04-009-02:** Full clone wall time surfaced in scan metadata; timeout participates in budget (EPIC-DG-01).
- **AC-DG-04-009-03:** If history unused by graph, feature is no-op aside from clone cost (document).

---

## US-DG-04-010 — Record resolved `repo_commit_sha` on scan

**As an** auditor, **I want** immutable commit SHA on the scan row, **so that** evidence ties to exact revision.

**Acceptance criteria**

- **AC-DG-04-010-01:** After clone, `repo_commit_sha` persisted on `scans` even when request sent only `ref` (Architecture §29.1).
- **AC-DG-04-010-02:** Detached HEAD state recorded correctly.
- **AC-DG-04-010-03:** Mismatch between requested `commit_sha` and resolved head fails with clear `error_code` when strict mode enabled.

---

## US-DG-04-011 — Hermes metadata for languages and file counts

**As a** mapper, **I want** `RepoMetadata` with LOC estimates and excluded binary counts, **so that** Athena can tune retrieval.

**Acceptance criteria**

- **AC-DG-04-011-01:** `repo_metadata` includes total files, ignored paths summary, binary-skipped count (fields documented in schema).
- **AC-DG-04-011-02:** Extremely large file list truncation flagged for report appendix (Architecture §11.6).
- **AC-DG-04-011-03:** Metadata serialisable size bounded; spill to artifact ref if huge (Architecture §5.3).

---

## US-DG-04-012 — Cloud snapshot per-region fan-out and compression

**As a** multi-region customer, **I want** multiple regions per profile, **so that** Cassandra sees full estate.

**Acceptance criteria**

- **AC-DG-04-012-01:** `cloud_profiles[].regions` array honoured; failures per region recorded in snapshot metadata (EPIC-DG-07).
- **AC-DG-04-012-02:** Snapshots stored compressed (`*.json.zst`) under object layout §32.1.
- **AC-DG-04-012-03:** Partial regional success still produces snapshot with `coverage_percent` field.
