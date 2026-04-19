# Numbering conventions & traceability

## Hierarchy

```
EPIC-DG-{ee}          (01–99)   Business capability / bounded context
  └── US-DG-{ee}-{sss} (001–999) User story within epic
        └── AC-DG-{ee}-{sss}-{aa} (01–99) Atomic acceptance criterion
              └── TC-DG-{ee}-{sss}-{aa}[.{n}] Optional test case(s) targeting AC
```

**TC ID alignment:** `TC-DG-*` uses the **same numeric suffix** as `AC-DG-*` — replace the `AC-` prefix with `TC-` (e.g. `AC-DG-02-014-03` → primary `TC-DG-02-014-03`, negative/variant `TC-DG-02-014-03.2`). The generator `scripts/generate_ac_details_and_squad_docs.py` emits these automatically in the matrix and squad docs.

- **`ee`**: two-digit epic number (`01` … `13` in this repository drop).
- **`sss`**: three-digit story sequence within the epic (zero-padded).
- **`aa`**: two-digit AC sequence within the story (zero-padded).

### Examples

- `US-DG-02-014` = Epic **02**, story **014**.
- `AC-DG-02-014-03` = third acceptance criterion of that story.
- `TC-DG-02-014-03` = primary automated test for that AC (split variants: `TC-DG-02-014-03.1`, `.2`).

## Writing test cases for traceability

Each **test case** SHOULD declare:

| Field | Example | Notes |
|-------|---------|--------|
| `covers_ac` | `AC-DG-02-014-03` | Minimum; comma-separate if one test proves several ACs |
| `covers_us` | `US-DG-02-014` | Roll-up |
| `covers_epic` | `EPIC-DG-02` | Portfolio reporting |

### pytest example (marker / nodeid convention)

```text
@pytest.mark.req("AC-DG-02-014-03")
def test_create_scan_idempotency_returns_same_scan_id():
    ...
```

## Master traceability matrix (template)

Copy to your test management tool; maintain **one row per AC** minimum.

| EPIC ID | US ID | AC ID | AC summary | Test IDs (TC-*) | Automated? | Status |
|---------|-------|-------|------------|-----------------|------------|--------|
| EPIC-DG-02 | US-DG-02-001 | AC-DG-02-001-01 | … | TC-DG-02-001-01 | Y | Planned |

## Extended planning fields (generator schema)

`traceability-ac-detail-matrix.csv` includes additional governance columns:

- `phase_primary`, `phase_secondary` (from `IMPLEMENTATION_PLAN.md` epic mapping)
- `priority`, `moscow`, `release`
- `requirement_type`, `nfr_metric`, `nfr_target`
- `depends_on_epics`, `depends_on_us`, `depends_on_acs`
- `test_layer_required`, `min_automated_tests`
- `framework_tags`, `control_clause_ids`
- `owner_role`, `estimate_points`

Use these to drive sprint cut-lines, dependency ordering, and compliance exports.

## Non-functional requirements (NFR)

When an AC is non-functional (latency, SLO, cost cap), keep the same `AC-DG-*` IDs but tag:

- `kind=NFR`
- `metric=` e.g. `p95_scan_duration`, `webhook_delivery_rate`

Architecture targets appear in `Architecture_Design.md` §21, §28, §35.

## Change control

- **Do not renumber** released/stored IDs; supersede with `AC-DG-…-99` “deprecated” row or add a new story.
- **New stories** continue the next free `sss` within the epic.
