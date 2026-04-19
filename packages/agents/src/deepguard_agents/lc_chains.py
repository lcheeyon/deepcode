"""LangChain runnable composition for Athena / Circe (Architecture §7.2)."""

from __future__ import annotations

from typing import Any, cast
from uuid import UUID, uuid4

from deepguard_core.models import Finding, Remediation
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda, RunnableSequence

from deepguard_agents.athena_fake import ComplianceFindingList, fake_athena_batch
from deepguard_agents.lc_budget import _gate_llm_input
from deepguard_agents.lc_schemas import AthenaAgentInput, CirceAgentInput, CirceRemediationDraft


def _as_athena_input(inp: AthenaAgentInput | dict[str, Any]) -> AthenaAgentInput:
    return inp if isinstance(inp, AthenaAgentInput) else AthenaAgentInput.model_validate(inp)


def _budget_athena(inp: AthenaAgentInput | dict[str, Any], config: Any) -> AthenaAgentInput:
    a = _as_athena_input(inp)
    _gate_llm_input(a.model_dump_json(), config)
    return a


def _athena_human_vars(inp: AthenaAgentInput) -> dict[str, str]:
    return {
        "framework": inp.framework,
        "policy_version": inp.policy_version,
        "policy_excerpt": inp.policy_excerpt,
        "control_lines": "\n".join(f"- {c}" for c in inp.control_ids),
    }


def _athena_prompt_with_format() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are Athena. Emit JSON matching the parser instructions exactly.",
            ),
            (
                "human",
                "Framework: {framework}\nPolicy version: {policy_version}\n"
                "Controls:\n{control_lines}\n\nPolicy excerpt:\n{policy_excerpt}\n\n"
                "{format_instructions}",
            ),
        ]
    )


def _athena_prompt_tool() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are Athena. Call the structured tool with the compliance findings batch.",
            ),
            (
                "human",
                "Framework: {framework}\nPolicy version: {policy_version}\n"
                "Controls:\n{control_lines}\n\nPolicy excerpt:\n{policy_excerpt}",
            ),
        ]
    )


def compliance_findings_to_models(
    batch: ComplianceFindingList,
    *,
    scan_id: UUID,
    tenant_id: UUID,
    framework: str,
    policy_version: str,
) -> list[Finding]:
    """Map Athena structured batch items into API ``Finding`` rows."""

    out: list[Finding] = []
    for it in batch.findings:
        out.append(
            Finding(
                scan_id=scan_id,
                tenant_id=tenant_id,
                framework=framework,
                control_id=it.control_id,
                status=it.status,
                severity=it.severity,
                title=it.title,
                evidence_refs=[],
                reasoning_summary=None,
                confidence_score=it.confidence,
                policy_version=policy_version,
            )
        )
    return out


def build_athena_compliance_runnable(
    *,
    chat_model: BaseChatModel | None = None,
    offline: bool = True,
) -> Runnable[AthenaAgentInput | dict[str, Any], ComplianceFindingList]:
    """Return structured ``ComplianceFindingList`` (tool / JSON path per model capabilities)."""

    if offline or chat_model is None:
        return RunnableLambda(
            lambda inp: fake_athena_batch(_as_athena_input(inp).control_ids),
        )

    try:
        structured = chat_model.with_structured_output(ComplianceFindingList)
    except NotImplementedError:
        parser = PydanticOutputParser(pydantic_object=ComplianceFindingList)
        fmt = parser.get_format_instructions()
        prompt = _athena_prompt_with_format().partial(format_instructions=fmt)
        return RunnableSequence(
            RunnableLambda(_budget_athena),
            RunnableLambda(_athena_human_vars),
            prompt,
            chat_model,
            parser,
        )

    prompt = _athena_prompt_tool()
    return RunnableSequence(
        RunnableLambda(_budget_athena),
        RunnableLambda(_athena_human_vars),
        prompt,
        cast(Runnable[Any, ComplianceFindingList], structured),
    )


def _as_circe_input(inp: CirceAgentInput | dict[str, Any]) -> CirceAgentInput:
    return inp if isinstance(inp, CirceAgentInput) else CirceAgentInput.model_validate(inp)


