# User Stories Specification Changelog

Tracks structural changes to user-story specification assets (`EPIC-*.md`, traceability matrix schema, generation/validation tooling).

---

## 2026-04-19

### Added

- `scripts/generate_ac_details_and_squad_docs.py` enhanced with:
  - phase mapping (`phase_primary`, `phase_secondary`)
  - dependency fields (`depends_on_epics`, `depends_on_us`, `depends_on_acs`)
  - planning fields (`priority`, `release`, `owner_role`, `estimate_points`)
  - requirement classification (`requirement_type`, `nfr_metric`, `nfr_target`)
  - test governance (`test_layer_required`, `min_automated_tests`)
  - compliance tags (`framework_tags`, `control_clause_ids`)
  - JSON export: `traceability-ac-detail.json`
  - generated DoD checklist appended to per-squad detailed epic files
- `scripts/generate_bdd_stubs_from_traceability.py` to create `docs/user-stories/bdd-stubs/*.feature` stubs from AC matrix.
- `scripts/validate_user_stories_traceability.py` strengthened to enforce required metadata columns and non-empty key fields.

### Changed

- `traceability-ac-detail-matrix.csv` schema expanded (breaking change for downstream consumers expecting old column set).
- `docs/user-stories/README.md` updated with generation/validation workflow and advanced enhancements.
- `.cursor/skills/deepguard-requirements-traceability/SKILL.md` updated to include generation + validation commands.

### Notes

- Canonical source of requirements remains `docs/user-stories/EPIC-*.md`.
- Generated artifacts should be refreshed after requirement edits:
  1. `python3 scripts/generate_ac_details_and_squad_docs.py`
  2. `python3 scripts/generate_bdd_stubs_from_traceability.py`
  3. `python3 scripts/validate_user_stories_traceability.py`

