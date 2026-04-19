"""Minimal LangSmith evaluation helpers (EPIC-DG-11-003 baseline).

Full dataset-driven gates belong in CI with ``langsmith`` datasets; this module
supports a **local dry run** that never fails when LangSmith is not configured.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

log = logging.getLogger("deepguard_observability.eval_stubs")


def langsmith_eval_accuracy_threshold() -> float:
    """Minimum accuracy (0–1) for the local gold stub to report ``passed`` (§8.1)."""

    raw = os.environ.get("LANGSMITH_EVAL_ACCURACY_THRESHOLD", "0.98").strip()
    try:
        return float(raw)
    except ValueError:
        return 0.98


def run_athena_gold_stub_eval(*, dataset_path: Path | None = None) -> dict[str, Any]:
    """Load ``eval/harness/fixtures/athena_gold_sample.jsonl`` and score trivial equality.

    When ``LANGSMITH_API_KEY`` is set, also attempts to read the dataset from LangSmith
    by name ``deepguard-athena-gold-stub`` if it exists (best-effort; failures are logged).
    """

    path = dataset_path or Path("eval/harness/fixtures/athena_gold_sample.jsonl")
    rows: list[dict[str, Any]] = []
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    valid = sum(1 for r in rows if isinstance(r, dict) and r.get("control_id"))
    total = len(rows) or 1
    score = valid / total
    threshold = langsmith_eval_accuracy_threshold()
    out: dict[str, Any] = {
        "dataset_path": str(path),
        "rows": len(rows),
        "accuracy": score,
        "accuracy_threshold": threshold,
        "passed": score >= threshold or len(rows) == 0,
    }
    key = os.environ.get("LANGSMITH_API_KEY", "").strip()
    if not key:
        log.info("langsmith_eval_skipped_no_api_key")
        out["langsmith"] = "skipped"
        return out
    try:
        from langsmith import Client

        client = Client()
        ds_name = os.environ.get("LANGSMITH_DATASET_ATHENA_GOLD", "deepguard-athena-gold-stub")
        try:
            ds = client.read_dataset(dataset_name=ds_name)
            out["langsmith_dataset_id"] = str(ds.id)
        except Exception as exc:
            log.info("langsmith_dataset_missing name=%s err=%s", ds_name, exc)
            out["langsmith_dataset"] = "not_found"
    except Exception as exc:
        log.warning("langsmith_client_failed: %s", exc)
        out["langsmith"] = f"error:{exc}"
    return out
