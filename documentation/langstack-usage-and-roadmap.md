# LangChain, LangGraph, LangSmith & LangFuse — Current Usage and Roadmap

This document describes how **LangGraph** and related **LangChain** primitives appear in the **implemented** DeepGuard codebase today, how **LangSmith** and **LangFuse** are wired for **EPIC-DG-11**, and concrete directions to deepen usage for **agent performance** and **observability**.

The authoritative product stack narrative also lives in `Architecture_Design.md` (§4 LangGraph, §6 LangChain, §7–8 observability) and `documentation/agentic-orchestration.md`. This file ties those ideas to **what is actually imported and run** in the monorepo.

---

## 1. Summary

| Library | Declared / transitive | Used in runtime code today | Notes |
|--------|------------------------|----------------------------|--------|
| **LangGraph** | Yes (`langgraph`, `langgraph-checkpoint-postgres` in root `pyproject.toml`) | **Yes** — Odysseus shell graph, checkpoints in tests/worker | Core orchestration primitive |
| **LangChain (`langchain` / `langchain_core`)** | Yes (`langchain` for LangFuse callback integration; `langchain_core` via LangGraph) | **`RunnableConfig`** typing on worker `invoke`; graph tests | No LCEL chat pipelines in `packages/agents` yet |
| **LangSmith** | Optional extras **`tracing-langsmith`** / **`tracing`** (not in minimal `pip install .`) | **Env-based tracing** — `LANGCHAIN_TRACING_V2` defaults per `configure_langsmith_env_defaults`; set `LANGSMITH_API_KEY` (or `LANGCHAIN_API_KEY`) to export runs. Worker `invoke`/`stream` passes **`graph_invoke_config`** metadata: `scan_id`, `tenant_id`, `idempotency_key`, `deepguard.graph_version`, `deepguard.correlation_id`, `deepguard.run_name`. | **`[dev]`** and **`[tracing]`** include `langsmith` for CI/local; air-gap: omit extras + `DEEPGUARD_AIR_GAP=1` |
| **LangFuse** | Optional extras **`tracing-langfuse`** / **`tracing`** | **`CallbackHandler`** when `LANGFUSE_HOST` + keys are set; worker passes it in **`invoke` callbacks** (dual-sink with LangSmith auto-trace). | Same optional layout as LangSmith; see `docker/langfuse/README.md` |

**OpenTelemetry (EPIC-DG-11-005):** `configure_observability_at_startup` installs a console `TracerProvider` by default; **FastAPI** is instrumented when the SDK provider is active. **Stub graph nodes** wrap `graph_node_span` (OTEL) with `scan_id` / `tenant_id` and **`deepguard.correlation_id`** when the worker sets `graph_correlation_context`. **Redaction** (`excerpt_for_trace_sink`, `redact_secrets`, `sanitize_trace_metadata_value`) caps long metadata strings before sinks (EPIC-DG-11-001 / §8.2).

---

## 2. LangGraph — how it is used

### 2.1 Graph topology (`packages/graph`)

- **`deepguard_graph.graph.build_odysseus_graph`** constructs a **`StateGraph`** over **`OdysseusState`** (`deepguard_graph.state`), with nodes: Hermes → Tiresias → Argus → parallel Laocoon / Cassandra (or explicit **skip** nodes) → convergence gate → Athena → Circe → Penelope → `END`.
- **Parallel fan-out** uses **`langgraph.types.Send`** in `fan_out_after_argus`, with routing rules driven by `job_config.scan_layers` and presence of `cloud_snapshots`, matching the architecture intent (skip branches must still converge).
- **Stub nodes** (`deepguard_graph.stub_nodes`) return small partial-state dicts (e.g. `execution_log`, `stub_findings`) and wrap each step in **`graph_node_span`** (OpenTelemetry) for node-level spans.

### 2.2 State model

- **`OdysseusState`** is a **`TypedDict`** with reducers (`Annotated[..., operator.add]`) for lists that must merge across steps and parallel branches — the standard LangGraph pattern for append-only logs and collected outputs.

