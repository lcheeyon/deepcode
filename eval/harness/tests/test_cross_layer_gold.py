"""Gold expectations for Athena fake batch (Architecture §7.3 direction, Phase L10)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

from deepguard_agents.athena_fake import fake_athena_batch
from deepguard_core.models.enums import FindingAssessmentStatus


def _gold_path() -> Path:
    return Path(__file__).resolve().parents[1] / "fixtures" / "athena_gold_sample.jsonl"


def test_cross_layer_gold_matches_fake_athena_batch() -> None:
    """Each JSONL row defines expected control outcome for ``LLM_MODE=fake`` stub."""

    rows: list[dict[str, object]] = []
    for line in _gold_path().read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))

    for row in rows:
        cid = str(row["control_id"])
        want = FindingAssessmentStatus(str(row["expected_status"]))
        min_conf = float(cast(str | int | float, row["min_confidence"]))
        out = fake_athena_batch([cid])
        assert len(out.findings) == 1
        f0 = out.findings[0]
        assert f0.control_id == cid
        assert f0.status == want
        assert f0.confidence >= min_conf
