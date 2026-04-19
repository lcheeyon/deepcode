# Repository agents — DeepGuard / 玄武

**Architecture skill:** `.cursor/skills/deepguard-architecture/SKILL.md`  
**Tables / API / env:** `.cursor/skills/deepguard-architecture/reference.md`  
**Full spec:** `Architecture_Design.md`  
**Implementation plan:** `IMPLEMENTATION_PLAN.md`  
**Delivery & tests (80% unit, integration, Playwright BDD, UAT last):** `.cursor/skills/deepguard-delivery-quality/SKILL.md`  
**Ad-hoc browser troubleshooting (optional CLI):** `.cursor/skills/deepguard-agent-browser/SKILL.md` — [agent-browser](https://agent-browser.dev/) for snapshot/ref-driven flows alongside Playwright.  
**MCP CLI (Chrome DevTools MCP + others):** `.cursor/skills/deepguard-mcporter/SKILL.md` — [MCPorter](https://mcporter.dev/) to `list` / `call` / `generate-cli` MCP servers from the shell ([repo](https://github.com/steipete/mcporter)).

Claude Code also resolves `.claude/skills/*` → `.cursor/skills/*` (symlinks). For prose context, see `CLAUDE.md`.

---

## Default checks after creating or updating Python code

Run from the repo root with dev deps (`pip3 install -e ".[dev]"`) and the project venv active. **Do not treat a change as complete until the checks below pass**, including Pyright.

### One-shot (preferred)

- **Git checkout:** `pre-commit run --all-files` (after `pre-commit install` once). This runs Ruff (check + format), Mypy, Pyright, a **fast** pytest slice (`-m "not integration"`, `--maxfail=5`), **import-linter**, and **Bandit** on apps + sensitive packages (see `.pre-commit-config.yaml`).
- **No git / CI parity:** `make ci-quality` → `scripts/ci_quality.sh` — same as pre-commit hooks, plus **`deptry`**, then full **`pytest --cov --cov-fail-under=80`**. For **`pip-audit`** (transitive CVE triage), run **`make audit`** (GitHub Actions runs it in a non-blocking job; see `.github/workflows/quality.yml`).

### Manual order (if hooks are not used)

1. **`ruff check .`** and **`ruff format --check .`** (or `ruff format .` to fix).  
2. **`mypy -p deepguard_core -p deepguard_graph -p deepguard_policies -p deepguard_parsers -p deepguard_connectors -p deepguard_agents -p deepguard_reporting -p deepguard_observability -p deepguard_api -p deepguard_worker`**.  
3. **`python3 -m pyright`**.  
4. **`bash scripts/run_lint_imports.sh`** — import-layer contracts (`[tool.importlinter]` in `pyproject.toml`).  
5. **`python3 -m bandit -c pyproject.toml -q -r apps/api/src apps/worker/src packages/agents/src packages/connectors/src`**.  
6. **`python3 -m deptry .`** — unused / undeclared dependency check. **`make audit`** adds **`pip-audit`** when you are triaging CVEs (can fail on transitive advisories until pins are updated).  
7. **`pytest -q --cov --cov-fail-under=80`** (or a narrow slice first, then full before merge).

Fix Pyright, Mypy, import-linter, deptry, Bandit, and test failures in the **same** change series when possible; do not merge known debt.