### 2.3 Checkpointing

- **In-process tests** (`packages/graph/tests/test_odysseus_graph_l5.py`): graphs compile with **`langgraph.checkpoint.memory.MemorySaver`**. Tests assert ordering, skip behaviour, and **resume after `interrupt_after`** without duplicating stub findings (checkpoint semantics).
- **Postgres checkpointer helper** (`deepguard_graph.checkpoint_pg.postgres_checkpointer`): wraps **`langgraph.checkpoint.postgres.PostgresSaver`** with `setup()` for production-style persistence (sync `postgresql://` URI as documented in `docs/dev-setup.md`).
- **Worker** (`apps/worker/job_executor.py`): compiles with **`PostgresSaver`** when `CHECKPOINT_DB_URL` or `LANGGRAPH_CHECKPOINT_BACKEND=postgres` + `DATABASE_URL` resolve to a sync URI; otherwise **`MemorySaver`**. **`graph_invoke_config`** supplies `thread_id`, LangSmith/LangFuse **metadata** (`idempotency_key`, `deepguard.graph_version`, `deepguard.correlation_id`, …) and **LangFuse callbacks** on `stream`/`invoke` (LangGraph `compile()` does not take callbacks).

### 2.4 Invocation API

- Worker uses **`app.stream(..., stream_mode="values")`** and updates Redis heartbeat with recent node ids; batch semantics unchanged vs one-shot `invoke`.

---

## 3. LangChain — how it appears today

- **Agents** (`packages/agents`): **`deepguard_agents.lc_chains`** builds **LCEL `Runnable`s** for Athena/Circe with **`with_structured_output`** when the chat model supports it, plus **budget** / **policy excerpt cache** helpers (`lc_budget`, `lc_retrieval`) — see §7.2 in this doc.
- **Graph / worker** use **`langchain_core.runnables.RunnableConfig`** for **`thread_id`**, **`tenant_id`**, and tracing **metadata** on `invoke` / `stream` / resume.
- Hermes ingestion remains outside LangChain chat abstractions; LangChain is the path for **structured LLM agent I/O** (Athena/Circe) and **sink callbacks**.

---

## 4. LangSmith — implemented behaviour

- **Package:** Install **`langsmith`** via **`pip install ".[tracing-langsmith]"`**, **`".[tracing]"`**, or **`".[dev]"`** (minimal **`pip install .`** omits it for air-gap images).
- **Tracing:** LangGraph/LangChain runs pick up **LangSmith** when `LANGCHAIN_TRACING_V2=true` and `LANGSMITH_API_KEY` / `LANGCHAIN_API_KEY` is set — no extra handler is required for basic run export. **`langsmith_tracing_effective()`** in `llm_callbacks.py` mirrors that predicate for runbooks.
- **Defaults:** `configure_langsmith_env_defaults()` (worker `__main__` and `configure_observability_at_startup`) sets `LANGCHAIN_TRACING_V2=false` when `CI`, `GITHUB_ACTIONS`, or `DEEPGUARD_AIR_GAP` is set, or when the variable is already explicitly provided (AC-DG-11-009-01).
- **Evaluations (baseline):** `run_athena_gold_stub_eval` scores the sample JSONL under `eval/harness/fixtures/` and best-effort reads the **LangSmith** dataset API when a key is present. Pass/fail threshold is tunable via **`LANGSMITH_EVAL_ACCURACY_THRESHOLD`** (default `0.98`). CLI: `python3 scripts/run_langsmith_eval_stub.py`.

---

## 5. LangFuse — self-hosted

- **Package:** Install **`langfuse`** via **`pip install ".[tracing-langfuse]"`**, **`".[tracing]"`**, or **`".[dev]"`**.
- **Callback:** `build_langchain_callbacks` constructs **`langfuse.langchain.CallbackHandler`** when host + keys are present; failures are logged and do not break the worker (AC-DG-11-009-02).
- **Compose:** `docker/langfuse/README.md` points at the upstream LangFuse **docker-compose** stack (run in an isolated project to avoid port clashes with `docker/compose.dev.yml`).

