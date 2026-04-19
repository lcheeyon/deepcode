"""LangChain-compatible callbacks for LangSmith (env) + LangFuse (self-hosted) (EPIC-DG-11-001)."""

from __future__ import annotations

import logging
import os
from typing import Any

from deepguard_observability.correlation import primary_correlation_id
from deepguard_observability.redaction import redact_secrets

log = logging.getLogger("deepguard_observability.llm_callbacks")


def langfuse_tracing_enabled() -> bool:
    """LangFuse is on when host + keys are present (EPIC-DG-11-009-02)."""

    host = os.environ.get("LANGFUSE_HOST", "").strip()
    pk = os.environ.get("LANGFUSE_PUBLIC_KEY", "").strip()
    sk = os.environ.get("LANGFUSE_SECRET_KEY", "").strip()
    return bool(host and pk and sk)


def langsmith_tracing_effective() -> bool:
    """Whether LangSmith runs are expected (env + API key; EPIC-DG-11 / §8.1)."""

    if os.environ.get("LANGCHAIN_TRACING_V2", "").strip().lower() in ("0", "false", "no"):
        return False
    return bool(
        os.environ.get("LANGSMITH_API_KEY", "").strip()
        or os.environ.get("LANGCHAIN_API_KEY", "").strip()
    )


def observability_feature_matrix() -> dict[str, str]:
    """Which tracing backends are active — for runbooks / health checks (§8.3)."""

    return {
        "langsmith_effective": "on" if langsmith_tracing_effective() else "off",
        "langfuse_callbacks": "on" if langfuse_tracing_enabled() else "off",
        "air_gap": "on"
        if os.environ.get("DEEPGUARD_AIR_GAP", "").lower() in ("1", "true", "yes")
        else "off",
    }


def build_langchain_callbacks(
    *,
    scan_id: str,
    tenant_id: str,
    run_name: str | None = None,
) -> list[Any]:
    """Return ordered callback handlers: LangFuse first, then any explicit handlers.

    LangSmith run trees are created when ``LANGCHAIN_TRACING_V2=true`` and
    ``LANGSMITH_API_KEY`` / ``LANGCHAIN_API_KEY`` are set — no extra handler required
    for most LangGraph ``invoke`` calls (EPIC-DG-11 / LangSmith docs).
    Dual-sink order when both active: **LangFuse → LangSmith auto-trace** (EPIC-DG-11-009-03).
    """

    handlers: list[Any] = []
    log.debug(
        "build_langchain_callbacks scan_id=%s tenant_id=%s run_name=%s",
        scan_id,
        tenant_id,
        run_name,
    )
    if langfuse_tracing_enabled():
        try:
            from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler
        except ModuleNotFoundError as exc:
            log.warning("langfuse_callback_unavailable: %s", exc)
        else:
            try:
                pk = os.environ.get("LANGFUSE_PUBLIC_KEY", "").strip() or None
                handlers.append(LangfuseCallbackHandler(public_key=pk))
            except Exception:
                log.exception("langfuse_callback_construct_failed")
    return handlers


def graph_invoke_config(
    *,
    scan_id: str,
    tenant_id: str,
    callbacks: list[Any] | None = None,
    run_name: str | None = None,
    idempotency_key: str | None = None,
    correlation_id: str | None = None,
    graph_version: str | None = None,
    redis_message_id: str | None = None,
) -> dict[str, Any]:
    """RunnableConfig for graph ``invoke`` / ``stream`` with joinable metadata (§8.1 / §8.3).

    LangGraph ``compile()`` does not accept callbacks; pass this config to ``invoke`` or
    ``stream`` so each node is a traced step when LangSmith / LangFuse is configured.
    """

    corr = correlation_id or primary_correlation_id(
        scan_id=scan_id,
        redis_message_id=redis_message_id,
    )
    meta: dict[str, object] = {
        "scan_id": scan_id,
        "tenant_id": tenant_id,
        "deepguard.correlation_id": corr,
    }
    if run_name:
        meta["deepguard.run_name"] = run_name
    if idempotency_key:
        meta["idempotency_key"] = idempotency_key
    if graph_version:
        meta["deepguard.graph_version"] = graph_version
    cfg: dict[str, Any] = {
        "configurable": {
            "thread_id": scan_id,
            "tenant_id": tenant_id,
            "deepguard.correlation_id": corr,
        },
        "metadata": redact_secrets(meta),
    }
    if callbacks:
        cfg["callbacks"] = callbacks
    return cfg
