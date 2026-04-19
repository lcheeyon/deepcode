"""Athena structured batch stub (Phase L10; ``LLM_MODE=fake`` direction)."""

from __future__ import annotations

from deepguard_core.models.enums import FindingAssessmentStatus, FindingSeverity
from pydantic import BaseModel, ConfigDict, Field


class ComplianceFindingItem(BaseModel):
    """One batched mapping outcome (Architecture §31.3 batching direction)."""

    model_config = ConfigDict(extra="forbid")

    control_id: str = Field(min_length=1, max_length=256)
    status: FindingAssessmentStatus
    severity: FindingSeverity
    title: str = Field(min_length=1, max_length=512)
    confidence: float = Field(ge=0.0, le=1.0)


class ComplianceFindingList(BaseModel):
    """Structured output envelope for Athena."""

    model_config = ConfigDict(extra="forbid")

    findings: list[ComplianceFindingItem] = Field(default_factory=list)


def fake_athena_batch(control_ids: list[str]) -> ComplianceFindingList:
    """Deterministic stub — no network; safe for CI (no secrets in output)."""

    out: list[ComplianceFindingItem] = []
    for cid in control_ids:
        out.append(
            ComplianceFindingItem(
                control_id=cid,
                status=FindingAssessmentStatus.PARTIAL,
                severity=FindingSeverity.MEDIUM,
                title=f"Stub assessment for {cid}",
                confidence=0.75,
            )
        )
    return ComplianceFindingList(findings=out)


def trace_excerpt_for_export(summary: str) -> str:
    """Strip patterns that must never leave the tenant boundary (L10 redaction hook)."""

    redacted = summary
    for token in ("AKIA", "sk-", "BEGIN RSA PRIVATE KEY"):
        if token in redacted:
            redacted = redacted.replace(token, "[REDACTED]")
    return redacted
