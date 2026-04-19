---
status: approved
approved_date: 2026-04-18
approvers: [Engineering bootstrap — per IMPLEMENTATION_PLAN Phase L0]
related_phases: [L0]
---

# Design: L0 monorepo scaffold

## Goal

Establish a **runnable Python workspace** with `packages/core`, `packages/graph`, `apps/api`, `apps/worker`, **Ruff**, **Mypy** (strict on `deepguard_core` + `deepguard_graph`), **Pytest** + **80% coverage** gate, without product logic.

## Decisions

| Topic | Choice |
|-------|--------|
| Build | Single root `pyproject.toml`, `setuptools`, editable install `.[dev]` |
| Layout | `src/` under each package per Architecture §25 |
| Lint scope | Ruff on `packages/`, `apps/`, `tests/`; exclude legacy root `diagrams*.py`, `generate_*.py`, `scripts/` |
| Mypy | Strict on `deepguard_core`, `deepguard_graph` only; `mypy_path` in `pyproject.toml` |
| Coverage | `fail_under=80` on the four packages |

## Out of scope (L0)

- FastAPI routes, LangGraph, Docker compose data plane (L1+).

## Tests

- `tests/test_l0_smoke.py` — import smoke for all four packages.
