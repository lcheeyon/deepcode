"""Integration: LangSmith client reachable when API key present (§8.1)."""

from __future__ import annotations

import os

import pytest


@pytest.mark.integration
def test_langsmith_client_lists_projects_or_workspaces() -> None:
    pytest.importorskip("langsmith")
    from langsmith import Client

    if not os.environ.get("LANGSMITH_API_KEY", "").strip():
        pytest.skip("LANGSMITH_API_KEY not set")

    client = Client()
    datasets = list(client.list_datasets(limit=1))
    assert isinstance(datasets, list)
