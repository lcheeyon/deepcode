"""Phase L8 — Argus chunker + dependency graph caps."""

from __future__ import annotations

from deepguard_parsers.chunker import StubASTAwareChunker
from deepguard_parsers.dependency_graph import cap_dependency_graph_depth


def test_stub_chunker_splits_source() -> None:
    ch = StubASTAwareChunker()
    parts = ch.chunk_source("a.py", "x" * 100, max_chunk_chars=40)
    assert len(parts) >= 3
    assert "".join(parts) == "x" * 100


def test_dependency_graph_truncation_flag_deep_chain() -> None:
    g = {
        "nodes": [{"id": n} for n in ("a", "b", "c", "d", "e")],
        "edges": [
            {"from": "a", "to": "b"},
            {"from": "b", "to": "c"},
            {"from": "c", "to": "d"},
            {"from": "d", "to": "e"},
        ],
    }
    capped = cap_dependency_graph_depth(g, max_depth=2)
    assert capped["truncated"] is True
    assert capped["max_depth_observed"] >= 3
