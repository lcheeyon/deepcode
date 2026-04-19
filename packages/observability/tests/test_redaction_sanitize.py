"""Sink-safe metadata shaping (§8.2)."""

from __future__ import annotations

from deepguard_observability.redaction import redact_secrets, sanitize_trace_metadata_value


def test_sanitize_trace_metadata_value_truncates_long_strings() -> None:
    huge = "x" * 10_000
    out = sanitize_trace_metadata_value(huge, max_bytes=64)
    assert isinstance(out, str)
    assert len(out.encode("utf-8")) <= 64


def test_redact_secrets_still_masks_tokens() -> None:
    m = redact_secrets({"scan_id": "s", "api_key": "secret", "nested": {"ok": "y" * 5000}})
    assert m["api_key"] == "[REDACTED]"
    assert m["scan_id"] == "s"
