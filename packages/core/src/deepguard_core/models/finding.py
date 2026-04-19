"""Compliance finding row shape (Architecture §29.1 ``findings`` table, API list)."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from deepguard_core.models.enums import FindingAssessmentStatus, FindingSeverity


class Finding(BaseModel):
    """Finding returned by ``GET /v1/scans/{id}/findings`` and stored in Postgres."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: UUID | None = None
    tenant_id: UUID | None = None
    scan_id: UUID
    framework: str = Field(min_length=1)
    control_id: str = Field(min_length=1)
    status: FindingAssessmentStatus
    severity: FindingSeverity
    title: str = Field(min_length=1, max_length=512)
    evidence_refs: list[dict[str, Any]] = Field(default_factory=list)
    reasoning_summary: str | None = Field(default=None, max_length=16_384)
    confidence_score: float = Field(ge=0.0, le=1.0)
    policy_version: str = Field(min_length=1, max_length=128)
