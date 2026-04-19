# Engineering design specs (pre-coding)

Design specs in this directory are **slice/delta** documents for a feature, epic story set, or `IMPLEMENTATION_PLAN.md` phase. They **do not replace** `Architecture_Design.md`.

## Required before implementation

1. Link **`US-DG-*`** and **`AC-DG-*`** from `docs/user-stories/`.
2. Frontmatter includes `status: draft | in-review | approved`, `approvers`, `approved_date` when approved.
3. Follow **`.cursor/skills/deepguard-delivery-quality/SKILL.md`** for approval rules and test strategy.

## Naming

Use either `DG-{epic}-{story}-design.md` or `phase-L{n}-{slug}.md`; keep one convention per team.

## Examples in this repo

- [`phase-L0-monorepo-scaffold.md`](phase-L0-monorepo-scaffold.md) — Phase L0 workspace bootstrap.
- [`phase-L1-data-plane.md`](phase-L1-data-plane.md) — Phase L1 Docker + Alembic + seed.
- [`frontend-console-mvp-wireframes-and-mockups.md`](frontend-console-mvp-wireframes-and-mockups.md) — EPIC-DG-14 console UX (pre-Figma).
- [`frontend-implementation-plan.md`](frontend-implementation-plan.md) — Ordered build & verification steps for `apps/web`.
