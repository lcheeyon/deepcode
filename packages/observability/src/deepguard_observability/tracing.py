"""Tracer setup + graph node span helper (Architecture §7–8)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import contextmanager

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
    SpanExporter,
    SpanExportResult,
)


class CollectingSpanExporter(SpanExporter):
    """Test double that records exported spans in memory."""

    def __init__(self) -> None:
        self.spans: list[ReadableSpan] = []

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        self.spans.extend(spans)
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        return None

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


def configure_tracer_provider(
    *,
    service_name: str,
    exporter: SpanExporter | None = None,
) -> TracerProvider:
    """Install SDK provider. Defaults to console export (dev). LangSmith stays opt-in."""

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    exp = exporter if exporter is not None else ConsoleSpanExporter()
    provider.add_span_processor(BatchSpanProcessor(exp))
    trace.set_tracer_provider(provider)
    return provider


@contextmanager
def graph_node_span(
    node_id: str,
    *,
    scan_id: str,
    tenant_id: str,
    tracer: trace.Tracer | None = None,
    observation_semantic: str = "GRAPH_NODE",
) -> Iterator[None]:
    """Emit one span per graph node with correlation + LangFuse-oriented hints (L13 / §8.2)."""

    from deepguard_observability.correlation import graph_correlation_context

    tr = tracer or trace.get_tracer("deepguard.graph")
    name = f"graph.node.{node_id}"
    corr = graph_correlation_context.get()
    attributes: dict[str, str] = {
        "deepguard.graph.node": node_id,
        "scan_id": scan_id,
        "tenant_id": tenant_id,
        "deepguard.observation.kind": observation_semantic,
    }
    if corr:
        attributes["deepguard.correlation_id"] = corr
    with tr.start_as_current_span(
        name,
        attributes=attributes,
    ):
        yield


def configure_test_tracing(*, service_name: str = "deepguard-test") -> CollectingSpanExporter:
    """In-memory export for pytest (L13)."""

    exp = CollectingSpanExporter()
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    provider.add_span_processor(SimpleSpanProcessor(exp))
    trace.set_tracer_provider(provider)
    return exp
