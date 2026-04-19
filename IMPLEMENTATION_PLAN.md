# DeepGuard Compliance Engine — Detailed Implementation Plan

**Version:** 1.0  
**Date:** April 2026  
**Scope:** Execution order from **fully local** (laptop + Docker) through **multi-cloud** deploy and test.  
**Normative references:** `Architecture_Design.md` (§25–§35 implementation contracts), `.cursor/skills/deepguard-architecture/SKILL.md`, `.cursor/skills/deepguard-requirements-traceability/SKILL.md`, `.cursor/skills/deepguard-delivery-quality/SKILL.md`, `docs/user-stories/EPIC-*.md`.

---

## 1. How to use this document

- **Quality pipeline (mandatory for each Part/Phase):** follow `.cursor/skills/deepguard-delivery-quality/SKILL.md`: **user stories + ACs** → **design spec in `docs/design/` written and approved** → **implementation** → **unit tests ≥80% line coverage on touched packages** → **integration tests** (Docker-backed) → **Playwright BDD** → **manual human UAT last**. No phase is “done” until automated gates and UAT sign-off are met (or a documented waiver with follow-up ticket). For shareable machine output, run **`python3 scripts/generate_phase_html_reports.py`** to emit **self-contained HTML** under `reports/html/phase-*` (see `docs/dev-setup.md`).
- Each phase lists **deliverables**, **commands to run** (where applicable), and **exit criteria** so progress is objectively verifiable.
- **Local phases (L0–L14)** assume macOS or Linux, **Docker Desktop** (or Colima), **python3** / **pip3**, and **git**. No paid cloud accounts required until **Phase C1**.
- **Cloud phases (C1+)** assume separate AWS / Azure / other accounts for **non-production** integration environments first.
- Traceability: EPIC IDs in `docs/user-stories/` are cited as **DG-01**, **DG-02**, etc.

---

## 2. Global definitions

### 2.1 Repository target layout (Architecture §25)

```
apps/api/, apps/worker/
packages/core/, graph/, agents/, tools/, retrieval/, connectors/, parsers/, policies/, reporting/
infra/terraform/, infra/helm/
eval/datasets/, eval/fixtures/repos/
docker/compose.dev.yml
```

### 2.2 Scan graph order (immutable for v0)

`hermes` → `tiresias` → `argus` → (`laocoon` ∥ `cassandra`) → `convergence_gate` → `athena` → `circe` → `penelope`

### 2.3 Definition of Done (shared)

- **Stories + ACs** updated under `docs/user-stories/` with **`AC-DG-*`** traceability to this phase.
- **Design spec** for the slice exists under `docs/design/` with **`status: approved`** and approvers recorded (see delivery-quality skill).
- **Unit tests:** **≥80%** line coverage on **touched** packages for the PR/branch (`pytest-cov` with `--cov-fail-under=80` on agreed paths in CI).
- **Integration tests** green for in-scope ACs (Docker Compose stack).
- **Playwright BDD** suite green; scenarios reference **`US-DG-*` / `AC-DG-*`**.
- **Manual UAT** checklist signed off before marking the phase complete in this plan.
- Automated tests declare **`@pytest.mark.req("AC-DG-…")`** (or repo convention) per `00-numbering-and-traceability.md`.
- No secrets committed; `.env.example` documents variables only.
- `Architecture_Design.md` or `reference.md` updated when contracts change.

### 2.4 Phase ↔ EPIC traceability

Each **implementation phase** below maps to **`EPIC-DG-*`** backlog files under `docs/user-stories/`. **Primary** = epic whose stories are the main deliverable for that phase; **Secondary** = epics touched for integration, auth, or shared infrastructure.

