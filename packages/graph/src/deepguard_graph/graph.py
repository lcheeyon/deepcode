"""Odysseus ``StateGraph`` builder (Architecture §4.1, §4.5; Phase L5)."""

from __future__ import annotations

from typing import Any, cast

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

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


def fan_out_after_argus(state: OdysseusState) -> list[Send]:
    """Parallel Laocoon + Cassandra with deterministic skips (AC-DG-01-001-02/03).

    IaC runs when ``scan_layers.iac``. Cloud runs when ``scan_layers.cloud`` and
    ``cloud_snapshots`` is non-empty (Architecture §4.5), else a skip node runs so the
    convergence gate never blocks on an empty cloud branch.
    """

    layers = _scan_layers(state)
    snaps = state.get("job_config", {}).get("cloud_snapshots") or {}
    cloud_ready = bool(layers["cloud"] and snaps)

    sends: list[Send] = []
    if layers["iac"]:
        sends.append(Send("laocoon", state))
    else:
        sends.append(Send("laocoon_skipped", state))
    if cloud_ready:
        sends.append(Send("cassandra", state))
    else:
        sends.append(Send("cassandra_skipped", state))
    return sends


def build_odysseus_graph() -> StateGraph[Any]:
    """Compile-ready graph: Hermes → … → Penelope (stub nodes only)."""

    g = StateGraph(OdysseusState)

    g.add_node("hermes", cast(Any, stub_hermes))
    g.add_node("tiresias", cast(Any, stub_tiresias))
    g.add_node("argus", cast(Any, stub_argus))
    g.add_node("laocoon", cast(Any, stub_laocoon))
    g.add_node("laocoon_skipped", cast(Any, stub_laocoon_skipped))
    g.add_node("cassandra", cast(Any, stub_cassandra))
    g.add_node("cassandra_skipped", cast(Any, stub_cassandra_skipped))
    g.add_node("convergence_gate", cast(Any, stub_convergence_gate))
    g.add_node("athena", cast(Any, stub_athena))
    g.add_node("circe", cast(Any, stub_circe))
    g.add_node("penelope", cast(Any, stub_penelope))

    g.add_edge(START, "hermes")
    g.add_edge("hermes", "tiresias")
    g.add_edge("tiresias", "argus")

    fan_targets = ["laocoon", "laocoon_skipped", "cassandra", "cassandra_skipped"]
    g.add_conditional_edges("argus", cast(Any, fan_out_after_argus), fan_targets)

    for n in fan_targets:
        g.add_edge(n, "convergence_gate")

    g.add_edge("convergence_gate", "athena")
    g.add_edge("athena", "circe")
    g.add_edge("circe", "penelope")
    g.add_edge("penelope", END)

    return g
