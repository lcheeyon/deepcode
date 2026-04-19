"""Artifact pointer for object-store payloads (Architecture §5.3)."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ArtifactRef(BaseModel):
    """Reference to bytes in S3-compatible storage — never embed raw secrets or source."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    artifact_id: UUID
    store: Literal["s3", "oss", "obs", "local"]
    bucket: str = Field(min_length=1, max_length=256)
    key: str = Field(min_length=1, max_length=1024)
    checksum: str = Field(min_length=64, max_length=64, description="SHA-256 hex digest.")
    size_bytes: int = Field(ge=0)
    expires_at: datetime | None = None
    encrypted: bool = True
