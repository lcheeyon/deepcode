"""Findings triage + scan artifacts (US-DG-12-004 / US-DG-12-005)."""

from __future__ import annotations

import logging
from typing import Annotated, Literal
from uuid import UUID

from deepguard_api.auth_deps import get_dev_tenant_id
from deepguard_api.config import Settings
from deepguard_api.deps import get_console_store, get_settings
from deepguard_api.repositories.console import (
    ArtifactDownload,
    ConsoleStore,
    export_findings_csv,
    export_findings_json,
)
from deepguard_api.schemas import ArtifactsListResponse, FindingsPage
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse, Response

router = APIRouter(prefix="/scans/{scan_id}", tags=["scan-console"])
log = logging.getLogger("deepguard_api.scan_console")


def _scan_not_found() -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="scan not found")


@router.get("/findings", response_model=FindingsPage)
async def list_findings(
    scan_id: UUID,
    store: Annotated[ConsoleStore, Depends(get_console_store)],
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
    cursor: Annotated[
        UUID | None,
        Query(description="Opaque cursor (finding id)."),
    ] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    severity: Annotated[str | None, Query()] = None,
    framework: Annotated[str | None, Query()] = None,
) -> FindingsPage:
    try:
        return await store.list_findings(
            tenant_id=tenant_id,
            scan_id=scan_id,
            cursor=cursor,
            limit=limit,
            severity=severity,
            framework=framework,
        )
    except LookupError:
        raise _scan_not_found() from None


@router.get("/findings/export", response_model=None)
async def export_findings(
    scan_id: UUID,
    store: Annotated[ConsoleStore, Depends(get_console_store)],
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
    export_format: Annotated[
        Literal["csv", "json"],
        Query(alias="format"),
    ] = "csv",
    severity: Annotated[str | None, Query()] = None,
    framework: Annotated[str | None, Query()] = None,
    ids: Annotated[
        str | None,
        Query(
            description=(
                "Comma-separated finding UUIDs; when omitted, exports all matching filters."
            ),
        ),
    ] = None,
) -> Response:
    finding_ids: list[UUID] | None = None
    if ids:
        try:
            finding_ids = [UUID(x.strip()) for x in ids.split(",") if x.strip()]
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="invalid finding id in ids parameter",
            ) from exc
    try:
        rows = await store.list_findings_for_export(
            tenant_id=tenant_id,
            scan_id=scan_id,
            finding_ids=finding_ids,
            severity=severity,
            framework=framework,
        )
    except LookupError:
        raise _scan_not_found() from None
    log.info(
        "api_findings_export",
        extra={
            "event": "api.findings.export",
            "scan_id": str(scan_id),
            "tenant_id": str(tenant_id),
            "format": export_format,
            "count": len(rows),
        },
    )
    if export_format == "json":
        body = export_findings_json(rows)
        return Response(
            content=body,
            media_type="application/json",
            headers={
                "Content-Disposition": 'attachment; filename="findings_v1.json"',
            },
        )
    body = export_findings_csv(rows)
    return Response(
        content=body,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="findings_v1.csv"'},
    )


@router.get("/artifacts", response_model=ArtifactsListResponse)
async def list_scan_artifacts(
    scan_id: UUID,
    store: Annotated[ConsoleStore, Depends(get_console_store)],
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
) -> ArtifactsListResponse:
    try:
        items = await store.list_artifacts(tenant_id=tenant_id, scan_id=scan_id)
    except LookupError:
        raise _scan_not_found() from None
    return ArtifactsListResponse(artifacts=items)


@router.get("/artifacts/{artifact_id}", response_model=None)
async def download_scan_artifact(
    scan_id: UUID,
    artifact_id: UUID,
    store: Annotated[ConsoleStore, Depends(get_console_store)],
    tenant_id: Annotated[UUID, Depends(get_dev_tenant_id)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> Response | RedirectResponse:
    result = await store.resolve_artifact_download(
        tenant_id=tenant_id,
        scan_id=scan_id,
        artifact_id=artifact_id,
        settings=settings,
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="artifact not found or download unavailable",
        )
    return _artifact_response(result)


def _artifact_response(result: ArtifactDownload) -> Response | RedirectResponse:
    if result.mode == "redirect":
        if not result.redirect_url:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="artifact storage is not configured for download",
            )
        return RedirectResponse(url=result.redirect_url, status_code=status.HTTP_302_FOUND)
    if not result.content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="empty artifact")
    return Response(
        content=result.content,
        media_type=result.media_type,
        headers={"Content-Disposition": 'attachment; filename="report.pdf"'},
    )
