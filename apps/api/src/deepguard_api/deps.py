"""FastAPI dependencies (DB session, repositories)."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated, cast

from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from deepguard_api.config import Settings
from deepguard_api.repositories.scans import PostgresScanRepository, ScanRepository


def get_settings(request: Request) -> Settings:
    return cast(Settings, request.app.state.settings)


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    maker: async_sessionmaker[AsyncSession] = request.app.state.session_maker
    async with maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_scan_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ScanRepository:
    return PostgresScanRepository(session)


async def get_redis_optional(request: Request) -> Redis | None:
    """Redis client when API is configured as queue producer; else ``None``."""

    return getattr(request.app.state, "redis", None)
