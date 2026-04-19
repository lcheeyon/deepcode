---
name: deepguard-delivery-quality
description: >-
  DeepGuard delivery pipeline: well-written user stories and ACs, design
  specifications written and explicitly approved before any implementation
  coding, then unit tests at 80% coverage on touched code, integration tests,
  Playwright BDD scenarios, and only then manual human UAT. Use when executing
  IMPLEMENTATION_PLAN.md Parts or Phases, opening or reviewing PRs, defining CI
  gates, authoring Playwright or Gherkin tests, design reviews, or when the
  user mentions coverage, BDD, sign-off, or definition of done.
---

# DeepGuard — delivery, design approval, and test pyramid

**Companion skills:** `deepguard-requirements-traceability` (IDs + matrix), `deepguard-architecture` (technical contracts).  
**Backlog:** `docs/user-stories/EPIC-*.md`, `docs/user-stories/00-numbering-and-traceability.md`.

---

## 1. Mandatory order (do not skip steps)

For **every** Part / Phase slice (e.g. `IMPLEMENTATION_PLAN.md` L3, C1) or releasable feature branch:

```text
(1) User stories + ACs written ──► (2) Design spec written ──► (3) Design approved
         │                                    │
         │                                    └── Record approver + date in spec frontmatter
         ▼
(4) Implementation (code) ──► (5) Unit tests ≥80% on touched packages ──► (6) Integration tests green
         │
         ▼
(7) Playwright BDD suite green ──► (8) Manual UAT / exploratory ──► (9) Merge / deploy
```

**Agent / human rule:** **No production-bound implementation** (merging to `main` or deploying) until steps **(1)–(7)** are satisfied for that slice. Step **(8)** is required before marking a Phase **done** in the plan or releasing to customers.

If an emergency hotfix bypasses a step, it **must** be ticketed to backfill stories, spec delta, and tests within one sprint.

---

## 2. User stories (before design)

### 2.1 Quality bar

- Stories follow **INVEST** (Independent, Negotiable, Valuable, Estimable, Small, Testable).  
- Each story has **clear persona** (“As a … I want … So that …”).  
- **Acceptance criteria** are atomic, observable, and each maps to one **`AC-DG-*`** ID (see traceability skill).  
- Non-functional needs use **`AC-DG-*`** with `kind=NFR` + measurable threshold.

### 2.2 Where to write

- Add or extend **`docs/user-stories/EPIC-{nn}-*.md`** and **`docs/user-stories/README.md`** index if new EPIC.  
- Update **traceability matrix** (CSV or tool export) with one row per **AC** before requesting design approval.

### 2.3 Exit gate — “Stories ready for design”

- [ ] Every AC is **testable** (can write a failing test or BDD scenario title).  
- [ ] Story IDs (`US-DG-*`) linked to Phase/Part in `IMPLEMENTATION_PLAN.md` or epic notes.  
- [ ] No orphan scope: every story references `Architecture_Design.md` section(s) or ADR where relevant.

---

## 3. Design specifications (before coding)

### 3.1 What counts as a design spec

A **design spec** is a short engineering document that **closes ambiguity** before code. It is **not** a duplicate of `Architecture_Design.md`; it is a **slice** or **delta** for the current feature/phase.

Minimum contents:

| Section | Purpose |
|---------|---------|
| Context & goals | Link `US-DG-*`, `EPIC-DG-*`, `IMPLEMENTATION_PLAN` phase id (e.g. L4) |
| Decisions | APIs, schemas, state transitions, error codes, feature flags |
| Out of scope | Explicit boundaries to prevent gold-plating |
| Risks / open questions | Or “none” |
| Test strategy | Which ACs → unit vs integration vs Playwright file |

**Suggested path:** `docs/design/DG-{epic}-{story}-design.md` or `docs/design/phase-L{n}-{slug}.md` (pick one convention per repo and keep it).

### 3.2 Approval

- Spec status line in frontmatter: `status: draft | in-review | approved`.  
- **`approved`** requires **at least two** of: *Product owner / PM*, *Tech lead / Architect*, *Security champion* (same person may not count twice for regulated features—use two distinct people when policy demands).  
- Record: `approvers: [name, name]`, `approved_date: YYYY-MM-DD` in the spec header.

### 3.3 Exit gate — “Design approved; coding allowed”

- [ ] Spec file exists and `status: approved`.  
- [ ] Spec links all **`AC-DG-*`** in scope.  
- [ ] Contradictions with `Architecture_Design.md` **resolved** (update architecture doc or ADR, not silent drift).

---

## 4. Implementation (coding)