| Phase | Primary EPICs | Secondary / enabling EPICs |
|-------|----------------|---------------------------|
| **L0** | — (foundation) | **DG-01**, **DG-02** (repo layout supports worker/API packages) |
| **L1** | **DG-02**, **DG-01** | **DG-13** (DB encryption, secrets placeholders per AC catalogue) |
| **L2** | **DG-01**, **DG-02** | **DG-03**–**DG-10** (shared `core` models consumed later) |
| **L3** | **DG-02** | **DG-03** (tenant/auth middleware) |
| **L4** | **DG-01** | **DG-02** (enqueue from API, status in DB) |
| **L5** | **DG-01** | **DG-02** |
| **L6** | **DG-04** | **DG-01**, **DG-02** |
| **L7** | **DG-05** | **DG-04**, **DG-02** |
| **L8** | **DG-06** | **DG-04**, **DG-01** |
| **L9** | **DG-07** | **DG-06**, **DG-04** |
| **L10** | **DG-08** | **DG-05**, **DG-06**, **DG-07** |
| **L11** | **DG-09**, **DG-10** | **DG-08** |
| **L12** | **DG-01**–**DG-10** (full golden path) | **DG-11** (webhooks, trace hooks), **DG-12** (Playwright only if console exists) |
| **L13** | **DG-11** | **DG-01** |
| **L14** | **DG-03**, **DG-13** | **DG-02**, **DG-11** |
| **C0** | **DG-13** | **DG-01**, **DG-02** |
| **C1** | **DG-07**, **DG-13** | **DG-01**, **DG-02**, **DG-11** |
| **C2** | **DG-07**, **DG-13** | **DG-01**, **DG-02**, **DG-11** |
| **C3** | **DG-07**, **DG-13** | **DG-01**, **DG-02**, **DG-11** |
| **C4** | **DG-07**, **DG-13** | **DG-01**, **DG-02**, **DG-11** |
| **C5** | **DG-11**, **DG-13**, **DG-02** | **DG-03**, **DG-12** |

#### EPIC-DG-12 (console) — where it **starts** and how stories **split** across phases

**EPIC-DG-12 is intentionally split across many phases** (unlike DG-04…DG-08, which each own one main L-phase). The UI depends on API and graph behaviour that land at different times.

| Milestone | Phase | What starts here |
|-----------|--------|-------------------|
| **Optional scaffold** | **L0–L2** | Next.js app shell, lint, CI, **mocked** API only — does **not** count as EPIC-DG-12 delivery for traceability until wired to real `/v1`. |
| **Integrated EPIC-DG-12 starts** | **L3** | **First stories tied to real APIs:** e.g. **US-DG-12-001** (login shell + tenant context against auth stub), **US-DG-12-002** (scan list) once **`GET /v1/scans`** and **`POST /v1/scans`** response shapes are stable (EPIC-DG-02). Treat **start of L3** as the epic’s **integration kickoff**; first merged vertical slice often closes at **L3 exit** or early **L4**. |
| **Live progress in UI** | **L4–L5** | **US-DG-12-003** (scan detail / stage timeline, cancel) when queue + graph expose accurate `current_stage` / `percent_complete` (EPIC-DG-01). |
| **Findings & evidence** | **L10–L12** | **US-DG-12-004** (findings triage), **US-DG-12-009** (cross-layer view) after Athena + data APIs exist (EPIC-DG-08). |
| **Reports & policies** | **L11–L12** | **US-DG-12-005** (PDF download), **US-DG-12-006** (policy upload UI) (EPIC-DG-10, EPIC-DG-05). |
| **BDD / regression** | **L12+** | Playwright suite owns cross-flow ACs for **US-DG-12-002**–**005** (minimum); expand as features land. |
| **Admin / auditor depth** | **L13–L14** | **US-DG-12-007** (runtime flags read-only), **US-DG-12-012** (reasoning excerpt) with EPIC-DG-11/DG-03; **US-DG-12-008** (webhook/budget forms) with stable **DG-02** notifications. |
| **SaaS / tenant ops** | **L14** | **US-DG-12-011** (API keys, optional), **US-DG-12-014** (retention / classification defaults). |
| **Production polish** | **C5** | **US-DG-12-010** (a11y / i18n baseline), **US-DG-12-013** (mobile scan view), SSO / hardening with EPIC-DG-13. |

**Summary:** EPIC-DG-12 **integration work starts at L3**; earlier phases may hold **scaffold-only** UI work. **No single L-phase owns the whole epic** — plan design specs **per slice** (e.g. `phase-L3-console-scan-list.md`) with explicit **US-DG-12-*** in scope.

