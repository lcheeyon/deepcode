"""Phase L9 — Cassandra fixture connector (frozen snapshot)."""

from __future__ import annotations

from pathlib import Path

from deepguard_connectors.fixture import FixtureConnector


def test_load_snapshot_by_ref_json_only() -> None:
    root = Path(__file__).resolve().parents[3] / "eval" / "fixtures" / "cloud"
    conn = FixtureConnector(root)
    snap = conn.load_snapshot("resource_snapshot_min")
    assert snap["schema"] == "deepguard.resource_snapshot/v1"
    assert snap["resources"][0]["type"] == "aws_s3_bucket"
