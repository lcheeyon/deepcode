"""Planned Odysseus graph nodes for UI checklists (dynamic fan-out vs architecture §4.5)."""

from __future__ import annotations

from typing import Any


def _scan_layers(job_config: dict[str, Any] | None) -> dict[str, bool]:
    jc = job_config or {}
    raw = jc.get("scan_layers") or {}
    if not isinstance(raw, dict):
        return {"code": False, "iac": False, "cloud": False}
    return {
        "code": bool(raw.get("code")),
        "iac": bool(raw.get("iac")),
        "cloud": bool(raw.get("cloud")),
    }


def _code_analysis_shard_keys(job_config: dict[str, Any] | None) -> list[str]:
    jc = job_config or {}
    raw = jc.get("langgraph")
    if not isinstance(raw, dict):
        return []
    keys = raw.get("code_analysis_shard_keys")
    if not isinstance(keys, list):
        return []
    return [str(k).strip() for k in keys if str(k).strip()][:2]


def odysseus_planned_graph_nodes(*, job_config: dict[str, Any] | None) -> list[str]:
    """Return ordered top-level graph node ids expected for this ``job_config``."""

    jc = job_config or {}
    layers = _scan_layers(jc)
    snaps = (jc.get("cloud_snapshots") or {}) if isinstance(jc, dict) else {}
    cloud_ready = bool(layers["cloud"] and snaps)
    shard_keys = _code_analysis_shard_keys(jc)

    out: list[str] = ["ingestion"]
    out.append("laocoon" if layers["iac"] else "laocoon_skipped")
    out.append("cassandra" if cloud_ready else "cassandra_skipped")
    for i, _label in enumerate(shard_keys):
        if i > 1:
            break
        out.append(f"parallel_code_{i}")
    out.extend(["convergence_gate", "athena", "circe", "penelope"])
    return out
