"""Odysseus ``StateGraph`` builder (Architecture §4.1, §4.5; Phase L5 + §7.1 LangGraph)."""

from __future__ import annotations

from typing import Any, cast

from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy, Send

from deepguard_graph.state import OdysseusState
from deepguard_graph.stub_nodes import (
    stub_argus,
    stub_athena,
    stub_cassandra,
    stub_cassandra_skipped,
    stub_circe,
    stub_convergence_gate,
    stub_hermes,
    stub_laocoon,
    stub_laocoon_skipped,
    stub_parallel_code_shard,
    stub_penelope,
    stub_tiresias,
)


def _scan_layers(state: OdysseusState) -> dict[str, bool]:
    jc = state.get("job_config") or {}
    raw = jc.get("scan_layers") or {}
    return {
        "code": bool(raw.get("code")),
        "iac": bool(raw.get("iac")),
        "cloud": bool(raw.get("cloud")),
    }


def _code_analysis_shard_keys(state: OdysseusState) -> list[str]:
    jc = state.get("job_config") or {}
    raw = jc.get("langgraph")
    if not isinstance(raw, dict):
        return []
    keys = raw.get("code_analysis_shard_keys")
    if not isinstance(keys, list):
        return []
    out = [str(k).strip() for k in keys if str(k).strip()]
    return out[:2]


def fan_out_after_argus(state: OdysseusState) -> list[Send]:
    """Parallel Laocoon + Cassandra + optional code shards (§7.1 ``Send`` / map-reduce).

    IaC runs when ``scan_layers.iac``. Cloud runs when ``scan_layers.cloud`` and
    ``cloud_snapshots`` is non-empty (Architecture §4.5), else a skip node runs so the
    convergence gate never blocks on an empty cloud branch.

    When ``job_config.langgraph.code_analysis_shard_keys`` is non-empty, emit up to two
    additional ``Send`` targets (``parallel_code_0`` / ``parallel_code_1``) with
    ``map_shard_label`` set for mapper stubs.
    """

    layers = _scan_layers(state)
    snaps = state.get("job_config", {}).get("cloud_snapshots") or {}
    cloud_ready = bool(layers["cloud"] and snaps)
    shard_keys = _code_analysis_shard_keys(state)

    sends: list[Send] = []
    if layers["iac"]:
        sends.append(Send("laocoon", state))
    else:
        sends.append(Send("laocoon_skipped", state))
    if cloud_ready:
        sends.append(Send("cassandra", state))
    else:
        sends.append(Send("cassandra_skipped", state))
    for i, label in enumerate(shard_keys):
        if i > 1:
            break
        slot = str(i)
        sends.append(Send(f"parallel_code_{slot}", {**state, "map_shard_label": label}))
    return sends


def _build_ingestion_subgraph(argus_node: Any) -> StateGraph[OdysseusState]:
    """Hermes → Tiresias → Argus as a compiled subgraph (§7.1)."""

    sub = StateGraph(OdysseusState)
    sub.add_node("hermes", cast(Any, stub_hermes))
    sub.add_node("tiresias", cast(Any, stub_tiresias))
    sub.add_node(
        "argus",
        cast(Any, argus_node),
        retry_policy=RetryPolicy(
            max_attempts=5,
            initial_interval=0.05,
            max_interval=2.0,
        ),
    )
    sub.add_edge(START, "hermes")
    sub.add_edge("hermes", "tiresias")
    sub.add_edge("tiresias", "argus")
    sub.add_edge("argus", END)
    return sub


def build_odysseus_graph(*, argus_node: Any | None = None) -> StateGraph[Any]:
    """Compile-ready graph: ingestion subgraph → parallel analysis → remediation (stub nodes)."""

    argus = stub_argus if argus_node is None else argus_node
    ingestion = _build_ingestion_subgraph(argus).compile()

    g = StateGraph(OdysseusState)

    g.add_node("ingestion", ingestion)
    g.add_node("laocoon", cast(Any, stub_laocoon))
    g.add_node("laocoon_skipped", cast(Any, stub_laocoon_skipped))
    g.add_node("cassandra", cast(Any, stub_cassandra))
    g.add_node("cassandra_skipped", cast(Any, stub_cassandra_skipped))
    g.add_node("parallel_code_0", cast(Any, stub_parallel_code_shard("0")))
    g.add_node("parallel_code_1", cast(Any, stub_parallel_code_shard("1")))
    g.add_node("convergence_gate", cast(Any, stub_convergence_gate))
    g.add_node("athena", cast(Any, stub_athena))
    g.add_node("circe", cast(Any, stub_circe))
    g.add_node("penelope", cast(Any, stub_penelope))

    g.add_edge(START, "ingestion")
    fan_targets = [
        "laocoon",
        "laocoon_skipped",
        "cassandra",
        "cassandra_skipped",
        "parallel_code_0",
        "parallel_code_1",
    ]
    g.add_conditional_edges("ingestion", cast(Any, fan_out_after_argus), fan_targets)

    for n in fan_targets:
        g.add_edge(n, "convergence_gate")

    g.add_edge("convergence_gate", "athena")
    g.add_edge("athena", "circe")
    g.add_edge("circe", "penelope")
    g.add_edge("penelope", END)

    return g
