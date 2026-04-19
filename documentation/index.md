# DeepGuard documentation

**DeepGuard (玄武)** is an agentic compliance engine: **code, IaC, and cloud configuration** flow through policy controls toward **findings**, **remediations**, and **PDF reports**. This site summarizes what is **implemented today** in the monorepo and how to run, test, and extend it.

!!! tip "Source of truth in the repository"
    Long-form specifications remain in the repo root and under `docs/` as Markdown files (architecture, phased plan, user stories). This site is a **curated guide** with stable navigation and search. Clone the repository to follow file paths referenced here.

## Where to go next

| I want to… | Start here |
|------------|------------|
| Set up Python, run tests, run the API | [Getting started](getting-started.md) |
| Understand the agent graph, gates, and messaging | [Agentic orchestration](agentic-orchestration.md) |
| Understand packages and boundaries | [Monorepo layout](monorepo.md) |
| Call `POST /v1/scans`, health checks, uploads | [Control plane API](control-plane-api.md) |
| Run the worker and Redis stream consumption | [Worker & queue](worker-queue.md) |
| Postgres, Redis, MinIO locally | [Docker & data plane](docker-data-plane.md) |
| Ruff, Mypy, Pyright, pytest, pre-commit | [Testing & CI](testing-ci.md) |
| EPICs, acceptance criteria, squads | [Backlog & traceability](backlog.md) |
| Phase L0/L1 design notes, console wireframes | [Design artifacts](design.md) |

## Normative references (repo)

- **Architecture:** `Architecture_Design.md` (implementation contracts from §24 onward).
- **Phased delivery:** `IMPLEMENTATION_PLAN.md` (L0–L14 and cloud phases).
- **Developer setup (copy-paste commands):** `docs/dev-setup.md`.
- **Agent / quality checklist:** `AGENTS.md`.
- **Console (Next.js) build checklist:** `docs/design/frontend-implementation-plan.md` and `apps/web/README.md`.

## Building this site locally

Requires Python **3.12+** and the optional **docs** extra:

```bash
pip3 install -e ".[docs]"
python3 -m mkdocs serve
```

Open the URL printed in the terminal (usually `http://127.0.0.1:8000`). A strict production build:

```bash
make docs
```

Output is written to `site/`. The theme is [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
