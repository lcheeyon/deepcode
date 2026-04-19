"""Root LangChain run id capture for vendor trace URLs."""

from __future__ import annotations

from uuid import uuid4

from deepguard_observability.langchain_root_run import LangChainRootRunRecorder


def test_root_run_recorder_captures_first_root_chain() -> None:
    h = LangChainRootRunRecorder()
    rid = uuid4()
    h.on_chain_start({}, {}, run_id=rid, parent_run_id=None)
    assert h.root_run_id == str(rid)
    rid2 = uuid4()
    h.on_chain_start({}, {}, run_id=rid2, parent_run_id=None)
    assert h.root_run_id == str(rid)
