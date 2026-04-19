# EPIC-DG-10 — Report assembly & PDF (Penelope)

> **AC-level test specifications (generated):** Squad copy [`squads/remediation-reporting/EPIC-DG-10-detailed.md`](squads/remediation-reporting/EPIC-DG-10-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py`.


**Goal:** Deterministically assemble audit-grade PDFs with CJK support, structured sections, and encrypted object storage per `Architecture_Design.md` §18, §32.

**Primary personas:** Auditor, Executive sponsor.

---

## US-DG-10-001 — Generate full report outline

**As an** auditor, **I want** the PDF to follow the mandated section order, **so that** my firm’s review checklist maps cleanly.

**Wireframe — report TOC preview (HTML/PDF)**

```text
┌──────── Report preview ──────────────────────┐
│ 1 Executive summary                        │
│ 2 Scan metadata                            │
│ 3 Compliance score dashboard               │
│ … Cross-layer correlation …                │
│ 9 Remediation roadmap                      │
│ Appendix B Evidence references             │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-10-001-01:** Sections 1–13 from §18.1 appear with stable ordering and anchors.
- **AC-DG-10-001-02:** Same inputs + policy version yield structurally identical skeleton (determinism goal Architecture §2.3) — allow bounded LLM variance only in narrative blocks explicitly flagged “LLM-polished”.

---

## US-DG-10-002 — CJK font embedding for Chinese reports

**As a** China assessor, **I want** Chinese text rendered correctly, **so that** submissions are accepted.

**Acceptance criteria**

- **AC-DG-10-002-01:** ReportLab pipeline bundles CJK fonts (STHeiti/Songti) in image layer (Architecture §18.2; Business doc §16).

---

## US-DG-10-003 — Encrypted PDF artefact with checksum

**As a** security officer, **I want** encrypted PDF stored in tenant object namespace, **so that** confidentiality matches contract.

**Acceptance criteria**

- **AC-DG-10-003-01:** Final `report.pdf` registered in `artifacts` with `checksum_sha256`, encryption mode, optional `expires_at` for presigned flows (Architecture §29.1, §32.1).
- **AC-DG-10-003-02:** Default retention aligns to 7-year audit requirement where configured (Architecture §14.2, §32.2).

---

## US-DG-10-004 — Evidence appendix with file:line citations

**As an** external auditor, **I want** appendix B to enumerate evidence pointers, **so that** sampling is efficient.

**Acceptance criteria**

- **AC-DG-10-004-01:** Appendix B lists `file_path:line` or cloud ARN references matching DB `evidence_refs` JSON (Architecture §18.1; §29.1).

---

## US-DG-10-005 — Methodology & limitations transparency

**As a** risk committee member, **I want** explicit methodology including model versions, **so that** we understand residual risk.

**Acceptance criteria**

- **AC-DG-10-005-01:** Appendix documents tool versions, LLM models, cache thresholds, known truncation warnings (Architecture §18.1 item 11).

---

## US-DG-10-006 — Radar / heatmap charts for framework domains

**As a** risk committee member, **I want** visual radar of control domains, **so that** weak domains stand out (Architecture §18.1 item 3; Business doc §16).

**Acceptance criteria**

- **AC-DG-10-006-01:** Charts generated via matplotlib or equivalent; embedded as vector or high-DPI raster in PDF.
- **AC-DG-10-006-02:** Chart data JSON archived alongside PDF for reproducibility.
- **AC-DG-10-006-03:** Failure to render chart downgrades to table without failing scan.

---

## US-DG-10-007 — Markdown intermediate artefact

**As a** integrator, **I want** optional `report.md` artefact, **so that** I can publish to Confluence or Git.

**Acceptance criteria**

- **AC-DG-10-007-01:** Jinja → Markdown stage stored as artifact kind `report_md` with checksum (Architecture §18.2).
- **AC-DG-10-007-02:** Markdown excludes raw secrets; same redaction rules as PDF (Architecture §20.3).
- **AC-DG-10-007-03:** Download path mirrors PDF artefact API pattern (EPIC-DG-02).

---

## US-DG-10-008 — Cover page branding and classification

**As a** enterprise customer, **I want** logo, classification banner (`Confidential`), **so that** PDFs meet policy (Business doc §16 cover).

**Acceptance criteria**

- **AC-DG-10-008-01:** Tenant settings supply `logo_url`, `classification_label`, `footer_text` with size limits.
- **AC-DG-10-008-02:** Broken logo URL does not fail PDF; placeholder used.
- **AC-DG-10-008-03:** Classification appears on every page footer when configured.

---

## US-DG-10-009 — Digital fingerprint / hash page for integrity

**As a** recipient, **I want** SHA-256 of PDF printed on appendix, **so that** I can verify file integrity out-of-band.

**Acceptance criteria**

- **AC-DG-10-009-01:** Printed hash matches `artifacts.checksum_sha256` for stored object.
- **AC-DG-10-009-02:** Optional PGP signing is deployment-specific (document if supported).
- **AC-DG-10-009-03:** UI displays same hash next to download (EPIC-DG-12).

---

## US-DG-10-010 — Report generation idempotency on retry

**As a** worker, **I want** Penelope retries not to duplicate PDFs with different ids, **so that** artefact inventory stays clean.

**Acceptance criteria**

- **AC-DG-10-010-01:** Re-invoking Penelope after success returns same `report_artifact_id` or supersedes with version pointer (document).
- **AC-DG-10-010-02:** Partial PDF write never exposes corrupt download; atomic rename pattern.
- **AC-DG-10-010-03:** Failed PDF render sets `error_code` on scan and retains logs.

---

## US-DG-10-011 — Appendix C scan configuration dump

**As an** assessor, **I want** redacted `job_config` JSON in appendix, **so that** methodology reviewers see scope.

**Acceptance criteria**

- **AC-DG-10-011-01:** Secrets and credential refs replaced with `[REDACTED]` literal (Architecture §20.3).
- **AC-DG-10-011-02:** Includes `policy_versions` map used for the run (Architecture §29.1).
- **AC-DG-10-011-03:** Includes model routing summary (which providers invoked) without API keys.
