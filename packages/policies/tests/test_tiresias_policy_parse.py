"""Phase L7 — Tiresias policy fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from deepguard_core.models.agent_error import AgentRuntimeError
from deepguard_policies.cache_keys import tiresias_cache_key
from deepguard_policies.parse import parse_policy_file
from deepguard_policies.registry import POLICY_PARSER_EXTENSIONS


def _fx(name: str) -> Path:
    return Path(__file__).resolve().parent / "fixtures" / name


def test_parse_two_framework_fixtures() -> None:
    r1 = parse_policy_file(_fx("owasp_subset.yaml"))
    r2 = parse_policy_file(_fx("iso_synthetic.yaml"))
    assert r1.controls[0].framework == "OWASP_ASVS"
    assert r2.controls[0].framework == "ISO_27001_SYNTHETIC"
    assert {r1.policy_version, r2.policy_version} <= {"4.0.3", "2022-demo"}


def test_invalid_policy_raises_agent_error(tmp_path: Path) -> None:
    p = tmp_path / "bad.yaml"
    p.write_text("not: [broken", encoding="utf-8")
    with pytest.raises(AgentRuntimeError) as ei:
        parse_policy_file(p)
    assert "POLICY" in ei.value.record.code or "YAML" in ei.value.record.code


def test_policy_root_not_mapping_raises(tmp_path: Path) -> None:
    p = tmp_path / "scalar.yaml"
    p.write_text("- item", encoding="utf-8")
    with pytest.raises(AgentRuntimeError) as ei:
        parse_policy_file(p)
    assert ei.value.record.code == "POLICY_ROOT_NOT_OBJECT"


def test_policy_missing_framework_raises(tmp_path: Path) -> None:
    p = tmp_path / "empty_fw.yaml"
    p.write_text(
        "version: '1'\ncontrols:\n  - control_id: X\n    title: T\n",
        encoding="utf-8",
    )
    with pytest.raises(AgentRuntimeError) as ei:
        parse_policy_file(p)
    assert ei.value.record.code == "POLICY_MISSING_FIELDS"


def test_evidence_types_skip_unknown_enum_values(tmp_path: Path) -> None:
    p = tmp_path / "mixed_evidence.yaml"
    p.write_text(
        "framework: F\nversion: '1'\ncontrols:\n"
        "  - control_id: C1\n    title: T\n"
        "    evidence_types: [NOT_A_REAL_EVIDENCE_TYPE, file_reference]\n",
        encoding="utf-8",
    )
    r = parse_policy_file(p)
    assert r.controls[0].evidence_types  # file_reference retained; unknown skipped


def test_tiresias_cache_key_stable() -> None:
    b = b"hello"
    k1 = tiresias_cache_key(framework="OWASP", source_bytes=b)
    k2 = tiresias_cache_key(framework="OWASP", source_bytes=b)
    assert k1 == k2
    assert k1.startswith("tiresias:policy:owasp:")


def test_yaml_registered_in_policy_parser_extensions() -> None:
    assert ".yaml" in POLICY_PARSER_EXTENSIONS