#### Reverse index — EPIC → first phase as primary driver

| EPIC ID | File | First phase (primary) | Notes |
|---------|------|------------------------|--------|
| EPIC-DG-01 | `EPIC-01-scan-job-orchestration.md` | **L1** (persistence), **L4** (queue worker) | Deep implementation **L4–L5**, **L12** |
| EPIC-DG-02 | `EPIC-02-control-plane-api.md` | **L1**, **L3** | Webhooks **L12**; SLOs **C5** |
| EPIC-DG-03 | `EPIC-03-identity-tenancy-rbac.md` | **L3** (stub), **L14** (full) | Ongoing hardening **C5** |
| EPIC-DG-04 | `EPIC-04-ingestion-hermes.md` | **L6** | |
| EPIC-DG-05 | `EPIC-05-policy-tiresias.md` | **L7** | |
| EPIC-DG-06 | `EPIC-06-code-indexing-argus.md` | **L8** | |
| EPIC-DG-07 | `EPIC-07-iac-cloud-analyzers.md` | **L9** (fixtures), **C1**–**C4** (live connectors) | |
| EPIC-DG-08 | `EPIC-08-compliance-athena.md` | **L10** | |
| EPIC-DG-09 | `EPIC-09-remediation-circe.md` | **L11** | |
| EPIC-DG-10 | `EPIC-10-reporting-penelope.md` | **L11** | |
| EPIC-DG-11 | `EPIC-11-observability-cost-governance.md` | **L13** | Budgets/alerts **C5** |
| EPIC-DG-12 | `EPIC-12-console-ui.md` | **L3** (first integrated slice vs real `/v1`); stories continue **L4→C5** | Optional **L0–L2** scaffold only; see **§2.4 EPIC-DG-12** table above |
| EPIC-DG-13 | `EPIC-13-security-deployment-modes.md` | **L1** (light), **L14**, **C0**–**C5** | Air-gap / SaaS / secrets |

Use this section when writing **`docs/design/phase-*.md`** headers: link **phase id** (e.g. `L8`) to **EPIC-DG-06** and the specific **`US-DG-*` / `AC-DG-*`** in scope.

---

# Part A — Local laptop phases (executable & testable)

These phases must complete **before** any mandatory cloud spend. All verification steps run on the developer machine.

---

## Phase L0 — Monorepo scaffold & quality gates

**Goal:** Empty runnable workspace with linting, typing, and test runner wired; no business logic yet.

| Item | Detail |
|------|--------|
| Deliverables | Root `pyproject.toml` (workspace), `packages/core` as installable package, `apps/api` and `apps/worker` as apps with `pyproject` or src layout; `ruff`, `mypy` (strict on `core` + `graph` when added), `pytest`; optional `pre-commit` |
| EPIC | Cross-cutting (DG-13 security posture prep indirectly) |

**Execute & test**

```bash
cd /path/to/deep-code
python3 -m venv .venv && source .venv/bin/activate
pip3 install -e ".[dev]"   # or per-package installs once pyproject exists
ruff check .
mypy packages/core packages/graph  # graph when present
pytest -q
```

**Exit criteria**

- [x] `ruff check .` exits 0  
- [x] `pytest -q` runs with coverage gate (smoke test added)  
- [x] README + `docs/dev-setup.md` document venv activation and commands  
- [x] Approved design note: `docs/design/phase-L0-monorepo-scaffold.md`  

---

## Phase L1 — Local data plane (Docker Compose)

**Goal:** Postgres **with pgvector**, Redis, MinIO up; migrations apply cleanly (Architecture §34, §29).

| Item | Detail |
|------|--------|
| Deliverables | `docker/compose.dev.yml`; `alembic.ini` + `alembic/versions/001_initial.py` creating extensions and core tables (`tenants`, `scans`, `findings`, … §29); seed script `scripts/seed_dev_tenant.py` |
| EPIC | DG-02 (persistence backing API), DG-01 (worker will use same DB) |

**Execute & test**

```bash
docker compose -f docker/compose.dev.yml up -d
# wait for healthy
python3 -m alembic upgrade head
python3 scripts/seed_dev_tenant.py
docker compose -f docker/compose.dev.yml exec postgres psql -U deepguard -d deepguard -c "SELECT count(*) FROM tenants;"
```

