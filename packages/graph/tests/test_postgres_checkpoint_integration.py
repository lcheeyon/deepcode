"""Integration: Postgres checkpointer round-trip (requires ``CHECKPOINT_DB_URL``)."""

from __future__ import annotations

import os
import uuid
from typing import cast

import pytest
from deepguard_graph.checkpoint_pg import postgres_checkpointer
from deepguard_graph.checkpoint_resolve import to_sync_postgres_uri
from deepguard_graph.compilation import compile_odysseus_app, resume_odysseus_after_interrupt
from deepguard_graph.state import empty_odysseus_state
from langchain_core.runnables import RunnableConfig


@pytest.mark.integration
def test_postgres_checkpoint_hitl_resume_roundtrip() -> None:
    raw = os.environ.get("CHECKPOINT_DB_URL", "").strip()
    if not raw:
        pytest.skip("CHECKPOINT_DB_URL not set (integration Postgres checkpointer)")
    url = to_sync_postgres_uri(raw)

    tid = str(uuid.uuid4())
    cfg = cast(RunnableConfig, {"configurable": {"thread_id": tid}})
    job = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    init = empty_odysseus_state(
        scan_id=tid,
        created_at="2026-04-18T12:00:00+00:00",
        job_config=job,
    )

    with postgres_checkpointer(url) as saver:
        app = compile_odysseus_app(checkpointer=saver, interrupt_before_athena=True)
        mid = app.invoke(init, config=cfg)
        assert "athena" not in mid.get("execution_log", [])

        end = resume_odysseus_after_interrupt(checkpointer=saver, scan_id=tid, tenant_id="")
        assert end.get("execution_log", [])[-1] == "penelope"
