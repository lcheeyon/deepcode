# DeepGuard architecture — reference tables

Companion to [SKILL.md](SKILL.md). Source: `Architecture_Design.md` (v0.2).

## Repository layout (normative)

```
apps/api          — FastAPI control plane
apps/worker     — LangGraph runner (same image, different CMD)
packages/core   — Pydantic models, ScanState (no langgraph import)
packages/graph  — StateGraph build, compile, checkpoint
packages/agents — Node factories Hermes…Penelope
packages/tools  — @tool implementations, RepoSandbox only
packages/retrieval, connectors, parsers, policies, reporting
```

**Import rule:** `graph` imports `agents`; `agents` must not import `apps.api`; `core` must not import cloud SDKs or `langgraph`.

## Scan lifecycle (API + DB)

`PENDING` → `QUEUED` → `INGESTING` → `INDEXING` → `ANALYZING` → `MAPPING` → `REMEDIATING` → `REPORTING` → `COMPLETE`  
Terminals: `FAILED`, `CANCELLED`; optional `AWAITING_REVIEW` (HITL before Athena).

## HTTP API (v1 prefix)

| Method | Path |
|--------|------|
| POST | `/v1/scans` |
| GET | `/v1/scans/{scan_id}` |
| GET | `/v1/scans/{scan_id}/findings` |
| GET | `/v1/scans/{scan_id}/artifacts/{artifact_id}` |
| POST | `/v1/scans/{scan_id}/cancel` |
| POST | `/v1/scans/{scan_id}/resume` |
| GET | `/v1/policies` |
| POST | `/v1/policies:upload` |

Idempotency: optional `Idempotency-Key` on create (24h dedupe per tenant).

## Core environment variables

| Variable | Role |
|----------|------|
| `DATABASE_URL` | Postgres async |
| `REDIS_URL` | Streams, cache, heartbeat |
| `OBJECT_STORE_URL` | Artifacts |
| `LANGGRAPH_CHECKPOINT` | `postgres` (prod) / `memory` (tests) |
| `TOOL_SANDBOX_ROOT` | Writable clone root |
| `LANGCHAIN_TRACING_V2`, `LANGSMITH_*` | Optional SaaS trace |
| `LANGFUSE_*` | Self-hosted observability |
| `JWT_ISSUER`, `JWT_AUDIENCE` | API auth (multi-tenant) |
| `MAX_CONCURRENT_SCANS_PER_TENANT` | Backpressure |

Secrets: resolve via Calypso (`CALYPSO_BACKEND`); do not log or checkpoint secret values.

## Relational tables (names)

`tenants`, `scans` (includes `cancellation_requested`, `job_config`, `idempotency_key`), `findings`, `reasoning_traces`, `artifacts`, `webhook_deliveries`.  
Vectors: `code_chunks` (tenant-scoped), `policy_chunks` (catalog + version).

## Queue message (`ScanJobMessage`)

```json
{ "schema_ver": "1.0", "scan_id": "uuid", "tenant_id": "uuid", "enqueued_at": "ISO8601", "priority": 0 }
```

Redis Stream default: `stream:scans`, consumer group `workers`. Heartbeat key `scan:{scan_id}:heartbeat`, TTL ~120s, refresh ~30s.

## `tenants.runtime_config` keys (v0)

`semantic_cache_enabled`, `semantic_cache_threshold` (0.95–0.99), `athena_per_control_send`, `delta_skip_analysis`, `graph_interrupt_before_athena`, `circe_terraform_validation`, `max_concurrent_scans`, `retention_repo_archive_hours`.

## Compliance frameworks (examples)

ISO 27001:2022, SOC 2, MAS TRM, GB/T 22239 (等保), MLPS, CSL, DSL, PIPL, GenAI measures, GDPR, HIPAA, PCI-DSS 4.0, NIST CSF, CIS — extensible registry in architecture doc §16.

## Cross-layer finding (Athena)

Correlate **IaC promise vs code behaviour vs live cloud** (e.g. bucket encrypted in config but app bypasses; IAM tight but code assumes broader role). Treat as **first-class** `CrossLayerFinding` with mapped control IDs.

## Reporting (Penelope)

Structured findings → Jinja → Markdown → ReportLab PDF; CJK fonts for Chinese reports; evidence as file:line or resource identifiers.

## CI / quality gates

`ruff`, `mypy` (strict on `core`, `graph`), `pytest`, coverage on parsers/tools; LangSmith / gold datasets for regression on prompt or mapper changes; maintain `false-positive-registry` discipline.

## Delivery & test layers (normative)

Follow `.cursor/skills/deepguard-delivery-quality/SKILL.md` for ordering. Summary:

| Layer | Tooling | Coverage / criterion |
|-------|---------|----------------------|
| User stories + ACs | `docs/user-stories/EPIC-*.md` | INVEST; each AC testable; `AC-DG-*` IDs |
| Design spec | `docs/design/*.md` | **Approved** before coding (frontmatter) |
| Unit | `pytest`, `pytest-cov` | **≥80%** line coverage on **touched** packages per change |
| Integration | `pytest` + Docker Compose | Real DB/Redis/MinIO/API/worker; `@pytest.mark.integration` |
| BDD | **Playwright** (`e2e/playwright/` or `tests/e2e_bdd/`) | Scenarios linked to `US-DG-*` / `AC-DG-*`; green in CI before UAT |
| Manual UAT | Checklist / sign-off | Last gate before phase “done” or release |

## Local dev services (compose)

Postgres **pgvector**, Redis, MinIO, `api`, `worker` (`LLM_MODE=fake` for deterministic tests), optional Ollama.
