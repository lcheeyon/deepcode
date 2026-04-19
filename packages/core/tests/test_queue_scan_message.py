"""Phase L4 — ``ScanJobMessage`` Redis field map (Architecture §30)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from deepguard_core.queue import ScanJobMessage


def test_scan_job_message_roundtrip_stream_fields() -> None:
    sid = UUID("00000000-0000-4000-8000-000000000002")
    tid = UUID("00000000-0000-4000-8000-000000000001")
    when = datetime(2026, 4, 18, 12, 0, tzinfo=UTC)
    original = ScanJobMessage(
        schema_ver="1.0",
        scan_id=sid,
        tenant_id=tid,
        enqueued_at=when,
        priority=7,
    )
    fields = original.to_stream_fields()
    parsed = ScanJobMessage.from_stream_fields(fields)
    assert parsed.scan_id == sid
    assert parsed.tenant_id == tid
    assert parsed.enqueued_at == when
    assert parsed.priority == 7
    assert parsed.schema_ver == "1.0"
