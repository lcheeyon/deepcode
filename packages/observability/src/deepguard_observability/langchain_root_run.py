"""Capture root LangChain run id for vendor trace URLs (EPIC-DG-14-017)."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler


class LangChainRootRunRecorder(BaseCallbackHandler):
    """Records the first chain run with ``parent_run_id is None`` (LangGraph root)."""

    def __init__(self) -> None:
        super().__init__()
        self.root_run_id: str | None = None

    def on_chain_start(
        self,
        serialized: dict[str, Any],
        inputs: dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        if parent_run_id is None and self.root_run_id is None:
            self.root_run_id = str(run_id)
        return None
