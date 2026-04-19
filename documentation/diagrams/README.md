# Diagram sources (Mermaid)

PNG exports for MkDocs live in **`documentation/images/`**. Edit the **`.mmd`** files here, then regenerate.

## Full Odysseus agent flow

**Source:** [`odysseus-full-agent-flow.mmd`](odysseus-full-agent-flow.mmd)  
**PNG (built artefact):** [`../images/odysseus-full-agent-flow.png`](../images/odysseus-full-agent-flow.png)

### Regenerate (recommended — no local Chrome)

From repository root:

```bash
bash scripts/render_documentation_diagrams.sh
```

This calls **[Kroki](https://kroki.io/)** over HTTPS to render Mermaid to PNG.

### Alternative: Mermaid CLI (local Chromium)

```bash
cd documentation/diagrams
npx -y @mermaid-js/mermaid-cli@10 -i odysseus-full-agent-flow.mmd \
  -o ../images/odysseus-full-agent-flow.png \
  -b white -w 2400 -H 2000
```

Requires a working **headless Chrome** (Puppeteer); may fail in restricted sandboxes.
