"""Stub nodes — pass-through state updates (Phase L5; no real agents)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from deepguard_observability.tracing import graph_node_span

from deepguard_graph.state import OdysseusState


def _step(name: str) -> dict[str, Any]:
    fid = f"finding:{name}"
    return {"execution_log": [name], "stub_findings": [fid]}


def _tenant_scan(state: OdysseusState) -> tuple[str, str]:
    return (state.get("scan_id") or "", state.get("tenant_id") or "")


def stub_hermes(state: OdysseusState) -> dict[str, Any]:
    sid, tid = _tenant_scan(state)
    with graph_node_span("hermes", scan_id=sid, tenant_id=tid):
        return _step("hermes")


def stub_tiresias(state: OdysseusState) -> dict[str, Any]:
    sid, tid = _tenant_scan(state)
    with graph_node_span("tiresias", scan_id=sid, tenant_id=tid):
        return _step("tiresias")


def stub_argus(state: OdysseusState) -> dict[str, Any]:
    sid, tid = _tenant_scan(state)
    with graph_node_span("argus", scan_id=sid, tenant_id=tid):
        return _step("argus")


def stub_laocoon(state: OdysseusState) -> dict[str, Any]:
    sid, tid = _tenant_scan(state)
    with graph_node_span("laocoon", scan_id=sid, tenant_id=tid):
        return _step("laocoon")


def stub_laocoon_skipped(state: OdysseusState) -> dict[str, Any]:
    sid, tid = _tenant_scan(state)
    with graph_node_span("laocoon_skipped", scan_id=sid, tenant_id=tid):
        return _step("laocoon_skipped")


def stub_cassandra(state: OdysseusState) -> dict[str, Any]:
    sid, tid = _tenant_scan(state)
    with graph_node_span("cassandra", scan_id=sid, tenant_id=tid):
        return _step("cassandra")


def stub_cassandra_skipped(state: OdysseusState) -> dict[str, Any]:
    sid, tid = _tenant_scan(state)
    with graph_node_span("cassandra_skipped", scan_id=sid, tenant_id=tid):
        return _step("cassandra_skipped")


def stub_convergence_gate(state: OdysseusState) -> dict[str, Any]:
    sid, tid = _tenant_scan(state)
    with graph_node_span("convergence_gate", scan_id=sid, tenant_id=tid):
        return _step("convergence_gate")


def stub_athena(state: OdysseusState) -> dict[str, Any]:
    sid, tid = _tenant_scan(state)
    with graph_node_span("athena", scan_id=sid, tenant_id=tid):
        return _step("athena")


def stub_circe(state: OdysseusState) -> dict[str, Any]:
    sid, tid = _tenant_scan(state)
    with graph_node_span("circe", scan_id=sid, tenant_id=tid):
        return _step("circe")


def stub_penelope(state: OdysseusState) -> dict[str, Any]:
    sid, tid = _tenant_scan(state)
    with graph_node_span("penelope", scan_id=sid, tenant_id=tid):
        return _step("penelope")


def stub_parallel_code_shard(slot: str) -> Callable[[OdysseusState], dict[str, Any]]:
    """Return a mapper node that records ``map_shard_label`` (parallel ``Send`` targets)."""

    node_id = f"parallel_code_{slot}"

    def _run(state: OdysseusState) -> dict[str, Any]:
        sid, tid = _tenant_scan(state)
        label = (state.get("map_shard_label") or "").strip() or f"shard_{slot}"
        with graph_node_span(node_id, scan_id=sid, tenant_id=tid):
            return _step(f"code_shard:{slot}:{label}")

    return _run
