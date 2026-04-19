"""Integration: OpenAI ``with_structured_output`` for Athena (optional package + API key)."""

from __future__ import annotations

import os
import uuid

import pytest


@pytest.mark.integration
def test_openai_athena_structured_output_minimal() -> None:
    pytest.importorskip("langchain_openai")
    from deepguard_agents.lc_chains import build_athena_compliance_runnable
    from deepguard_agents.lc_schemas import AthenaAgentInput
    from langchain_openai import ChatOpenAI

    if not os.environ.get("OPENAI_API_KEY", "").strip():
        pytest.skip("OPENAI_API_KEY not set")

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = build_athena_compliance_runnable(chat_model=model, offline=False)
    inp = AthenaAgentInput(
        scan_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        framework="TEST",
        policy_version="0",
        control_ids=["CTRL-DEMO-1"],
        policy_excerpt="All systems must enable audit logging.",
    )
    out = chain.invoke(inp)
    assert out.findings
    assert out.findings[0].control_id == "CTRL-DEMO-1"
