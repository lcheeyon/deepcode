# Self-hosted LangFuse (EPIC-DG-11)

DeepGuard sends LangChain/LangGraph runs to **LangFuse** when these env vars are set on the **worker** (and any future LLM entrypoints):

| Variable | Purpose |
|----------|---------|
| `LANGFUSE_HOST` | Base URL of the LangFuse web API (e.g. `http://127.0.0.1:3000`) |
| `LANGFUSE_PUBLIC_KEY` | Project public key |
| `LANGFUSE_SECRET_KEY` | Project secret key |

If any of these are missing, the LangFuse callback is **not** constructed and startup does not fail (AC-DG-11-009-02).

## Official stack

LangFuse publishes a full **Docker Compose** stack (Postgres, ClickHouse, Redis, MinIO, `langfuse-web`, `langfuse-worker`). Use it in an **isolated** directory or Docker project name so ports do not clash with `docker/compose.dev.yml`:

```bash
mkdir -p ../langfuse-local && cd ../langfuse-local
curl -fsSL -o docker-compose.yml https://raw.githubusercontent.com/langfuse/langfuse/main/docker-compose.yml
docker compose up -d
```

Then point `LANGFUSE_HOST` at the published `langfuse-web` port (default **3000** in upstream; remap host ports if needed).

## LangSmith (SaaS or self-hosted)

- Set `LANGSMITH_API_KEY` (or `LANGCHAIN_API_KEY`) for export.
- `LANGCHAIN_TRACING_V2` defaults to **true** outside CI; set `false` for air-gap (see `DEEPGUARD_AIR_GAP=1` or explicit `LANGCHAIN_TRACING_V2=false`).

## OpenTelemetry

- `DEEPGUARD_OTEL_BOOTSTRAP=1` (default): API/worker install a console OTLP-friendly `TracerProvider` via `configure_observability_at_startup`.
- `DEEPGUARD_OTEL_BOOTSTRAP=0`: skip provider install (used in `pytest` via `tests/conftest.py` and in `scripts/ci_quality.sh`).
