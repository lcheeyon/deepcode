# DeepGuard benchmark corpus (OSS)

This directory defines a reproducible benchmark input set for demonstrating DeepGuard value to technical reviewers and investors.

## Files

- `deepguard-benchmark-manifest.yaml` — human-readable benchmark catalog.
- `deepguard-benchmark-manifest.json` — machine-readable manifest consumed by E2E tests and scripts.

## Corpus design goals

- Mix intentionally vulnerable apps (high true-positive signal).
- Mix real-world production-style repos (false-positive pressure test).
- Mix IaC, Kubernetes, and policy-as-code repos.
- Include both **git clone** and **zip/archive** ingestion paths.

## Suggested benchmark campaign

1. Run benchmark scans for all manifest entries (or per phase/sprint subset).
2. Persist resulting scan IDs and generated report artifact links.
3. Publish a sanitized evidence bundle to GitHub:
   - `reports/benchmark/index.md` summary table
   - report PDFs (or links to signed URLs if policy permits)
   - methodology and caveats
4. Update investor/reviewer documentation with:
   - number of findings by severity
   - cross-layer findings count
   - false-positive adjudication notes
   - remediation quality examples

## GitHub report index export

After benchmark scans complete, generate a GitHub-ready markdown index:

```bash
python3 scripts/export_benchmark_reports_index.py \
  --api-base-url http://127.0.0.1:8000 \
  --api-key dev \
  --scan-ids-file reports/benchmark/scan-ids.txt \
  --output reports/benchmark/index.md
```

`scan-ids.txt` format: one scan UUID per line.

## Compliance report sharing checklist (GitHub-safe)

- Remove secrets, credentials, and any tenant identifiers.
- Redact cloud account IDs where needed.
- Keep only benchmark repos and synthetic fixture tenants.
- Include model/version + policy version metadata for reproducibility.
- Add legal disclaimer for intentionally vulnerable repos.
