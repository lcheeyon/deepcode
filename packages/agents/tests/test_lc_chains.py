"""Unit tests for LangChain Athena / Circe runnables (Architecture §7.2)."""

from __future__ import annotations

import uuid

import pytest
from deepguard_agents.athena_fake import ComplianceFindingItem, ComplianceFindingList
from deepguard_agents.lc_budget import BudgetExceededError, LLMRuntimeBudget, llm_budget_context
from deepguard_agents.lc_chains import (
    build_athena_compliance_runnable,
    build_athena_to_findings_runnable,
    build_circe_remediation_runnable,
    build_circe_to_remediation_runnable,
    circe_draft_to_remediation,
    compliance_findings_to_models,
)
from deepguard_agents.lc_schemas import AthenaAgentInput, CirceAgentInput
from deepguard_core.models.enums import FindingAssessmentStatus, FindingSeverity
from langchain_core.language_models.fake_chat_models import FakeListChatModel


def _athena_inp() -> AthenaAgentInput:
    return AthenaAgentInput(
        scan_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        framework="ISO-27001",
        policy_version="2022",
        control_ids=["AC-1", "AC-2"],
        policy_excerpt="Access control policy text.",
    )


def test_offline_athena_returns_compliance_list() -> None:
    chain = build_athena_compliance_runnable(offline=True)
    out = chain.invoke(_athena_inp())
    assert isinstance(out, ComplianceFindingList)
    assert {f.control_id for f in out.findings} == {"AC-1", "AC-2"}


def test_fake_chat_model_json_path_matches_parser() -> None:
    batch = ComplianceFindingList(
        findings=[
            ComplianceFindingItem(
                control_id="Z",
                status=FindingAssessmentStatus.PARTIAL,
                severity=FindingSeverity.HIGH,
                title="z-title",
                confidence=0.9,
            )
        ]
    )
    model = FakeListChatModel(responses=[batch.model_dump_json()])
    chain = build_athena_compliance_runnable(chat_model=model, offline=False)
    out = chain.invoke(_athena_inp())
    assert out.findings[0].control_id == "Z"
    assert out.findings[0].title == "z-title"


def test_athena_to_findings_mapping() -> None:
    chain = build_athena_to_findings_runnable(offline=True)
    rows = chain.invoke(_athena_inp())
    assert len(rows) == 2
    assert rows[0].framework == "ISO-27001"
    assert rows[0].policy_version == "2022"


def test_offline_circe_draft_and_remediation() -> None:
    cid = uuid.uuid4()
    inp = CirceAgentInput(
        scan_id=cid,
        finding_id=None,
        finding_title="Open SG",
        code_context="resource aws_security_group",
    )
    draft = build_circe_remediation_runnable(offline=True).invoke(inp)
    rem = circe_draft_to_remediation(draft, scan_id=cid)
    assert rem.scan_id == cid
    assert rem.diff_preview.startswith("---")


def test_circe_end_to_end_runnable() -> None:
    cid = uuid.uuid4()
    inp = CirceAgentInput(scan_id=cid, finding_title="x", code_context="y")
    rem = build_circe_to_remediation_runnable(offline=True).invoke(inp)
    assert rem.scan_id == cid


def test_compliance_findings_to_models_control_ids() -> None:
    sid = uuid.uuid4()
    tid = uuid.uuid4()
    batch = ComplianceFindingList(
        findings=[
            ComplianceFindingItem(
                control_id="c1",
                status=FindingAssessmentStatus.PASS,
                severity=FindingSeverity.INFO,
                title="t",
                confidence=0.5,
            )
        ]
    )
    rows = compliance_findings_to_models(
        batch,
        scan_id=sid,
        tenant_id=tid,
        framework="F",
        policy_version="v",
    )
    assert rows[0].scan_id == sid
    assert rows[0].tenant_id == tid


def test_budget_gate_exceeds_on_second_llm_call() -> None:
    from deepguard_agents.lc_budget import llm_budget_gate

    tok = llm_budget_context.set(LLMRuntimeBudget(max_llm_calls=1))
    try:
        gate = llm_budget_gate()
        gate.invoke("a", config={})
        with pytest.raises(BudgetExceededError):
            gate.invoke("b", config={})
    finally:
        llm_budget_context.reset(tok)


def test_athena_online_chain_respects_token_budget() -> None:
    batch = ComplianceFindingList(
        findings=[
            ComplianceFindingItem(
                control_id="Z",
                status=FindingAssessmentStatus.PARTIAL,
                severity=FindingSeverity.HIGH,
                title="t",
                confidence=0.5,
            )
        ]
    )
    model = FakeListChatModel(responses=[batch.model_dump_json()])
    tok = llm_budget_context.set(LLMRuntimeBudget(max_estimated_tokens=2))
    try:
        chain = build_athena_compliance_runnable(chat_model=model, offline=False)
        inp = _athena_inp().model_copy(update={"policy_excerpt": "word " * 200})
        with pytest.raises(BudgetExceededError):
            chain.invoke(inp)
    finally:
        llm_budget_context.reset(tok)


def test_apply_usd_charge_accumulates_metadata() -> None:
    from deepguard_agents.lc_budget import apply_usd_charge

    cfg: dict = {"metadata": {}}
    apply_usd_charge(usd=0.01, config=cfg)
    apply_usd_charge(usd=0.02, config=cfg)
    assert cfg["metadata"]["deepguard.llm_spend_usd"] == pytest.approx(0.03)
