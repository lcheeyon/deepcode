# EPIC-DG-09 — Remediation advisor (Circe)

> **AC-level test specifications (generated):** Squad copy [`squads/remediation-reporting/EPIC-DG-09-detailed.md`](squads/remediation-reporting/EPIC-DG-09-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then `python3 scripts/validate_user_stories_traceability.py`.


**Goal:** Generate diff-only remediation artefacts (code, IaC, CLI guidance) with safety metadata and optional validation per `Architecture_Design.md` §17, §23.1 Q10.

**Primary personas:** Developer, DevSecOps lead.

---

## US-DG-09-001 — Produce unified diff patches (not auto-applied)

**As a** developer, **I want** Circe to output `git diff` style patches, **so that** I can review in PR tooling.

**Wireframe — remediation panel**

```text
┌──────── Remediation: SQLi in orders.py ────┐
│ Type: Code patch                            │
│ Risk of fix: Medium                         │
│ Test suggestion: pytest tests/test_orders… │
│ ┌─ unified diff preview ─────────────────┐ │
│ │ @@ class OrderRepository …              │ │
│ └──────────────────────────────────────────┘ │
│ [ Copy patch ] [ Open in editor ]          │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-09-001-01:** Patches never auto-apply; include `test_suggestion` field (Architecture §17.1–17.2).
- **AC-DG-09-001-02:** Security-critical patches include `risk_of_fix` (Architecture §17.2).
- **AC-DG-09-001-03:** Multi-file patches include ordering metadata (Architecture §17.2).

---

## US-DG-09-002 — Terraform validation (best-effort)

**As a** DevSecOps lead, **I want** optional `terraform validate` / `tflint` hooks, **so that** IaC remediations are sanity-checked.

**Acceptance criteria**

- **AC-DG-09-002-01:** When `circe_terraform_validation=true`, run fmt-check/validate/tflint where Terraform present (Architecture §23.1 Q10).
- **AC-DG-09-002-02:** Record `remediation.validation_status` + stdout/stderr excerpts; failures do not fail entire scan (Architecture §23.1 Q10).

---

## US-DG-09-003 — CLI remediation snippets per cloud

**As a** cloud engineer, **I want** provider-specific CLI remediation commands, **so that** I can operationalise fixes.

**Acceptance criteria**

- **AC-DG-09-003-01:** Remediation type `generate_cli_remediation` supported with provider tagging (Architecture §17.1; Business doc §11.3 examples).

---

## US-DG-09-004 — IaC unified diff (Terraform / ROS / CFN)

**As a** DevOps engineer, **I want** Circe to emit HCL/YAML unified diffs for IaC findings, **so that** I can open a single PR for infra fixes.

**Acceptance criteria**

- **AC-DG-09-004-01:** `generate_iac_patch` tool produces diff with file path headers per resource block (Architecture §17.1).
- **AC-DG-09-004-02:** Multi-file IaC patches include explicit file order metadata (Architecture §17.2).
- **AC-DG-09-004-03:** Patches never include secrets or data values from live cloud — only template fixes (Architecture §2.3).

---

## US-DG-09-005 — Remediation priority queue by CVSS and effort

**As a** project manager, **I want** remediations sorted by composite priority, **so that** roadmaps align to risk reduction.

**Wireframe — roadmap table**

```text
┌──────── Remediation roadmap ────────────────────────────────┐
│ Rank │ Finding      │ Effort │ Owner hint │ Dep           │
│ 1    │ TLS min ver  │ S      │ AppSec     │ —             │
│ 2    │ S3 policy *  │ M      │ Cloud      │ after IAM-12  │
└──────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-09-005-01:** Sorting uses severity, CVSS when present, exploitability hints, and estimated effort enum (Architecture §18.1 item 10).
- **AC-DG-09-005-02:** Ordering dependencies between remediations validated acyclic; cycles broken with warning.
- **AC-DG-09-005-03:** Export to CSV/JSON includes `remediation_id` joinable to `finding_id`.

---

## US-DG-09-006 — “No new imports” patch guardrail

**As a** supply-chain owner, **I want** Circe patches blocked from adding new `import` lines, **so that** dependency risk does not grow (Architecture §17.2).

**Acceptance criteria**

- **AC-DG-09-006-01:** Patch validator rejects hunks introducing new import statements unless `admin_override` flag on job (document risk).
- **AC-DG-09-006-02:** Violations surface as `remediation.status=rejected_guardrail` with machine reason.
- **AC-DG-09-006-03:** Report appendix lists skipped remediations with guardrail reason.

---

## US-DG-09-007 — Kubernetes patch suggestions (manifest-level)

**As a** platform engineer, **I want** remediations for privileged pods as strategic merge patch JSON, **so that** I can apply via `kubectl patch`.

**Acceptance criteria**

- **AC-DG-09-007-01:** Output format `json_patch` or strategic merge documented per finding type.
- **AC-DG-09-007-02:** Patches reference GVK + namespace + name in metadata (EPIC-DG-07).
- **AC-DG-09-007-03:** Dry-run instructions included in `test_suggestion` field.

---

## US-DG-09-008 — Remediation linkage back to controls

**As an** auditor, **I want** each remediation row to list `control_id`(s), **so that** fix traceability is bidirectional.

**Acceptance criteria**

- **AC-DG-09-008-01:** `Remediation` model includes `finding_id` + `control_id` + `framework` foreign keys or string ids matching findings table.
- **AC-DG-09-008-02:** API `GET …/remediations` optional endpoint or embedded in findings export (EPIC-DG-02).
- **AC-DG-09-008-03:** PDF section cross-links finding number to remediation number (EPIC-DG-10).
