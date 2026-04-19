"""Redis Streams queue contract (Architecture §30.1–30.2)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# Normative stream names (§30.1)
SCAN_STREAM_KEY = "stream:scans"
SCAN_CONSUMER_GROUP = "workers"


def scan_timeline_pubsub_channel(*, scan_id: UUID) -> str:
    """Redis channel for SSE fan-out after each ``scan_run_events`` insert."""

    return f"deepguard:scan:{scan_id}:timeline"


class ScanJobMessage(BaseModel):
    """Payload carried on ``stream:scans`` entries."""

    model_config = ConfigDict(extra="forbid")

    schema_ver: str = Field(default="1.0", max_length=16)
    scan_id: UUID
    tenant_id: UUID
    enqueued_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    priority: int = Field(default=0, ge=0, le=100)

    def to_stream_fields(self) -> dict[str, str]:
        """Flat string map for ``XADD``."""

        return {
            "schema_ver": self.schema_ver,
            "scan_id": str(self.scan_id),
            "tenant_id": str(self.tenant_id),
            "enqueued_at": self.enqueued_at.isoformat(),
            "priority": str(self.priority),
        }

    @classmethod
    def from_stream_fields(cls, fields: dict[str, str]) -> ScanJobMessage:
        return cls.model_validate(
            {
                "schema_ver": fields.get("schema_ver", "1.0"),
                "scan_id": fields["scan_id"],
                "tenant_id": fields["tenant_id"],
                "enqueued_at": fields["enqueued_at"],
                "priority": int(fields.get("priority", "0")),
            }
        )
