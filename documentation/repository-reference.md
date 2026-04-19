# Repository reference

Quick map of high-value files at the repository root (not duplicated inside this site).

| File | Description |
|------|-------------|
| `README.md` | Project overview and quick start. |
| `AGENTS.md` | Agent skills, quality gates, tool hints for AI assistants. |
| `CLAUDE.md` | Cross-tool prose pointer (if present). |
| `Architecture_Design.md` | Full architecture specification. |
| `IMPLEMENTATION_PLAN.md` | Phased implementation and EPIC mapping. |
| `pyproject.toml` | Workspace metadata, Ruff/Mypy/Pyright/import-linter/deptry/Bandit. |
| `mkdocs.yml` | This documentation site configuration. |
| `.env.example` | Documented environment variables (no secrets). |
| `.pre-commit-config.yaml` | Local hook pipeline. |
| `.github/workflows/` | CI workflows (quality, audit, etc.). |

## Cursor skills

Agent-oriented skills under **`.cursor/skills/`** include architecture, delivery quality, UI style guide, browser tooling, and MCPorter. See **`AGENTS.md`** for the canonical list.
