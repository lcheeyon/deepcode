# Worker & queue

## Producer (API)

When **`DATABASE_URL`** and **`REDIS_URL`** are configured, a successful **`POST /v1/scans`** (that is not satisfied purely by idempotency replay) **publishes a job** to the Redis stream used by workers (`stream:scans`, consumer group **`workers`** — see architecture and core queue helpers).

## Consumer (worker)

Run the worker from the repo root with the workspace installed:

```bash
python3 -m deepguard_worker
```

Required environment matches the data plane: **`DATABASE_URL`**, **`REDIS_URL`**. Optional tuning includes consumer name, heartbeat interval, and stub iterations (see **`docs/dev-setup.md`** Phase L4 section).

## Graph execution

The worker integrates the **Odysseus** LangGraph built in **`deepguard_graph`** (checkpoint configuration for Postgres-backed resume is documented in **`docs/dev-setup.md`** Phase L5).

## Verification

- Unit tests: `pytest tests/test_l4_api.py tests/test_l4_worker_unit.py packages/core/tests/test_queue_scan_message.py -q`
- Broader pipeline: package tests under `packages/graph/tests`, `packages/agents/tests`, etc., as listed in **`docs/dev-setup.md`**.
