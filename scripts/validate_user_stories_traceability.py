#!/usr/bin/env python3
"""
Validate that every AC-DG-* in canonical docs/user-stories/EPIC-*.md appears
exactly once in traceability-ac-detail-matrix.csv (and optionally flag CSV orphans).

Run from repo root:
  python3 scripts/validate_user_stories_traceability.py
Exit 0 if OK, 1 if mismatches.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_STORIES = ROOT / "docs" / "user-stories"
MATRIX = USER_STORIES / "traceability-ac-detail-matrix.csv"

# Same as generator: colon inside bold
AC_IN_LINE = re.compile(r"\*\*(AC-DG-\d{2}-\d{3}-\d{2}):\*\*")
AC_IN_CSV = re.compile(r"^AC-DG-\d{2}-\d{3}-\d{2}$")


def ac_ids_in_epics() -> dict[str, str]:
    """ac_id -> source file name"""
    found: dict[str, str] = {}
    for path in sorted(USER_STORIES.glob("EPIC-*.md")):
        text = path.read_text(encoding="utf-8")
        for m in AC_IN_LINE.finditer(text):
            ac_id = m.group(1)
            if ac_id in found and found[ac_id] != path.name:
                raise SystemExit(f"Duplicate AC {ac_id} in {found[ac_id]} and {path.name}")
            found[ac_id] = path.name
    return found


def ac_ids_in_matrix() -> set[str]:
    with MATRIX.open(encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        if "ac_id" not in (r.fieldnames or []):
            raise SystemExit(f"CSV missing ac_id column: {MATRIX}")
        return {row["ac_id"].strip() for row in r if row.get("ac_id")}


def main() -> int:
    if not MATRIX.is_file():
        print(
            f"ERROR: matrix not found: {MATRIX} — run generate_ac_details_and_squad_docs.py",
            file=sys.stderr,
        )
        return 1

    epic_acs = ac_ids_in_epics()
    matrix_acs = ac_ids_in_matrix()

    missing_in_matrix = sorted(set(epic_acs) - matrix_acs)
    orphans_in_matrix = sorted(matrix_acs - set(epic_acs))

    if missing_in_matrix:
        print("ERROR: ACs in EPIC markdown but missing from CSV:", file=sys.stderr)
        for x in missing_in_matrix[:50]:
            print(f"  {x}  ({epic_acs[x]})", file=sys.stderr)
        if len(missing_in_matrix) > 50:
            print(f"  ... and {len(missing_in_matrix) - 50} more", file=sys.stderr)
        return 1

    if orphans_in_matrix:
        print("WARN: AC rows in CSV not found in canonical EPIC files:", file=sys.stderr)
        for x in orphans_in_matrix[:30]:
            print(f"  {x}", file=sys.stderr)
        if len(orphans_in_matrix) > 30:
            print(f"  ... and {len(orphans_in_matrix) - 30} more", file=sys.stderr)
        return 1

    print(f"OK: {len(epic_acs)} ACs in EPIC-*.md match {len(matrix_acs)} CSV rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
