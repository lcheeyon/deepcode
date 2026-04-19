"""Phase L5 — Odysseus stub graph order, skips, checkpoint resume (Architecture §4)."""

from __future__ import annotations

import uuid
from typing import cast

from deepguard_graph.graph import build_odysseus_graph
from deepguard_graph.state import empty_odysseus_state
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver


def _job(
    *,
    iac: bool,
    cloud: bool,
    cloud_snapshots: dict | None = None,
) -> dict:
    return {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": iac, "cloud": cloud},
        **({"cloud_snapshots": cloud_snapshots} if cloud_snapshots is not None else {}),
    }


def _compile(**compile_kwargs):
    return build_odysseus_graph().compile(**compile_kwargs)


def _thread_config() -> RunnableConfig:
    return cast(
        RunnableConfig,
        {"configurable": {"thread_id": str(uuid.uuid4())}},
    )


def test_graph_order_matches_architecture_section_4() -> None:
    """Hermes → Tiresias → Argus → (parallel) → gate → Athena → Circe → Penelope."""

    app = _compile(checkpointer=MemorySaver())
    sid = str(uuid.uuid4())
    init = empty_odysseus_state(
        scan_id=sid,
        created_at="2026-04-18T12:00:00+00:00",
        job_config=_job(iac=True, cloud=True, cloud_snapshots={"c1": {}}),
    )
    out = app.invoke(init, config=_thread_config())
    log = out["execution_log"]

    prefix = ["hermes", "tiresias", "argus"]
    suffix = ["convergence_gate", "athena", "circe", "penelope"]
    for i in range(len(prefix) - 1):
        assert log.index(prefix[i]) < log.index(prefix[i + 1])
    gate_i = log.index("convergence_gate")
    assert log.index("argus") < gate_i
    for i in range(len(suffix) - 1):
        assert log.index(suffix[i]) < log.index(suffix[i + 1])
    assert gate_i < log.index("athena")

    assert "laocoon" in log
    assert "cassandra" in log
    assert log.index("laocoon") < gate_i
    assert log.index("cassandra") < gate_i


def test_skip_iac_and_cloud_does_not_block_on_gate() -> None:
    """AC-DG-01-001-02/03: skipped branches still reach convergence and downstream nodes."""

    app = _compile(checkpointer=MemorySaver())
    init = empty_odysseus_state(
        scan_id=str(uuid.uuid4()),
        created_at="2026-04-18T12:00:00+00:00",
        job_config=_job(iac=False, cloud=False),
    )
    out = app.invoke(init, config=_thread_config())
    log = out["execution_log"]

    assert "laocoon_skipped" in log
    assert "cassandra_skipped" in log
    assert "laocoon" not in log
    assert "cassandra" not in log
    assert log.index("convergence_gate") < log.index("penelope")


def test_cloud_layer_without_snapshots_skips_cassandra() -> None:
    """Architecture §4.5: Cassandra dispatches only when cloud snapshots exist."""

    app = _compile(checkpointer=MemorySaver())
    init = empty_odysseus_state(
        scan_id=str(uuid.uuid4()),
        created_at="2026-04-18T12:00:00+00:00",
        job_config=_job(iac=False, cloud=True, cloud_snapshots=None),
    )
    out = app.invoke(init, config=_thread_config())
    log = out["execution_log"]
    assert "cassandra_skipped" in log
    assert "cassandra" not in log


def test_odysseus_memory_checkpoint_resume_no_duplicate_stub_findings() -> None:
    """Interrupt after Argus, resume with same ``thread_id`` — stubs do not double-append."""

    mem = MemorySaver()
    app = _compile(checkpointer=mem, interrupt_after=["argus"])
    cfg = _thread_config()
    init = empty_odysseus_state(
        scan_id=str(uuid.uuid4()),
        created_at="2026-04-18T12:00:00+00:00",
        job_config=_job(iac=True, cloud=True, cloud_snapshots={"c1": {}}),
    )
    mid = app.invoke(init, config=cfg)
    assert mid["execution_log"] == ["hermes", "tiresias", "argus"]
    assert len(mid["stub_findings"]) == 3

    cont = app.invoke(None, config=cfg)
    findings = cont["stub_findings"]
    assert len(findings) == len(set(findings))
    assert findings.count("finding:hermes") == 1
    assert cont["execution_log"][-1] == "penelope"
