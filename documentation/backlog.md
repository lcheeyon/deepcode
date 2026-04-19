# Backlog & traceability

## User stories

Canonical epic files:

- Path: **`docs/user-stories/EPIC-NN-*.md`**
- Index: **`docs/user-stories/README.md`**
- Numbering rules: **`docs/user-stories/00-numbering-and-traceability.md`**

Each epic uses **`US-DG-*`** user stories and **`AC-DG-*`** acceptance criteria. Tests may declare **`@pytest.mark.req("AC-DG-…")`** per project convention.

## Generated artefacts

Running **`python3 scripts/generate_ac_details_and_squad_docs.py`** updates:

- **`docs/user-stories/traceability-ac-detail-matrix.csv`** — per-AC rows.
- **`docs/user-stories/squads/<squad>/EPIC-DG-NN-detailed.md`** — squad-facing copies.

Validate with **`python3 scripts/validate_user_stories_traceability.py`**.

## Supplements

Design-only or contract supplements that **must not** be parsed as epics (to avoid duplicate epic numbers in the generator) use names like **`SUPPLEMENT-EPIC-02-04-ingestion-contracts.md`** instead of **`EPIC-*.md`**.

## Implementation plan mapping

**`IMPLEMENTATION_PLAN.md`** contains a phase ↔ EPIC matrix (L0–L14 and cloud phases). Use it to see which epics are primary drivers for each delivery slice.
