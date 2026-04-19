"""OTEL graph spans pick up correlation context (§8.3)."""

from __future__ import annotations

from deepguard_observability.correlation import graph_correlation_context
from deepguard_observability.tracing import CollectingSpanExporter, graph_node_span
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor


def test_graph_node_span_includes_correlation_from_context() -> None:
    exp = CollectingSpanExporter()
    provider = TracerProvider(resource=Resource.create({"service.name": "deepguard-test-local"}))
    provider.add_span_processor(SimpleSpanProcessor(exp))
    tracer = provider.get_tracer("deepguard.graph")
    tok = graph_correlation_context.set("scan-abc:msg-1")
    try:
        with graph_node_span(
            "hermes",
            scan_id="scan-abc",
            tenant_id="tenant-1",
            tracer=tracer,
        ):
            pass
    finally:
        graph_correlation_context.reset(tok)

    assert exp.spans
    attrs = exp.spans[-1].attributes or {}
    assert attrs.get("deepguard.correlation_id") == "scan-abc:msg-1"
    assert attrs.get("deepguard.observation.kind") == "GRAPH_NODE"
