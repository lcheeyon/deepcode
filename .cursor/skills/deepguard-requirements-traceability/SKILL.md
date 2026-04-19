---
name: deepguard-requirements-traceability
description: >-
  DeepGuard / 玄武 requirements IDs (EPIC, user story, acceptance criteria, test
  case) and traceability rules for backlog docs and automated tests. Use when
  writing or editing docs/user-stories, acceptance criteria, test plans,
  pytest markers, TestRail/Xray keys, traceability matrices, mapping ACs to
  unit/integration/Playwright tests, or when the user mentions AC-DG-, US-DG-,
  EPIC-DG-, requirements traceability, or coverage mapping for DeepGuard.
---

# DeepGuard — requirements traceability & numbering

**Canonical prose + templates:** `docs/user-stories/00-numbering-and-traceability.md`  
**EPIC backlog + AC catalogue:** `docs/user-stories/README.md` and `docs/user-stories/EPIC-*.md`  
**Per-AC detail (CSV):** `docs/user-stories/traceability-ac-detail-matrix.csv` — regenerate with `python3 scripts/generate_ac_details_and_squad_docs.py`  
**Consistency:** `python3 scripts/validate_user_stories_traceability.py` — fails if EPIC markdown ACs ≠ CSV rows  
**Per-squad expanded specs:** `docs/user-stories/squads/<squad>/EPIC-DG-NN-detailed.md` (same stories + test-spec table per AC)  
**Sample import sheet:** `docs/user-stories/traceability-matrix-sample.csv`

When creating new backlog items or tests in this repo, **assign IDs from this scheme** and **reference `AC-DG-*` from tests** so coverage rolls up to stories and epics.

## Delivery pipeline (read with this skill)

**Before coding:** user stories + ACs here → **design spec written and approved** (`docs/design/…`, see `.cursor/skills/deepguard-delivery-quality/SKILL.md`).  
**After coding:** **unit tests ≥80%** on touched packages → **integration tests** → **Playwright BDD** → **manual UAT last**. Every automated test should declare which **`AC-DG-*`** it proves.

## ID hierarchy (do not renumber released IDs)

```text
EPIC-DG-{ee}                 ee = 01–99   (capability / bounded context)
  └── US-DG-{ee}-{sss}       sss = 001–999 (story within epic)
        └── AC-DG-{ee}-{sss}-{aa}   aa = 01–99 (atomic acceptance criterion)
              └── TC-DG-{ee}-{sss}-{aa}[.{n}]   optional test case(s) for that AC
```

- **Epic** `EPIC-DG-01` … `EPIC-DG-13` — see index in `docs/user-stories/README.md`.
- **Story** `US-DG-02-014` = Epic **02**, story **014**.
- **AC** `AC-DG-02-014-03` = third AC of that story.
- **Test case** `TC-DG-02-014-03` — same numeric body as `AC-DG-02-014-03` with **`AC-` → `TC-`**; variants `TC-DG-02-014-03.2` for negative/additional cases. The generator emits `suggested_tc_primary` / `suggested_tc_negative` columns in the CSV.

**Padding:** `ee` two digits; `sss` three digits; `aa` two digits (e.g. `US-DG-02-001`, not `US-DG-2-1`).

## Rules for authors

1. **New story:** next free `US-DG-{epic}-{sss}` in that epic file; never reuse a retired story ID for a different meaning.
2. **New AC:** next free `AC-DG-{epic}-{sss}-{aa}` under that story; keep ACs **testable** (observable behaviour, one main concern per AC when possible).
3. **Supersede, do not rename:** if an AC is wrong, mark deprecated in prose and add a replacement AC with a new number; do not change digits once used in tickets/tests.
4. **NFR / SLO:** same `AC-DG-*` pattern; tag in prose `kind=NFR` and the metric (e.g. P95 scan duration).

## Rules for tests (pytest / CI)

- Minimum: each automated test declares which AC it proves, e.g. `@pytest.mark.req("AC-DG-02-014-03")` or nodeid convention documented in `00-numbering-and-traceability.md`.
- One **traceability matrix row per AC** minimum; test columns may list one or many `TC-*` IDs.
- **Unit layer:** mark `@pytest.mark.unit` where helpful; enforce **≥80% line coverage** on touched packages per PR (see delivery-quality skill).
- **Integration layer:** `@pytest.mark.integration`; Docker-backed; maps ACs to multi-service flows.
- **BDD layer:** Playwright (or repo-standard runner); map **scenarios → `US-DG-*` / `AC-DG-*`** in file headers; run in CI before manual UAT.

## Cross-tool usage (Cursor + Claude Code)

- **Cursor:** skill loads from `.cursor/skills/deepguard-requirements-traceability/` (this directory).
- **Claude Code:** use the symlink `.claude/skills/deepguard-requirements-traceability` → this directory (same as `deepguard-architecture`), or read `CLAUDE.md` which points here.

## Quick examples

| Artefact | Example ID |
|----------|------------|
| Epic | `EPIC-DG-08` |
| User story | `US-DG-08-003` |
| Acceptance criterion | `AC-DG-08-003-02` |
| Test mapping | `TC-DG-08-003-02` covers `AC-DG-08-003-02` |

## Relationship to other skills

- **Architecture / implementation:** `.cursor/skills/deepguard-architecture/SKILL.md`
- **Delivery gates, design approval, 80% / integration / Playwright / UAT order:** `.cursor/skills/deepguard-delivery-quality/SKILL.md`
- **Backlog IDs + test traceability:** this skill

Do not duplicate full EPIC lists here; extend `docs/user-stories/EPIC-*.md` when scope grows.
