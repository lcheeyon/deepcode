# EPIC-DG-08 — Compliance mapping & cross-layer reasoning (Athena)

> **AC-level test specifications (generated):** Squad copy [`squads/compliance-engine/EPIC-DG-08-detailed.md`](squads/compliance-engine/EPIC-DG-08-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py`.


**Goal:** Map controls to PASS/FAIL/PARTIAL/NA with evidence, run generator–critic reconciliation, emit cross-layer composite findings, and expose confidence for governance per `Architecture_Design.md` §3, §16, §18.

**Primary personas:** Compliance officer, Security architect.

---

## US-DG-08-001 — Per-control structured findings

**As a** compliance officer, **I want** each control mapped with severity and evidence refs, **so that** audits are traceable.

**Wireframe — control detail drawer**

```text
┌──────── Finding: ISO27001-A.10.1.1 ────────┐
│ Status: FAIL   Severity: HIGH              │
│ Confidence: 0.82                         │
│ Evidence:                                   │
│  • src/crypto/tls.ts:L42-L58               │
│  • iac/modules/s3/main.tf:L12             │
│ Reasoning summary: [expand/collapse]      │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-08-001-01:** Findings include `control_id`, `severity`, `evidence_refs`, `reasoning_summary`, `confidence_score`, `status` (Architecture §3.1, §29.1).
- **AC-DG-08-001-02:** Low confidence after max iterations marks `UNCERTAIN` + `should_escalate` behaviours per thresholds (Architecture §3.2).

---

## US-DG-08-002 — Generator + critic reconciliation

**As a** false-positive champion, **I want** critic pass to challenge generator output, **so that** over-claiming FAIL is reduced.

**Acceptance criteria**

- **AC-DG-08-002-01:** Two-pass Athena emits separate trace spans `athena_generator_pass`, `athena_critic_pass` (Architecture §3.3, §23.1 Q5).
- **AC-DG-08-002-02:** Disagreements resolve to `UNCERTAIN` per reconcile rules (Architecture §3.3).

---

## US-DG-08-003 — Cross-layer correlation findings

**As a** security architect, **I want** composite findings linking code + IaC + cloud, **so that** I see “policy on paper vs reality” gaps.

**Wireframe — correlation timeline**

```text
Code ────────● mis-use of presigned URL (Argus)
IaC  ────● bucket encryption ON (Laocoon)
Cloud ─● bucket policy s3:GetObject * (Cassandra)
        └─► Composite: HIGH — access path defeats encryption intent
```

**Acceptance criteria**

- **AC-DG-08-003-01:** `cross_layer_findings` list includes mapped frameworks + composite severity rationale (Architecture §3.4, §4.2).
- **AC-DG-08-003-02:** Executive report section highlights top cross-layer items (Architecture §18.1 item 7).

---

## US-DG-08-004 — Batched control processing (MVP)

**As a** performance owner, **I want** controls processed in semantic batches, **so that** P95 mapping stays within SLO.

**Acceptance criteria**

- **AC-DG-08-004-01:** Batch size target 8–12 controls with clustering on `scope_tags` + embedding similarity (Architecture §31.3).
- **AC-DG-08-004-02:** Feature flag `ATHENA_PER_CONTROL_SEND` defaults off (Architecture §23.1 Q1).

---

## US-DG-08-005 — Prompt injection hardening in evidence path

**As a** security reviewer, **I want** evidence wrapped and structured outputs enforced, **so that** malicious repo content cannot hijack tools.

**Acceptance criteria**

- **AC-DG-08-005-01:** Evidence segments use boundary markers in prompts (Architecture §20.2).
- **AC-DG-08-005-02:** Outputs parsed strictly to Pydantic models; free-form discarded (Architecture §6.4, §20.2).

---

## US-DG-08-006 — Compliance summary and per-framework scores

**As an** executive, **I want** `ComplianceSummary` with radar-friendly scores, **so that** board packs are one glance.

**Wireframe — score strip**

```text
┌──────── Compliance summary ────────────────────────────────┐
│ ISO 27001:  78%   等保三级: 64%   SOC2: 81%                 │
│ Cross-layer HIGH: 3   UNCERTAIN: 4   (review queue)         │
└──────────────────────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-08-006-01:** `compliance_summary` persisted with per-framework pass/fail/partial/NA counts (Architecture §4.2).
- **AC-DG-08-006-02:** Scoring weights honour `severity_weight` on controls (Architecture §16.2).
- **AC-DG-08-006-03:** UNCERTAIN ratio >30% triggers report banner + optional webhook (Architecture §8.4).

---

## US-DG-08-007 — Bilingual output for MAS / 等保 reports

**As a** regional customer, **I want** Chinese + English finding titles where configured, **so that** mixed audit teams can read reports.

**Acceptance criteria**

- **AC-DG-08-007-01:** `job_config.locale` or tenant default selects `zh`, `en`, `bilingual` modes (product schema).
- **AC-DG-08-007-02:** Bilingual mode renders primary + secondary column in finding tables (EPIC-DG-10).
- **AC-DG-08-007-03:** LLM routing prefers Qwen/DeepSeek for Chinese narrative when deployment requires (Architecture §13.1; Business doc §12).

---

## US-DG-08-008 — MMR re-ranking for diverse code evidence

**As a** mapper engineer, **I want** MMR on Athena code retrieval, **so that** top-K chunks are not near-duplicates (Architecture §12.2).

**Acceptance criteria**

- **AC-DG-08-008-01:** Athena code path uses MMR with documented lambda; falls back to plain top-K if disabled by flag.
- **AC-DG-08-008-02:** Retrieved chunk ids logged in reasoning trace redacted excerpt metadata only (EPIC-DG-11).
- **AC-DG-08-008-03:** Deterministic tie-break on chunk id ordering when scores tie (`temperature=0` path).

---

## US-DG-08-009 — Batch failure isolation and retry

**As a** reliability engineer, **I want** one Athena batch failure not to lose prior batches’ findings, **so that** resume cost is bounded.

**Acceptance criteria**

- **AC-DG-08-009-01:** Failed batch increments `error_log` and can retry batch only without re-running completed batches (Architecture §31.3–31.4).
- **AC-DG-08-009-02:** After max batch retries, remaining controls marked `UNCERTAIN` with explicit reason code.
- **AC-DG-08-009-03:** Checkpoint state after each successful batch is durable (EPIC-DG-01).

---

## US-DG-08-010 — Control applicability (NA) with justification

**As an** auditor, **I want** explicit NA with reason, **so that** frameworks do not show false gaps.

**Acceptance criteria**

- **AC-DG-08-010-01:** NA requires `na_reason` enum + short text; empty NA rejected by schema.
- **AC-DG-08-010-02:** Layer relevance from `PolicyControl` respected — e.g. pure cloud control skips code-only evidence requirement (Architecture §16.2).
- **AC-DG-08-010-03:** NA rate anomalies (>40% in a framework) flagged for product review dataset (eval hook).

---

## US-DG-08-011 — Evidence strength scoring in finding object

**As a** triage analyst, **I want** `evidence_strength` or equivalent, **so that** I sort by corroboration depth.

**Acceptance criteria**

- **AC-DG-08-011-01:** Finding schema includes machine-readable evidence grade (e.g. `direct_code_ref`, `config_only`, `heuristic`).
- **AC-DG-08-011-02:** Cross-layer findings require ≥2 layers’ evidence refs or downgrade severity (Architecture §3.4 spirit).
- **AC-DG-08-011-03:** UI and API expose same field (EPIC-DG-12).

---

## US-DG-08-012 — Trace compaction before context overflow

**As a** graph engineer, **I want** trace compaction when token budget exceeded, **so that** `ContextLengthError` triggers recovery (Architecture §10.3–10.5, §19.1).

**Acceptance criteria**

- **AC-DG-08-012-01:** On `ContextLengthError`, compactor reduces prior steps per §10.3 and retries bounded times.
- **AC-DG-08-012-02:** Compaction events logged with before/after token counts (redacted trace).
- **AC-DG-08-012-03:** If still failing, control marked `UNCERTAIN` with `error_code=CONTEXT_LIMIT`.
