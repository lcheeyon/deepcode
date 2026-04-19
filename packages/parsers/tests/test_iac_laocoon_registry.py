"""Phase L9 — IaC parser registry (Laocoon)."""

from __future__ import annotations

from pathlib import Path

from deepguard_parsers.iac.registry import IaC_PARSERS, parse_iac_file


def test_tf_parser_registered() -> None:
    assert ".tf" in IaC_PARSERS


def test_parse_minimal_tf_fixture() -> None:
    p = Path(__file__).resolve().parents[3] / "eval" / "fixtures" / "iac" / "minimal.tf"
    rows = parse_iac_file(p)
    assert rows and rows[0]["rule"] == "STUB_TF_SCAN"
