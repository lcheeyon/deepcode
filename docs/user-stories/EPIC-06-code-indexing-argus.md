# EPIC-DG-06 — Code indexing & retrieval (Argus)

> **AC-level test specifications (generated):** Squad copy [`squads/ingestion-codeintel/EPIC-DG-06-detailed.md`](squads/ingestion-codeintel/EPIC-DG-06-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then `python3 scripts/validate_user_stories_traceability.py`.


**Goal:** Parse multi-language code, build dependency signals, chunk semantically, embed into pgvector, and support hybrid retrieval per `Architecture_Design.md` §11–§12.

**Primary personas:** Security engineer, ML engineer (tuning).

---

## US-DG-06-001 — Language-aware AST parse & chunking

**As a** security engineer, **I want** AST-boundary chunking, **so that** embeddings preserve semantic units.

**Wireframe — language coverage dashboard**

```text
┌──────── Repo language breakdown ────────────┐
│ Python   ████████████  62%                │
│ TypeScript ██████      28%                │
│ Go       ██            10%                │
│ [ View excluded files ]                    │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-06-001-01:** GA languages from support matrix use tree-sitter path (Architecture §11.2–11.4).
- **AC-DG-06-001-02:** Chunker never splits mid-function/class for configured node types (Architecture §11.4).
- **AC-DG-06-001-03:** `language_breakdown` populated in `ScanState` (Architecture §4.2).

---

## US-DG-06-002 — Build dependency graph with caps

**As a** engineer, **I want** dependency graph construction with truncation flags, **so that** monorepos remain tractable.

**Acceptance criteria**

- **AC-DG-06-002-01:** Graph includes external deps and vulnerable deps cross-ref hooks (Architecture §11.5–11.6).
- **AC-DG-06-002-02:** When exceeding `max_nodes` / `max_depth`, status `TRUNCATED` recorded and warning surfaces in report (Architecture §23.1 Q6).

---

## US-DG-06-003 — Hybrid retrieval (BM25 + vector)

**As a** mapper author, **I want** hybrid retrieval for code, **so that** identifier-exact matches are not missed.

**Acceptance criteria**

- **AC-DG-06-003-01:** Ensemble retriever weights documented default (0.3 BM25 / 0.7 vector) configurable within bounds (Architecture §12.3).
- **AC-DG-06-003-02:** `code_chunks` rows include `tenant_id`, `scan_id`, metadata JSON for file/line span (Architecture §12.1).

---

## US-DG-06-004 — Large repository handling modes

**As a** enterprise customer, **I want** predictable behaviour beyond 500k LOC, **so that** scans complete within SLA targets.

**Acceptance criteria**

- **AC-DG-06-004-01:** Strategies per size tier applied (Architecture §11.6).
- **AC-DG-06-004-02:** For >2M LOC, scan requires explicit sub-path scoping or async batch mode flag (Architecture §11.6).

---

## US-DG-06-005 — Security pattern signals (non-LLM layer)

**As a** false-positive owner, **I want** semgrep-style checks where configured, **so that** obvious issues have deterministic anchors.

**Acceptance criteria**

- **AC-DG-06-005-01:** Security pattern scanner outputs feed Athena context as structured signals (Architecture §11.3).

---

## US-DG-06-006 — Respect `.deepguardignore` and repo ignore patterns

**As a** developer, **I want** vendor and generated dirs excluded, **so that** scans focus on first-party code.

**Acceptance criteria**

- **AC-DG-06-006-01:** Ignore file grammar documented; default excludes `node_modules/`, `.git/`, large `dist/` unless overridden.
- **AC-DG-06-006-02:** Excluded path count and total bytes skipped recorded in `repo_metadata` / scan summary.
- **AC-DG-06-006-03:** Explicit `include_paths` in job config overrides ignore for emergency audits (admin only).

---

## US-DG-06-007 — Embedding batch pipeline with L4 cache

**As a** cost owner, **I want** embedding cache hits by `sha256(text_chunk + model_id)`, **so that** re-scans avoid re-embedding unchanged chunks when policy allows (Architecture §9.1, §9.4 L4).

**Acceptance criteria**

- **AC-DG-06-007-01:** Cache key and TTL 7d default; invalidation on embedding model version change (Architecture §9.4).
- **AC-DG-06-007-02:** Cache miss path records latency metric per batch (EPIC-DG-11).
- **AC-DG-06-007-03:** Tenant flag can disable shared embedding cache for paranoid mode (document trade-off).

---

## US-DG-06-008 — Incremental / delta index when feature enabled

**As a** frequent CI user, **I want** delta scope between commits, **so that** token spend drops 60–80% when enabled (Architecture §9.3).

**Acceptance criteria**

- **AC-DG-06-008-01:** When `DELTA_SKIP_ANALYSIS` / `delta_skip_analysis` true and fingerprint matches, behaviour matches MVP decision §23.1 Q7 (re-run Athena+Circe+Penelope on policy bump; optional skip analysis layers).
- **AC-DG-06-008-02:** Delta fingerprint includes `repo_commit_sha` + `policy_version` + `scan_layers` (Architecture §23.1 Q7).
- **AC-DG-06-008-03:** Carry-forward findings list references prior `scan_id` for audit trail.

---

## US-DG-06-009 — BM25 index lifecycle per scan

**As a** search engineer, **I want** BM25 index built for `scan_id` tenant scope, **so that** hybrid retrieval is isolated.

**Acceptance criteria**

- **AC-DG-06-009-01:** BM25 documents deleted or tombstoned when scan artefacts expire (align retention §14.2).
- **AC-DG-06-009-02:** No cross-tenant BM25 query possible at API/SQL layer.
- **AC-DG-06-009-03:** Reindex job idempotent if worker retries Argus node.

---

## US-DG-06-010 — Binary and generated file detection

**As a** platform engineer, **I want** binaries skipped from embedding, **so that** pgvector is not polluted.

**Acceptance criteria**

- **AC-DG-06-010-01:** linguist-style heuristics + size cap classify binaries; list surfaced in report appendix.
- **AC-DG-06-010-02:** Misclassified text-as-binary override API for path glob (admin).
- **AC-DG-06-010-03:** Skipped files do not appear as false “missing coverage” without explicit control mapping (Athena prompt guidance).

---

## US-DG-06-011 — Vulnerable dependency enrichment (OSV/NVD)

**As a** AppSec lead, **I want** `vulnerable_deps` populated when lockfiles present, **so that** Athena correlates CVE with call paths.

**Acceptance criteria**

- **AC-DG-06-011-01:** Lockfile parsers for npm, pip, go mod, Maven documented; graceful skip if absent (Architecture §11.5–11.6).
- **AC-DG-06-011-02:** Advisory feed version pinned; air-gap mode uses bundled snapshot (EPIC-DG-13).
- **AC-DG-06-011-03:** Each vulnerable dep links to dependency graph node ids for evidence (Architecture §11.5).

---

## US-DG-06-012 — pgvector index maintenance

**As a** DBA, **I want** IVFFlat/ HNSW parameters tunable per deployment, **so that** recall meets SLO.

**Acceptance criteria**

- **AC-DG-06-012-01:** Index creation runs in migration or async job; documented for `lists` / M values (Architecture §12.1).
- **AC-DG-06-012-02:** Vacuum/reindex playbook linked from ops doc (Architecture §35.3).
- **AC-DG-06-012-03:** Embedding dimension mismatch fails fast at index time with `error_code`.
