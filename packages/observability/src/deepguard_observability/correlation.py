"""Single correlation identifier for worker → graph → OTEL → LangSmith/LangFuse (§8.3)."""

from __future__ import annotations

from contextvars import ContextVar

graph_correlation_context: ContextVar[str | None] = ContextVar(
    "deepguard_graph_correlation_id",
    default=None,
)


def primary_correlation_id(
    *,
    scan_id: str,
    redis_message_id: str | None = None,
) -> str:
    """Return the primary ID carried in OTEL and LangChain ``RunnableConfig`` metadata.

    ``thread_id`` remains ``scan_id`` for LangGraph checkpointing; correlation may add a
    queue id when Redis stream metadata is available.
    """

    sid = scan_id.strip()
    if redis_message_id and redis_message_id.strip():
        return f"{sid}:{redis_message_id.strip()}"
    return sid
