"""Scan create + read (Architecture §28.3–28.4)."""

from __future__ import annotations

import logging
from typing import Annotated
from uuid import UUID

from deepguard_api.auth_deps import get_dev_tenant_id
from deepguard_api.deps import get_redis_optional, get_scan_repository
from deepguard_api.queue_publish import publish_scan_job
from deepguard_api.repositories.scans import ScanRepository
from deepguard_api.schemas import ScanCancelResponse, ScanResponse
from deepguard_core.models import CreateScanRequest
from fastapi import APIRouter, Depends, Header, HTTPException, status
from redis.asyncio import Redis

router = APIRouter(prefix="/scans", tags=["scans"])
log = logging.getLogger("deepguard_api.scans")


@router.post("", response_model=ScanResponse, status_code=status.HTTP_201_CREATED)
async def create_scan(
    body: CreateScanRequest,
    repo: Annotated[ScanRepository, Depends(get_scan_repository)],
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
    redis: Annotated[Redis | None, Depends(get_redis_optional)],
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> ScanResponse:
    idem = (idempotency_key or "").strip() or None
    row = await repo.create_scan(
        tenant_id=tenant_id,
        body=body,
        idempotency_key=idem,
    )
    if redis is not None and not row.reused_from_idempotency:
        await publish_scan_job(redis, tenant_id=tenant_id, scan_id=row.id)
    return row.to_response()


@router.post(
    "/{scan_id}/cancel",
    response_model=ScanCancelResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def cancel_scan(
    scan_id: UUID,
    repo: Annotated[ScanRepository, Depends(get_scan_repository)],
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
) -> ScanCancelResponse:
    ok = await repo.set_cancellation_requested(tenant_id=tenant_id, scan_id=scan_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="scan not found")
    return ScanCancelResponse(scan_id=scan_id, cancellation_requested=True)


@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(
    scan_id: UUID,
    repo: Annotated[ScanRepository, Depends(get_scan_repository)],
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
) -> ScanResponse:
    log.info(
        "api_scan_get",
        extra={
            "event": "api.scan.get",
            "scan_id": str(scan_id),
            "tenant_id": str(tenant_id),
        },
    )
    row = await repo.get_scan(tenant_id=tenant_id, scan_id=scan_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="scan not found")
    return row.to_response()
