"""§28.4 CreateScanRequest / ScanJobConfig validation (AC-DG-02-001-02/03)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import cast

import pytest
from deepguard_core.models import (
    AgentError,
    AgentErrorSeverity,
    BudgetConfig,
    CloudProfile,
    CloudProvider,
    CreateScanRequest,
    Finding,
    FindingAssessmentStatus,
    FindingSeverity,
    NotificationSettings,
    PolicyControl,
    RepoSpec,
    ScanJobConfig,
    ScanLayer,
    ScanLayers,
    ScanStatePartial,
    WebhookEvent,
)
from pydantic import AnyHttpUrl, ValidationError


def _repo() -> RepoSpec:
    return RepoSpec(url=cast(AnyHttpUrl, "https://github.com/acme/svc"), ref="main")


def _layers(**kwargs: bool) -> ScanLayers:
    return ScanLayers(
        code=kwargs.get("code", False),
        iac=kwargs.get("iac", False),
        cloud=kwargs.get("cloud", False),
    )


def _policies() -> list[str]:
    return ["ISO-27001-2022"]


def test_cloud_only_with_profiles_no_repo_ok() -> None:
    req = CreateScanRequest(
        repo=None,
        policy_ids=_policies(),
        scan_layers=_layers(cloud=True),
        cloud_profiles=[
            CloudProfile(
                profile_id="aws-1",
                provider=CloudProvider.AWS,
                connector_credential_ref="calypso://secret/x",
                regions=["ap-southeast-1"],
            )
        ],
    )
    assert req.repo is None
    assert req.scan_layers.cloud is True


def test_cloud_with_repo_only_no_profiles_ok() -> None:
    req = CreateScanRequest(
        repo=_repo(),
        policy_ids=_policies(),
        scan_layers=_layers(cloud=True),
        cloud_profiles=[],
    )
    assert req.cloud_profiles == []


def test_code_requires_repo() -> None:
    with pytest.raises(ValidationError) as exc:
        CreateScanRequest(
            repo=None,
            policy_ids=_policies(),
            scan_layers=_layers(code=True),
        )
    assert "scan_layers.code" in str(exc.value).lower() or "repo" in str(exc.value).lower()


def test_iac_requires_repo() -> None:
    with pytest.raises(ValidationError) as exc:
        CreateScanRequest(
            repo=None,
            policy_ids=_policies(),
            scan_layers=_layers(iac=True),
        )
    assert "repo" in str(exc.value).lower()


def test_cloud_requires_repo_or_profiles() -> None:
    with pytest.raises(ValidationError) as exc:
        CreateScanRequest(
            repo=None,
            policy_ids=_policies(),
            scan_layers=_layers(cloud=True),
            cloud_profiles=[],
        )
    assert "cloud_profiles" in str(exc.value) or "repo" in str(exc.value)


def test_all_layers_false_rejected() -> None:
    with pytest.raises(ValidationError) as exc:
        CreateScanRequest(
            repo=_repo(),
            policy_ids=_policies(),
            scan_layers=ScanLayers(code=False, iac=False, cloud=False),
        )
    assert "scan_layers" in str(exc.value).lower() or "layer" in str(exc.value).lower()


def test_empty_policy_ids_rejected() -> None:
    with pytest.raises(ValidationError):
        CreateScanRequest(
            repo=_repo(),
            policy_ids=[],
            scan_layers=_layers(code=True),
        )


def test_scan_job_config_alias_same_model() -> None:
    assert ScanJobConfig is CreateScanRequest


def test_optional_notifications_and_budget() -> None:
    req = CreateScanRequest(
        repo=_repo(),
        policy_ids=_policies(),
        scan_layers=_layers(code=True, iac=True),
        notifications=NotificationSettings(
            webhook_url=cast(AnyHttpUrl, "https://hooks.example.com/dg"),
            on=[WebhookEvent.COMPLETED, WebhookEvent.FAILED],
        ),
        budget=BudgetConfig(max_llm_usd=10.0, max_wall_seconds=7200),
    )
    assert req.notifications is not None
    assert req.budget is not None
    assert req.budget.max_wall_seconds == 7200


def test_scan_state_partial_roundtrip() -> None:
    sid = uuid.uuid4()
    cfg = CreateScanRequest(
        repo=_repo(),
        policy_ids=_policies(),
        scan_layers=_layers(code=True),
    )
    err = AgentError(agent="hermes", code="CLONE_TIMEOUT", message="timed out")
    state = ScanStatePartial(
        scan_id=sid,
        created_at=datetime.now(UTC),
        job_config=cfg,
        error_log=[err],
        should_abort=False,
    )
    data = state.model_dump(mode="json")
    restored = ScanStatePartial.model_validate(data)
    assert restored.scan_id == sid
    assert restored.error_log[0].severity == AgentErrorSeverity.RECOVERABLE


def test_finding_model_validation() -> None:
    f = Finding(
        scan_id=uuid.uuid4(),
        framework="ISO-27001-2022",
        control_id="A.8.1.4",
        status=FindingAssessmentStatus.FAIL,
        severity=FindingSeverity.HIGH,
        title="Weak TLS",
        evidence_refs=[{"path": "tls.py", "line": 12}],
        confidence_score=0.91,
        policy_version="2024-01",
    )
    assert f.evidence_refs[0]["path"] == "tls.py"


def test_policy_control_requires_layer_relevance() -> None:
    pc = PolicyControl(
        control_id="A.1.2",
        framework="ISO-27001-2022",
        title="Access control policy",
        description="Organisation shall document access control policy.",
        layer_relevance=[ScanLayer.CODE, ScanLayer.IAC],
        severity_weight=1.5,
    )
    assert ScanLayer.CLOUD not in pc.layer_relevance


def test_finding_confidence_out_of_range() -> None:
    with pytest.raises(ValidationError):
        Finding(
            scan_id=uuid.uuid4(),
            framework="X",
            control_id="Y",
            status=FindingAssessmentStatus.PASS,
            severity=FindingSeverity.INFO,
            title="t",
            confidence_score=1.5,
            policy_version="1",
        )


def test_json_roundtrip_create_scan() -> None:
    raw = {
        "repo": {"url": "https://gitlab.com/g/p.git", "ref": "develop"},
        "policy_ids": ["GB-T-22239-2019"],
        "scan_layers": {"code": True, "iac": False, "cloud": False},
    }
    m = CreateScanRequest.model_validate(raw)
    assert m.repo is not None
    assert str(m.repo.url).startswith("https://gitlab.com/")
    assert m.repo.source == "git"


def test_archive_repo_scan_requires_storage_uri() -> None:
    req = CreateScanRequest(
        repo=RepoSpec(
            source="archive",
            storage_uri="s3://deepguard-dev/uploads/t/u/repo.tar.gz",
        ),
        policy_ids=["ISO-27001-2022"],
        scan_layers=ScanLayers(code=True, iac=False, cloud=False),
    )
    assert req.repo is not None
    assert req.repo.source == "archive"
    assert req.repo.storage_uri.startswith("s3://")


def test_git_repo_rejects_storage_uri() -> None:
    with pytest.raises(ValidationError):
        RepoSpec(
            source="git",
            url=cast(AnyHttpUrl, "https://github.com/acme/svc"),
            ref="main",
            storage_uri="s3://b/k",
        )
