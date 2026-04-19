"""Odysseus shared graph state (Architecture §4.1–4.2; L5 stub slice)."""

from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict


class OdysseusState(TypedDict, total=False):
    """Minimal state for the L5 LangGraph shell; fields grow with real agents."""

    scan_id: str
    """Primary key as string; use ``thread_id=str(scan_id)`` in RunnableConfig."""

    created_at: str
    """ISO-8601 timestamp string for checkpoint-friendly serialization."""

    job_config: dict[str, Any]
    """``CreateScanRequest`` JSON (includes ``scan_layers`` for routing)."""

    execution_log: Annotated[list[str], operator.add]
    """Ordered node ids for tests (parallel branches may interleave before the gate)."""

    stub_findings: Annotated[list[str], operator.add]
    """Synthetic finding ids — used to assert no duplicates after checkpoint resume."""


def empty_odysseus_state(
    *,
    scan_id: str,
    created_at: str,
    job_config: dict[str, Any],
) -> OdysseusState:
    """Build initial invoke payload with reducers seeded to empty lists."""

    return {
        "scan_id": scan_id,
        "created_at": created_at,
        "job_config": job_config,
        "execution_log": [],
        "stub_findings": [],
    }
