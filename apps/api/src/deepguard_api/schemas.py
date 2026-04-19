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
    report_artifact_id: UUID | None = Field(
        default=None,
        description="Latest ``report_pdf`` artifact for this scan when present.",
    )


class ScanCancelResponse(BaseModel):
    """Accepted cancellation request (Architecture §30.4)."""

    model_config = ConfigDict(extra="forbid")

    scan_id: UUID
    cancellation_requested: bool = True


class FindingListItem(BaseModel):
    """Single row for findings triage (US-DG-12-004)."""

    model_config = ConfigDict(extra="forbid")

    finding_id: UUID
    framework: str
    control_id: str
    status: str
    severity: str
    title: str
    evidence_refs: list[dict[str, Any]] = Field(default_factory=list)
    reasoning_summary: str | None = None
    confidence_score: float = Field(ge=0.0, le=1.0)
    policy_version: str
    created_at: datetime


class FindingsPage(BaseModel):
    """Cursor-paginated findings list."""

    model_config = ConfigDict(extra="forbid")

    items: list[FindingListItem]
    next_cursor: str | None = None


class ArtifactSummary(BaseModel):
    """Report or other scan artifact metadata (US-DG-12-005)."""

    model_config = ConfigDict(extra="forbid")

    artifact_id: UUID
    kind: str
    checksum_sha256: str
    size_bytes: int = Field(ge=0)
    storage_uri: str
    created_at: datetime


class ArtifactsListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifacts: list[ArtifactSummary]


class PolicyUploadWarning(BaseModel):
    model_config = ConfigDict(extra="forbid")

    detail: str


class PolicyUploadResponse(BaseModel):
    """Parse summary after ``POST /v1/policies:upload`` (US-DG-12-006)."""

    model_config = ConfigDict(extra="forbid")

    upload_id: UUID
    policy_version: str
    controls_extracted: int = Field(ge=0)
    warnings: list[PolicyUploadWarning] = Field(default_factory=list)
    source_filename: str


class PolicyUploadListItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    upload_id: UUID
    policy_version: str
    source_filename: str
    controls_extracted: int
    warnings: list[PolicyUploadWarning] = Field(default_factory=list)
    created_at: datetime


class PolicyUploadListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    uploads: list[PolicyUploadListItem]


class ScanWorkflowChecklistItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    node: str
    state: str = Field(description="pending | completed | failed | skipped | running")


class ScanWorkflowHandoffItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    from_agent: str
    to_agent: str
    message_type: str
    summary: str | None = None
    at: datetime


class ScanWorkflowEventItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID
    event_seq: int
    event_type: str
    node: str | None
    correlation_id: str | None
    graph_version: str | None
    created_at: datetime
    payload: dict[str, Any]


class TraceLinkItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vendor: str
    url: str | None = None
    reason: str | None = None
    root_run_id: str | None = None
    trace_id: str | None = None
    project_id: str | None = None
    workspace_id: str | None = None


class ScanWorkflowResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scan_id: UUID
    tenant_id: UUID
    status: str
    current_stage: str
    percent_complete: int
    correlation_id: str | None = None
    graph_version: str | None = None
    planned_nodes: list[str]
    checklist: list[ScanWorkflowChecklistItem]
    handoffs: list[ScanWorkflowHandoffItem]
    events: list[ScanWorkflowEventItem] = Field(default_factory=list)
    trace_links: list[TraceLinkItem] = Field(default_factory=list)
    summary_counts: dict[str, Any] = Field(default_factory=dict)


class TraceLinksResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scan_id: UUID
    links: list[TraceLinkItem]
