"""Circe remediation record (Architecture §18; diff-only, never auto-apply)."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Remediation(BaseModel):
    """Suggested fix with diff preview only — operators apply changes out-of-band."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: UUID
    scan_id: UUID
    finding_id: UUID | None = None
    title: str = Field(min_length=1, max_length=512)
    diff_preview: str = Field(
        min_length=1,
        description="Unified diff or patch text; never auto-applied by DeepGuard.",
    )
    terraform_validate_exit_code: int | None = Field(
        default=None,
        description="Optional sandbox ``terraform validate`` result (best-effort).",
    )
