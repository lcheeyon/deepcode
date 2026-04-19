"""Hermes worker phase — skip paths (no live git / S3)."""

from __future__ import annotations

import uuid
from typing import cast

from deepguard_agents.hermes_ingest import HermesRuntimeConfig, run_hermes_phase
from deepguard_core.models import CloudProfile, CreateScanRequest, RepoSpec, ScanLayers
from deepguard_core.models.enums import CloudProvider
from pydantic import AnyHttpUrl


def test_hermes_skips_when_disabled_even_without_s3() -> None:
    body = CreateScanRequest(
        repo=RepoSpec(url=cast(AnyHttpUrl, "https://github.com/acme/svc"), ref="main"),
        policy_ids=["ISO-27001-2022"],
        scan_layers=ScanLayers(code=True, iac=False, cloud=False),
    )
    cfg = HermesRuntimeConfig(enabled=False, repo_max_bytes=100, clone_depth=1, s3=None)
    out = run_hermes_phase(
        body.model_dump(mode="json"),
        tenant_id="t",
        scan_id=str(uuid.uuid4()),
        cfg=cfg,
    )
    assert out is None


def test_hermes_skips_cloud_only_scan() -> None:
    body = CreateScanRequest(
        repo=None,
        policy_ids=["ISO-27001-2022"],
        scan_layers=ScanLayers(code=False, iac=False, cloud=True),
        cloud_profiles=[
            CloudProfile(
                profile_id="p",
                provider=CloudProvider.AWS,
                connector_credential_ref="calypso://x",
                regions=["us-east-1"],
            )
        ],
    )
    cfg = HermesRuntimeConfig(enabled=True, repo_max_bytes=100, clone_depth=1, s3=None)
    out = run_hermes_phase(
        body.model_dump(mode="json"),
        tenant_id="t",
        scan_id=str(uuid.uuid4()),
        cfg=cfg,
    )
    assert out is None