- Implement only what the **approved design spec** and **`AC-DG-*`** require.  
- Trace commits / PR description to **`US-DG-*` / `AC-DG-*`**.  
- Follow `deepguard-architecture` for stack, boundaries, and security.

---

## 5. Unit tests (coverage gate)

### 5.1 Threshold

- **Minimum 80% line coverage** on **packages touched** by the change (not only new lines). Scope = directories listed in the PR/design spec (e.g. `packages/core`, `packages/parsers`).  
- Use **`pytest-cov`** with `--cov-fail-under=80` scoped to those paths in CI for the PR.  
- **Exclude** generated code, `if TYPE_CHECKING`, and trivial `__repr__` only if excluded paths are documented in `pyproject.toml` / `coveragerc`.

### 5.2 Traceability

- Each unit test **must** reference at least one **`AC-DG-*`** via `@pytest.mark.req("AC-DG-…")` (or repo-agreed equivalent documented in `00-numbering-and-traceability.md`).

### 5.3 Exit gate — “Unit tests sufficient”

- [ ] `pytest` + coverage ≥ **80%** on agreed paths; CI job **red** if below.  
- [ ] No skipped tests without ticket / reason in PR.

---

## 6. Integration tests

### 6.1 Definition (for this repo)

- Run against **real local dependencies**: Docker Compose Postgres, Redis, MinIO, API + worker processes as needed.  
- **No Playwright** in this layer unless driving only HTTP API without browser chrome (prefer **httpx** / **pytest** for API integration).  
- Prove **cross-component** behaviour: e.g. `POST /v1/scans` → queue → worker status → DB row.

### 6.2 Location & naming

- Suggested: `tests/integration/` with markers `@pytest.mark.integration`.  
- CI: separate job from unit tests (slower); may run on `main` only if cost-sensitive, but **must run before merge** for release branches.

### 6.3 Exit gate

- [ ] All integration tests for in-scope **ACs** pass.  
- [ ] Each test documents which **`AC-DG-*`** it covers.

---

## 7. BDD tests (Playwright)

### 7.1 Role

- **Playwright** implements **BDD-style** acceptance: **Given / When / Then** expressed as `test.describe` + readable step comments **or** Gherkin via **`pytest-bdd`** / **`behave`** only if the team standardises one parser—**default recommendation: Playwright Test runner** with TypeScript or JavaScript under `e2e/playwright/` **or** Python `pytest-playwright` under `tests/e2e_bdd/`; pick one and document in design spec.

### 7.2 Mapping

- One **feature file** or **describe block** per **`US-DG-*`** (or per epic slice), file header lists **`US-DG-*`**, **`AC-DG-*`**.  
- Scenarios must be **executable** against **local** or **CI** environment URL (`BASE_URL` env).

### 7.3 Exit gate — “BDD green before manual”

- [ ] Playwright (or agreed BDD runner) **0 failures** on target branch.  
- [ ] Traces/videos on failure retained in CI artefacts (not committed).  
- [ ] **No manual UAT** until this gate passes (except documented smoke for environment access).

---

## 8. Manual human testing (last)

### 8.1 Purpose

- Exploratory testing, UX judgement, accessibility, demo to stakeholder, production-like sanity.  
- **Does not replace** automated gates.

### 8.2 Exit gate — “Phase / Part complete”

- [ ] Short **UAT checklist** in PR or `docs/uat/phase-L{n}.md` with sign-off names + date.  
- [ ] Known defects logged with severity; **no** open **P1** for in-scope ACs.

---

## 9. CI pipeline order (recommended)

```text
lint (ruff) → typecheck (mypy) → unit tests (cov ≥80%) → build images → integration tests → Playwright BDD → (optional) deploy to ephemeral env
```

Manual UAT occurs **after** green CI when validating a release candidate or closing a Phase in `IMPLEMENTATION_PLAN.md`.

---

## 10. Mapping to `IMPLEMENTATION_PLAN.md` Parts / Phases

- **Before starting any L* or C* phase:** ensure stories + ACs exist for that phase; write **phase design spec** summarising components touched; get **approved**.  
- **Before closing the phase:** unit (80%) + integration + Playwright for scenarios tied to that phase’s stories; then manual checklist.  
- Update **`IMPLEMENTATION_PLAN.md`** exit criteria checkboxes only when **§8** UAT sign-off exists for that phase (or explicit waiver with ticket).

---

## 11. Memory compaction — preserve

- Order: **stories → approved design spec → code → unit 80% → integration → Playwright BDD → manual UAT**.  
- Coverage: **80%** on **touched** packages for the change.  
- Traceability: **`AC-DG-*`** on all automated tests.  
- Skill name: **`deepguard-delivery-quality`**.
