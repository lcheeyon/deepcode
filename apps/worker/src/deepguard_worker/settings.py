"""Worker environment (Phase L4 + Hermes ingestion)."""

from __future__ import annotations

import os
from dataclasses import dataclass

from deepguard_agents.hermes_ingest import HermesRuntimeConfig
from deepguard_agents.hermes_s3 import ObjectStoreConfig


def _env(*names: str) -> str:
    for n in names:
        v = os.environ.get(n, "").strip()
        if v:
            return v
    return ""


@dataclass(frozen=True, slots=True)
class WorkerSettings:
    database_url: str
    redis_url: str
    consumer_name: str
    heartbeat_interval_sec: float
    stub_iterations: int
    hermes_enabled: bool
    repo_max_bytes: int
    repo_clone_depth: int
    s3_bucket: str | None
    s3_region: str
    s3_endpoint_url: str | None
    s3_access_key_id: str | None
    s3_secret_access_key: str | None

    def hermes_runtime(self) -> HermesRuntimeConfig:
        s3: ObjectStoreConfig | None = None
        if self.s3_bucket and self.s3_access_key_id and self.s3_secret_access_key:
            s3 = ObjectStoreConfig(
                bucket=self.s3_bucket,
                access_key_id=self.s3_access_key_id,
                secret_access_key=self.s3_secret_access_key,
                endpoint_url=self.s3_endpoint_url,
                region_name=self.s3_region,
            )
        return HermesRuntimeConfig(
            enabled=self.hermes_enabled,
            repo_max_bytes=self.repo_max_bytes,
            clone_depth=self.repo_clone_depth,
            s3=s3,
        )


def load_worker_settings() -> WorkerSettings:
    db = os.environ["DATABASE_URL"].strip()
    rurl = os.environ["REDIS_URL"].strip()
    name = os.environ.get("DEEPGUARD_WORKER_CONSUMER", f"worker-{os.getpid()}")
    hb = float(os.environ.get("DEEPGUARD_WORKER_HEARTBEAT_SEC", "30"))
    iters = int(os.environ.get("DEEPGUARD_WORKER_STUB_ITERATIONS", "0"))
    hermes_on = _env("DEEPGUARD_HERMES_ENABLED").lower() in ("1", "true", "yes")
    rmax = int(_env("DEEPGUARD_REPO_MAX_BYTES") or str(2_147_483_648))
    depth = int(_env("DEEPGUARD_REPO_CLONE_DEPTH") or "50")
    bucket = _env("DEEPGUARD_S3_BUCKET", "AWS_S3_BUCKET") or None
    region = _env("DEEPGUARD_S3_REGION", "AWS_REGION", "AWS_DEFAULT_REGION") or "us-east-1"
    endpoint = _env("DEEPGUARD_S3_ENDPOINT_URL", "AWS_ENDPOINT_URL_S3") or None
    ak = _env("DEEPGUARD_S3_ACCESS_KEY_ID", "AWS_ACCESS_KEY_ID") or None
    sk = _env("DEEPGUARD_S3_SECRET_ACCESS_KEY", "AWS_SECRET_ACCESS_KEY") or None
    return WorkerSettings(
        database_url=db,
        redis_url=rurl,
        consumer_name=name,
        heartbeat_interval_sec=hb,
        stub_iterations=iters,
        hermes_enabled=hermes_on,
        repo_max_bytes=rmax,
        repo_clone_depth=depth,
        s3_bucket=bucket,
        s3_region=region,
        s3_endpoint_url=endpoint,
        s3_access_key_id=ak,
        s3_secret_access_key=sk,
    )
