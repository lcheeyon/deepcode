"""EPIC-DG-11 callback factory and LangSmith default rules."""

from __future__ import annotations

import os

from deepguard_observability.llm_callbacks import (
    build_langchain_callbacks,
    graph_invoke_config,
    langfuse_tracing_enabled,
    langsmith_tracing_effective,
    observability_feature_matrix,
)
from deepguard_observability.runtime import configure_langsmith_env_defaults


def test_langfuse_enabled_only_with_host_and_keys(monkeypatch) -> None:
    monkeypatch.delenv("LANGFUSE_HOST", raising=False)
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    assert langfuse_tracing_enabled() is False
    monkeypatch.setenv("LANGFUSE_HOST", "http://localhost:3000")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk")
    assert langfuse_tracing_enabled() is True


def test_graph_invoke_config_metadata(monkeypatch) -> None:
    monkeypatch.delenv("LANGFUSE_HOST", raising=False)
    cfg = graph_invoke_config(
        scan_id="s1",
        tenant_id="t1",
        callbacks=None,
        run_name="test-run",
        idempotency_key="ik-1",
        graph_version="0.1.0",
        redis_message_id="r99",
    )
    assert cfg["configurable"]["thread_id"] == "s1"
    assert cfg["metadata"]["scan_id"] == "s1"
    assert cfg["metadata"]["deepguard.run_name"] == "test-run"
    assert cfg["metadata"]["idempotency_key"] == "ik-1"
    assert cfg["metadata"]["deepguard.graph_version"] == "0.1.0"
    assert cfg["metadata"]["deepguard.correlation_id"] == "s1:r99"
    assert cfg["configurable"]["deepguard.correlation_id"] == "s1:r99"


def test_langsmith_tracing_effective_respects_env(monkeypatch) -> None:
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "true")
    monkeypatch.setenv("LANGSMITH_API_KEY", "x")
    assert langsmith_tracing_effective() is True
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "false")
    assert langsmith_tracing_effective() is False


def test_observability_feature_matrix_keys(monkeypatch) -> None:
    monkeypatch.delenv("LANGSMITH_API_KEY", raising=False)
    monkeypatch.delenv("LANGCHAIN_API_KEY", raising=False)
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "false")
    monkeypatch.delenv("LANGFUSE_HOST", raising=False)
    m = observability_feature_matrix()
    assert m["langsmith_effective"] == "off"
    assert m["langfuse_callbacks"] == "off"


def test_build_callbacks_empty_without_langfuse(monkeypatch) -> None:
    monkeypatch.delenv("LANGFUSE_HOST", raising=False)
    assert build_langchain_callbacks(scan_id="a", tenant_id="b") == []


def test_configure_langsmith_defaults_respects_explicit_false(monkeypatch) -> None:
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "false")
    monkeypatch.delenv("CI", raising=False)
    configure_langsmith_env_defaults()
    assert os.environ["LANGCHAIN_TRACING_V2"] == "false"


def test_configure_langsmith_defaults_forces_off_in_ci(monkeypatch) -> None:
    monkeypatch.delenv("LANGCHAIN_TRACING_V2", raising=False)
    monkeypatch.setenv("CI", "true")
    configure_langsmith_env_defaults()
    assert os.environ["LANGCHAIN_TRACING_V2"] == "false"


def test_configure_langsmith_defaults_on_locally(monkeypatch) -> None:
    monkeypatch.delenv("LANGCHAIN_TRACING_V2", raising=False)
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.delenv("DEEPGUARD_AIR_GAP", raising=False)
    configure_langsmith_env_defaults()
    assert os.environ["LANGCHAIN_TRACING_V2"] == "true"
