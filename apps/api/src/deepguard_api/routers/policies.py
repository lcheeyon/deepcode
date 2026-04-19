"""Policy admin upload + listing (US-DG-12-006)."""

from __future__ import annotations

import logging
from typing import Annotated
from uuid import UUID

from deepguard_api.auth_deps import get_dev_tenant_id
from deepguard_api.deps import get_console_store
from deepguard_api.repositories.console import ConsoleStore
from deepguard_api.schemas import PolicyUploadListResponse, PolicyUploadResponse
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

router = APIRouter(tags=["policies"])
log = logging.getLogger("deepguard_api.policies")


@router.post(
    "/policies:upload",
    response_model=PolicyUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_policy_document(
    store: Annotated[ConsoleStore, Depends(get_console_store)],
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
    file: Annotated[UploadFile, File(description="YAML policy fixture.")],
) -> PolicyUploadResponse:
    name = (file.filename or "policy.yaml").strip() or "policy.yaml"
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="empty upload")
    if len(raw) > 2_000_000:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="file exceeds 2 MiB limit",
        )
    try:
        out = await store.upload_policy(tenant_id=tenant_id, filename=name, data=raw)
    except ValueError as exc:
        log.info("policy_upload_rejected", extra={"reason": str(exc)[:256]})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)[:4096],
        ) from exc
    log.info(
        "policy_upload_ok",
        extra={
            "event": "api.policy.upload",
            "tenant_id": str(tenant_id),
            "upload_id": str(out.upload_id),
            "controls": out.controls_extracted,
        },
    )
    return out


@router.get("/policies", response_model=PolicyUploadListResponse)
async def list_policy_uploads(
    store: Annotated[ConsoleStore, Depends(get_console_store)],
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
) -> PolicyUploadListResponse:
    return await store.list_policy_uploads(tenant_id=tenant_id)
