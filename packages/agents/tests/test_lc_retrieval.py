"""Unit tests for retrieval / embedding helpers (Architecture §7.2)."""

from __future__ import annotations

from deepguard_agents.lc_retrieval import (
    PolicyExcerptCache,
    fake_embedding_runnable,
    fake_embedding_vector,
    policy_excerpt_runnable,
)


def test_policy_excerpt_cache_dedupes() -> None:
    cache = PolicyExcerptCache()
    r = policy_excerpt_runnable(cache)
    calls = {"n": 0}

    def body() -> str:
        calls["n"] += 1
        return "long policy text"

    inp = {"policy_id": "p1", "ref": "r1", "body": body}
    assert r.invoke(inp) == "long policy text"
    assert r.invoke(inp) == "long policy text"
    assert calls["n"] == 1


def test_fake_embedding_vector_deterministic() -> None:
    a = fake_embedding_vector("hello", dimensions=4)
    b = fake_embedding_vector("hello", dimensions=4)
    c = fake_embedding_vector("hellp", dimensions=4)
    assert a == b
    assert a != c


def test_fake_embedding_runnable() -> None:
    r = fake_embedding_runnable(dimensions=3)
    assert r.invoke("x") == fake_embedding_vector("x", dimensions=3)