**Exit criteria**

- [x] `CREATE EXTENSION vector` succeeds  
- [x] All tables from Architecture §29.1 + §29.3 + §29.4 exist (`tenants`, `scans`, `findings`, `reasoning_traces`, `artifacts`, `webhook_deliveries`, `code_chunks`, `policy_chunks`)  
- [x] MinIO health endpoint reachable; bucket `deepguard-dev` created via `minio-init`  
- [x] Redis `PING` returns `PONG`  
- [x] Design spec: `docs/design/phase-L1-data-plane.md`  

---

## Phase L2 — Core domain models (`packages/core`)

**Goal:** Pydantic v2 models mirror architecture: `ScanJobConfig`, partial `ScanState`, `PolicyControl`, `Finding`, `AgentError`, enums for status/stage/severity (Architecture §4.2, §16.2).

| Item | Detail |
|------|--------|
| Deliverables | `packages/core/deepguard_core/models/*.py`; JSON Schema export optional; unit tests for validation edge cases |
| EPIC | All EPICs depend on this |

**Execute & test**

```bash
pytest packages/core/tests -q --cov=packages/core --cov-report=term-missing
```

**Exit criteria**

- [x] `CreateScanRequest`-compatible validation matches Architecture §28.4 rules (reject invalid layer combinations)  
- [x] `mypy -p deepguard_core` strict passes  

---

## Phase L3 — Control plane API skeleton (`apps/api`)

**Goal:** FastAPI app with `/v1/healthz`, auth stub (dev API key or JWT mock), `POST /v1/scans` persisting row `QUEUED`, `GET /v1/scans/{id}` (Architecture §28).

| Item | Detail |
|------|--------|
| Deliverables | `apps/api` lifespan: DB pool; OpenAPI at `/v1/openapi.json`; tenant middleware reading fixed dev tenant |
| EPIC | DG-02 (US-DG-02-001–003), DG-03 identity stub |

**Execute & test**

```bash
export DATABASE_URL=postgresql+asyncpg://deepguard:deepguard@127.0.0.1:5432/deepguard
export DEEPGUARD_DEV_TENANT_ID=<uuid from seed_dev_tenant>
pip3 install -e ".[dev]"
uvicorn deepguard_api.main:app --reload --port 8000
curl -s localhost:8000/v1/healthz | jq .
curl -s -X POST localhost:8000/v1/scans -H "Content-Type: application/json" -H "X-API-Key: dev" -d @eval/fixtures/api/create_scan_min.json | jq .
curl -s localhost:8000/v1/scans/<scan_id> -H "X-API-Key: dev" | jq .
```

**Exit criteria**

- [x] OpenAPI documents `CreateScanRequest` and `Scan` response  
- [x] Idempotency behaviour covered by test (DG-02 US-DG-02-002)  
- [x] Structured JSON logs with `scan_id` in request path  

---

## Phase L4 — Job queue + worker skeleton (`apps/worker`)

**Goal:** Worker consumes `stream:scans` (Redis Streams), claims job, transitions `QUEUED` → `INGESTING`, heartbeat key set; **no LangGraph** yet (Architecture §30).

| Item | Detail |
|------|--------|
| Deliverables | Producer: API enqueues message after `POST /v1/scans`; consumer group `workers`; visibility timeout + `XCLAIM` documented |
| EPIC | DG-01 (orchestration transport), DG-02 |

**Execute & test**

```bash
# Automated gate (no Docker):
pytest tests/test_l4_api.py tests/test_l4_worker_unit.py tests/test_l4_worker_settings.py packages/core/tests/test_queue_scan_message.py -q

# Manual stack: terminal 1 — compose + API; terminal 2 — worker:
python3 -m deepguard_worker
# (equivalent shim from repo root: ``python3 -m apps.worker.main``)

# terminal 3: POST scan, observe DB status + Redis consumer group pending
redis-cli XINFO GROUPS stream:scans
```

**Exit criteria**

