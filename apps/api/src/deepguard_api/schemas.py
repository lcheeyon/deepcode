"""HTTP response models (OpenAPI)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ScanResponse(BaseModel):
    """Public scan resource returned by ``GET /v1/scans/{scan_id}``."""

    model_config = ConfigDict(extra="forbid")

    scan_id: UUID = Field(description="Primary key of the scan row.")
    tenant_id: UUID
    status: str
    current_stage: str
    percent_complete: int = Field(ge=0, le=100)
    job_config: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    idempotency_key: str | None = None
    repo_commit_sha: str | None = None
    cancellation_requested: bool = False


class ScanCancelResponse(BaseModel):
    """Accepted cancellation request (Architecture §30.4)."""

    model_config = ConfigDict(extra="forbid")

    scan_id: UUID
    cancellation_requested: bool = True
