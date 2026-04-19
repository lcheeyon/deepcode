"""Presigned repo artefact uploads (US-DG-02-011, US-DG-04-008)."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID, uuid4

from deepguard_api.auth_deps import get_dev_tenant_id
from deepguard_api.config import Settings
from deepguard_api.deps import get_settings
from deepguard_api.s3_presign import presigned_put_url, staging_object_key
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/repo-uploads", tags=["repo-uploads"])


class PrepareRepoUploadRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filename: str = Field(default="repo.tar.gz", min_length=1, max_length=256)
    content_type: str = Field(default="application/gzip", min_length=3, max_length=256)


class PrepareRepoUploadResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    upload_id: UUID
    upload_url: str
    upload_headers: dict[str, str]
    storage_uri: str
    expires_in_seconds: int = 3600


@router.post("", response_model=PrepareRepoUploadResponse, status_code=status.HTTP_201_CREATED)
async def prepare_repo_upload(
    body: PrepareRepoUploadRequest,
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> PrepareRepoUploadResponse:
    if not settings.s3_repo_upload_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error_code": "REPO_UPLOAD_S3_UNCONFIGURED",
                "message": "S3/MinIO settings are not configured for presigned repo uploads.",
            },
        )
    assert settings.s3_bucket is not None
    assert settings.s3_access_key_id is not None
    assert settings.s3_secret_access_key is not None
    upload_id = uuid4()
    key = staging_object_key(tenant_id=tenant_id, upload_id=upload_id, filename=body.filename)
    url, hdrs = presigned_put_url(
        bucket=settings.s3_bucket,
        key=key,
        endpoint_url=settings.s3_endpoint_url,
        access_key_id=settings.s3_access_key_id,
        secret_access_key=settings.s3_secret_access_key,
        region=settings.s3_region,
        content_type=body.content_type,
        expires_in=3600,
    )
    storage_uri = f"s3://{settings.s3_bucket}/{key}"
    return PrepareRepoUploadResponse(
        upload_id=upload_id,
        upload_url=url,
        upload_headers=hdrs,
        storage_uri=storage_uri,
        expires_in_seconds=3600,
    )