- [x] End-to-end: POST scan → worker sets status within N seconds (manual with compose; unit tests cover claim + stub loop with FakeRedis / memory repo)  
- [x] Heartbeat key `scan:{id}:heartbeat` TTL refreshed during processing (TTL asserted in tests)  
- [x] `POST /v1/scans/{id}/cancel` sets flag; worker respects cooperative cancel between stages (DG-01 US-DG-01-003)  

---

## Phase L5 — LangGraph runtime shell (`packages/graph`)

**Goal:** Compiled graph with **stub nodes** (pass-through state updates), `MemorySaver` in tests, **Postgres checkpointer** in dev compose (Architecture §31, §4.6).

| Item | Detail |
|------|--------|
| Deliverables | `build_odysseus_graph()`; `thread_id=str(scan_id)`; conditional edges for skipped layers; tests: invoke + resume |
| EPIC | DG-01 (US-DG-01-001–002) |

**Execute & test**

```bash
pytest packages/graph/tests -q
# Focus checkpoint / resume behaviour:
pytest packages/graph/tests -q -k "checkpoint"
# optional: run worker with GRAPH_USE_STUBS=true against one scan
```

**Exit criteria**

- [x] Graph order matches §2.2; convergence does not block when branch skipped (DG-01 AC-DG-01-001-02/03) — covered by ``test_odysseus_graph_l5.py``  
- [x] Resume test: interrupt mid-graph, resume with same ``thread_id``; stub findings list has no duplicates (MemorySaver; Postgres via ``postgres_checkpointer()`` in dev)  

---

## Phase L6 — Hermes (ingestion) local

**Goal:** Clone public fixture repo **or** extract tarball into `TOOL_SANDBOX_ROOT`; upload archive ref to MinIO; populate `repo_metadata`, `repo_local_path` in state (Architecture §11, EPIC DG-04).

| Item | Detail |
|------|--------|
| Deliverables | `HermesAgent` / node; `safe_read` boundary; size limits `REPO_MAX_BYTES` |
| EPIC | DG-04 |

**Execute & test**

```bash
pytest packages/agents/tests -q -k hermes
# manual: scan job pointing to tiny public repo under eval/fixtures/repos/
```

**Exit criteria**

- [x] Path traversal attempts rejected by sandbox tests (``packages/agents/tests/test_hermes_sandbox.py``)  
- [x] Artifact ``ArtifactRef`` returned from Hermes staging (no raw archive bytes in result object)  

---

## Phase L7 — Tiresias (policy parse) local

**Goal:** Fixture policies (YAML/JSON) → `policy_controls[]`; optional single **FakeLLM** call for PDF slice later (Architecture §16; EPIC DG-05).

| Item | Detail |
|------|--------|
| Deliverables | Parser registry; version string `policy_version`; cache key in Redis (Architecture §9) |
| EPIC | DG-05 |

**Execute & test**

```bash
pytest packages/policies/tests packages/agents/tests -q -k tiresias
```

**Exit criteria**

- [x] At least two frameworks represented in fixtures (``packages/policies/tests/fixtures/``)  
- [x] Invalid policy file raises ``AgentRuntimeError`` wrapping structured ``AgentError`` (no bare crash)  

---

## Phase L8 — Argus (code indexing) local

**Goal:** tree-sitter parse fixture repo languages; chunk; embed with **local fake embeddings** or small deterministic model; upsert `code_chunks` (Architecture §11–12; EPIC DG-06).

| Item | Detail |
|------|--------|
| Deliverables | `ASTAwareChunker` contract; pgvector dimensions consistent with embedding stub |
| EPIC | DG-06 |

**Execute & test**

```bash
pytest packages/parsers/tests packages/agents/tests -q -k argus
# SQL: SELECT count(*) FROM code_chunks WHERE scan_id = '...';
```

**Exit criteria**

- [x] Minimum **vector-only** path: ``StubASTAwareChunker`` (``packages/parsers``); BM25 / hybrid deferred  
- [x] ``dependency_graph`` depth observation + ``truncated`` flag (``cap_dependency_graph_depth``)  

---

## Phase L9 — Laocoon & Cassandra (analysis) with fixtures

