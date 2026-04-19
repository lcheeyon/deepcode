"""Phase L10 — Athena structured stub."""

from __future__ import annotations

from deepguard_agents.athena_fake import (
    ComplianceFindingList,
    fake_athena_batch,
    trace_excerpt_for_export,
)


def test_fake_athena_batch_returns_valid_model() -> None:
    out = fake_athena_batch(["C-1", "C-2"])
    assert isinstance(out, ComplianceFindingList)
    assert len(out.findings) == 2
    assert out.findings[0].control_id == "C-1"


def test_trace_excerpt_redacts_sensitive_tokens() -> None:
    s = "prefix AKIAIOSFODNN7EXAMPLE suffix"
    assert "AKIA" not in trace_excerpt_for_export(s)
    assert "[REDACTED]" in trace_excerpt_for_export(s)
