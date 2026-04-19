"""Parsed policy control requirement (Architecture §16.2)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from deepguard_core.models.enums import EvidenceType, ScanLayer


class PolicyControl(BaseModel):
    """Single control requirement produced by Tiresias for Athena."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    control_id: str = Field(min_length=1, max_length=256)
    framework: str = Field(min_length=1, max_length=128)
    title: str = Field(min_length=1, max_length=512)
    description: str = Field(min_length=1)
    scope_tags: list[str] = Field(default_factory=list)
    layer_relevance: list[ScanLayer] = Field(min_length=1)
    severity_weight: float = Field(ge=0.0, le=10.0)
    test_procedures: list[str] = Field(default_factory=list)
    evidence_types: list[EvidenceType] = Field(default_factory=list)
    chinese_title: str | None = Field(default=None, max_length=512)
