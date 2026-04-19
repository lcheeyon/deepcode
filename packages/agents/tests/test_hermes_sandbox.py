"""Phase L6 — Hermes sandbox + staging."""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest
from deepguard_agents.hermes import HermesAgent, safe_read_bytes
from deepguard_core.models.agent_error import AgentRuntimeError


def test_safe_read_rejects_path_traversal(tmp_path: Path) -> None:
    inner = tmp_path / "repo" / "x.txt"
    inner.parent.mkdir(parents=True)
    inner.write_text("ok", encoding="utf-8")
    with pytest.raises(AgentRuntimeError) as ei:
        safe_read_bytes(tmp_path / "repo", "../../../etc/passwd")
    assert ei.value.record.code == "SANDBOX_PATH_ESCAPE"


def test_hermes_stages_fixture_and_returns_artifact_ref_not_raw_archive(tmp_path: Path) -> None:
    src = Path(__file__).resolve().parents[3] / "eval" / "fixtures" / "repos" / "tiny"
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()
    agent = HermesAgent(sandbox_root=sandbox, repo_max_bytes=1_000_000)
    sid = str(uuid.uuid4())
    result = agent.stage_fixture_copy(src, scan_id=sid)
    assert Path(result.repo_local_path).is_dir()
    assert result.repo_metadata["bytes_total"] > 0
    assert result.archive_artifact.store == "local"
    assert result.archive_artifact.key == f"{sid}/repo.tgz"
    body = safe_read_bytes(Path(result.repo_local_path), "README.md")
    assert b"fixture" in body.lower()
