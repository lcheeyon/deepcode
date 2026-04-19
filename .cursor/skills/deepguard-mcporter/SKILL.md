---
name: deepguard-mcporter
description: >-
  Uses MCPorter (npx mcporter) to list and call MCP servers from the shell,
  including the Chrome DevTools MCP via stdio, generate-cli for standalone
  tool CLIs, and daemon lifecycle for stateful browsers. Use when troubleshooting
  pages with DevTools-level APIs (console, network, performance, DOM snapshots),
  discovering MCP tool names/schemas on demand, wrapping stdio MCPs without
  editor MCP slots, or when the user mentions MCPorter, mcporter, or Chrome
  DevTools MCP.
---

# DeepGuard — MCPorter + Chrome DevTools MCP (CLI troubleshooting)

**What MCPorter is:** A [Model Context Protocol](https://modelcontextprotocol.io/) **runtime and CLI** ([steipete/mcporter](https://github.com/steipete/mcporter), [mcporter.dev](https://mcporter.dev/)) that **discovers** MCP servers already configured in **Cursor, Claude Code, Codex**, merges `~/.mcporter/mcporter.json` and project `config/mcporter.json`, and exposes **`list`** / **`call`** / **`generate-cli`** / **`emit-ts`** without hand-written glue.

**Chrome DevTools:** The **browser inspection surface** comes from the **`chrome-devtools-mcp`** server (stdio), not from MCPorter itself. MCPorter **invokes** that MCP—so agents get **tool names + schemas** via `mcporter list` and run **`mcporter call chrome-devtools.<tool> …`** the same way as in-editor MCP, but from **any terminal** (including when the IDE MCP panel is full or unavailable).

**Companion:** For **Rust-native** snapshot/click flows without MCP, see `deepguard-agent-browser` ([agent-browser.dev](https://agent-browser.dev/)). Use **MCPorter + chrome-devtools** when you need **DevTools semantics** (network, console, performance); use **agent-browser** for **ref-driven UI automation**.

---

## 1. Prerequisites

- **Node / npx** on the PATH (try without global install): `npx mcporter --help`.
- **Chrome** running with a debugging target as required by `chrome-devtools-mcp` (follow upstream MCP docs when calls fail to attach).

**Air-gap / no egress:** `npx` pulls packages from the registry unless artifacts are vendored; align with org policy before using on locked-down laptops.

---

## 2. Discover tools on demand (before any `call`)

```bash
# All servers MCPorter can see (imports Cursor/Claude/etc. + local config)
npx mcporter list

# One server: TypeScript-style signatures + doc comments (copy/paste into call)
npx mcporter list chrome-devtools

# Full JSON schema per tool
npx mcporter list chrome-devtools --schema

# Every optional parameter visible
npx mcporter list chrome-devtools --all-parameters
```

**No config yet — ad-hoc stdio** (still listable):

```bash
npx mcporter list --stdio "npx -y chrome-devtools-mcp@latest" --name chrome-devtools
```

Add `--persist config/mcporter.local.json` (or `mcporter config add` with `--scope home|project`) when the team wants a **stable name** without repeating `--stdio`.

**Machine-readable:**

```bash
npx mcporter list --json
```

---

## 3. Call Chrome DevTools tools from the shell

After `list` shows the exact tool id:

```bash
npx mcporter call chrome-devtools.take_snapshot
```

**Syntax variants** (from upstream docs): colon args `tool arg:value`, function-call style `mcporter call 'server.tool(a: "x")'`, optional `--output json|markdown|raw` for scripts.

**Ad-hoc server** (repeat the same `--stdio` as in `list`):

```bash
npx mcporter call --stdio "npx -y chrome-devtools-mcp@latest" --name chrome-devtools <tool.name> ...
```

---

## 4. Stateful sessions (Chrome tab stays warm)

`chrome-devtools` and similar stdio servers can use MCPorter’s **daemon** so connections survive repeated calls:

```bash
npx mcporter daemon status
npx mcporter daemon start    # optional: --log, --log-servers chrome-devtools
npx mcporter daemon stop
npx mcporter daemon restart
```

Use **`daemon start --log`** when diagnosing transport or spawn errors.

---

## 5. Standalone CLI (`generate-cli`)

To **mint a dedicated CLI** for the Chrome DevTools MCP (shareable script, fewer moving flags):

```bash
npx mcporter generate-cli --command "npx -y chrome-devtools-mcp@latest" --output ./tools/chrome-devtools-cli
# See upstream for --bundle, --compile, --include-tools, --runtime bun|node
```

Regenerate when the upstream MCP adds tools and you want new subcommands.

---

## 6. DeepGuard troubleshooting playbook

1. Start the app under test (e.g. `uvicorn` per `docs/dev-setup.md`) and open the page in Chrome as required by the MCP.
2. **`npx mcporter list chrome-devtools`** — note the exact tool names for snapshot, console, network, etc.
3. **`npx mcporter call …`** with **`--output json`** when piping into scripts or comparing responses.
4. If the second call “loses” the tab, check **`mcporter daemon status`** and keep-alive notes in the [MCPorter README](https://github.com/steipete/mcporter/blob/main/README.md).
5. **CI:** Do not depend on MCPorter or live Chrome for default CI; keep assertions in **pytest / Playwright**.

**Full flag matrix:** [docs/cli-reference.md](https://github.com/steipete/mcporter/blob/main/docs/cli-reference.md) in the MCPorter repo.
