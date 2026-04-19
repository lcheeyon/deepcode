#!/usr/bin/env python3
"""Emit one self-contained HTML pytest report per implementation phase (IMPLEMENTATION_PLAN).

Phases **L0–L14** and **C0–C5** get a directory under ``reports/html/phase-<id>/``.
Phases with no mapped tests yet receive a stub ``report.html`` explaining that no
automated gate exists yet.

**L1** requires Docker Compose, migrations, seed, and the usual env (see
``docs/dev-setup.md``). The script passes through ``DATABASE_URL_SYNC``,
``REDIS_URL``, ``MINIO_HEALTH_URL``, and sets ``DEEPGUARD_INTEGRATION=1`` when
running L1 integration tests.

Usage (repo root)::

    python3 scripts/generate_phase_html_reports.py

Optional::

    python3 scripts/generate_phase_html_reports.py --open
"""

from __future__ import annotations

import argparse
import html as html_lib
import os
import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import TypedDict

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_HTML = REPO_ROOT / "reports" / "html"

# Order matches IMPLEMENTATION_PLAN local + cloud phases.
ALL_PHASE_IDS: tuple[str, ...] = tuple(f"L{i}" for i in range(15)) + tuple(
    f"C{i}" for i in range(6)
)


class _PhasePytestSpec(TypedDict):
    paths: tuple[str, ...]
    l1_env: bool


# Phases that run pytest (override root addopts: no ``-m "not integration"``).
PHASE_PYTEST: dict[str, _PhasePytestSpec] = {
    "L0": {"paths": ("tests/test_l0_smoke.py",), "l1_env": False},
    "L1": {"paths": ("tests/integration/test_l1_data_plane.py",), "l1_env": True},
    "L2": {"paths": ("packages/core/tests/",), "l1_env": False},
    "L3": {"paths": ("tests/test_l3_api.py",), "l1_env": False},
    "L4": {
        "paths": (
            "tests/test_l4_api.py",
            "tests/test_l4_worker_unit.py",
            "tests/test_l4_worker_settings.py",
            "packages/core/tests/test_queue_scan_message.py",
        ),
        "l1_env": False,
    },
    "L5": {"paths": ("packages/graph/tests/",), "l1_env": False},
    "L6": {"paths": ("packages/agents/tests/",), "l1_env": False},
    "L7": {"paths": ("packages/policies/tests/",), "l1_env": False},
    "L8": {"paths": ("packages/parsers/tests/",), "l1_env": False},
    "L9": {
        "paths": ("packages/parsers/tests/", "packages/connectors/tests/"),
        "l1_env": False,
    },
    "L10": {
        "paths": ("packages/agents/tests/", "eval/harness/tests/"),
        "l1_env": False,
    },
    "L11": {"paths": ("packages/reporting/tests/",), "l1_env": False},
    "L12": {"paths": ("tests/e2e/", "tests/test_l12_worker_graph_memory.py"), "l1_env": False},
    "L13": {"paths": ("packages/observability/tests/",), "l1_env": False},
    "L14": {"paths": ("apps/api/tests/",), "l1_env": False},
}

BASE_PYTEST_ADDOPTS = "-q --strict-markers"


def _stub_report(phase_id: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    safe = html_lib.escape(phase_id)
    dest.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>DeepGuard — Phase {safe} test report (stub)</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; max-width: 48rem; }}
    code {{ background: #f4f4f4; padding: 0.1rem 0.3rem; }}
  </style>
</head>
<body>
  <h1>Phase {safe} — no automated tests yet</h1>
  <p>
    There is no pytest collection mapped for this phase in
    <code>scripts/generate_phase_html_reports.py</code>.
    When this phase lands, add paths (and any env) there so a real HTML report is produced.
  </p>
</body>
</html>
""",
        encoding="utf-8",
    )


def _run_pytest(phase_id: str, paths: tuple[str, ...], *, l1_env: bool) -> int:
    out = REPORTS_HTML / f"phase-{phase_id}" / "report.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd: list[str] = [
        sys.executable,
        "-m",
        "pytest",
        "-o",
        f"addopts={BASE_PYTEST_ADDOPTS}",
        *paths,
        f"--html={out.resolve()}",
        "--self-contained-html",
    ]
    env = os.environ.copy()
    if l1_env:
        env.setdefault("DEEPGUARD_INTEGRATION", "1")
        env.setdefault(
            "DATABASE_URL_SYNC",
            "postgresql://deepguard:deepguard@127.0.0.1:5432/deepguard",
        )
        env.setdefault("REDIS_URL", "redis://127.0.0.1:6379/0")
        env.setdefault("MINIO_HEALTH_URL", "http://127.0.0.1:9000/minio/health/live")
    return subprocess.run(cmd, cwd=REPO_ROOT, env=env).returncode


def _write_index() -> None:
    rows = []
    for pid in ALL_PHASE_IDS:
        href = f"./phase-{pid}/report.html"
        rows.append(
            f'<tr><td><a href="{html_lib.escape(href)}">{html_lib.escape(pid)}</a></td>'
            f"<td><code>{html_lib.escape(href)}</code></td></tr>"
        )
    body_rows = "\n    ".join(rows)
    index = REPO_ROOT / "reports" / "html" / "index.html"
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>DeepGuard — phase test reports</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; }}
    table {{ border-collapse: collapse; }}
    th, td {{ border: 1px solid #ccc; padding: 0.4rem 0.75rem; text-align: left; }}
    th {{ background: #f0f0f0; }}
    code {{ font-size: 0.9em; }}
  </style>
</head>
<body>
  <h1>Implementation phase test reports</h1>
  <p>Generated by <code>scripts/generate_phase_html_reports.py</code>
     (pytest-html, self-contained).</p>
  <table>
    <thead><tr><th>Phase</th><th>Report</th></tr></thead>
    <tbody>
    {body_rows}
    </tbody>
  </table>
</body>
</html>
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate per-phase HTML pytest reports.")
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open reports/html/index.html in a browser after generation.",
    )
    args = parser.parse_args()

    failures = 0
    for phase_id in ALL_PHASE_IDS:
        spec = PHASE_PYTEST.get(phase_id)
        if spec is None:
            _stub_report(phase_id, REPORTS_HTML / f"phase-{phase_id}" / "report.html")
            continue
        paths = spec["paths"]
        rc = _run_pytest(phase_id, paths, l1_env=spec["l1_env"])
        if rc != 0:
            failures += 1
            print(f"Phase {phase_id}: pytest exited {rc}", file=sys.stderr)

    _write_index()
    index_url = (REPO_ROOT / "reports" / "html" / "index.html").as_uri()
    print(f"Wrote phase reports under {REPORTS_HTML}")
    print(f"Index: {index_url}")
    if args.open:
        webbrowser.open(index_url)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
