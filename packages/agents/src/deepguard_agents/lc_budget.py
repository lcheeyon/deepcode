"""Centralised token / call budget guardrails for LLM runnables (Architecture §7.2)."""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

from langchain_core.runnables import RunnableConfig, RunnableLambda


class BudgetExceededError(RuntimeError):
    """Raised when an LLM path exceeds configured DeepGuard runtime limits."""


@dataclass
class LLMRuntimeBudget:
    """Process-local budget counters (use ``llm_budget_context`` in tests / workers)."""

    max_estimated_tokens: int | None = None
    max_llm_calls: int | None = None
    estimated_tokens_used: int = 0
    llm_calls_used: int = 0


llm_budget_context: ContextVar[LLMRuntimeBudget | None] = ContextVar(
    "deepguard_llm_budget",
    default=None,
)


def estimate_tokens(text: str) -> int:
    """Rough input token estimate (cheap guardrail; not a tokenizer)."""

    return max(1, len(text) // 4)


def _gate_llm_input(x: Any, config: RunnableConfig) -> Any:
    """Pre-model hook: count calls + estimated input tokens against ``llm_budget_context``."""

    _ = config
    b = llm_budget_context.get()
    if b is None:
        return x
    if b.max_llm_calls is not None and b.llm_calls_used >= b.max_llm_calls:
        msg = "LLM call budget exceeded"
        raise BudgetExceededError(msg)
    b.llm_calls_used += 1
    est = estimate_tokens(str(x))
    if (
        b.max_estimated_tokens is not None
        and b.estimated_tokens_used + est > b.max_estimated_tokens
    ):
        msg = "Estimated token budget exceeded"
        raise BudgetExceededError(msg)
    b.estimated_tokens_used += est
    return x


def llm_budget_gate() -> RunnableLambda[Any, Any]:
    """Return a passthrough runnable that enforces ``LLMRuntimeBudget`` when set."""

    return RunnableLambda(_gate_llm_input)


def apply_usd_charge(*, usd: float, config: RunnableConfig | None = None) -> None:
    """Optional USD accounting hook (metadata only; extend for billing pipelines)."""

    if usd <= 0 or config is None:
        return
    meta = config.get("metadata")
    if not isinstance(meta, dict):
        return
    raw = meta.get("deepguard.llm_spend_usd", 0.0)
    prev = float(raw) if isinstance(raw, (int, float, str)) else 0.0
    meta["deepguard.llm_spend_usd"] = prev + usd
