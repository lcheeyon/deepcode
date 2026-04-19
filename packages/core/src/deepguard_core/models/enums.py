"""Domain StrEnums (Architecture §4.2, §16.2, §28.5)."""

from __future__ import annotations

from enum import StrEnum


class ScanLayer(StrEnum):
    """Which platform layers a control or scan touches."""

    CODE = "CODE"
    IAC = "IAC"
    CLOUD = "CLOUD"


class EvidenceType(StrEnum):
    """Kinds of evidence cited against a control (Architecture §16.2)."""

    FILE_REFERENCE = "file_reference"
    CONFIG_SNIPPET = "config_snippet"
    CLOUD_RESOURCE = "cloud_resource"
    POLICY_EXCERPT = "policy_excerpt"
    DEPENDENCY_GRAPH = "dependency_graph"
    OTHER = "other"


class CloudProvider(StrEnum):
    """Supported read-only cloud connector families (Architecture §15)."""

    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ALIBABA = "alibaba"
    TENCENT = "tencent"
    HUAWEI = "huawei"


class ScanLifecycleStatus(StrEnum):
    """Row-level scan status (Architecture §28.5)."""

    PENDING = "PENDING"
    QUEUED = "QUEUED"
    INGESTING = "INGESTING"
    INDEXING = "INDEXING"
    ANALYZING = "ANALYZING"
    MAPPING = "MAPPING"
    REMEDIATING = "REMEDIATING"
    REPORTING = "REPORTING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    AWAITING_REVIEW = "AWAITING_REVIEW"


class FindingAssessmentStatus(StrEnum):
    """Per-finding mapping outcome (Architecture §3.3, §16)."""

    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    NA = "NA"
    UNCERTAIN = "UNCERTAIN"


class FindingSeverity(StrEnum):
    """Normalized severity for triage and reporting."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class WebhookEvent(StrEnum):
    """Outbound webhook subscription events (Architecture §28.4)."""

    COMPLETED = "completed"
    FAILED = "failed"


class AgentErrorSeverity(StrEnum):
    """Whether an agent error allows the graph to continue (Architecture §31.4)."""

    RECOVERABLE = "recoverable"
    FATAL = "fatal"
