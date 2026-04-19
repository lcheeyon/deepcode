"""Compile Odysseus ``StateGraph`` with checkpointing and HITL options (§7.1)."""

from __future__ import annotations

from typing import Any, cast

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver

from deepguard_graph.graph import build_odysseus_graph


def compile_odysseus_app(
    *,
    checkpointer: BaseCheckpointSaver,  # type: ignore[type-arg]
    interrupt_before_athena: bool = False,
    argus_node: Any | None = None,
) -> Any:
    """Return a compiled graph sharing ``OdysseusState`` and optional Argus override (tests)."""

    builder = build_odysseus_graph(argus_node=argus_node)
    ib: list[str] | None = ["athena"] if interrupt_before_athena else None
    return builder.compile(checkpointer=checkpointer, interrupt_before=ib)


def resume_odysseus_after_interrupt(
    *,
    checkpointer: BaseCheckpointSaver,  # type: ignore[type-arg]
    scan_id: str,
    tenant_id: str,
) -> dict[str, Any]:
    """Resume after ``interrupt_before`` using input ``None``; HITL cleared on re-compile."""

    app = compile_odysseus_app(checkpointer=checkpointer, interrupt_before_athena=False)
    cfg = cast(
        RunnableConfig,
        {"configurable": {"thread_id": scan_id, "tenant_id": tenant_id}},
    )
    last: dict[str, Any] | None = None
    for state in app.stream(None, config=cfg, stream_mode="values"):
        last = cast(dict[str, Any], state)
    if last is None:
        msg = "resume produced no graph state"
        raise RuntimeError(msg)
    return last
