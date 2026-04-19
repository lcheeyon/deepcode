"""Hermes optional S3/MinIO tarball upload (moto)."""

from __future__ import annotations

from pathlib import Path

import boto3
from deepguard_agents.hermes import HermesAgent
from deepguard_agents.hermes_s3 import ObjectStoreConfig
from moto import mock_aws


@mock_aws
def test_stage_fixture_copy_and_upload_puts_tar_gz(tmp_path: Path) -> None:
    src = tmp_path / "fixture_repo"
    src.mkdir()
    (src / "README.md").write_text("hello", encoding="utf-8")
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="deepguard-dev")

    cfg = ObjectStoreConfig(
        bucket="deepguard-dev",
        access_key_id="test",
        secret_access_key="test",
    )
    agent = HermesAgent(sandbox_root=sandbox)
    out = agent.stage_fixture_copy_and_upload(src, scan_id="scan-e2e", object_store=cfg)

    assert out.repo_metadata["object_store_uploaded"] is True
    assert out.archive_artifact.store == "s3"
    assert out.archive_artifact.key.endswith("/repo.tar.gz")
    head = s3.head_object(Bucket="deepguard-dev", Key=out.archive_artifact.key)
    assert int(head["ContentLength"]) > 0
