#!/usr/bin/env python3
"""
Generate BDD stub feature files from docs/user-stories/traceability-ac-detail-matrix.csv.

Outputs:
  docs/user-stories/bdd-stubs/EPIC-DG-XX.feature (grouped by epic)

Run:
  python3 scripts/generate_bdd_stubs_from_traceability.py
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_STORIES = ROOT / "docs" / "user-stories"
MATRIX = USER_STORIES / "traceability-ac-detail-matrix.csv"
OUT = USER_STORIES / "bdd-stubs"

EPIC_NUM = re.compile(r"EPIC-DG-(\d{2})")


def sanitize(s: str, max_len: int = 180) -> str:
    s = " ".join((s or "").split())
    if len(s) > max_len:
        return s[: max_len - 1] + "…"
    return s


def tagify_ac(ac_id: str) -> str:
    return "@ac_" + ac_id.replace("-", "_")


def main() -> None:
    if not MATRIX.is_file():
        raise SystemExit(f"Matrix not found: {MATRIX}. Run generate_ac_details_and_squad_docs.py first.")

    with MATRIX.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    by_epic: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_epic[row["epic_id"]].append(row)

    OUT.mkdir(parents=True, exist_ok=True)
    for epic, epic_rows in sorted(by_epic.items()):
        # stable AC sort
        epic_rows = sorted(epic_rows, key=lambda r: r["ac_id"])
        m = EPIC_NUM.match(epic)
        epic_num = m.group(1) if m else "00"
        path = OUT / f"{epic}.feature"
        lines: list[str] = [
            f"# Auto-generated from {MATRIX.relative_to(ROOT)}",
            f"# Edit AC text in EPIC-*.md, then regenerate.",
            "",
            f"@epic_{epic.replace('-', '_')}",
            f"Feature: {epic} acceptance criteria traceability stubs",
            "",
            "  These scenarios are placeholders for BDD mapping.",
            "  Replace Given/When/Then with executable step definitions.",
            "",
        ]
        for row in epic_rows:
            ac = row["ac_id"]
            us = row["us_id"]
            squad = row.get("squad", "unknown")
            req = sanitize(row.get("requirement_statement", ""))
            pre = sanitize(row.get("preconditions", ""))
            expected = sanitize(row.get("expected_result", ""))
            lines.extend(
                [
                    f"  {tagify_ac(ac)} @us_{us.replace('-', '_')} @squad_{squad.replace('-', '_')}",
                    f"  Scenario: {ac} — {req}",
                    f"    # phase: {row.get('phase_primary','')} / priority: {row.get('priority','')}",
                    f"    Given {pre or 'preconditions are satisfied'}",
                    f"    When the system executes behavior for \"{ac}\"",
                    f"    Then {expected or 'the expected result is observed'}",
                    "",
                ]
            )
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    readme = OUT / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# BDD stubs from AC matrix",
                "",
                "Generated files map every `AC-DG-*` to a placeholder scenario.",
                "",
                "Regenerate:",
                "",
                "```bash",
                "python3 scripts/generate_bdd_stubs_from_traceability.py",
                "```",
                "",
                "Source matrix: `../traceability-ac-detail-matrix.csv`.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Wrote BDD stubs to {OUT.relative_to(ROOT)} ({len(by_epic)} feature files).")


if __name__ == "__main__":
    main()
