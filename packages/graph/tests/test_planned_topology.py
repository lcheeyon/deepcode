"""Planned Odysseus node list mirrors graph fan-out rules."""

from __future__ import annotations

from deepguard_graph import odysseus_planned_graph_nodes


def test_default_job_config_planned_nodes() -> None:
    planned = odysseus_planned_graph_nodes(job_config={})
    assert planned[0] == "ingestion"
    assert "laocoon_skipped" in planned
    assert "cassandra_skipped" in planned
    assert planned[-1] == "penelope"


def test_iac_layer_selects_laocoon() -> None:
    planned = odysseus_planned_graph_nodes(
        job_config={"scan_layers": {"code": True, "iac": True, "cloud": False}}
    )
    assert "laocoon" in planned
    assert "laocoon_skipped" not in planned
