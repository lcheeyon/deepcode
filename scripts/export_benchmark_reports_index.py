#!/usr/bin/env python3
"""
Export a GitHub-ready benchmark report index markdown from DeepGuard scan IDs.

Example:
  python3 scripts/export_benchmark_reports_index.py \
    --api-base-url http://127.0.0.1:8000 \
    --api-key dev \
    --scan-id 11111111-1111-4111-8111-111111111111 \
    --scan-id 22222222-2222-4222-8222-222222222222 \
    --output reports/benchmark/index.md
"""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "reports" / "benchmark" / "index.md"


def request_json(url: str, api_key: str) -> dict:
    req = urllib.request.Request(url, headers={"X-API-Key": api_key})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def check_artifact_endpoint(url: str, api_key: str) -> int | None:
    req = urllib.request.Request(url, headers={"X-API-Key": api_key}, method="GET")
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
    try:
        with opener.open(req, timeout=30) as resp:
            return getattr(resp, "status", 200)
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


def sanitize_repo(repo: dict) -> str:
    url = str(repo.get("url", ""))
    if "@" in url and "://" in url:
        # strip userinfo if any
        parsed = urllib.parse.urlsplit(url)
        netloc = parsed.hostname or ""
        if parsed.port:
            netloc += f":{parsed.port}"
        return urllib.parse.urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment))
    return url


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--api-base-url", required=True, help="e.g. http://127.0.0.1:8000")
    p.add_argument("--api-key", required=True)
    p.add_argument("--scan-id", action="append", default=[], help="repeatable")
    p.add_argument("--scan-ids-file", help="optional newline-delimited scan IDs")
    p.add_argument("--output", default=str(DEFAULT_OUT))
    args = p.parse_args()

    scan_ids: list[str] = []
    scan_ids.extend(args.scan_id)
    if args.scan_ids_file:
        for line in Path(args.scan_ids_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                scan_ids.append(line)
    scan_ids = list(dict.fromkeys(scan_ids))
    if not scan_ids:
        raise SystemExit("No scan IDs provided. Use --scan-id or --scan-ids-file.")

    base = args.api_base_url.rstrip("/")
    rows: list[dict[str, str]] = []
    for sid in scan_ids:
        data = request_json(f"{base}/v1/scans/{sid}", args.api_key)
        status = str(data.get("status", "UNKNOWN"))
        job_config = data.get("job_config", {}) if isinstance(data.get("job_config"), dict) else {}
        repo = job_config.get("repo", {}) if isinstance(job_config.get("repo"), dict) else {}
        policy_ids = job_config.get("policy_ids", [])
        policy_str = ", ".join(policy_ids) if isinstance(policy_ids, list) else str(policy_ids)

        artifact_id = (
            data.get("report_artifact_id")
            or (data.get("report_artifact_ref") or {}).get("artifact_id")
            if isinstance(data.get("report_artifact_ref"), dict)
            else data.get("report_artifact_id")
        )
        report_url = ""
        report_status = ""
        if artifact_id:
            report_url = f"{base}/v1/scans/{sid}/artifacts/{artifact_id}"
            rs = check_artifact_endpoint(report_url, args.api_key)
            report_status = str(rs) if rs is not None else "N/A"

        rows.append(
            {
                "scan_id": sid,
                "status": status,
                "repo": sanitize_repo(repo),
                "ref": str(repo.get("ref", "")),
                "policies": policy_str,
                "report_artifact_id": str(artifact_id or ""),
                "report_endpoint": report_url,
                "report_endpoint_status": report_status,
            }
        )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    lines = [
        "# DeepGuard benchmark compliance report index",
        "",
        f"_Generated: {now}_",
        "",
        "> Reviewer note: this page should only include benchmark/fake tenants and sanitized metadata.",
        "",
        "| Scan ID | Status | Repository | Ref | Policies | Report artifact | Report endpoint status |",
        "|---------|--------|------------|-----|----------|-----------------|------------------------|",
    ]
    for r in rows:
        report_cell = (
            f"[`{r['report_artifact_id']}`]({r['report_endpoint']})" if r["report_artifact_id"] else "N/A"
        )
        lines.append(
            f"| `{r['scan_id']}` | `{r['status']}` | `{r['repo']}` | `{r['ref']}` | `{r['policies']}` | {report_cell} | `{r['report_endpoint_status'] or 'N/A'}` |"
        )
    lines.extend(
        [
            "",
            "## Publishing checklist",
            "",
            "- [ ] Verify no real customer tenant or credentials are present.",
            "- [ ] Ensure report links are intended for public/shared audience (or replace with local file links).",
            "- [ ] Add benchmark methodology summary and findings highlights.",
            "",
        ]
    )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote benchmark report index: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
