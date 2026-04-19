"""Phase L5 — Odysseus stub graph order, skips, checkpoint resume (Architecture §4 + §7.1)."""

from __future__ import annotations

import uuid
from typing import Any, cast

from deepguard_graph.compilation import compile_odysseus_app, resume_odysseus_after_interrupt
from deepguard_graph.graph import build_odysseus_graph
from deepguard_graph.state import empty_odysseus_state
from deepguard_graph.stub_nodes import stub_argus as stub_argus_impl
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver


def _job(
    *,
    iac: bool,
    cloud: bool,
    cloud_snapshots: dict | None = None,
    langgraph: dict | None = None,
) -> dict:
    d: dict = {
        "repo": {"url": "https://github.com/acme/svc", "ref": "main"},
        "policy_ids": ["ISO-27001-2022"],
        "scan_layers": {"code": True, "iac": iac, "cloud": cloud},
    }
    if cloud_snapshots is not None:
        d["cloud_snapshots"] = cloud_snapshots
    if langgraph is not None:
        d["langgraph"] = langgraph
    return d


def _compile(**compile_kwargs: Any):
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
    """Interrupt after ingestion; resume on same ``thread_id`` without duplicate stub findings."""

    mem = MemorySaver()
    app = _compile(checkpointer=mem, interrupt_after=["ingestion"])
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


def test_code_analysis_shard_keys_add_parallel_code_mappers() -> None:
    """§7.1 map-reduce: optional ``Send`` targets ``parallel_code_*`` with shard labels."""

    app = _compile(checkpointer=MemorySaver())
    init = empty_odysseus_state(
        scan_id=str(uuid.uuid4()),
        created_at="2026-04-18T12:00:00+00:00",
        job_config=_job(
            iac=False,
            cloud=False,
            langgraph={"code_analysis_shard_keys": ["svc/a", "svc/b"]},
        ),
    )
    out = app.invoke(init, config=_thread_config())
    log = out["execution_log"]
    assert "code_shard:0:svc/a" in log
    assert "code_shard:1:svc/b" in log


def test_argus_retry_recovers_from_transient_error() -> None:
    """§7.1 retry policy on Argus — transient ``ConnectionError`` then success."""

    calls = {"n": 0}

    def flaky_argus(state: Any) -> dict[str, Any]:
        calls["n"] += 1
        if calls["n"] < 2:
            raise ConnectionError("transient")
        return stub_argus_impl(state)

    app = compile_odysseus_app(checkpointer=MemorySaver(), argus_node=flaky_argus)
    init = empty_odysseus_state(
        scan_id=str(uuid.uuid4()),
        created_at="2026-04-18T12:00:00+00:00",
        job_config=_job(iac=False, cloud=False),
    )
    out = app.invoke(init, config=_thread_config())
    assert calls["n"] == 2
    assert "argus" in out["execution_log"]


def test_hitl_interrupt_before_athena_then_resume() -> None:
    """§7.1 HITL — pause before Athena, then resume to Penelope on same checkpoint thread."""

    mem = MemorySaver()
    tid = str(uuid.uuid4())
    cfg = cast(RunnableConfig, {"configurable": {"thread_id": tid}})
    app = compile_odysseus_app(checkpointer=mem, interrupt_before_athena=True)
    init = empty_odysseus_state(
        scan_id=tid,
        created_at="2026-04-18T12:00:00+00:00",
        job_config=_job(iac=False, cloud=False),
    )
    mid = app.invoke(init, config=cfg)
    assert "athena" not in mid["execution_log"]
    assert mid["execution_log"][-1] == "convergence_gate"

    end = resume_odysseus_after_interrupt(checkpointer=mem, scan_id=tid, tenant_id="")
    assert end["execution_log"][-1] == "penelope"
    assert end["execution_log"].count("convergence_gate") == 1
