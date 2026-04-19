"""FastAPI application factory (Phase L3)."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import cast

import redis.asyncio as redis_async
from fastapi import APIRouter, Depends, FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from deepguard_api.auth_deps import require_api_key
from deepguard_api.config import Settings, load_settings
from deepguard_api.deps import get_scan_repository
from deepguard_api.logging_json import configure_logging
from deepguard_api.repositories.scans import MemoryScanRepository, ScanRepository
from deepguard_api.routers import health, repo_uploads, scans


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    settings: Settings = app.state.settings
    if not settings.use_memory_store:
        if not settings.database_url:
            msg = "DATABASE_URL is required unless DEEPGUARD_L3_MEMORY_STORE=1"
            raise RuntimeError(msg)
        if not settings.redis_url:
            msg = "REDIS_URL is required when DATABASE_URL is set (Phase L4 queue producer)"
            raise RuntimeError(msg)
        engine = create_async_engine(settings.database_url, pool_pre_ping=True)
        app.state.engine = engine
        app.state.session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        app.state.redis = redis_async.from_url(settings.redis_url, decode_responses=True)
    yield
    r = getattr(app.state, "redis", None)
    if r is not None:
        await r.aclose()
    eng = getattr(app.state, "engine", None)
    if eng is not None:
        await eng.dispose()


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build app. Tests pass explicit ``Settings``; production uses ``load_settings()``."""

    resolved = settings if settings is not None else load_settings()
    app = FastAPI(
        title="DeepGuard Control Plane",
        version="0.1.0",
        lifespan=_lifespan,
        openapi_url="/v1/openapi.json",
        docs_url="/v1/docs",
        redoc_url="/v1/redoc",
    )
    app.state.settings = resolved
    if resolved.use_memory_store:
        app.state.memory_repo = MemoryScanRepository()

        async def _memory_repo(request: Request) -> ScanRepository:
            return cast(ScanRepository, request.app.state.memory_repo)

        app.dependency_overrides[get_scan_repository] = _memory_repo

    v1 = APIRouter(prefix="/v1")
    v1.include_router(health.router)
    v1.include_router(scans.router, dependencies=[Depends(require_api_key)])
    v1.include_router(repo_uploads.router, dependencies=[Depends(require_api_key)])
    app.include_router(v1)
    if resolved.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(resolved.cors_origins),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    return app


app = create_app()