---

## 6. OpenTelemetry — API + worker

- **`configure_observability_at_startup(service_name=...)`** — used by API lifespan and worker loop start; respects `DEEPGUARD_OTEL_BOOTSTRAP` (`0` in `tests/conftest.py` and `scripts/ci_quality.sh`).
- **`instrument_fastapi_app`** — attaches **OpenTelemetry FastAPI** instrumentation when an SDK `TracerProvider` is installed.
- **`graph_node_span`** — per-node OTEL spans with `deepguard.observation.kind` (default **`GRAPH_NODE`**) and optional **`deepguard.correlation_id`** from **`graph_correlation_context`** (EPIC-DG-11-005-02 / §8.2 mapping hint for LangFuse dashboards).

---

## 7. Recommendations — performance of agentic workflows

These build on what LangGraph and LangChain are good at once real LLM/tool nodes replace stubs.

### 7.1 LangGraph

1. **Production checkpointing** — **Done:** worker selects **`PostgresSaver`** via `CHECKPOINT_DB_URL` or `LANGGRAPH_CHECKPOINT_BACKEND=postgres` + `DATABASE_URL`; otherwise **`MemorySaver`**.
2. **`astream_events` / `stream_mode`** — **Done (baseline):** worker uses **`stream_mode="values"`** and Redis heartbeat tail; optional **SSE/Webhook** remains future work.
3. **Subgraphs per agent** — Model Hermes, Argus, Athena, etc. as **compiled subgraphs** with clear IO contracts; keeps parent graph readable and allows per-subgraph retries and policies.
4. **Retry and fallibility policies** — Use LangGraph’s supported patterns for **retrying transient tool/LLM failures** on specific nodes only (e.g. cloud connector) while failing fast on deterministic validation errors.
5. **Send / map-reduce patterns** — For large repos, extend **`Send`** to shard work (e.g. per-directory or per-service) into parallel mappers with a reducer node, controlled by budget caps.
6. **Interrupts / HITL** — Use `interrupt_before` on high-risk nodes (e.g. Athena) when policy flags `AWAITING_REVIEW`, aligned with architecture §4.7.

### 7.2 LangChain (when agents call models)

1. **Structured output** — Use **`with_structured_output`** (or tool calling) so Athena/Circe emit **Pydantic** `Finding` / remediation types directly, reducing repair loops and token waste.
2. **Runnable composition** — Wrap each agent as a **`Runnable`** with explicit input/output schemas for unit testing and for LangSmith/LangFuse run trees.
3. **Caching and embeddings** — Use LangChain caching for repeated policy excerpts and retrieval steps; pair with pgvector indexing already planned in the architecture.
4. **Middleware** — Centralise rate limiting, token counting, and **budget enforcement** in runnable middleware so every LLM path gets the same guardrails.

---

## 8. Observability — implemented (§8 roadmap)

### 8.1 LangSmith (optional SaaS / team dev)

| Item | Implementation |
|------|----------------|
| Optional install | **`[tracing-langsmith]`**, **`[tracing]`**, **`[dev]`** in `pyproject.toml`; **not** in bare `dependencies` so **`pip install .`** stays air-gap friendly. |
| Tracing env | `LANGCHAIN_TRACING_V2`, `LANGSMITH_API_KEY` / `LANGCHAIN_API_KEY`; **`configure_langsmith_env_defaults()`** for CI/air-gap. |
| `RunnableConfig` | **`graph_invoke_config()`** attaches **callbacks** (LangFuse) + **metadata** to **`invoke` / `stream`** — LangGraph **`compile()`** does not accept callbacks; node-level LangSmith steps come from the runtime + metadata on those calls. |
| Joinable metadata | **`scan_id`**, **`tenant_id`**, **`idempotency_key`**, **`deepguard.graph_version`**, **`deepguard.correlation_id`**, **`deepguard.run_name`** (all passed through **`redact_secrets`**). |
| Datasets / eval gate | **`run_athena_gold_stub_eval`** + env **`LANGSMITH_EVAL_ACCURACY_THRESHOLD`**; merge gating remains a CI policy choice (architecture §33). |