def _budget_circe(inp: CirceAgentInput | dict[str, Any], config: Any) -> CirceAgentInput:
    c = _as_circe_input(inp)
    _gate_llm_input(c.model_dump_json(), config)
    return c


def _circe_vars(inp: CirceAgentInput) -> dict[str, str]:
    return {
        "finding_title": inp.finding_title,
        "code_context": inp.code_context,
    }


def _circe_prompt_with_format() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", "You are Circe. Emit JSON matching the parser instructions exactly."),
            (
                "human",
                "Finding: {finding_title}\n\n"
                "Code / IaC context:\n{code_context}\n\n{format_instructions}",
            ),
        ]
    )


def _circe_prompt_tool() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", "You are Circe. Call the structured tool with the remediation draft."),
            ("human", "Finding: {finding_title}\n\nCode / IaC context:\n{code_context}"),
        ]
    )


def _offline_circe_draft(inp: CirceAgentInput | dict[str, Any]) -> CirceRemediationDraft:
    c = _as_circe_input(inp)
    return CirceRemediationDraft(
        title=f"Stub remediation for {c.finding_title[:120]}",
        diff_preview="--- a/file.tf\n+++ b/file.tf\n@@ -1,1 +1,1 @@\n- old\n+ new\n",
        finding_id=c.finding_id,
    )


def circe_draft_to_remediation(
    draft: CirceRemediationDraft,
    *,
    scan_id: UUID,
    remediation_id: UUID | None = None,
) -> Remediation:
    return Remediation(
        id=remediation_id or uuid4(),
        scan_id=scan_id,
        finding_id=draft.finding_id,
        title=draft.title,
        diff_preview=draft.diff_preview,
        terraform_validate_exit_code=None,
    )


def build_circe_remediation_runnable(
    *,
    chat_model: BaseChatModel | None = None,
    offline: bool = True,
) -> Runnable[CirceAgentInput | dict[str, Any], CirceRemediationDraft]:
    """Return structured ``CirceRemediationDraft``."""

    if offline or chat_model is None:
        return RunnableLambda(_offline_circe_draft)

    try:
        structured = chat_model.with_structured_output(CirceRemediationDraft)
    except NotImplementedError:
        parser = PydanticOutputParser(pydantic_object=CirceRemediationDraft)
        cfmt = parser.get_format_instructions()
        prompt = _circe_prompt_with_format().partial(format_instructions=cfmt)
        return RunnableSequence(
            RunnableLambda(_budget_circe),
            RunnableLambda(_circe_vars),
            prompt,
            chat_model,
            parser,
        )

    prompt = _circe_prompt_tool()
    return RunnableSequence(
        RunnableLambda(_budget_circe),
        RunnableLambda(_circe_vars),
        prompt,
        cast(Runnable[Any, CirceRemediationDraft], structured),
    )


def build_athena_to_findings_runnable(
    *,
    chat_model: BaseChatModel | None = None,
    offline: bool = True,
) -> Runnable[AthenaAgentInput | dict[str, Any], list[Finding]]:
    """Athena runnable composed with row mapping into ``Finding`` list."""

    base = build_athena_compliance_runnable(chat_model=chat_model, offline=offline)

    def _pair(inp: AthenaAgentInput | dict[str, Any], config: RunnableConfig) -> list[Finding]:
        a = _as_athena_input(inp)
        batch = base.invoke(a, config=config)
        return compliance_findings_to_models(
            batch,
            scan_id=a.scan_id,
            tenant_id=a.tenant_id,
            framework=a.framework,
            policy_version=a.policy_version,
        )

    return RunnableLambda(_pair)


def build_circe_to_remediation_runnable(
    *,
    chat_model: BaseChatModel | None = None,
    offline: bool = True,
) -> Runnable[CirceAgentInput | dict[str, Any], Remediation]:
    base = build_circe_remediation_runnable(chat_model=chat_model, offline=offline)

    def _pair(inp: CirceAgentInput | dict[str, Any], config: RunnableConfig) -> Remediation:
        c = _as_circe_input(inp)
        draft = base.invoke(c, config=config)
        return circe_draft_to_remediation(draft, scan_id=c.scan_id)

    return RunnableLambda(_pair)
