"""Build vendor UI URLs for persisted trace references (US-DG-14-017)."""

from __future__ import annotations

import os


def langsmith_run_url(
    *,
    root_run_id: str,
    organization_id: str | None,
    project_id: str | None,
    ui_origin: str | None = None,
) -> tuple[str | None, str | None]:
    """Return ``(url, reason_if_url_none)``."""

    origin = (ui_origin or os.environ.get("LANGSMITH_UI_ORIGIN", "").strip() or "https://smith.langchain.com").rstrip(
        "/"
    )
    org = (organization_id or os.environ.get("LANGSMITH_ORGANIZATION_ID", "").strip()) or None
    proj = (project_id or os.environ.get("LANGSMITH_PROJECT_ID", "").strip() or os.environ.get(
        "LANGCHAIN_PROJECT", ""
    ).strip()) or None
    if not org or not proj:
        return None, "missing_langsmith_org_or_project"
    return f"{origin}/o/{org}/projects/p/{proj}/r/{root_run_id}", None


def langfuse_trace_url(
    *,
    trace_id: str | None,
    project_id: str | None,
    host: str | None = None,
) -> tuple[str | None, str | None]:
    """Return ``(url, reason_if_url_none)`` for LangFuse self-hosted or cloud."""

    base = (host or os.environ.get("LANGFUSE_HOST", "").strip()).rstrip("/")
    if not base or not trace_id:
        return None, "missing_langfuse_host_or_trace_id"
    pid = project_id or os.environ.get("LANGFUSE_PROJECT_ID", "").strip() or None
    if pid:
        return f"{base}/project/{pid}/traces/{trace_id}", None
    return f"{base}/trace/{trace_id}", None