### 8.2 LangFuse (self-hosted)

| Item | Implementation |
|------|----------------|
| Optional install | **`[tracing-langfuse]`**, **`[tracing]`**, **`[dev]`**. |
| LangChain handler | **`build_langchain_callbacks`** → **`langfuse.langchain.CallbackHandler`** when env trio is set; ordered **LangFuse → LangSmith** (EPIC-DG-11-009-03). |
| `graph_node_span` ↔ LangFuse | OTEL span name **`graph.node.<node>`**, attributes **`deepguard.graph.node`**, **`deepguard.observation.kind`**; LangFuse continues to observe **LLM** generations via LangChain callbacks when real models are wired. |
| Redaction | **`redact_secrets`**, **`excerpt_for_trace_sink`**, **`sanitize_trace_metadata_value`** on metadata payloads (§23.1 / EPIC-DG-11-001). |

### 8.3 Unified correlation & feature matrix

| Item | Implementation |
|------|----------------|
| Correlation ID | **`primary_correlation_id(scan_id=..., redis_message_id=...)`**; worker sets **`graph_correlation_context`** for the graph **`stream`** so **`graph_node_span`** and LangChain **`configurable["deepguard.correlation_id"]`** align. Optional env **`DEEPGUARD_REDIS_MESSAGE_ID`** joins the queue message id into the correlation string. |
| `thread_id` | Remains **`scan_id`** for LangGraph checkpointing (unchanged). |
| Runbook helper | **`observability_feature_matrix()`** → `langsmith_effective`, `langfuse_callbacks`, `air_gap` flags. |

### 8.4 First-party workflow timeline, UI API, and OTEL mirror (A–F)

| Item | Implementation |
|------|----------------|
| **A** — Persisted timeline | Alembic **`0003_scan_workflow_observability`**: **`scan_run_events`** (`event_seq`, `event_type`, `node`, `correlation_id`, `graph_version`, redacted `payload` JSON); worker **`_persist_timeline_event`** + concurrent **`SimpleQueue`** drain (avoids `run_coroutine_threadsafe` deadlock with **`asyncio.to_thread`**). |
| **B** — Graph inspector | **`GET /v1/scans/{scan_id}/workflow`** (`include_events` query); **`deepguard_graph.odysseus_planned_graph_nodes`** drives checklist; payloads sanitized with **`redact_secrets`**; no checkpoint JSON exposed. |
| **C** — Live updates | **`GET /v1/scans/{scan_id}/workflow/stream`** (`text/event-stream`): Postgres path polls new `event_seq` rows + optional **Redis** `PUBSUB` on **`deepguard:scan:{scan_id}:timeline`** (same payload shape as DB); memory store polls in-process events. Clients should use **`fetch` + streaming** (not `EventSource`) so **`X-API-Key`** works. |
| **D** — Vendor trace links | **`scan_external_trace_refs`** + **`GET /v1/scans/{scan_id}/trace-links`**; LangSmith URL from **`langsmith_run_url()`** (`LANGSMITH_UI_ORIGIN`, **`LANGSMITH_ORGANIZATION_ID`** stored in `workspace_id`, **`LANGSMITH_PROJECT_ID`** in `project_id`); **`LangChainRootRunRecorder`** captures root run id when LangSmith tracing is effective. |
| **E** — Agent handoffs | Worker emits **`agent_handoff`** events (`from_agent`, `to_agent`, `message_type=graph_edge`, redacted `summary`) between consecutive **`node_progress`** steps. |
| **F** — OTEL-neutral mirror | Worker emits **`otel_span_mirror`** per graph step with **`span_name`** = `graph.node.<id>` and **`observation_kind`** aligned with **`graph_node_span`**. |

