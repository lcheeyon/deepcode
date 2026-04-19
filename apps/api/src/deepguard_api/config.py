"""Runtime settings for the control plane API (Phase L3)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Settings:
    """Loaded once at app startup (``create_app``)."""

    database_url: str | None
    """Async SQLAlchemy URL, e.g. ``postgresql+asyncpg://...``."""

    dev_tenant_id: UUID
    """Fixed tenant for dev / stub auth until DG-03 JWT lands."""

    dev_api_key: str
    """Shared secret for ``X-API-Key`` or ``Authorization: Bearer`` (dev only)."""

    use_memory_store: bool
    """In-process scan store (tests or laptop without ``DATABASE_URL``)."""

    redis_url: str | None = None
    """``redis://`` for ``stream:scans`` producer (required with ``DATABASE_URL``)."""

    s3_bucket: str | None = None
    s3_region: str = "us-east-1"
    s3_endpoint_url: str | None = None
    s3_access_key_id: str | None = None
    s3_secret_access_key: str | None = None
    cors_origins: tuple[str, ...] = ()
    """Allowed browser origins for CORS (e.g. local Next console). Empty = disabled."""

    langsmith_ui_origin: str | None = None
    langsmith_organization_id: str | None = None
    langsmith_project_id: str | None = None
    langfuse_public_host: str | None = None

    def s3_repo_upload_configured(self) -> bool:
        return bool(self.s3_bucket and self.s3_access_key_id and self.s3_secret_access_key)


def _env(*names: str) -> str:
    for n in names:
        v = os.environ.get(n, "").strip()
        if v:
            return v
    return ""


def load_settings() -> Settings:
    raw_tenant = os.environ.get("DEEPGUARD_DEV_TENANT_ID", "").strip()
    if not raw_tenant:
        raw_tenant = "00000000-0000-4000-8000-000000000001"
    db = os.environ.get("DATABASE_URL", "").strip() or None
    explicit_memory = os.environ.get("DEEPGUARD_L3_MEMORY_STORE", "").lower() in (
        "1",
        "true",
        "yes",
    )
    use_memory = explicit_memory or db is None
    if use_memory:
        db = None
    redis_raw = os.environ.get("REDIS_URL", "").strip() or None
    bucket = _env("DEEPGUARD_S3_BUCKET", "AWS_S3_BUCKET") or None
    region = _env("DEEPGUARD_S3_REGION", "AWS_REGION", "AWS_DEFAULT_REGION") or "us-east-1"
    endpoint = _env("DEEPGUARD_S3_ENDPOINT_URL", "AWS_ENDPOINT_URL_S3") or None
    ak = _env("DEEPGUARD_S3_ACCESS_KEY_ID", "AWS_ACCESS_KEY_ID") or None
    sk = _env("DEEPGUARD_S3_SECRET_ACCESS_KEY", "AWS_SECRET_ACCESS_KEY") or None
    cors_raw = os.environ.get("DEEPGUARD_CORS_ORIGINS", "").strip()
    cors_origins = tuple(
        o.strip() for o in cors_raw.split(",") if o.strip()
    ) if cors_raw else ()
    ls_origin = os.environ.get("LANGSMITH_UI_ORIGIN", "").strip() or None
    ls_org = os.environ.get("LANGSMITH_ORGANIZATION_ID", "").strip() or None
    ls_proj = (
        os.environ.get("LANGSMITH_PROJECT_ID", "").strip()
        or os.environ.get("LANGCHAIN_PROJECT", "").strip()
        or None
    )
    lf_host = os.environ.get("LANGFUSE_HOST", "").strip() or None
    return Settings(
        database_url=db,
        dev_tenant_id=UUID(raw_tenant),
        dev_api_key=os.environ.get("DEEPGUARD_DEV_API_KEY", "dev").strip(),
        use_memory_store=use_memory,
        redis_url=redis_raw,
        s3_bucket=bucket,
        s3_region=region,
        s3_endpoint_url=endpoint,
        s3_access_key_id=ak,
        s3_secret_access_key=sk,
        cors_origins=cors_origins,
        langsmith_ui_origin=ls_origin,
        langsmith_organization_id=ls_org,
        langsmith_project_id=ls_proj,
        langfuse_public_host=lf_host,
    )
