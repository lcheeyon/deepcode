"""OpenTelemetry hooks (Phase L13 / EPIC DG-11)."""

from deepguard_observability.tracing import (
    CollectingSpanExporter,
    configure_test_tracing,
    configure_tracer_provider,
    graph_node_span,
)

__all__ = [
    "CollectingSpanExporter",
    "configure_test_tracing",
    "configure_tracer_provider",
    "graph_node_span",
]