**Goal:** **Laocoon:** parse Terraform/K8s fixtures → `iac_findings`. **Cassandra:** load **frozen** `ResourceSnapshot` JSON from `eval/fixtures/cloud/` (no live API yet) (Architecture §15; EPIC DG-07).

| Item | Detail |
|------|--------|
| Deliverables | `IaC_PARSERS` registry; `CloudConnector` interface + `FixtureConnector` |
| EPIC | DG-07 |

**Execute & test**

```bash
pytest packages/parsers/tests packages/connectors/tests -q -k "laocoon|cassandra|fixture"
```

**Exit criteria**

- [x] Cassandra fixture path loads snapshot by **ref id** (JSON file), not inlined megabyte payloads (``FixtureConnector``)  
- [x] IaC path uses ``IaC_PARSERS`` registry + small ``.tf`` fixture (``eval/fixtures/iac/``)  

---

## Phase L10 — Athena (compliance mapping) with FakeLLM

**Goal:** Batched controls (8–12); **structured output** Pydantic; generator + critic passes; persist `findings`; confidence & `UNCERTAIN` path (Architecture §3, §31.3; EPIC DG-08).

| Item | Detail |
|------|--------|
| Deliverables | `ComplianceFindingList` schema; LangChain `with_structured_output`; traces written to `reasoning_traces` with redaction for export |
| EPIC | DG-08 |

**Execute & test**

```bash
export LLM_MODE=fake
pytest packages/agents/tests -q -k athena
pytest eval/harness/tests -q -k cross_layer_gold  # when dataset exists
```

**Exit criteria**

- [x] Gold JSONL + eval harness (``eval/harness/fixtures/athena_gold_sample.jsonl``, ``eval/harness/tests/test_cross_layer_gold.py``)  
- [x] Trace export hook redacts obvious secret prefixes (``trace_excerpt_for_export`` in ``packages/agents``)  

---

## Phase L11 — Circe & Penelope

**Goal:** **Circe:** remediation records with optional `terraform validate` / `tflint` subprocess in sandbox (best-effort, Architecture §23.1 Q10). **Penelope:** Jinja → PDF bytes → MinIO `reports/report.pdf` (Architecture §18; EPIC DG-09, DG-10).

| Item | Detail |
|------|--------|
| Deliverables | `Remediation` model; `report_artifact_id` on scan complete |
| EPIC | DG-09, DG-10 |

**Execute & test**

```bash
pytest packages/reporting/tests -q
# manual: GET presigned or proxy GET artifact → open PDF locally
```

**Exit criteria**

- [x] PDF contains cover + finding section (``build_scan_pdf_bytes`` + ``packages/reporting/tests``)  
- [x] Circe stub returns **diff-only** ``Remediation`` (no apply / no filesystem writes)  

---

## Phase L12 — End-to-end golden scan (local)

**Goal:** Single command runs migrate → seed → enqueue → worker full graph → `COMPLETE` with PDF (EPICs DG-01–DG-10 integrated). Use ``make e2e-full`` (``scripts/e2e_full_scan.sh``) for API + worker + poll; ``make e2e-local`` remains HTTP-only smoke when you start processes yourself.

**Execute & test**

```bash
docker compose -f docker/compose.dev.yml up -d
python3 -m alembic upgrade head && python3 scripts/seed_dev_tenant.py
export LLM_MODE=fake
pytest tests/test_l12_worker_graph_memory.py -q
# optional: full stack (compose + API + worker + poll for COMPLETE)
make e2e-full
# or HTTP-only smoke (start API yourself): ``make e2e-local``
```

**Exit criteria**

- [x] P95 wall-time smoke on ``POST /v1/scans`` when ``DEEPGUARD_E2E_LOCAL=1`` and API is up (``tests/e2e/test_full_scan_local.py``)  
- [x] Worker runs stub Odysseus graph → ``build_scan_pdf_bytes`` → ``artifacts`` row + scan ``COMPLETE`` (``deepguard_worker/job_executor.py``; unit: ``tests/test_l12_worker_graph_memory.py``)  
- [x] Full-stack poll when ``DEEPGUARD_E2E_FULL=1`` + ``make e2e-full`` / ``scripts/e2e_full_scan.sh`` (``tests/e2e/test_full_scan_local.py``)  
- [x] API accepts ``notifications.webhook_url`` on create (``apps/api/tests/test_scan_notifications_accepted.py``); delivery to sink remains worker-owned  