**Tests:** `apps/api/tests/test_scan_workflow_api.py`, `packages/graph/tests/test_planned_topology.py`, `packages/observability/tests/test_langchain_root_run.py`, extended **`tests/test_l12_worker_graph_memory.py`**.

**Tests (§8.1–8.3):** `packages/observability/tests/test_llm_callbacks.py`, `test_tracing_correlation.py`, `test_redaction_sanitize.py`; integration: **`test_langsmith_client_integration.py`** (`@pytest.mark.integration`, requires **`langsmith`** + **`LANGSMITH_API_KEY`**).

---

## 9. Quick file reference (implementation)

| Area | Path |
|------|------|
| Graph builder | `packages/graph/src/deepguard_graph/graph.py` |
| State | `packages/graph/src/deepguard_graph/state.py` |
| Stubs | `packages/graph/src/deepguard_graph/stub_nodes.py` |
| Postgres saver helper | `packages/graph/src/deepguard_graph/checkpoint_pg.py` |
| Graph tests (checkpoints, `RunnableConfig`) | `packages/graph/tests/test_odysseus_graph_l5.py` |
| Worker invoke + tracing config + timeline queue | `apps/worker/src/deepguard_worker/job_executor.py` |
| Planned graph nodes (checklist) | `packages/graph/src/deepguard_graph/planned_topology.py` |
| Workflow API + SSE | `apps/api/src/deepguard_api/routers/scan_workflow.py` |
| Workflow response assembly | `apps/api/src/deepguard_api/services/workflow_response.py`, `trace_urls.py` |
| LangSmith root run capture | `packages/observability/src/deepguard_observability/langchain_root_run.py` |
| Timeline Redis channel helper | `packages/core/src/deepguard_core/queue.py` (`scan_timeline_pubsub_channel`) |
| DB migration (events + trace refs) | `alembic/versions/0003_scan_workflow_observability.py` |
| LangSmith/LangFuse callbacks + `graph_invoke_config` | `packages/observability/src/deepguard_observability/llm_callbacks.py` |
| Correlation ID helpers | `packages/observability/src/deepguard_observability/correlation.py` |
| OTEL bootstrap + FastAPI hook | `packages/observability/src/deepguard_observability/runtime.py` |
| Redaction / excerpts | `packages/observability/src/deepguard_observability/redaction.py` |
| Observability tests (§8) | `packages/observability/tests/test_llm_callbacks.py`, `test_tracing_correlation.py`, `test_redaction_sanitize.py`, `test_langsmith_client_integration.py` |
| Eval stub | `packages/observability/src/deepguard_observability/eval_stubs.py`, `scripts/run_langsmith_eval_stub.py` |
| OTEL span helper | `packages/observability/src/deepguard_observability/tracing.py` |
| LangFuse self-host notes | `docker/langfuse/README.md` |
| Dev notes (EPIC-DG-11) | `docs/dev-setup.md`, `.env.example` |

---

## 10. Closing

The codebase **fully utilises LangGraph** as the orchestration shell (ingestion subgraph, `Send`, retries, HITL `interrupt_before`, Postgres or memory checkpointing in the worker, **`stream_mode="values"`** heartbeats). **LangChain** runnables cover **Athena/Circe structured I/O** with budget and excerpt caching. **EPIC-DG-11 / §8** now wire **optional** **`langsmith`** / **`langfuse`** packages, **rich `graph_invoke_config` metadata**, **correlation context** for OTEL + LangChain, **`observability_feature_matrix()`**, **metadata string sanitisation**, and **eval threshold** env tuning. **§8.4** adds **first-party `scan_run_events`**, **sanitized workflow + SSE APIs**, **explicit handoffs**, **LangSmith trace deep links**, and **OTEL-span-mirror events** for air-gap parity. Remaining stretch: **dataset-backed merge gates** on LangSmith, **LangFuse session/user ids** where the SDK exposes them, **mid-graph SSE without polling** under extreme throughput, and **OTLP export** into LangFuse if/when you standardise on that path instead of LangChain callbacks only.
