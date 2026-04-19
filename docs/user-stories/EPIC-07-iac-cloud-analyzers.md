# EPIC-DG-07 — IaC & live cloud analysers (Laocoon + Cassandra)

> **AC-level test specifications (generated):** Squad copy [`squads/connectors/EPIC-DG-07-detailed.md`](squads/connectors/EPIC-DG-07-detailed.md); per-AC rows [`traceability-ac-detail-matrix.csv`](traceability-ac-detail-matrix.csv), JSON [`traceability-ac-detail.json`](traceability-ac-detail.json). Regenerate: `python3 scripts/generate_ac_details_and_squad_docs.py` then `python3 scripts/validate_user_stories_traceability.py`.


**Goal:** Produce normalised IaC findings and cloud posture findings using read-only connectors and typed tool calls per `Architecture_Design.md` §15–§16, product multi-cloud claims.

**Primary personas:** Cloud security engineer, DevOps.

---

## US-DG-07-001 — IaC parser registry coverage

**As a** DevOps engineer, **I want** Terraform/CFN/K8s/ROS/Huawei templates parsed, **so that** misconfigurations become evidence-backed findings.

**Wireframe — IaC inventory**

```text
┌──────── IaC files detected ─────────────────┐
│ ./infra/main.tf          Terraform  [view] │
│ ./k8s/prod/deploy.yaml   Kubernetes [view]│
│ Filters: [provider ▼] [severity ▼]         │
└─────────────────────────────────────────────┘
```

**Acceptance criteria**

- **AC-DG-07-001-01:** Parser registry includes backends listed in §15.1 for GA targets (Terraform, CFN, K8s, Ali ROS, Huawei template).
- **AC-DG-07-001-02:** Tool execution uses `safe_read` sandbox — no path traversal (Architecture §6.5, §20.3).

---

## US-DG-07-002 — Structured tool-calling loop with caps

**As a** platform engineer, **I want** bounded ReAct iterations, **so that** runaway tool loops cannot burn tokens.

**Acceptance criteria**

- **AC-DG-07-002-01:** `max_iterations` default 5 per agent configuration (Architecture §3.1).
- **AC-DG-07-002-02:** Tool failures append `AgentError`, mark resource `SKIPPED`, continue when non-fatal (Architecture §31.4).

---

## US-DG-07-003 — Cloud connector abstraction

**As a** multi-cloud customer, **I want** provider-specific SDKs behind `CloudConnector`, **so that** adding a vendor does not fork core mapping.

**Acceptance criteria**

- **AC-DG-07-003-01:** Interface methods include IAM/network/storage/compute/encryption/audit accessors (Architecture §15.2).
- **AC-DG-07-003-02:** AWS + Alibaba + Tencent + Huawei connectors enumerated in Chinese business doc map to same `ResourceSnapshot` canonical model (Business doc §13–§14).

---

## US-DG-07-004 — Read-only enforcement

**As a** CISO, **I want** guarantees connectors cannot mutate resources, **so that** production safety is preserved.

**Acceptance criteria**

- **AC-DG-07-004-01:** Cloud credentials documented as read-only IAM/CAM policies (Architecture §2.3; Business doc §13.x).
- **AC-DG-07-004-02:** No write APIs invoked in connector code paths (static analysis / contract tests).

---

## US-DG-07-005 — Partial cloud degradation

**As an** operator, **I want** scans to continue when a region API fails, **so that** I still receive partial coverage.

**Acceptance criteria**

- **AC-DG-07-005-01:** `CloudConnectorError` triggers degraded snapshot with explicit coverage gaps in report appendix (Architecture §19.1).

---

## US-DG-07-006 — Kubernetes manifest validation findings

**As a** platform engineer, **I want** privileged containers, hostPath, and missing resource limits flagged, **so that** CIS/K8s controls map cleanly.

**Acceptance criteria**