---

## Phase L13 — Observability & cost hooks (local)

**Goal:** OpenTelemetry traces to console or OTLP collector container; token/cost fields in DB or LangFuse **dev** container optional (Architecture §7–8, §35; EPIC DG-11).

**Execute & test**

```bash
docker compose -f docker/compose.dev.yml --profile observability up -d
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 pytest tests/e2e -q
```

**Exit criteria**

- [x] Graph node span helper attaches ``scan_id`` and ``tenant_id`` (``packages/observability/tests``)  
- [x] EPIC-DG-11: LangSmith + LangFuse + OTEL wired (see ``docs/dev-setup.md``, ``documentation/langstack-usage-and-roadmap.md``); LangSmith tracing defaults **on** outside CI when ``LANGCHAIN_TRACING_V2`` is unset; CI/pytest force off  

---

## Phase L14 — Security, RBAC, and deployment modes (local behaviour)

**Goal:** API key vs JWT paths; tenant isolation integration tests; `runtime_config` merge (Architecture §24); EPIC DG-03, DG-13 narrative for `PRIVATE` / `SAAS` flags without real cloud.

**Execute & test**

```bash
pytest apps/api/tests -q -k "tenant|auth|runtime_config"
```

**Exit criteria**

- [x] Cross-tenant scan ``GET`` returns 404 (``apps/api/tests/test_l14_tenant_and_auditor.py``)  
- [x] ``redact_for_auditor`` strips secret-classified keys from nested JSON (same test module)  

---

# Part B — Cloud phases (deploy & test)

Prerequisites for all cloud phases: **container images** for `api` and `worker` published to a registry; secrets via cloud secret manager; **TLS** for public endpoints; **non-prod** environment naming.

---

## Phase C0 — Container build & generic Helm/K8s manifest

**Goal:** Production-like images (non-root, healthchecks), Helm chart or Kustomize with values for image tag, DB URL, Redis URL, S3 endpoint (Architecture §25 `infra/helm`).

**Execute & test**

```bash
docker build -f apps/api/Dockerfile -t deepguard-api:0.1.0 .
docker build -f apps/worker/Dockerfile -t deepguard-worker:0.1.0 .
# local k8s: kind or minikube
kind create cluster && kubectl apply -k infra/k8s/local/
kubectl rollout status deployment/deepguard-api
```

**Exit criteria**

- [ ] Image scan (Trivy or equivalent) in CI with acceptable baseline  
- [ ] Readiness probes hit `/v1/healthz`  

---

## Phase C1 — AWS (reference cloud)

**Goal:** Deploy to **AWS** dev account: EKS **or** ECS Fargate; **Amazon RDS for PostgreSQL** with pgvector; **ElastiCache Redis**; **S3**; **Secrets Manager**; private subnets; worker → RDS/Redis/S3 via IAM roles; optional **Bedrock** in VPC for LLM (Architecture §22, business docs).

| Workstream | Tasks |
|------------|--------|
| Network | VPC, private subnets, NAT for image pull only if needed |
| Data | RDS parameter group + `pgvector`; rotation secrets |
| Compute | EKS + IRSA or ECS task roles |
| LLM | Start with `LLM_MODE=fake` in AWS dev, then Bedrock endpoint |
| Observability | CloudWatch + OTLP exporter optional |

**Execute & test**

```bash
# After terraform apply in infra/terraform/aws/dev
export API_URL=https://api.dev.deepguard.example
curl -s "$API_URL/v1/healthz"
curl -s -X POST "$API_URL/v1/scans" -H "Authorization: Bearer $TOKEN" -d @eval/fixtures/api/create_scan_min.json
# Poll until COMPLETE; download PDF artifact presigned URL
```

**Exit criteria**

- [ ] At least one full scan **COMPLETE** in AWS dev with real RDS checkpoint resume tested once  
- [ ] S3 bucket policies deny public read; encryption at rest enabled  
- [ ] Runbook: rotate DB password via Secrets Manager without code deploy  

