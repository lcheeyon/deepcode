# DeepGuard / 玄武 — Claude Code project context

This repository implements the **DeepGuard Compliance Engine** (玄武): an **agentic**, **LangGraph**-orchestrated pipeline that analyses **application code**, **IaC**, and **read-only cloud configuration** against **compliance frameworks**, producing **findings**, **remediations**, and **PDF reports**.

## Single source of truth for agents

1. **Primary skill (use for every implementation task):**  
   `.cursor/skills/deepguard-architecture/SKILL.md`  
2. **Dense tables (API, env, DB, flags, layout):**  
   `.cursor/skills/deepguard-architecture/reference.md`  
3. **Requirements / user-story IDs and test traceability (`EPIC-DG-*`, `US-DG-*`, `AC-DG-*`, `TC-DG-*`):**  
   `.cursor/skills/deepguard-requirements-traceability/SKILL.md`  
4. **Full specification:** `Architecture_Design.md`  
5. **Phased delivery (local laptop → multi-cloud):** `IMPLEMENTATION_PLAN.md`  
6. **Quality pipeline (stories → approved design → code → 80% unit → integration → Playwright BDD → UAT):**  
   `.cursor/skills/deepguard-delivery-quality/SKILL.md`
7. **Optional browser CLI for live troubleshooting (snapshots, refs, screenshots; not a CI default):**  
   `.cursor/skills/deepguard-agent-browser/SKILL.md` — see [agent-browser.dev](https://agent-browser.dev/).
8. **Optional MCPorter CLI (discover and call MCP tools from the terminal, including Chrome DevTools MCP):**  
   `.cursor/skills/deepguard-mcporter/SKILL.md` — see [mcporter.dev](https://mcporter.dev/) and [steipete/mcporter](https://github.com/steipete/mcporter).

The directories under `.claude/skills/` are **symlinks** into `.cursor/skills/` so Cursor and Claude Code stay aligned.

## Non-negotiables

- Default **no code egress**; VPC / air-gap deployments first-class.  
- **Read-only** cloud APIs only.  
- **Typed** `ScanState` / Pydantic; **structured** LLM outputs; validated tool plans.  
- **Secrets:** short-lived via Calypso; never in checkpoints or traces (redact for LangFuse/LangSmith).

## Graph order (Odysseus)

`hermes` → `tiresias` → `argus` → (`laocoon` ∥ `cassandra`) → convergence → `athena` → `circe` → `penelope`.

## Python and tooling

Use **python3** and **pip3** per project conventions. Target stack: Python **3.12**, LangGraph, LangChain LCEL, FastAPI, Postgres+pgvector, Redis, Alembic.

## Epics and stories

See `docs/user-stories/` for EPIC-level scope aligned with the architecture.  
Numbering and traceability rules: `docs/user-stories/00-numbering-and-traceability.md` (summarised in the traceability skill above).
