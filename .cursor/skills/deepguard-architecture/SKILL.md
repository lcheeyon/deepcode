---
name: deepguard-architecture
description: >-
  DeepGuard (玄武) Compliance Engine — agentic LangGraph scan pipeline, tenancy,
  data-sovereignty rules, API/DB/queue contracts. Use when implementing or
  refactoring this repo, working on scans, agents, Hermes–Penelope pipeline,
  compliance mapping, IaC/cloud connectors, reports, IMPLEMENTATION_PLAN phases,
  or when the user mentions DeepGuard, 玄武, Odysseus, LangGraph scan state, or
  Architecture_Design.md.
---

# DeepGuard / 玄武 — project architecture skill

**Authoritative spec:** `Architecture_Design.md` (v0.2+). This skill is a **compressed** checklist; if anything conflicts, follow `Architecture_Design.md`.

## Product one-liner (do not drop when compacting)

Autonomous **compliance engine**: ingest **source code + IaC + read-only cloud snapshots**, map to **policy controls** (ISO 27001, SOC 2, 等保, etc.), output **findings + remediations + audit-style PDF**, with **VPC / air-gap** option so sensitive code and config stay inside the customer boundary.

## Hard constraints (non-negotiable)

1. **No code egress by default** — source must not leave the customer VPC unless an explicit SaaS LLM tier is chosen; design for **artifact refs** + on-prem indexing.
2. **Cloud connectors are read-only** — no mutating customer infrastructure.
3. **Typed shared state** — `ScanState` / Pydantic; **structured LLM outputs** and validated **ToolCallPlan** before tools run (prompt-injection defence).
4. **Secrets** — short-lived credentials via **Calypso** pattern; never persist API keys or raw secrets in `ScanState`, checkpoints, or observability payloads.

## Odysseus pipeline (graph order)

Single orchestrated DAG (**Odysseus Engine** / 姜子牙):

`hermes` → `tiresias` → `argus` → **parallel** `laocoon` + `cassandra` → `convergence_gate` → `athena` → `circe` → `penelope` → end.

- **Hermes:** clone/stage repo, optional cloud snapshot fetch.  
- **Tiresias:** policies → `PolicyControl[]`.  
- **Argus:** AST index, dependency graph, embeddings / `code_index_id`.  
- **Laocoon / Cassandra:** IaC findings + cloud findings (artifact refs if large).  
- **Athena:** compliance mapping + **cross-layer** findings; generator + critic pattern.  
- **Circe:** remediation (diffs, IaC fixes, CLI suggestions) — **not auto-applied**.  
- **Penelope:** report → PDF to object store.

## Agent registry (code → role)

| Code | Role |
|------|------|
| Hermes | Ingestion |
| Tiresias | Policy parser |
| Argus | Code indexer |
| Laocoon | IaC |
| Cassandra | Cloud config |
| Athena | Compliance mapper |
| Circe | Remediation |
| Penelope | Report assembler |
| Calypso | Secrets |
| Aeolus | Queue / events |
| Eumaeus | AuthZ |

## Implementation anchors (v0)

- **Monorepo:** `apps/api`, `apps/worker`, `packages/{core,graph,agents,tools,retrieval,connectors,parsers,policies,reporting}` — see `reference.md`.  
- **Stack:** Python **3.12**, **LangGraph** (checkpoint **Postgres**), **LangChain / LCEL**, **FastAPI**, **PostgreSQL + pgvector**, **Redis** (streams + cache), **S3-compatible** object store.  
- **Graph runtime:** `thread_id = scan_id`; resume with `invoke(None, config)` after checkpoint.  
- **Athena MVP:** **single node**, controls batched (**8–12** per generator+critic cycle), checkpoint after each batch.  
- **Semantic cache default:** **0.97** similarity threshold (tunable per tenant).  
- **Traces:** full raw LLM payload in **tenant DB**; LangSmith/LangFuse get **redacted** excerpts only.

## Inter-agent communication

Agents **do not call each other directly**. Use **partial `ScanState` updates**, **Redis/Kafka** for async work, and **object-store artifact refs** for large blobs — never embed huge payloads in messages.

## Reasoning pattern (per agent)

**Structured ReAct:** observe typed state → think → **typed** tool plan → tool execution → verify → emit typed outputs + **confidence_score**; cap iterations; low confidence → `UNCERTAIN` / escalation flags per architecture doc.

## Delivery & quality gate (before merge / phase close)

Follow **`.cursor/skills/deepguard-delivery-quality/SKILL.md`** for every Part/Phase:

1. **User stories + `AC-DG-*`** updated in `docs/user-stories/`  
2. **Design spec** in `docs/design/` — **approved** (not draft) before implementation  
3. **Code** → **unit tests ≥80%** line coverage on touched packages → **integration tests** (Docker) → **Playwright BDD** → **manual UAT last**

Do not treat architecture-only discussion as substitute for an **approved** design spec for the slice in flight.

## When editing this repo

1. Match **existing** package boundaries and naming (`ScanState`, `PolicyControl`, `Finding`, Greek code names in internal IDs where used).  
2. Prefer **LCEL** `Runnable`s over legacy chains.  
3. Tools: **allowlisted**, paths via **repo sandbox** (`safe_read`); no arbitrary execution.  
4. New cloud or IaC support: implement behind **`CloudConnector` / parser registry`**, normalise to shared snapshot types before Athena.  
5. Before merge: **tests** for parsers/tools; **coverage and BDD gates** per delivery-quality skill; do not regress **false-positive** eval expectations when touching prompts or mapping.

## Memory compaction — preserve if summarizing chat

Keep this minimum block in any summary you write back to the user or to future turns:

- **Name:** DeepGuard Compliance Engine (玄武) — code + IaC + cloud → controls → PDF.  
- **Graph:** hermes → tiresias → argus → (laocoon ∥ cassandra) → gate → athena → circe → penelope.  
- **Rules:** no default code egress; read-only cloud; typed state + structured outputs; secrets Calypso TTL; `thread_id=scan_id`.  
- **Spec path:** `Architecture_Design.md`.  
- **Delivery:** stories → **approved** design spec → code → **unit ≥80%** → integration → **Playwright BDD** → manual UAT (`deepguard-delivery-quality` skill).

## Deeper detail (load on demand)

- Tables: env vars, HTTP routes, DB tables, `runtime_config` keys, scan statuses, import matrix → [reference.md](reference.md)  
- Full narrative, diagrams, open questions → `Architecture_Design.md`  
- Product epics → `docs/user-stories/`  
- Delivery / test pyramid → `.cursor/skills/deepguard-delivery-quality/SKILL.md`
