# Architecture

## System intent

DeepGuard models compliance work as a **directed scan pipeline**: ingestion and context (**Hermes**), policy interpretation (**Tiresias**), code indexing (**Argus**), parallel analysis branches (**Laocoon**, **Cassandra**), a convergence gate, compliance mapping (**Athena**), remediation (**Circe**), and report assembly (**Penelope**). The normative agent registry and data contracts live in **`Architecture_Design.md`** in the repository root.

## What is implemented in code today

The monorepo delivers:

- **Shared models and queue messages** (`deepguard_core`) — scan requests, job config, partial state, findings-shaped types, and related enums.
- **LangGraph shell** (`deepguard_graph`) — Odysseus graph construction, checkpoints, stub nodes aligned to the architecture doc.
- **Library packages** — policies, parsers, connectors, agents, reporting, observability — with tests and import boundaries enforced by **import-linter** (see `pyproject.toml`).
- **Control plane** (`deepguard_api`) — FastAPI app, **`/v1`** routes, dev tenant resolution, optional Postgres persistence, Redis-backed enqueue when configured.
- **Worker** (`deepguard_worker`) — stream consumer, Hermes-phase wiring and job execution hooks per current phases.

Scan execution order for v0 is fixed in **`IMPLEMENTATION_PLAN.md`**: Hermes → Tiresias → Argus → (Laocoon ∥ Cassandra) → convergence → Athena → Circe → Penelope.

## Where to read more

| Document | Purpose |
|----------|---------|
| [Agentic orchestration](agentic-orchestration.md) | Curated walkthrough: agent roles, LangGraph topology, inter-agent state/messaging, convergence gate vs stubs. |
| [LangGraph / LangChain / LangSmith / LangFuse](langstack-usage-and-roadmap.md) | What the repo actually uses today vs architecture intent, and a roadmap for deeper integration and observability. |
| `Architecture_Design.md` | Full technical specification (C4-style context, LangGraph, API §28, schema §29, queue §30, storage §32, testing §33). |
| `.cursor/skills/deepguard-architecture/SKILL.md` | Condensed architecture skill for agents. |
| `.cursor/skills/deepguard-architecture/reference.md` | Tables, env vars, API surface notes. |
| `IMPLEMENTATION_PLAN.md` | Phase ↔ EPIC mapping and exit criteria. |

!!! note "Console product UI"
    Wireframes and MVP user stories for a **frontend console** tied to the current API are under `docs/design/` and `docs/user-stories/EPIC-14-console-frontend-backend-mvp.md`. See [Design artifacts](design.md).
