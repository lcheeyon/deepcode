#!/usr/bin/env python3
"""Dry-run LangSmith-oriented eval (EPIC-DG-11-003 baseline). Run from repo root."""

from __future__ import annotations

import json
import sys

from deepguard_observability.eval_stubs import run_athena_gold_stub_eval


def main() -> int:
    out = run_athena_gold_stub_eval()
    print(json.dumps(out, indent=2))
    return 0 if out.get("passed", True) else 1


if __name__ == "__main__":
    sys.exit(main())
