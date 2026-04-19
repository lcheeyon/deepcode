"""Retrieval helpers with in-process caching (Architecture §7.2; pgvector planned in §4)."""

from __future__ import annotations

from collections.abc import Callable, Hashable
from typing import Any, TypeVar

from langchain_core.runnables import RunnableLambda

T = TypeVar("T")


class PolicyExcerptCache:
    """Tiny excerpt cache for repeated policy slices (LangChain-style dedup; in-memory)."""

    def __init__(self) -> None:
        self._data: dict[tuple[Hashable, ...], str] = {}

    def get_or_set(self, key: tuple[Hashable, ...], factory: Callable[[], str]) -> str:
        if key not in self._data:
            self._data[key] = factory()
        return self._data[key]

    def clear(self) -> None:
        self._data.clear()


def policy_excerpt_runnable(cache: PolicyExcerptCache) -> RunnableLambda[Any, str]:
    """Build a ``Runnable`` that returns a cached policy excerpt for ``(policy_id, ref)``."""

    def _load(inp: Any) -> str:
        if not isinstance(inp, dict):
            msg = "policy_excerpt_runnable expects dict input with policy_id and ref"
            raise TypeError(msg)
        policy_id = str(inp.get("policy_id") or "")
        ref = str(inp.get("ref") or "")
        key = (policy_id, ref)

        def factory() -> str:
            raw = inp.get("body")
            if callable(raw):
                return str(raw())
            return str(raw or "")

        return cache.get_or_set(key, factory)

    return RunnableLambda(_load)


def fake_embedding_vector(text: str, *, dimensions: int = 8) -> list[float]:
    """Deterministic pseudo-embedding for tests (replace with pgvector-backed model)."""

    mix = sum(ord(c) * (i + 1) for i, c in enumerate(text)) + len(text) * 31
    base = float(mix % 997) / 1000.0
    return [round(base + i * 0.01, 4) for i in range(dimensions)]


def fake_embedding_runnable(*, dimensions: int = 8) -> RunnableLambda[str, list[float]]:
    """Runnable that maps query text → fixed-width vector (offline / CI)."""

    return RunnableLambda(lambda q: fake_embedding_vector(str(q), dimensions=dimensions))
