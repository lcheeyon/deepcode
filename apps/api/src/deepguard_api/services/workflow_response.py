"""Assemble sanitized ``GET /v1/scans/{id}/workflow`` payloads."""

from __future__ import annotations

from dataclasses import dataclass

from deepguard_graph import odysseus_planned_graph_nodes
from deepguard_observability.redaction import redact_secrets

from deepguard_api.repositories.scans import ExternalTraceRefRow, ScanRow, ScanRunEventRow
from deepguard_api.schemas import (
    ScanWorkflowChecklistItem,
    ScanWorkflowEventItem,
    ScanWorkflowHandoffItem,
    ScanWorkflowResponse,
    TraceLinkItem,
)
from deepguard_api.services import trace_urls


def _planned_key_for_event_node(node: str, planned: frozenset[str]) -> str | None:
    """Map stub ``execution_log`` tail names onto top-level planned graph ids."""

    if node in ("hermes", "tiresias", "argus"):
        return "ingestion" if "ingestion" in planned else None
    if node.startswith("code_shard:0"):
        return "parallel_code_0" if "parallel_code_0" in planned else None
    if node.startswith("code_shard:1"):
        return "parallel_code_1" if "parallel_code_1" in planned else None
    return node if node in planned else None


def _checklist_for_events(
    planned: list[str], events: list[ScanRunEventRow]
) -> list[ScanWorkflowChecklistItem]:
    pset = frozenset(planned)
    status: dict[str, str] = {n: "pending" for n in planned}
    for ev in events:
        if ev.event_type == "node_progress" and ev.node:
            key = _planned_key_for_event_node(ev.node, pset)
            if key:
                status[key] = "completed"
        if ev.event_type == "job_error" and ev.node:
            key = _planned_key_for_event_node(ev.node, pset)
            if key:
                status[key] = "failed"
    return [ScanWorkflowChecklistItem(node=n, state=status.get(n, "pending")) for n in planned]


def _handoffs_from_events(events: list[ScanRunEventRow]) -> list[ScanWorkflowHandoffItem]:
    out: list[ScanWorkflowHandoffItem] = []
    for ev in events:
        if ev.event_type != "agent_handoff":
            continue
        p = redact_secrets(dict(ev.payload))
        fa = str(p.get("from_agent") or "")
        ta = str(p.get("to_agent") or "")
        mt = str(p.get("message_type") or "graph_edge")
        summ = p.get("summary")
        summ_s = str(summ) if summ is not None else None
        out.append(
            ScanWorkflowHandoffItem(
                from_agent=fa,
                to_agent=ta,
                message_type=mt,
                summary=summ_s,
                at=ev.created_at,
            )
        )
    return out


def _last_correlation(events: list[ScanRunEventRow]) -> str | None:
    for ev in reversed(events):
        if ev.correlation_id:
            return ev.correlation_id
    return None


def _last_graph_version(events: list[ScanRunEventRow]) -> str | None:
    for ev in reversed(events):
        if ev.graph_version:
            return ev.graph_version
    return None


@dataclass(frozen=True, slots=True)
class TraceLinkBuildContext:
    langsmith_ui_origin: str | None = None
    langsmith_organization_id: str | None = None
    langsmith_project_id: str | None = None
    langfuse_host: str | None = None


def build_trace_link_items(
    refs: list[ExternalTraceRefRow], ctx: TraceLinkBuildContext
) -> list[TraceLinkItem]:
    items: list[TraceLinkItem] = []
    for r in refs:
        url: str | None = None
        reason: str | None = None
        if r.vendor == "langsmith" and r.root_run_id:
            url, reason = trace_urls.langsmith_run_url(
                root_run_id=r.root_run_id,
                organization_id=r.workspace_id or ctx.langsmith_organization_id,
                project_id=r.project_id or ctx.langsmith_project_id,
                ui_origin=ctx.langsmith_ui_origin,
            )
        elif r.vendor == "langfuse":
            url, reason = trace_urls.langfuse_trace_url(
                trace_id=r.trace_id,
                project_id=r.project_id,
                host=ctx.langfuse_host,
            )
        items.append(
            TraceLinkItem(
                vendor=r.vendor,
                url=url,
                reason=reason,
                root_run_id=r.root_run_id,
                trace_id=r.trace_id,
                project_id=r.project_id,
                workspace_id=r.workspace_id,
            )
        )
    return items


def build_scan_workflow_response(
    *,
    scan: ScanRow,
    events: list[ScanRunEventRow],
    trace_refs: list[ExternalTraceRefRow],
    include_events: bool,
    trace_ctx: TraceLinkBuildContext,
) -> ScanWorkflowResponse:
    planned = odysseus_planned_graph_nodes(job_config=scan.job_config)
    checklist = _checklist_for_events(planned, events)
    handoffs = _handoffs_from_events(events)
    ev_items: list[ScanWorkflowEventItem] = []
    if include_events:
        for ev in events:
            ev_items.append(
                ScanWorkflowEventItem(
                    id=ev.id,
                    event_seq=ev.event_seq,
                    event_type=ev.event_type,
                    node=ev.node,
                    correlation_id=ev.correlation_id,
                    graph_version=ev.graph_version,
                    created_at=ev.created_at,
                    payload=redact_secrets(dict(ev.payload)),
                )
            )
    trace_links = build_trace_link_items(trace_refs, trace_ctx)
    counts = {
        "events_total": len(events),
        "handoffs_total": len(handoffs),
        "node_progress": sum(1 for e in events if e.event_type == "node_progress"),
    }
    return ScanWorkflowResponse(
        scan_id=scan.id,
        tenant_id=scan.tenant_id,
        status=scan.status,
        current_stage=scan.current_stage,
        percent_complete=scan.percent_complete,
        correlation_id=_last_correlation(events),
        graph_version=_last_graph_version(events),
        planned_nodes=planned,
        checklist=checklist,
        handoffs=handoffs,
        events=ev_items,
        trace_links=trace_links,
        summary_counts=counts,
    )
