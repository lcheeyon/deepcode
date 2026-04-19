"""Agent-scoped error entries appended to ``ScanState.error_log`` (Architecture §31.4)."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

from deepguard_core.models.enums import AgentErrorSeverity


def _utc_now() -> datetime:
    return datetime.now(UTC)


class AgentError(BaseModel):
    """Structured failure from an Odysseus graph node or tool."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    agent: str = Field(
        min_length=1,
        max_length=64,
        description="Logical agent id (e.g. athena, hermes).",
    )
    code: str = Field(min_length=1, max_length=128, description="Stable machine error code.")
    message: str = Field(
        min_length=1,
        max_length=8192,
        description="Sanitised human-readable detail.",
    )
    severity: AgentErrorSeverity = AgentErrorSeverity.RECOVERABLE
    occurred_at: datetime = Field(default_factory=_utc_now)


class AgentRuntimeError(Exception):
    """Wraps ``AgentError`` for ``raise`` / ``except`` (Pydantic models are not exceptions)."""

    def __init__(self, record: AgentError) -> None:
        self.record = record
        super().__init__(record.message)
