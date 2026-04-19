#!/usr/bin/env python3
"""
Parse docs/user-stories/EPIC-*.md and emit:
1. docs/user-stories/traceability-ac-detail-matrix.csv — one row per AC
2. docs/user-stories/squads/<squad>/EPIC-DG-NN.md — epic copy with AC test specs

Run from repo root: python3 scripts/generate_ac_details_and_squad_docs.py
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_STORIES = ROOT / "docs" / "user-stories"
SQUADS = USER_STORIES / "squads"
MATRIX_PATH = USER_STORIES / "traceability-ac-detail-matrix.csv"

EPIC_FILES = sorted(USER_STORIES.glob("EPIC-*.md"))

# Epic number (from filename EPIC-01-...) -> squad directory name
EPIC_TO_SQUAD: dict[int, str] = {
    1: "platform-runtime",
    2: "control-plane",
    3: "identity-tenancy",
    4: "ingestion-codeintel",
    5: "policy",
    6: "ingestion-codeintel",
    7: "connectors",
    8: "compliance-engine",
    9: "remediation-reporting",
    10: "remediation-reporting",
    11: "observability",
    12: "frontend",
    13: "security-deployment",
    14: "frontend",
}

# Title separator may be em dash (—), en dash, or hyphen-minus between tools
US_HEADER = re.compile(r"^## (US-DG-\d{2}-\d{3})\s*[—–-]\s*(.+)$", re.MULTILINE)
# Markdown uses **AC-DG-…:** (colon inside bold before closing **)
AC_LINE = re.compile(r"^- \*\*(AC-DG-\d{2}-\d{3}-\d{2}):\*\*\s*(.*)$")
ARCH_REF = re.compile(r"\(Architecture([^)]*)\)")
EPIC_FN = re.compile(r"^EPIC-(\d{2})-")


def epic_num_from_path(path: Path) -> int:
    m = EPIC_FN.match(path.name)
    if not m:
        raise ValueError(path)
    return int(m.group(1))


def epic_id(n: int) -> str:
    return f"EPIC-DG-{n:02d}"


def parse_given(ac_text: str) -> str | None:
    if ac_text.lower().startswith("given "):
        rest = ac_text[6:].strip()
        # stop at next capital clause heuristic
        for sep in (" When ", " when ", "\n"):
            if sep in rest:
                rest = rest.split(sep)[0]
        return rest.strip().rstrip(".")
    return None


def architecture_refs(ac_text: str) -> str:
    parts = ARCH_REF.findall(ac_text)
    if not parts:
        return "Architecture_Design.md (see product spec)"
    return "; ".join("Architecture " + p.strip() for p in parts)


def build_spec(ac_id: str, us_id: str, epic_id: str, squad: str, statement: str) -> dict[str, str]:
    given = parse_given(statement) or "Tenant and scan fixtures exist; services healthy per test environment bootstrap."
    objective = (
        f"Verify the behaviour described in {ac_id}: "
        + (statement[:220] + ("…" if len(statement) > 220 else ""))
    )
    steps = [
        "Arrange test data and configuration to match preconditions.",
        "Execute the operation or graph path under test (single happy path unless AC implies negative).",
        "Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces as applicable.",
    ]
    if "reject" in statement.lower() or "403" in statement or "429" in statement or "invalid" in statement.lower():
        steps.append("Repeat with invalid input or unauthorised actor and assert stable error_code / no side effects.")

    expected = (
        "All assertions pass; no secret material in logs; stable machine-readable error_code on failures; "
        f"state remains tenant-scoped for {epic_id}."
    )
    edges = [
        "Concurrent requests: no cross-tenant leakage and no duplicate side effects when idempotency applies.",
        "Timeout / partial failure: system reaches documented terminal or degraded state without data corruption.",
    ]
    if "optional" in statement.lower() or "when " in statement.lower()[:80]:
        edges.append("Feature disabled path: behaviour is explicit no-op or skip with user-visible reason.")

    # Align with docs/user-stories/00-numbering-and-traceability.md: TC-DG-ee-sss-aa[.variant]
    tc_primary = ac_id.replace("AC-", "TC-", 1)
    tc_neg = tc_primary + ".2"

    return {
        "ac_id": ac_id,
        "us_id": us_id,
        "epic_id": epic_id,
        "squad": squad,
        "statement": statement,
        "objective": objective,
        "preconditions": given,
        "verification_steps": " | ".join(f"{i+1}. {s}" for i, s in enumerate(steps)),
        "expected_result": expected,
        "edge_cases": " | ".join(edges),
        "suggested_tc_primary": tc_primary,
        "suggested_tc_negative": tc_neg,
        "automation_hints": "pytest marker @pytest.mark.req(\"{ac_id}\") or Xray/TestRail key == ac_id".format(ac_id=ac_id),
        "architecture_refs": architecture_refs(statement),
    }


def escape_md_cell(text: str) -> str:
    """Avoid breaking markdown tables on pipes or newlines."""
    return text.replace("|", "\\|").replace("\n", " ").strip()


def format_ac_detail_block(spec: dict[str, str]) -> str:
    lines = [
        f"#### Test specification — {spec['ac_id']}",
        "",
        "| Attribute | Specification |",
        "|-----------|---------------|",
        f"| **Parent US** | `{spec['us_id']}` |",
        f"| **Parent EPIC** | `{spec['epic_id']}` |",
        f"| **Owning squad** | `{spec['squad']}` |",
        f"| **Requirement (verbatim)** | {escape_md_cell(spec['statement'])} |",
        f"| **Objective** | {escape_md_cell(spec['objective'])} |",
        f"| **Preconditions** | {escape_md_cell(spec['preconditions'])} |",
        f"| **Verification procedure** | {escape_md_cell(spec['verification_steps'])} |",
        f"| **Expected result** | {escape_md_cell(spec['expected_result'])} |",
        f"| **Edge / negative focus** | {escape_md_cell(spec['edge_cases'])} |",
        f"| **Primary automated test ID** | `{spec['suggested_tc_primary']}` |",
        f"| **Secondary / negative test ID** | `{spec['suggested_tc_negative']}` |",
        f"| **Automation hints** | {escape_md_cell(spec['automation_hints'])} |",
        f"| **Spec references** | {escape_md_cell(spec['architecture_refs'])} |",
        "",
    ]
    return "\n".join(lines)


def parse_epic(path: Path) -> tuple[int, str, list[tuple[str, str, str, list[tuple[str, str]]]]]:
    """Returns epic_num, raw_header_lines_before_first_us, list of (us_id, us_title, us_body_markdown, [(ac_id, ac_text)])"""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    epic_n = epic_num_from_path(path)

    first_us_idx = None
    for i, line in enumerate(lines):
        if US_HEADER.match(line):
            first_us_idx = i
            break
    header = "\n".join(lines[: first_us_idx or 0]) if first_us_idx else text

    stories: list[tuple[str, str, str, list[tuple[str, str]]]] = []
    if first_us_idx is None:
        return epic_n, header, stories

    i = first_us_idx
    while i < len(lines):
        m = US_HEADER.match(lines[i])
        if not m:
            i += 1
            continue
        us_id, title = m.group(1), m.group(2)
        start = i
        i += 1
        while i < len(lines) and not US_HEADER.match(lines[i]):
            i += 1
        block = "\n".join(lines[start:i])
        acs: list[tuple[str, str]] = []
        for bl in block.splitlines():
            am = AC_LINE.match(bl)
            if am:
                acs.append((am.group(1), am.group(2).strip()))
        body_wo_ac_expansion = block  # full story including AC bullets; we append specs after section
        stories.append((us_id, title, body_wo_ac_expansion, acs))

    return epic_n, header, stories


def inject_specs_into_story_block(block: str, ac_order: list[str], specs_md: dict[str, str]) -> str:
    """Append after full story block (including AC bullets) the AC test specification subsections."""
    if not ac_order:
        return block
    m = US_HEADER.search(block)
    if not m:
        raise ValueError("Story block missing ## US-DG- header:\n" + block[:200])
    us_id = m.group(1)
    appendix: list[str] = [
        "",
        f"### AC test specifications ({us_id})",
        "",
        "Expands each acceptance criterion for **QA authoring**, **pytest markers**, and **import into Xray/TestRail**.",
        "",
    ]
    for aid in ac_order:
        appendix.append(specs_md[aid])
    return block.rstrip() + "\n" + "\n".join(appendix)


def main() -> None:
    rows: list[dict[str, str]] = []
    squad_epic_bodies: dict[str, dict[int, str]] = defaultdict(dict)

    for path in EPIC_FILES:
        epic_n, _header, stories = parse_epic(path)
        eid = epic_id(epic_n)
        squad = EPIC_TO_SQUAD[epic_n]

        raw = path.read_text(encoding="utf-8")
        raw_lines = raw.splitlines()
        idx_first_us = next((i for i, line in enumerate(raw_lines) if US_HEADER.match(line)), len(raw_lines))
        header_lines = raw_lines[:idx_first_us]

        epic_parts: list[str] = [
            f"> **Generated** — AC test specifications for QA/traceability. "
            f"**Canonical backlog (edit here):** [`{path.name}`](../{path.name}). "
            f"**Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.",
            "",
            *header_lines,
            "",
        ]

        for us_id, title, block, acs in stories:
            specs_md: dict[str, str] = {}
            ac_order = [ac_id for ac_id, _ in acs]
            for ac_id, ac_text in acs:
                spec = build_spec(ac_id, us_id, eid, squad, ac_text)
                rows.append(spec)
                specs_md[ac_id] = format_ac_detail_block(spec)
            epic_parts.append(inject_specs_into_story_block(block, ac_order, specs_md))
            epic_parts.append("")

        squad_epic_bodies[squad][epic_n] = "\n".join(epic_parts).rstrip() + "\n"

    # Write CSV
    fieldnames = [
        "ac_id",
        "us_id",
        "epic_id",
        "squad",
        "requirement_statement",
        "objective",
        "preconditions",
        "verification_procedure",
        "expected_result",
        "edge_cases",
        "suggested_tc_primary",
        "suggested_tc_negative",
        "automation_hints",
        "architecture_refs",
    ]
    MATRIX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MATRIX_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(
                {
                    "ac_id": r["ac_id"],
                    "us_id": r["us_id"],
                    "epic_id": r["epic_id"],
                    "squad": r["squad"],
                    "requirement_statement": r["statement"],
                    "objective": r["objective"],
                    "preconditions": r["preconditions"],
                    "verification_procedure": r["verification_steps"],
                    "expected_result": r["expected_result"],
                    "edge_cases": r["edge_cases"],
                    "suggested_tc_primary": r["suggested_tc_primary"],
                    "suggested_tc_negative": r["suggested_tc_negative"],
                    "automation_hints": r["automation_hints"],
                    "architecture_refs": r["architecture_refs"],
                }
            )

    # Write squad files
    SQUADS.mkdir(parents=True, exist_ok=True)
    for squad, epics in squad_epic_bodies.items():
        d = SQUADS / squad
        d.mkdir(parents=True, exist_ok=True)
        for epic_n, body in sorted(epics.items()):
            out = d / f"EPIC-DG-{epic_n:02d}-detailed.md"
            out.write_text(body, encoding="utf-8")

    # Squad README
    squad_readme = SQUADS / "README.md"
    lines = [
        "# User stories by squad (generated + maintained)",
        "",
        "Each **`EPIC-DG-NN-detailed.md`** file is produced by `scripts/generate_ac_details_and_squad_docs.py`. "
        "It mirrors the canonical [`EPIC-NN-*.md`](../) file and appends a **test specification** subsection per AC.",
        "",
        "| Squad | Epics | Path |",
        "|-------|-------|------|",
    ]
    squad_epic_list: dict[str, list[int]] = defaultdict(list)
    for n, sq in EPIC_TO_SQUAD.items():
        squad_epic_list[sq].append(n)
    for squad in sorted(squad_epic_list.keys()):
        nums = ", ".join(f"`{epic_id(n)}`" for n in sorted(squad_epic_list[squad]))
        lines.append(f"| `{squad}` | {nums} | [`{squad}/`]({squad}/) |")
    lines.extend(
        [
            "",
            "## Regenerate",
            "",
            "```bash",
            "python3 scripts/generate_ac_details_and_squad_docs.py",
            "```",
            "",
            "## Machine-readable matrix",
            "",
            "All AC rows: [`../traceability-ac-detail-matrix.csv`](../traceability-ac-detail-matrix.csv).",
            "",
        ]
    )
    squad_readme.write_text("\n".join(lines), encoding="utf-8")

    # Link canonical EPIC markdown → squad detailed copy (idempotent)
    pointer_marker = "> **AC-level test specifications (generated):**"
    for path in EPIC_FILES:
        raw_canon = path.read_text(encoding="utf-8")
        if pointer_marker in raw_canon:
            continue
        epic_n = epic_num_from_path(path)
        squad = EPIC_TO_SQUAD[epic_n]
        rel = f"squads/{squad}/EPIC-DG-{epic_n:02d}-detailed.md"
        pointer = (
            f"{pointer_marker} "
            f"Squad copy [`{rel}`]({rel}); "
            f"per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv). "
            f"Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py`."
        )
        cl = raw_canon.splitlines()
        if cl:
            path.write_text(
                cl[0] + "\n\n" + pointer + "\n\n" + "\n".join(cl[1:]) + "\n",
                encoding="utf-8",
            )

    print(f"Wrote {len(rows)} AC rows to {MATRIX_PATH.relative_to(ROOT)}")
    print(f"Squad folders under {SQUADS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
