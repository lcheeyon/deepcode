# DeepGuard / 玄武合规引擎 — User Stories (Product Backlog)

This folder contains **EPIC**-grouped user stories derived from:

- `DeepGuard_Compliance_Engine.md` (product scope, roadmap, frameworks)
- `Architecture_Design.md` (Odysseus Engine, API §28, data model, workers, security)
- `玄武合规引擎_商业计划书.md` (regional deployment, domestic clouds, GTM)

## How to use these artefacts

1. Read **`00-numbering-and-traceability.md`** first for the **ID scheme** and how to build a **requirements → acceptance criteria → test case** matrix.
2. **Per squad (expanded AC test specs):** open [`squads/README.md`](squads/README.md) and your squad’s **`EPIC-DG-NN-detailed.md`** — generated from the canonical EPIC file, with a **test specification table per AC**.
3. **Machine-readable matrix (all ACs):** [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv) — filter by `squad`, `ac_id`, or `us_id`; regenerate with `python3 scripts/generate_ac_details_and_squad_docs.py`.
4. Edit **canonical** [`EPIC-NN-*.md`](EPIC-01-scan-job-orchestration.md) files at repo root of `docs/user-stories/`; then **regenerate** squad copies + CSV so IDs stay aligned. (Non-canonical supplements use a `SUPPLEMENT-*.md` filename so they are **not** picked up by the generator—see [`SUPPLEMENT-EPIC-02-04-ingestion-contracts.md`](SUPPLEMENT-EPIC-02-04-ingestion-contracts.md).)
5. When authoring tests, **reference the `AC-DG-*` IDs** (and suggested `TC-DG-*` from the CSV) in pytest markers / Xray so coverage rolls up to `US-DG-*` and `EPIC-DG-*`.
6. **Before implementation:** write an **approved** engineering design spec under **`docs/design/`** (slice/delta for the feature or `IMPLEMENTATION_PLAN` phase) and follow **`.cursor/skills/deepguard-delivery-quality/SKILL.md`** — stories → approved design → code → **unit coverage ≥80%** on touched packages → **integration** tests → **Playwright BDD** → **manual UAT** last.

## Implementation phase mapping

Each **`IMPLEMENTATION_PLAN.md`** phase (L0–L14, C0–C5) is mapped to **which EPICs** it primarily delivers — see **`IMPLEMENTATION_PLAN.md` §2.4** (Phase ↔ EPIC traceability). **EPIC-DG-12** is split across phases: **integrated UI starts at L3** (details in the same §2.4 subsection). Use that when scoping design specs and sprint goals.

## EPIC index

| EPIC ID | File | Squad (generated detail) | Theme |
|---------|------|---------------------------|--------|
| EPIC-DG-01 | `EPIC-01-scan-job-orchestration.md` | [`platform-runtime`](squads/platform-runtime/) | Scan lifecycle, queue, checkpoints, cancel/resume |
| EPIC-DG-02 | `EPIC-02-control-plane-api.md` | [`control-plane`](squads/control-plane/) | FastAPI `/v1` resources, idempotency, webhooks |
| EPIC-DG-03 | `EPIC-03-identity-tenancy-rbac.md` | [`identity-tenancy`](squads/identity-tenancy/) | JWT, roles, tenant isolation, runtime_config |
| EPIC-DG-04 | `EPIC-04-ingestion-hermes.md` | [`ingestion-codeintel`](squads/ingestion-codeintel/) | Repos, archives, CI injection, cloud snapshots |
| EPIC-DG-05 | `EPIC-05-policy-tiresias.md` | [`policy`](squads/policy/) | Frameworks, uploads, control catalogue |
| EPIC-DG-06 | `EPIC-06-code-indexing-argus.md` | [`ingestion-codeintel`](squads/ingestion-codeintel/) | Parsing, embeddings, hybrid retrieval |
| EPIC-DG-07 | `EPIC-07-iac-cloud-analyzers.md` | [`connectors`](squads/connectors/) | Laocoon + Cassandra, connectors |
| EPIC-DG-08 | `EPIC-08-compliance-athena.md` | [`compliance-engine`](squads/compliance-engine/) | Mapping, cross-layer, confidence, HITL |
| EPIC-DG-09 | `EPIC-09-remediation-circe.md` | [`remediation-reporting`](squads/remediation-reporting/) | Patches, validation, playbook output |
| EPIC-DG-10 | `EPIC-10-reporting-penelope.md` | [`remediation-reporting`](squads/remediation-reporting/) | PDF structure, artefacts, retention |
| EPIC-DG-11 | `EPIC-11-observability-cost-governance.md` | [`observability`](squads/observability/) | LangSmith/LangFuse, budgets, alerts |
| EPIC-DG-12 | `EPIC-12-console-ui.md` | [`frontend`](squads/frontend/) | Operator/developer UI flows (wireframes) |
| EPIC-DG-13 | `EPIC-13-security-deployment-modes.md` | [`security-deployment`](squads/security-deployment/) | Secrets, sandbox, SaaS/VPC/air-gap |
| EPIC-DG-14 | `EPIC-14-console-frontend-backend-mvp.md` | [`frontend`](squads/frontend/) (regenerate) | **MVP web console** — exercises **current** `/v1` API; wireframes in `docs/design/frontend-console-mvp-wireframes-and-mockups.md` |

