"""Dependency graph caps (Architecture §23.1)."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any


def cap_dependency_graph_depth(
    graph: dict[str, Any],
    *,
    max_depth: int = 6,
) -> dict[str, Any]:
    """Return a shallow copy with ``truncated`` if any simple path exceeds ``max_depth``.

    Expected shape::

        {
          "nodes": [{"id": "a"}, ...],
          "edges": [{"from": "a", "to": "b"}, ...],
        }
    """

    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    id_set = {str(n["id"]) for n in nodes if isinstance(n, dict) and "id" in n}
    adj: dict[str, list[str]] = defaultdict(list)
    indeg: dict[str, int] = defaultdict(int)
    for e in edges:
        if not isinstance(e, dict):
            continue
        a, b = e.get("from"), e.get("to")
        if a is None or b is None:
            continue
        sa, sb = str(a), str(b)
        if sa not in id_set or sb not in id_set:
            continue
        adj[sa].append(sb)
        indeg[sb] += 1
        indeg.setdefault(sa, indeg.get(sa, 0))
    roots = [n for n in id_set if indeg.get(n, 0) == 0] or list(id_set)

    max_seen = 0
    for r in roots:
        dq: deque[tuple[str, int]] = deque([(r, 0)])
        seen: set[str] = set()
        while dq:
            nid, d = dq.popleft()
            if nid in seen:
                continue
            seen.add(nid)
            max_seen = max(max_seen, d)
            for nxt in adj.get(nid, ()):
                dq.append((nxt, d + 1))

    out = dict(graph)
    out["truncated"] = bool(max_seen > max_depth)
    out["max_depth_observed"] = max_seen
    return out
