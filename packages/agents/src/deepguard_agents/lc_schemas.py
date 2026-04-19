"""Typed IO for LangChain agent runnables (Architecture §7.2)."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AthenaAgentInput(BaseModel):
    """Explicit Athena / policy-mapping input for ``Runnable`` composition and tests."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    scan_id: UUID
    tenant_id: UUID
    framework: str = Field(min_length=1, max_length=256)
    policy_version: str = Field(min_length=1, max_length=128)
    control_ids: list[str] = Field(min_length=1)
    policy_excerpt: str = Field(
        default="",
        max_length=65_536,
        description="Policy text slice for retrieval / RAG (cacheable key input).",
    )


class CirceAgentInput(BaseModel):
    """Explicit Circe remediation input."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    scan_id: UUID
    finding_id: UUID | None = None
    finding_title: str = Field(min_length=1, max_length=512)
    code_context: str = Field(default="", max_length=65_536)


class CirceRemediationDraft(BaseModel):
    """Structured LLM output for Circe before persisting a ``Remediation`` row."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=512)
    diff_preview: str = Field(min_length=1, max_length=65_536)
    finding_id: UUID | None = None