## Traceability artefacts

- `traceability-matrix-sample.csv` — starter columns for importing into Xray / TestRail / Sheets.
- **`traceability-ac-detail-matrix.csv`** — **one row per AC** with objective, preconditions, verification procedure, edge cases, suggested `TC-DG-*` IDs (generator-maintained).
- **`squads/`** — per-squad **`EPIC-DG-NN-detailed.md`** files (same stories as canonical EPICs + appended AC test spec sections).

## Backlog inventory (user stories)

| EPIC ID | User story ID range | Count (approx.) |
|---------|---------------------|-----------------|
| EPIC-DG-01 | US-DG-01-001 … US-DG-01-012 | 12 |
| EPIC-DG-02 | US-DG-02-001 … US-DG-02-014 | 14 |
| EPIC-DG-03 | US-DG-03-001 … US-DG-03-010 | 10 |
| EPIC-DG-04 | US-DG-04-001 … US-DG-04-012 | 12 |
| EPIC-DG-05 | US-DG-05-001 … US-DG-05-010 | 10 |
| EPIC-DG-06 | US-DG-06-001 … US-DG-06-012 | 12 |
| EPIC-DG-07 | US-DG-07-001 … US-DG-07-012 | 12 |
| EPIC-DG-08 | US-DG-08-001 … US-DG-08-012 | 12 |
| EPIC-DG-09 | US-DG-09-001 … US-DG-09-008 | 8 |
| EPIC-DG-10 | US-DG-10-001 … US-DG-10-011 | 11 |
| EPIC-DG-11 | US-DG-11-001 … US-DG-11-010 | 10 |
| EPIC-DG-12 | US-DG-12-001 … US-DG-12-014 | 14 |
| EPIC-DG-13 | US-DG-13-001 … US-DG-13-011 | 11 |
| EPIC-DG-14 | US-DG-14-001 … US-DG-14-014 | 14 |
| **Total** | | **~162** |

Cross-EPIC dependencies are called out in prose (e.g. UI stories reference API ACs). Prefer linking tests to **`AC-DG-*`** IDs, not only to `US-DG-*`.

## Consistency checks

After editing canonical `EPIC-*.md`, regenerate squad docs + CSV, then validate:

```bash
python3 scripts/generate_ac_details_and_squad_docs.py
python3 scripts/validate_user_stories_traceability.py
```

The validator fails if any `AC-DG-*` in markdown is missing from `traceability-ac-detail-matrix.csv` (or if the CSV has orphan rows).

## Possible further enhancements

These are **optional** backlog items for the specification itself (not product code):

| Enhancement | Why it helps |
|-------------|----------------|
| **Phase ↔ AC matrix** | Add a column or join file mapping each `AC-DG-*` to `IMPLEMENTATION_PLAN.md` L*/C* phases (beyond epic-level §2.4) for sprint planning. |
| **Explicit dependencies** | `depends_on: [US-DG-02-009]` (or AC-level) in story headers for ordering and critical path. |
| **MoSCoW / priority** | Tag each US or AC `Must` / `Should` / `Could` for MVP cut-lines. |
| **Regulatory mapping** | Extra column: ISO/等保/SOC2 clause ids already in text → structured IDs for assessor exports. |
| **Gherkin / BDD snippets** | Optional `Scenario:` block per AC in squad detail or a parallel `features/*.feature` generated stub. |
| **Non-functional tags** | `kind: NFR` + `metric: p95_scan_duration` in CSV for SLO ACs (some already implied in prose). |
| **Definition of Done** | Per-epic checklist (docs updated, metrics, runbook) linked from `EPIC-*` goal section. |
| **JSON export** | `traceability-ac-detail.json` for dashboards (same fields as CSV). |
| **CI gate** | Run `validate_user_stories_traceability.py` on PRs that touch `docs/user-stories/`. |
| **Changelog** | `docs/user-stories/CHANGELOG.md` recording AC additions/supersedions (audit of requirement drift). |
| **Smarter `Given` parsing** | Generator heuristics to shorten preconditions when “Given” spans multiple clauses. |

The traceability **skill** (`.cursor/skills/deepguard-requirements-traceability/SKILL.md`) can be extended when any of the above becomes team policy.

## Document status

**Draft for engineering & QA alignment** — IDs are stable; wording may evolve with implementation ADRs.
