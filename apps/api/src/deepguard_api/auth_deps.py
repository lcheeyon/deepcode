"""Stub API key auth until DG-03 JWT (Architecture §28.2)."""

from __future__ import annotations

from typing import cast
from uuid import UUID

from fastapi import Header, HTTPException, Request, status

from deepguard_api.config import Settings


async def require_api_key(
    request: Request,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    authorization: str | None = Header(default=None),
) -> None:
    settings = cast(Settings, request.app.state.settings)
    expected = settings.dev_api_key
    if x_api_key is not None and x_api_key == expected:
        return
    if authorization and authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ").strip()
        if token == expected:
            return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid or missing API credentials",
    )


async def get_dev_tenant_id(request: Request) -> UUID:
    """Fixed dev tenant until JWT supplies ``tenant_id`` claim."""

    settings = cast(Settings, request.app.state.settings)
    return settings.dev_tenant_id
