"""Partial graph state slice carried on LangGraph merges (Architecture §4.2)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from deepguard_core.models.agent_error import AgentError
from deepguard_core.models.create_scan import ScanJobConfig


class ScanStatePartial(BaseModel):
    """Minimum typed slice for ``scan_id`` + ``job_config`` + control flags.

    Full ``ScanState`` in Architecture is a TypedDict spanning all agents; L2
    freezes the job metadata and error channel so workers/API can construct
    initial state without importing LangGraph.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    scan_id: UUID
    created_at: datetime
    job_config: ScanJobConfig
    error_log: list[AgentError] = Field(default_factory=list)
    should_abort: bool = False
