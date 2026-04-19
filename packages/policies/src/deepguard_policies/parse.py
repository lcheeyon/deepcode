"""YAML / JSON policy fixture parser → ``PolicyControl`` (Phase L7)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml
from deepguard_core.models.agent_error import AgentError, AgentRuntimeError
from deepguard_core.models.enums import AgentErrorSeverity, EvidenceType, ScanLayer
from deepguard_core.models.policy_control import PolicyControl


@dataclass(frozen=True, slots=True)
class PolicyParseResult:
    """Outputs consumed by Tiresias / Athena."""

    controls: list[PolicyControl]
    policy_version: str


def _layer(s: str) -> ScanLayer:
    return ScanLayer(s.strip().upper())


def _evidence_types(items: object) -> list[EvidenceType]:
    out: list[EvidenceType] = []
    if not isinstance(items, list):
        return out
    for x in items:
        try:
            out.append(EvidenceType(str(x)))
        except ValueError:
            continue
    return out


def parse_policy_file(path: Path) -> PolicyParseResult:
    """Parse DeepGuard fixture YAML with ``framework``, ``version``, ``controls`` list."""

    raw = path.read_bytes()
    try:
        doc = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise AgentRuntimeError(
            AgentError(
                agent="tiresias",
                code="POLICY_YAML_INVALID",
                message=str(exc)[:4096],
                severity=AgentErrorSeverity.RECOVERABLE,
            )
        ) from exc
    if not isinstance(doc, dict):
        raise AgentRuntimeError(
            AgentError(
                agent="tiresias",
                code="POLICY_ROOT_NOT_OBJECT",
                message="Policy file must contain a mapping at the root.",
                severity=AgentErrorSeverity.RECOVERABLE,
            )
        )
    fw = str(doc.get("framework", "")).strip()
    ver = str(doc.get("version", "0")).strip()
    ctrs = doc.get("controls")
    if not fw or not isinstance(ctrs, list) or not ctrs:
        raise AgentRuntimeError(
            AgentError(
                agent="tiresias",
                code="POLICY_MISSING_FIELDS",
                message="Policy requires non-empty ``framework`` and ``controls``.",
                severity=AgentErrorSeverity.RECOVERABLE,
            )
        )
    out: list[PolicyControl] = []
    for i, c in enumerate(ctrs):
        if not isinstance(c, dict):
            raise AgentRuntimeError(
                AgentError(
                    agent="tiresias",
                    code=f"POLICY_CONTROL_NOT_OBJECT_{i}",
                    message="Each control must be a mapping.",
                    severity=AgentErrorSeverity.RECOVERABLE,
                )
            )
        try:
            layers = [_layer(x) for x in c.get("layer_relevance", ["CODE"])]
            out.append(
                PolicyControl(
                    control_id=str(c["control_id"]),
                    framework=fw,
                    title=str(c["title"]),
                    description=str(c.get("description", c["title"])),
                    scope_tags=list(c.get("scope_tags", [])),
                    layer_relevance=layers,
                    severity_weight=float(c.get("severity_weight", 1.0)),
                    test_procedures=list(c.get("test_procedures", [])),
                    evidence_types=_evidence_types(c.get("evidence_types", [])),
                )
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise AgentRuntimeError(
                AgentError(
                    agent="tiresias",
                    code=f"POLICY_CONTROL_INVALID_{i}",
                    message=str(exc)[:4096],
                    severity=AgentErrorSeverity.RECOVERABLE,
                )
            ) from exc
    if not out:
        raise AgentRuntimeError(
            AgentError(
                agent="tiresias",
                code="POLICY_NO_CONTROLS",
                message="No valid controls parsed from file.",
                severity=AgentErrorSeverity.RECOVERABLE,
            )
        )
    return PolicyParseResult(controls=out, policy_version=ver)
