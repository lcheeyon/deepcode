"""Process-wide observability bootstrap (LangSmith defaults, OTEL) — EPIC-DG-11."""

from __future__ import annotations

import logging
import os

from deepguard_observability.tracing import configure_tracer_provider

log = logging.getLogger("deepguard_observability.runtime")

_OTEL_BOOTSTRAPPED = False


def configure_langsmith_env_defaults() -> None:
    """Apply LangSmith-related environment defaults (EPIC-DG-11-009).

    - **CI / GitHub Actions:** tracing stays off unless explicitly enabled (no network surprises).
    - **Local / production:** ``LANGCHAIN_TRACING_V2`` defaults to **true** so LangSmith runs are
      created whenever ``LANGSMITH_API_KEY`` (or ``LANGCHAIN_API_KEY``) is configured.

    Set ``LANGCHAIN_TRACING_V2=false`` for air-gap or offline runs (AC-DG-11-009-01).
    """

    if os.environ.get("LANGCHAIN_TRACING_V2") is not None:
        return
    if os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true":
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        return
    if os.environ.get("DEEPGUARD_AIR_GAP", "").lower() in ("1", "true", "yes"):
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        return
    os.environ["LANGCHAIN_TRACING_V2"] = "true"


def configure_observability_at_startup(*, service_name: str) -> None:
    """Call once per process from API/worker entrypoints."""

    global _OTEL_BOOTSTRAPPED
    configure_langsmith_env_defaults()
    if os.environ.get("DEEPGUARD_OTEL_BOOTSTRAP", "1").lower() in ("0", "false", "no"):
        log.info("otel_bootstrap_skipped service=%s", service_name)
        return
    if _OTEL_BOOTSTRAPPED:
        return
    configure_tracer_provider(service_name=service_name)
    _OTEL_BOOTSTRAPPED = True
    log.info("otel_bootstrap_ok service=%s", service_name)


def instrument_fastapi_app(app: object) -> None:
    """Attach OpenTelemetry FastAPI instrumentation when an SDK tracer provider is active."""

    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider as SDKTracerProvider
    except ModuleNotFoundError:
        return
    if not isinstance(trace.get_tracer_provider(), SDKTracerProvider):
        log.info("fastapi_otel_skipped_no_sdk_provider")
        return
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    except ModuleNotFoundError:
        log.warning("fastapi_otel_instrumentation_unavailable")
        return
    try:
        FastAPIInstrumentor.instrument_app(app)  # type: ignore[arg-type]
    except Exception:
        log.exception("fastapi_otel_instrument_failed")
