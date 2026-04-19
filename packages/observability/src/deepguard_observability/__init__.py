"""OpenTelemetry + LangSmith/LangFuse hooks (Phase L13 / EPIC-DG-11)."""

from deepguard_observability.correlation import graph_correlation_context, primary_correlation_id
from deepguard_observability.eval_stubs import (
    langsmith_eval_accuracy_threshold,
    run_athena_gold_stub_eval,
)
from deepguard_observability.llm_callbacks import (
    build_langchain_callbacks,
    graph_invoke_config,
    langfuse_tracing_enabled,
    langsmith_tracing_effective,
    observability_feature_matrix,
)
from deepguard_observability.redaction import (
    excerpt_for_trace_sink,
    redact_secrets,
    sanitize_trace_metadata_value,
)
from deepguard_observability.runtime import (
    configure_langsmith_env_defaults,
    configure_observability_at_startup,
    instrument_fastapi_app,
)
from deepguard_observability.tracing import (
    CollectingSpanExporter,
    configure_test_tracing,
    configure_tracer_provider,
    graph_node_span,
)

__all__ = [
    "CollectingSpanExporter",
    "build_langchain_callbacks",
    "configure_langsmith_env_defaults",
    "configure_observability_at_startup",
    "configure_test_tracing",
    "configure_tracer_provider",
    "excerpt_for_trace_sink",
    "graph_correlation_context",
    "graph_invoke_config",
    "graph_node_span",
    "instrument_fastapi_app",
    "langfuse_tracing_enabled",
    "langsmith_eval_accuracy_threshold",
    "langsmith_tracing_effective",
    "observability_feature_matrix",
    "primary_correlation_id",
    "redact_secrets",
    "run_athena_gold_stub_eval",
    "sanitize_trace_metadata_value",
]
