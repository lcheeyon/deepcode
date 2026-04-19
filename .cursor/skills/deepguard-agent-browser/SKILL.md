---
name: deepguard-agent-browser
description: >-
  Runs agent-browser (Rust CLI) for compact accessibility-tree snapshots, ref-based
  clicks, forms, screenshots, and sessioned browser flows. Use when troubleshooting
  web UIs, reproducing bugs against a running app (e.g. local FastAPI + Swagger),
  validating BDD-related behaviour without editing Playwright tests, exploring
  external docs, or when the user mentions agent-browser, browser automation from
  the terminal, or snapshot-driven debugging.
---

# DeepGuard — agent-browser for troubleshooting

**Upstream docs:** [agent-browser.dev](https://agent-browser.dev/) — install, commands, snapshots, sessions, CDP mode.

**Role in this repo:** Optional **agent-driven** browser (shell commands, token-efficient text output). It complements **Playwright** in `.cursor/skills/deepguard-delivery-quality/SKILL.md` (structured BDD/CI). Use agent-browser for **ad-hoc investigation**; keep **regressions** in pytest/Playwright.

For **Chrome DevTools–level** inspection via **MCP** from the shell (`mcporter list` / `call`, optional `generate-cli`), see `.cursor/skills/deepguard-mcporter/SKILL.md`.

---

## 1. Install (once per machine)

Pick one:

```bash
npm install -g agent-browser
# or: brew install agent-browser
# or one-off: npx agent-browser open https://example.com
```

First-time Chrome download:

```bash
agent-browser install
```

Confirm: `agent-browser --help` (or your package manager’s equivalent).

---

## 2. Core loop (what the agent should do)

1. **Target** — Prefer **local dev** URLs (`http://127.0.0.1:8000`, etc.) or **non-production** staging. Do not drive **production** tenants or real secrets without explicit user approval.
2. **Open** — `agent-browser open <url>` (daemon starts if needed).
3. **Snapshot** — `agent-browser snapshot -i` for an accessibility tree with **`[ref=eN]`** lines (compact vs full DOM).
4. **Act** — Use refs from the latest snapshot: `agent-browser click @e2`, fill fields, navigate, etc. **Re-snapshot** after navigation or large DOM changes.
5. **Evidence** — `agent-browser screenshot path.png` when the user needs a visual record; paste or attach paths the user can open.
6. **Close** — `agent-browser close` when finished so sessions do not linger.

If commands fail, check [installation](https://agent-browser.dev/) and that **Chrome** was installed via `agent-browser install`.

---

## 3. DeepGuard-specific scenarios

| Goal | Suggestion |
|------|------------|
| **API / OpenAPI** | Run `uvicorn` per `docs/dev-setup.md`, then `agent-browser open http://127.0.0.1:8000/docs` (or `/redoc`), snapshot, exercise endpoints from the UI if needed. |
| **“It works in curl but not in browser”** | Same URL in agent-browser; inspect network or behaviour per upstream **Commands** docs. |
| **Compare envs** | Separate **sessions** (see upstream **Sessions**) for local vs staging to avoid cookie bleed. |
| **Playwright gap** | Use agent-browser to **explore** selectors and flows; then encode stable checks in Playwright/Gherkin. |

---

## 4. Practices

- **Determinism:** Always pair **click/type** with a **fresh snapshot** from the same session so `@eN` refs match the current tree.
- **CI:** Do not rely on agent-browser in GitHub Actions unless the team adds it explicitly; default CI stays **pytest / Playwright**.
- **Secrets:** Use dev API keys and seed tenants only; never paste live credentials into chat logs.
- **Cost:** Prefer `snapshot -i` over dumping huge HTML; that is the tool’s intended agent-first mode.

---

## 5. Quick reference (minimal)

```bash
agent-browser open http://127.0.0.1:8000/docs
agent-browser snapshot -i
agent-browser click @e2
agent-browser screenshot /tmp/deepguard-swagger.png
agent-browser close
```

For **50+ commands**, sessions, diffing, and CDP, use the official reference at [agent-browser.dev](https://agent-browser.dev/).
