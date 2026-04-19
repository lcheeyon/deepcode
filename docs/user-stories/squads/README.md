# User stories by squad (generated + maintained)

Each **`EPIC-DG-NN-detailed.md`** file is produced by `scripts/generate_ac_details_and_squad_docs.py`. It mirrors the canonical [`EPIC-NN-*.md`](../) file and appends a **test specification** subsection per AC.

| Squad | Epics | Path |
|-------|-------|------|
| `compliance-engine` | `EPIC-DG-08` | [`compliance-engine/`](compliance-engine/) |
| `connectors` | `EPIC-DG-07` | [`connectors/`](connectors/) |
| `control-plane` | `EPIC-DG-02` | [`control-plane/`](control-plane/) |
| `frontend` | `EPIC-DG-12`, `EPIC-DG-14` | [`frontend/`](frontend/) |
| `identity-tenancy` | `EPIC-DG-03` | [`identity-tenancy/`](identity-tenancy/) |
| `ingestion-codeintel` | `EPIC-DG-04`, `EPIC-DG-06` | [`ingestion-codeintel/`](ingestion-codeintel/) |
| `observability` | `EPIC-DG-11` | [`observability/`](observability/) |
| `platform-runtime` | `EPIC-DG-01` | [`platform-runtime/`](platform-runtime/) |
| `policy` | `EPIC-DG-05` | [`policy/`](policy/) |
| `remediation-reporting` | `EPIC-DG-09`, `EPIC-DG-10` | [`remediation-reporting/`](remediation-reporting/) |
| `security-deployment` | `EPIC-DG-13` | [`security-deployment/`](security-deployment/) |

## Regenerate

```bash
python3 scripts/generate_ac_details_and_squad_docs.py
```

## Machine-readable matrix

All AC rows: [`../traceability-ac-detail-matrix.csv`](../traceability-ac-detail-matrix.csv).
