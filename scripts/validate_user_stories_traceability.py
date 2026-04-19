#!/usr/bin/env python3
"""
Validate docs/user-stories traceability assets:
- every AC-DG-* in canonical EPIC-*.md appears once in CSV
- CSV has required columns for planning metadata
- key fields are non-empty for each row
- optional JSON export is present and row count aligned

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
JSON_EXPORT = USER_STORIES / "traceability-ac-detail.json"
PHASE_EXPORTS = USER_STORIES / "phase-exports"

# Same as generator: colon inside bold
AC_IN_LINE = re.compile(r"\*\*(AC-DG-\d{2}-\d{3}-\d{2}):\*\*")
AC_IN_CSV = re.compile(r"^AC-DG-\d{2}-\d{3}-\d{2}$")
REQUIRED_COLUMNS = {
    "ac_id",
    "us_id",
    "epic_id",
    "squad",
    "owner_role",
    "phase_primary",
    "priority",
    "moscow",
    "release",
    "requirement_type",
    "test_layer_required",
    "suggested_tc_primary",
    "requirement_statement",
}
NON_EMPTY_COLUMNS = {
    "ac_id",
    "us_id",
    "epic_id",
    "squad",
    "owner_role",
    "phase_primary",
    "priority",
    "moscow",
    "release",
    "requirement_type",
    "test_layer_required",
    "suggested_tc_primary",
    "requirement_statement",
}


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


def matrix_rows() -> list[dict[str, str]]:
    with MATRIX.open(encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        fieldnames = set(r.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - fieldnames)
        if missing:
            raise SystemExit(f"CSV missing required columns: {missing}")
        if "ac_id" not in fieldnames:
            raise SystemExit(f"CSV missing ac_id column: {MATRIX}")
        rows = list(r)
    return rows


def main() -> int:
    if not MATRIX.is_file():
        print(
            f"ERROR: matrix not found: {MATRIX} — run generate_ac_details_and_squad_docs.py",
            file=sys.stderr,
        )
        return 1

    epic_acs = ac_ids_in_epics()
    rows = matrix_rows()
    matrix_acs = {row["ac_id"].strip() for row in rows if row.get("ac_id")}

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

    invalid_ids = sorted(x for x in matrix_acs if not AC_IN_CSV.match(x))
    if invalid_ids:
        print("ERROR: malformed AC IDs in CSV:", file=sys.stderr)
        for x in invalid_ids[:30]:
            print(f"  {x}", file=sys.stderr)
        return 1

    empty_errors: list[str] = []
    for i, row in enumerate(rows, start=2):  # CSV header at line 1
        for col in NON_EMPTY_COLUMNS:
            if not (row.get(col) or "").strip():
                empty_errors.append(f"line {i}: empty `{col}` for ac_id={row.get('ac_id', '<missing>')}")
    if empty_errors:
        print("ERROR: required non-empty columns missing values:", file=sys.stderr)
        for msg in empty_errors[:50]:
            print(f"  {msg}", file=sys.stderr)
        if len(empty_errors) > 50:
            print(f"  ... and {len(empty_errors) - 50} more", file=sys.stderr)
        return 1

    if not JSON_EXPORT.is_file():
        print(f"ERROR: JSON export missing: {JSON_EXPORT}", file=sys.stderr)
        return 1

    import json

    data = json.loads(JSON_EXPORT.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print(f"ERROR: JSON export is not an array: {JSON_EXPORT}", file=sys.stderr)
        return 1
    if len(data) != len(rows):
        print(
            f"ERROR: JSON row count {len(data)} != CSV row count {len(rows)}",
            file=sys.stderr,
        )
        return 1

    if not PHASE_EXPORTS.is_dir():
        print(f"ERROR: phase exports directory missing: {PHASE_EXPORTS}", file=sys.stderr)
        return 1
    phase_csv = sorted(PHASE_EXPORTS.glob("traceability-*.csv"))
    phase_json = sorted(PHASE_EXPORTS.glob("traceability-*.json"))
    if not phase_csv or not phase_json:
        print("ERROR: phase exports missing csv/json files", file=sys.stderr)
        return 1
    phase_readme = PHASE_EXPORTS / "README.md"
    if not phase_readme.is_file():
        print(f"ERROR: phase exports README missing: {phase_readme}", file=sys.stderr)
        return 1

    print(
        f"OK: {len(epic_acs)} ACs in EPIC-*.md match {len(matrix_acs)} CSV rows; "
        f"required metadata columns present; phase exports available."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