---

## Phase C2 — Azure (second cloud)

**Goal:** **AKS**; **Azure Database for PostgreSQL** (flexible server with pgvector extension support per region); **Azure Cache for Redis**; **Blob Storage**; **Key Vault**; **Managed Identity** for pods; optional **Azure OpenAI** private endpoint (Architecture multi-cloud direction).

**Execute & test**

Same pattern as C1: `infra/terraform/azure/dev` (or Bicep), health check, POST scan, PDF retrieval.

**Exit criteria**

- [ ] Parity checklist with AWS: auth, enqueue, worker, storage, DB, cancel, webhook  
- [ ] Documented differences (e.g. Redis TLS port, Blob SAS vs S3 presign) in `docs/cloud/azure.md`  

---

## Phase C3 — GCP (optional third hyperscaler)

**Goal:** **GKE**; **Cloud SQL Postgres** + pgvector; **Memorystore Redis**; **GCS**; **Secret Manager**; optional **Vertex AI** (Architecture §14 roadmap).

**Exit criteria**

- [ ] One greenfield deploy doc + automated smoke test script in `scripts/smoke_gcp.sh`  

---

## Phase C4 — Regional clouds (Alibaba, Tencent, Huawei)

**Goal:** Repeat **C1 pattern** with vendor-managed K8s (ACK, TKE, CCE), PolarDB/TDSQL-C/GaussDB, OSS/COS/OBS, KMS equivalents, and **VPC-private LLM** endpoints (百炼 / 混元 / 盘古) per business plan; **国密** requirements tracked for Huawei track (Architecture §22.2).

**Exit criteria**

- [ ] At least **one** regional cloud reaches `COMPLETE` scan in dev with connector **read-only** IAM policy attached  
- [ ] Data-plane Terraform modules live under `infra/terraform/{aliyun,tencent,huawei}/` per Architecture §25  

---

## Phase C5 — Staging, production, and compliance hardening

**Goal:** Multi-AZ, backups, DR drill, rate limits, cost budgets (`max_llm_usd`), SOC 2 prep, pen-test remediation, customer-facing SLAs (Architecture §35; EPIC DG-13).

**Exit criteria**

- [ ] RTO/RPO documented; restore test from RDS snapshot  
- [ ] SOC 2 Type II audit window **planned** (SaaS track)  

---

## 3. Milestone summary (Gantt-style ordering)

| Phase | Environment | Primary outcome |
|-------|-------------|-----------------|
| L0–L2 | Laptop | Code + DB schema + models |
| L3–L4 | Laptop + Docker | API + queue + worker loop |
| L5 | Laptop + Docker | Real LangGraph + checkpoints |
| L6–L9 | Laptop + Docker | Real ingestion + indexing + fixture analysis |
| L10–L12 | Laptop + Docker | Mapping + report + full E2E |
| L13–L14 | Laptop + Docker | Observability + security polish |
| C0 | kind/minikube | K8s images |
| C1 | AWS dev | First real multi-service cloud |
| C2 | Azure dev | Second hyperscaler parity |
| C3 | GCP dev | Optional |
| C4 | Ali / Tencent / Huawei dev | Regional + sovereignty |
| C5 | Staging/prod | Hardening |

---

## 4. Risk register (implementation-focused)

| Risk | Mitigation |
|------|------------|
| LLM non-determinism breaks tests | `LLM_MODE=fake` in CI; temperature 0; golden thresholds documented |
| pgvector extension missing on managed DB | Verify extension allow-list **before** phase C1/C2 |
| Checkpoint DB migration drift | Pin `langgraph-checkpoint-postgres` version; dedicated migration job in Helm |
| Cloud cost overrun | Enforce `budget.max_llm_usd` early (L12 stub, C1 real metering) |

---

## 5. Document maintenance

Update this plan when:

- EPIC acceptance criteria change in `docs/user-stories/`.  
- Architecture §23.1 MVP decisions are superseded by ADR.  
- A cloud phase is reordered (e.g. customer mandates Azure before AWS).

---

*Owner: Engineering Lead. Review cadence: end of each L-phase and before each C-phase go-live.*
