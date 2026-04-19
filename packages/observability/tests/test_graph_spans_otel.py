"""Phase L13 — graph node spans carry scan + tenant ids."""

from __future__ import annotations

from deepguard_observability.tracing import (
    CollectingSpanExporter,
    configure_test_tracing,
    graph_node_span,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor


def test_graph_node_span_attributes_on_exported_span() -> None:
    exp = configure_test_tracing()
    with graph_node_span("hermes", scan_id="scan-1", tenant_id="tenant-9"):
        pass
    assert exp.spans, "expected at least one exported span"
    attrs = dict(exp.spans[0].attributes or {})
    assert attrs.get("scan_id") == "scan-1"
    assert attrs.get("tenant_id") == "tenant-9"
    assert attrs.get("deepguard.graph.node") == "hermes"


def test_collecting_exporter_shutdown_and_force_flush() -> None:
    exp = CollectingSpanExporter()
    assert exp.shutdown() is None
    assert exp.force_flush(timeout_millis=1) is True


def test_graph_node_span_with_explicit_tracer() -> None:
    """``graph_node_span`` accepts a tracer without mutating the process-global provider."""

    exp = CollectingSpanExporter()
    provider = TracerProvider(resource=Resource.create({"service.name": "local-test"}))
    provider.add_span_processor(SimpleSpanProcessor(exp))
    tracer = provider.get_tracer("custom")
    with graph_node_span("athena", scan_id="s", tenant_id="t", tracer=tracer):
        pass
    assert any((s.attributes or {}).get("deepguard.graph.node") == "athena" for s in exp.spans)
