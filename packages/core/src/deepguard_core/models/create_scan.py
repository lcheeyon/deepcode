"""Create scan API body and persisted job config (Architecture §28.4)."""

from __future__ import annotations

from typing import Literal, Self

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, field_validator, model_validator

from deepguard_core.models.enums import CloudProvider, WebhookEvent


class RepoSpec(BaseModel):
    """Source for Hermes: **git** clone or pre-staged **archive** (S3 URI).

    Back-compat: payloads without ``source`` default to **git** when ``url`` is
    present; to **archive** when ``storage_uri`` is set and ``url`` is absent.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source: Literal["git", "archive"] = "git"
    url: AnyHttpUrl | None = None
    ref: str = Field(default="main", min_length=1, max_length=512)
    commit_sha: str | None = Field(default=None, max_length=64)
    clone_depth: int | None = Field(default=None, ge=1, le=10_000)
    sub_path: str | None = Field(default=None, max_length=512)
    # archive (US-DG-04-008): client uploads to staging key, then passes URI here.
    storage_uri: str | None = Field(default=None, max_length=2048)
    checksum_sha256: str | None = Field(default=None, max_length=64)

    @model_validator(mode="before")
    @classmethod
    def _infer_source(cls, data: object) -> object:
        if not isinstance(data, dict):
            return data
        d = dict(data)
        if d.get("source") is None:
            if d.get("storage_uri") and not d.get("url"):
                d["source"] = "archive"
            else:
                d["source"] = "git"
        return d

    @model_validator(mode="after")
    def _validate_source_fields(self) -> Self:
        if self.source == "git":
            if self.url is None:
                msg = "repo.url is required when source is git"
                raise ValueError(msg)
            if self.storage_uri:
                msg = "repo.storage_uri must not be set when source is git"
                raise ValueError(msg)
        else:
            su = (self.storage_uri or "").strip()
            if not su.startswith("s3://"):
                msg = "archive repo requires storage_uri starting with s3://"
                raise ValueError(msg)
            if self.url is not None:
                msg = "repo.url must not be set when source is archive"
                raise ValueError(msg)
        if self.sub_path is not None:
            sp = self.sub_path.strip().replace("\\", "/")
            if ".." in sp.split("/"):
                msg = "repo.sub_path must not contain path segments '..'"
                raise ValueError(msg)
            if sp.startswith("/"):
                msg = "repo.sub_path must be relative"
                raise ValueError(msg)
        return self


class ScanLayers(BaseModel):
    """Boolean switches for code / IaC / cloud analysis."""

    model_config = ConfigDict(extra="forbid")

    code: bool = False
    iac: bool = False
    cloud: bool = False

    @model_validator(mode="after")
    def at_least_one_layer(self) -> Self:
        if not (self.code or self.iac or self.cloud):
            msg = "At least one of scan_layers.code, .iac, or .cloud must be true"
            raise ValueError(msg)
        return self


class CloudProfile(BaseModel):
    """Read-only cloud connector profile (Architecture §28.4)."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    profile_id: str = Field(min_length=1, max_length=256)
    provider: CloudProvider
    connector_credential_ref: str = Field(min_length=1, max_length=512)
    regions: list[str] = Field(min_length=1)


class NotificationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    webhook_url: AnyHttpUrl
    on: list[WebhookEvent] = Field(min_length=1)


class BudgetConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_llm_usd: float | None = Field(default=None, gt=0)
    max_wall_seconds: int | None = Field(default=None, gt=0)


class LangGraphJobOptions(BaseModel):
    """Optional LangGraph / worker runtime flags (Architecture §7.1, EPIC-DG-01)."""

    model_config = ConfigDict(extra="forbid")

    interrupt_before_athena: bool = False
    code_analysis_shard_keys: list[str] = Field(default_factory=list, max_length=2)

    @field_validator("code_analysis_shard_keys", mode="after")
    @classmethod
    def normalize_shard_keys(cls, v: list[str]) -> list[str]:
        return [s.strip() for s in v if s.strip()]


class CreateScanRequest(BaseModel):
    """`POST /v1/scans` JSON body — normative shape (Architecture §28.4).

    Validation rules (same section):
    - If ``scan_layers.cloud`` is true: at least one of ``repo`` or a non-empty
      ``cloud_profiles`` list must be provided.
    - If ``scan_layers.code`` or ``scan_layers.iac`` is true: ``repo`` is required.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    repo: RepoSpec | None = None
    policy_ids: list[str] = Field(min_length=1)
    scan_layers: ScanLayers
    cloud_profiles: list[CloudProfile] = Field(default_factory=list)
    notifications: NotificationSettings | None = None
    budget: BudgetConfig | None = None
    langgraph: LangGraphJobOptions | None = None

    @model_validator(mode="after")
    def validate_layer_inputs(self) -> Self:
        layers = self.scan_layers
        repo_ok = self.repo is not None
        profiles_nonempty = len(self.cloud_profiles) > 0

        if layers.cloud and (not repo_ok and not profiles_nonempty):
            msg = (
                "scan_layers.cloud requires a repo and/or at least one entry "
                "in cloud_profiles (Architecture §28.4)"
            )
            raise ValueError(msg)
        if (layers.code or layers.iac) and not repo_ok:
            msg = "scan_layers.code or scan_layers.iac requires repo (Architecture §28.4)"
            raise ValueError(msg)
        return self


# Persisted JSONB on ``scans.job_config`` uses the same shape for v0.
ScanJobConfig = CreateScanRequest
