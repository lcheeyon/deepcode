#!/usr/bin/env python3
"""
Parse docs/user-stories/EPIC-*.md and emit:
1. docs/user-stories/traceability-ac-detail-matrix.csv — one row per AC with
   phase/dependency/priority/NFR/regulatory/testing fields.
2. docs/user-stories/squads/<squad>/EPIC-DG-NN-detailed.md — epic copy with AC test specs.

Run from repo root:
  python3 scripts/generate_ac_details_and_squad_docs.py
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
JSON_PATH = USER_STORIES / "traceability-ac-detail.json"
PHASE_EXPORTS = USER_STORIES / "phase-exports"

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

# First usable phases from IMPLEMENTATION_PLAN §2.4 (primary + nearby secondary)
EPIC_PHASES: dict[int, tuple[str, str]] = {
    1: ("L4", "L5/L12"),
    2: ("L3", "L12/C5"),
    3: ("L3", "L14/C5"),
    4: ("L6", "L8/L9"),
    5: ("L7", "L10/L11"),
    6: ("L8", "L10"),
    7: ("L9", "C1-C4"),
    8: ("L10", "L11/L12"),
    9: ("L11", "L12"),
    10: ("L11", "L12"),
    11: ("L13", "C5"),
    12: ("L3", "L4-C5"),
    13: ("L14", "C0-C5"),
    14: ("L3", "L4/L5"),
}

SQUAD_OWNER_ROLE = {
    "platform-runtime": "platform_engineer",
    "control-plane": "backend_engineer",
    "identity-tenancy": "security_engineer",
    "ingestion-codeintel": "ml_platform_engineer",
    "policy": "compliance_engineer",
    "connectors": "cloud_security_engineer",
    "compliance-engine": "applied_ml_engineer",
    "remediation-reporting": "security_engineer",
    "observability": "sre",
    "frontend": "frontend_engineer",
    "security-deployment": "devsecops_engineer",
}

SQUAD_TEST_LAYER = {
    "platform-runtime": "integration",
    "control-plane": "unit+integration",
    "identity-tenancy": "unit+integration",
    "ingestion-codeintel": "unit+integration",
    "policy": "unit+integration",
    "connectors": "integration",
    "compliance-engine": "unit+integration",
    "remediation-reporting": "unit+integration",
    "observability": "integration",
    "frontend": "bdd+integration",
    "security-deployment": "integration",
}

# Title separator may be em dash (—), en dash, or hyphen-minus between tools
US_HEADER = re.compile(r"^## (US-DG-\d{2}-\d{3})\s*[—–-]\s*(.+)$", re.MULTILINE)
# Markdown uses **AC-DG-…:** (colon inside bold before closing **)
AC_LINE = re.compile(r"^- \*\*(AC-DG-\d{2}-\d{3}-\d{2}):\*\*\s*(.*)$")
ARCH_REF = re.compile(r"\(Architecture([^)]*)\)")
EPIC_REF = re.compile(r"(EPIC-DG-\d{2})")
US_REF = re.compile(r"(US-DG-\d{2}-\d{3})")
AC_REF = re.compile(r"(AC-DG-\d{2}-\d{3}-\d{2})")
FRAMEWORK_TAG_REF = re.compile(
    r"(ISO-?\s?27001|SOC2|MAS-?TRM|GB-?T-?22239|等保|PIPL|PCI-?DSS|NIST|GDPR|HIPAA|ISO-?\s?42001)",
    re.IGNORECASE,
)
CONTROL_CLAUSE_REF = re.compile(r"([A-Z]{2,8}[A-Za-z0-9\-]*\s?[A-Z]?\.\d+(?:\.\d+)*)")
EPIC_FN = re.compile(r"^EPIC-(\d{2})-")
PHASE_TOKEN = re.compile(r"^[LC](\d{1,2})$")
PHASE_RANGE = re.compile(r"^([LC])(\d{1,2})-([LC])?(\d{1,2})$")


def epic_num_from_path(path: Path) -> int:
    m = EPIC_FN.match(path.name)
    if not m:
        raise ValueError(path)
    return int(m.group(1))


def epic_id(n: int) -> str:
    return f"EPIC-DG-{n:02d}"


def parse_given(ac_text: str) -> str | None:
    lowered = ac_text.lower()
    if lowered.startswith("given "):
        rest = ac_text[6:].strip()
        for sep in (" When ", " when ", " Then ", " then ", "\n"):
            if sep in rest:
                rest = rest.split(sep)[0]
        return rest.strip().rstrip(".")
    return None


def architecture_refs(ac_text: str) -> str:
    parts = ARCH_REF.findall(ac_text)
    if not parts:
        return "Architecture_Design.md (see product spec)"
    return "; ".join("Architecture " + p.strip() for p in parts)


def classify_priority(statement: str, squad: str) -> str:
    low = statement.lower()
    if any(k in low for k in ("security", "secret", "read-only", "forbidden", "auth", "tenant", "encryption")):
        return "P0"
    if any(k in low for k in ("optional", "placeholder", "mobile", "branding", "tooltip")):
        return "P2"
    if squad in {"security-deployment", "identity-tenancy"}:
        return "P0"
    return "P1"


def classify_release(statement: str, requirement_type: str) -> str:
    low = statement.lower()
    if any(k in low for k in ("a11y", "lcp", "mobile", "hardening", "slo", "budget alert")):
        return "Hardening"
    if any(k in low for k in ("optional", "deferred", "phase 2", "beta")):
        return "Post-MVP"
    if requirement_type == "NFR":
        return "Hardening"
    return "MVP"


def moscow_from_priority(priority: str) -> str:
    return {"P0": "Must", "P1": "Should", "P2": "Could"}.get(priority, "Should")


def classify_requirement_type(statement: str) -> tuple[str, str, str]:
    low = statement.lower()
    nfr_keywords = {
        "p95": "p95_latency",
        "latency": "latency",
        "slo": "service_level_objective",
        "lcp": "lcp",
        "queue depth": "queue_depth",
        "cost": "scan_cost",
        "availability": "availability",
        "retry rate": "retry_rate",
    }
    for kw, metric in nfr_keywords.items():
        if kw in low:
            target = "Defined in AC statement" if ">" in statement or "<" in statement else "TBD"
            return ("NFR", metric, target)
    return ("Functional", "", "")


def extract_framework_tags(statement: str) -> str:
    tags = sorted({m.group(1).upper().replace(" ", "") for m in FRAMEWORK_TAG_REF.finditer(statement)})
    return "; ".join(tags)


def extract_control_clause_ids(statement: str) -> str:
    # Heuristic only: keeps short tokens that look like control IDs.
    vals = [m.group(1) for m in CONTROL_CLAUSE_REF.finditer(statement)]
    vals = [v.strip() for v in vals if len(v) <= 24]
    uniq = sorted(set(vals))
    return "; ".join(uniq)


def extract_dependencies(statement: str, current_us: str, current_epic: str) -> tuple[str, str, str]:
    epics = sorted(set(EPIC_REF.findall(statement)))
    stories = sorted(set(US_REF.findall(statement)))
    acs = sorted(set(AC_REF.findall(statement)))

    epics = [e for e in epics if e != current_epic]
    stories = [s for s in stories if s != current_us]
    return ("; ".join(epics), "; ".join(stories), "; ".join(acs))


def estimate_points(statement: str, requirement_type: str) -> str:
    low = statement.lower()
    base = 3
    if requirement_type == "NFR":
        base += 1
    if any(k in low for k in ("multi", "parallel", "cross-layer", "encryption", "fallback", "resume")):
        base += 2
    if "optional" in low:
        base = max(2, base - 1)
    return str(min(8, max(1, base)))


def build_spec(ac_id: str, us_id: str, epic: str, squad: str, statement: str) -> dict[str, str]:
    given = parse_given(statement) or "Tenant and scan fixtures exist; services healthy per test environment bootstrap."
    objective = f"Verify {ac_id}: " + (statement[:220] + ("…" if len(statement) > 220 else ""))
    steps = [
        "Arrange test data and configuration to match preconditions.",
        "Execute the operation or graph/API path under test.",
        "Assert post-conditions against DB rows, API responses, object store metadata, queue state, or traces.",
    ]
    if any(k in statement.lower() for k in ("reject", "invalid", "forbidden", "missing", "unauthor")):
        steps.append("Execute negative path and assert stable error_code with no side effects.")

    requirement_type, nfr_metric, nfr_target = classify_requirement_type(statement)
    priority = classify_priority(statement, squad)
    release = classify_release(statement, requirement_type)
    moscow = moscow_from_priority(priority)
    dep_epics, dep_us, dep_acs = extract_dependencies(statement, us_id, epic)
    phase_primary, phase_secondary = EPIC_PHASES[int(epic[-2:])]

    expected = (
        "Assertions pass; no secret material in logs; stable machine-readable error_code on failures; "
        f"tenant isolation preserved for {epic}."
    )
    edge = (
        "Concurrent requests do not duplicate side effects; timeout/partial failures reach documented degraded or terminal states."
    )
    if "optional" in statement.lower():
        edge += " Feature-disabled path yields explicit skip/no-op behaviour."

    tc_primary = ac_id.replace("AC-", "TC-", 1)
    tc_neg = tc_primary + ".2"
    owner_role = SQUAD_OWNER_ROLE[squad]
    test_layer = SQUAD_TEST_LAYER[squad]
    min_auto = "1"
    framework_tags = extract_framework_tags(statement)
    control_ids = extract_control_clause_ids(statement)

    return {
        "ac_id": ac_id,
        "us_id": us_id,
        "epic_id": epic,
        "squad": squad,
        "owner_role": owner_role,
        "estimate_points": estimate_points(statement, requirement_type),
        "phase_primary": phase_primary,
        "phase_secondary": phase_secondary,
        "priority": priority,
        "moscow": moscow,
        "release": release,
        "requirement_type": requirement_type,
        "nfr_metric": nfr_metric,
        "nfr_target": nfr_target,
        "depends_on_epics": dep_epics,
        "depends_on_us": dep_us,
        "depends_on_acs": dep_acs,
        "test_layer_required": test_layer,
        "min_automated_tests": min_auto,
        "framework_tags": framework_tags,
        "control_clause_ids": control_ids,
        "requirement_statement": statement,
        "objective": objective,
        "preconditions": given,
        "verification_procedure": " | ".join(f"{i+1}. {s}" for i, s in enumerate(steps)),
        "expected_result": expected,
        "edge_cases": edge,
        "suggested_tc_primary": tc_primary,
        "suggested_tc_negative": tc_neg,
        "automation_hints": f'pytest marker @pytest.mark.req("{ac_id}") or Xray/TestRail key == {ac_id}',
        "architecture_refs": architecture_refs(statement),
    }


def escape_md_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def normalize_phase_tokens(primary: str, secondary: str) -> list[str]:
    """Expand phase fields into normalized tokens like L3, C2."""
    raw = f"{primary}/{secondary}"
    tokens = [t.strip() for t in re.split(r"[\/,;\s]+", raw) if t.strip()]
    out: set[str] = set()
    for tok in tokens:
        if PHASE_TOKEN.match(tok):
            out.add(tok)
            continue
        m = PHASE_RANGE.match(tok)
        if m:
            p1, n1, p2, n2 = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
            p2 = p2 or p1
            if p1 == p2:
                lo, hi = (n1, n2) if n1 <= n2 else (n2, n1)
                for n in range(lo, hi + 1):
                    out.add(f"{p1}{n}")
            else:
                # Mixed-prefix range (e.g. L4-C5): include endpoints.
                out.add(f"{p1}{n1}")
                out.add(f"{p2}{n2}")
            continue
        # Fallback for odd tokens
        if tok.startswith(("L", "C")):
            out.add(tok)
    # Sort L* then C* numerically
    return sorted(out, key=lambda x: (x[0], int(x[1:])))


def format_ac_detail_block(spec: dict[str, str]) -> str:
    lines = [
        f"#### Test specification — {spec['ac_id']}",
        "",
        "| Attribute | Specification |",
        "|-----------|---------------|",
        f"| **Parent US** | `{spec['us_id']}` |",
        f"| **Parent EPIC** | `{spec['epic_id']}` |",
        f"| **Owning squad / role** | `{spec['squad']}` / `{spec['owner_role']}` |",
        f"| **Phase mapping** | primary `{spec['phase_primary']}`; secondary `{spec['phase_secondary']}` |",
        f"| **Priority / release** | `{spec['priority']}` / `{spec['release']}` |",
        f"| **MoSCoW** | `{spec['moscow']}` |",
        f"| **Requirement type** | `{spec['requirement_type']}` |",
        f"| **NFR metric / target** | `{spec['nfr_metric'] or '-'} / {spec['nfr_target'] or '-'}` |",
        f"| **Dependencies** | epics `{spec['depends_on_epics'] or '-'}`; stories `{spec['depends_on_us'] or '-'}`; ACs `{spec['depends_on_acs'] or '-'}` |",
        f"| **Required test layer** | `{spec['test_layer_required']}` (min automated tests: `{spec['min_automated_tests']}`) |",
        f"| **Framework / control tags** | `{spec['framework_tags'] or '-'}` / `{spec['control_clause_ids'] or '-'}` |",
        f"| **Estimate (story points hint)** | `{spec['estimate_points']}` |",
        f"| **Requirement (verbatim)** | {escape_md_cell(spec['requirement_statement'])} |",
        f"| **Objective** | {escape_md_cell(spec['objective'])} |",
        f"| **Preconditions** | {escape_md_cell(spec['preconditions'])} |",
        f"| **Verification procedure** | {escape_md_cell(spec['verification_procedure'])} |",
        f"| **Expected result** | {escape_md_cell(spec['expected_result'])} |",
        f"| **Edge / negative focus** | {escape_md_cell(spec['edge_cases'])} |",
        f"| **Primary automated test ID** | `{spec['suggested_tc_primary']}` |",
        f"| **Secondary / negative test ID** | `{spec['suggested_tc_negative']}` |",
        f"| **Automation hints** | {escape_md_cell(spec['automation_hints'])} |",
        f"| **Spec references** | {escape_md_cell(spec['architecture_refs'])} |",
        "",
    ]
    return "\n".join(lines)


def parse_epic(path: Path) -> tuple[int, list[str], list[tuple[str, str, str, list[tuple[str, str]]]]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    epic_n = epic_num_from_path(path)

    first_us_idx = next((i for i, line in enumerate(lines) if US_HEADER.match(line)), len(lines))
    header_lines = lines[:first_us_idx]

    stories: list[tuple[str, str, str, list[tuple[str, str]]]] = []
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
        stories.append((us_id, title, block, acs))
    return epic_n, header_lines, stories


def inject_specs_into_story_block(block: str, ac_order: list[str], specs_md: dict[str, str]) -> str:
    if not ac_order:
        return block
    m = US_HEADER.search(block)
    if not m:
        raise ValueError("Story block missing ## US-DG- header")
    us_id = m.group(1)
    appendix = [
        "",
        f"### AC test specifications ({us_id})",
        "",
        "Expands each AC with phase, dependency, priority, NFR, test-layer, and traceability fields.",
        "",
    ]
    for aid in ac_order:
        appendix.append(specs_md[aid])
    return block.rstrip() + "\n" + "\n".join(appendix)


def epic_dod_block(epic: str, squad: str) -> str:
    return "\n".join(
        [
            "## Epic Definition of Done checklist",
            "",
            f"- [ ] All in-scope ACs for `{epic}` implemented by `{squad}` and linked to automated tests (`TC-DG-*`).",
            "- [ ] Unit coverage on touched packages is >=80%.",
            "- [ ] Integration tests pass for all required ACs.",
            "- [ ] Playwright BDD updated where `test_layer_required` includes `bdd`.",
            "- [ ] Observability hooks and stable `error_code` behaviour validated.",
            "- [ ] Security/data-sovereignty constraints verified (no secret leaks, tenant isolation).",
            "- [ ] Design spec for slice exists under `docs/design/` with approved status.",
            "",
        ]
    )


def main() -> None:
    rows: list[dict[str, str]] = []
    squad_epic_bodies: dict[str, dict[int, str]] = defaultdict(dict)

    for path in EPIC_FILES:
        epic_n, header_lines, stories = parse_epic(path)
        eid = epic_id(epic_n)
        squad = EPIC_TO_SQUAD.get(epic_n, "frontend")

        epic_parts = [
            f"> **Generated** — AC test specifications for QA/traceability. "
            f"**Canonical backlog (edit here):** [`{path.name}`](../{path.name}). "
            f"**Regenerate:** `python3 scripts/generate_ac_details_and_squad_docs.py`.",
            "",
            *header_lines,
            "",
        ]

        for us_id, _title, block, acs in stories:
            specs_md: dict[str, str] = {}
            ac_order = [ac_id for ac_id, _ in acs]
            for ac_id, ac_text in acs:
                spec = build_spec(ac_id, us_id, eid, squad, ac_text)
                rows.append(spec)
                specs_md[ac_id] = format_ac_detail_block(spec)
            epic_parts.append(inject_specs_into_story_block(block, ac_order, specs_md))
            epic_parts.append("")

        epic_parts.append(epic_dod_block(eid, squad))
        squad_epic_bodies[squad][epic_n] = "\n".join(epic_parts).rstrip() + "\n"

    fieldnames = [
        "ac_id",
        "us_id",
        "epic_id",
        "squad",
        "owner_role",
        "estimate_points",
        "phase_primary",
        "phase_secondary",
        "priority",
        "moscow",
        "release",
        "requirement_type",
        "nfr_metric",
        "nfr_target",
        "depends_on_epics",
        "depends_on_us",
        "depends_on_acs",
        "test_layer_required",
        "min_automated_tests",
        "framework_tags",
        "control_clause_ids",
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
            w.writerow(r)

    # JSON export for dashboards
    import json

    JSON_PATH.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")

    # Phase-specific filtered exports
    PHASE_EXPORTS.mkdir(parents=True, exist_ok=True)
    phase_to_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        for ph in normalize_phase_tokens(row["phase_primary"], row["phase_secondary"]):
            phase_to_rows[ph].append(row)

    phase_fieldnames = fieldnames
    for phase, prows in sorted(phase_to_rows.items(), key=lambda kv: (kv[0][0], int(kv[0][1:]))):
        csv_path = PHASE_EXPORTS / f"traceability-{phase}.csv"
        json_path = PHASE_EXPORTS / f"traceability-{phase}.json"
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=phase_fieldnames, extrasaction="ignore")
            w.writeheader()
            for r in prows:
                w.writerow(r)
        json_path.write_text(json.dumps(prows, indent=2, ensure_ascii=False), encoding="utf-8")

    phase_readme = PHASE_EXPORTS / "README.md"
    phase_lines = [
        "# Phase-specific traceability exports",
        "",
        "Generated from `traceability-ac-detail-matrix.csv` by phase mapping fields.",
        "",
        "| Phase | AC rows | CSV | JSON |",
        "|-------|---------|-----|------|",
    ]
    for phase, prows in sorted(phase_to_rows.items(), key=lambda kv: (kv[0][0], int(kv[0][1:]))):
        phase_lines.append(
            f"| `{phase}` | {len(prows)} | "
            f"[`traceability-{phase}.csv`](traceability-{phase}.csv) | "
            f"[`traceability-{phase}.json`](traceability-{phase}.json) |"
        )
    phase_lines.extend(
        [
            "",
            "Regenerate:",
            "",
            "```bash",
            "python3 scripts/generate_ac_details_and_squad_docs.py",
            "```",
            "",
        ]
    )
    phase_readme.write_text("\n".join(phase_lines), encoding="utf-8")

    SQUADS.mkdir(parents=True, exist_ok=True)
    for squad, epics in squad_epic_bodies.items():
        d = SQUADS / squad
        d.mkdir(parents=True, exist_ok=True)
        for epic_n, body in sorted(epics.items()):
            out = d / f"EPIC-DG-{epic_n:02d}-detailed.md"
            out.write_text(body, encoding="utf-8")

    squad_readme = SQUADS / "README.md"
    lines = [
        "# User stories by squad (generated + maintained)",
        "",
        "Each `EPIC-DG-NN-detailed.md` file mirrors canonical backlog and appends full AC metadata + DoD checklist.",
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
            "## Machine-readable exports",
            "",
            "- CSV: [`../traceability-ac-detail-matrix.csv`](../traceability-ac-detail-matrix.csv)",
            "- JSON: [`../traceability-ac-detail.json`](../traceability-ac-detail.json)",
            "",
        ]
    )
    squad_readme.write_text("\n".join(lines), encoding="utf-8")

    pointer_marker = "> **AC-level test specifications (generated):**"
    for path in EPIC_FILES:
        raw = path.read_text(encoding="utf-8")
        epic_n = epic_num_from_path(path)
        squad = EPIC_TO_SQUAD.get(epic_n, "frontend")
        rel = f"squads/{squad}/EPIC-DG-{epic_n:02d}-detailed.md"
        pointer = (
            f"{pointer_marker} Squad copy [`{rel}`]({rel}); "
            f"per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), "
            f"JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). "
            f"Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then "
            f"`python3 scripts/validate_user_stories_traceability.py`."
        )
        lines_raw = raw.splitlines()
        if not lines_raw:
            continue
        if pointer_marker in raw:
            # Replace existing generated pointer line.
            out_lines: list[str] = []
            replaced = False
            for line in lines_raw:
                if line.startswith(pointer_marker):
                    if not replaced:
                        out_lines.append(pointer)
                        replaced = True
                    continue
                out_lines.append(line)
            path.write_text("\n".join(out_lines).rstrip() + "\n", encoding="utf-8")
        else:
            path.write_text(
                lines_raw[0] + "\n\n" + pointer + "\n\n" + "\n".join(lines_raw[1:]).rstrip() + "\n",
                encoding="utf-8",
            )

    print(f"Wrote {len(rows)} AC rows to {MATRIX_PATH.relative_to(ROOT)}")
    print(f"Wrote JSON export to {JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote phase exports under {PHASE_EXPORTS.relative_to(ROOT)}")
    print(f"Squad folders under {SQUADS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