- **AC-DG-07-006-01:** `kubernetes-validate` (or successor) integrated; invalid manifests produce `SKIPPED` with reason (Architecture §15.1).
- **AC-DG-07-006-02:** Findings reference `namespace/kind/name` keys in evidence.
- **AC-DG-07-006-03:** Helm charts expanded with `helm template` when `scan_layers.iac` includes helm (beta documented Architecture §11.2).

---

## US-DG-07-007 — Terraform module graph and provider constraints

**As a** DevOps engineer, **I want** module depth and provider version constraints summarised, **so that** Athena reasons about blast radius.

**Acceptance criteria**

- **AC-DG-07-007-01:** Parser extracts module tree to max depth configurable; truncates with warning (Architecture §11.6 spirit).
- **AC-DG-07-007-02:** Provider `required_version` and `terraform` block constraints appear in structured summary passed to Athena.
- **AC-DG-07-007-03:** Remote modules referenced by git URL recorded as third-party risk flag (Business doc supply chain).

---

## US-DG-07-008 — CloudConnector contract tests (VCR)

**As a** CI maintainer, **I want** sanitised VCR fixtures per provider, **so that** connectors do not regress.

**Acceptance criteria**

- **AC-DG-07-008-01:** Each connector has `pytest-recording` cassette suite with secrets redacted (Architecture §33.1).
- **AC-DG-07-008-02:** CI runs contract suite on provider SDK upgrades gated by maintainer approval.
- **AC-DG-07-008-03:** Recorded responses versioned with `schema_ver` bump when normaliser changes.

---

## US-DG-07-009 — Normalised `ResourceSnapshot` schema versioning

**As a** mapper author, **I want** versioned canonical schema for cloud resources, **so that** Athena prompts stay stable across vendors.

**Acceptance criteria**

- **AC-DG-07-009-01:** Every snapshot JSON includes `schema_ver` and `provider` and `captured_at`.
- **AC-DG-07-009-02:** Breaking normaliser changes bump `schema_ver` and trigger regression evals (EPIC-DG-11).
- **AC-DG-07-009-03:** Unknown resource types preserved as raw blob under typed envelope for forward compatibility.

---

## US-DG-07-010 — Alibaba / Tencent / Huawei-specific checks (domestic clouds)

**As a** China-region customer, **I want** checks aligned to RAM/CAM/IAM and OSS/COS/OBS patterns, **so that** 等保 evidence is meaningful (Business doc §13).

**Acceptance criteria**

- **AC-DG-07-010-01:** Alibaba: ActionTrail multi-region, OSS public access, ACK API exposure checks present in connector output mapping table (Business doc §13.1).
- **AC-DG-07-010-02:** Tencent: CloudAudit, COS public ACL, CWP coverage signals present (Business doc §13.2).
- **AC-DG-07-010-03:** Huawei: CTS, DEW/SM4 encryption flags, CBH presence captured where API allows (Business doc §13.3).

---

## US-DG-07-011 — Cloud resource rate limiting and pagination

**As a** connector developer, **I want** exponential backoff on API throttles, **so that** large accounts complete without fatal error.

**Acceptance criteria**

- **AC-DG-07-011-01:** Throttling uses jittered backoff; max retry count documented per SDK call site.
- **AC-DG-07-011-02:** Pagination cursors for massive IAM policy sets do not OOM; spill to artifact ref (Architecture §5.3).
- **AC-DG-07-011-03:** Partial completion sets `cloud_findings` metadata `coverage=partial` with reasons.

---

## US-DG-07-012 — CDK / Pulumi / Bicep beta paths

**As a** modern IaC user, **I want** optional analysis for CDK TypeScript and Bicep, **so that** roadmap parity is visible in scan config.

**Acceptance criteria**

- **AC-DG-07-012-01:** Feature flag gates CDK/Bicep/Pulumi parsers listed Architecture §15.1; disabled by default in MVP if unstable.
- **AC-DG-07-012-02:** When disabled, scan does not fail; stage skipped with user-visible notice.
- **AC-DG-07-012-03:** When enabled, findings tagged `layer=IAC` and `parser_version` set for audit.
