"""Stub nodes — pass-through state updates (Phase L5; no real agents)."""

from __future__ import annotations

from typing import Any

from deepguard_graph.state import OdysseusState


def _step(name: str) -> dict[str, Any]:
    fid = f"finding:{name}"
    return {"execution_log": [name], "stub_findings": [fid]}


def stub_hermes(_state: OdysseusState) -> dict[str, Any]:
    return _step("hermes")


def stub_tiresias(_state: OdysseusState) -> dict[str, Any]:
    return _step("tiresias")


def stub_argus(_state: OdysseusState) -> dict[str, Any]:
    return _step("argus")


def stub_laocoon(_state: OdysseusState) -> dict[str, Any]:
    return _step("laocoon")


def stub_laocoon_skipped(_state: OdysseusState) -> dict[str, Any]:
    return _step("laocoon_skipped")


def stub_cassandra(_state: OdysseusState) -> dict[str, Any]:
    return _step("cassandra")


def stub_cassandra_skipped(_state: OdysseusState) -> dict[str, Any]:
    return _step("cassandra_skipped")


def stub_convergence_gate(_state: OdysseusState) -> dict[str, Any]:
    return _step("convergence_gate")


def stub_athena(_state: OdysseusState) -> dict[str, Any]:
    return _step("athena")


def stub_circe(_state: OdysseusState) -> dict[str, Any]:
    return _step("circe")


def stub_penelope(_state: OdysseusState) -> dict[str, Any]:
    return _step("penelope")
