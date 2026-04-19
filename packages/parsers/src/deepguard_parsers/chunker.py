"""Chunking contract for Argus (Architecture §11–12; Phase L8 stub)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class ASTAwareChunker(Protocol):
    """Language-aware chunker; L8 ships a deterministic stub implementation."""

    def chunk_source(self, rel_path: str, source: str, *, max_chunk_chars: int = 256) -> list[str]:
        """Return ordered text chunks for embedding / retrieval."""
        ...


class StubASTAwareChunker:
    """Fixed-width chunks — no tree-sitter dependency (CI-friendly)."""

    def chunk_source(self, rel_path: str, source: str, *, max_chunk_chars: int = 256) -> list[str]:
        _ = rel_path
        if not source:
            return []
        w = max(16, min(max_chunk_chars, 4096))
        return [source[i : i + w] for i in range(0, len(source), w)]
