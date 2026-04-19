#!/usr/bin/env python3
"""Merge Playwright HTML report metadata + step screenshots into a single PDF.

Reads ``results.json`` emitted by the JSON reporter (see ``apps/web/playwright.config.ts``).
Attachments for ``test.step`` screenshots are usually embedded as base64 ``body`` fields.

Usage (from repository root)::

    cd apps/web && npm run test:e2e
    python3 scripts/playwright_bdd_report_to_pdf.py

Or after tests from ``apps/web``::

    python3 ../../scripts/playwright_bdd_report_to_pdf.py \\
      --report-dir playwright-report \\
      --output ../../reports/playwright-bdd-report.pdf
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from collections.abc import Iterator
from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path

try:
    from fpdf import FPDF
    from fpdf.errors import FPDFException
except ImportError as exc:  # pragma: no cover
    print(
        "Missing PDF dependency. From the repository root run:\n"
        "  pip3 install -e .\n"
        "or install only the library the script needs:\n"
        "  pip3 install 'fpdf2>=2.7.0'\n"
        "(The PyPI package name is fpdf2; it provides the ``fpdf`` import namespace.)",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


def _ascii(txt: str) -> str:
    return txt.encode("ascii", "replace").decode("ascii")


def _walk_suites(suite: dict, ancestors: list[str]) -> Iterator[tuple[list[str], dict, dict]]:
    """Yield (breadcrumb titles, spec dict, test dict)."""
    title = (suite.get("title") or "").strip()
    next_anc = ancestors + ([title] if title else [])
    for spec in suite.get("specs") or []:
        for test in spec.get("tests") or []:
            yield next_anc, spec, test
    for child in suite.get("suites") or []:
        yield from _walk_suites(child, next_anc)


def _image_bytes(att: dict) -> bytes | None:
    body = att.get("body")
    if isinstance(body, str) and body:
        return base64.b64decode(body)
    p = att.get("path")
    if isinstance(p, str) and p:
        path = Path(p)
        if path.is_file():
            return path.read_bytes()
    return None


def _is_image_attachment(att: dict) -> bool:
    ct = (att.get("contentType") or "").lower()
    name = (att.get("name") or "").lower()
    if ct.startswith("image/"):
        return True
    return name.endswith(".png") or name.endswith(".jpg") or name.endswith(".jpeg")


def build_pdf(*, report: dict, output: Path) -> None:
    stats = report.get("stats") or {}
    start = stats.get("startTime", "")
    duration_ms = stats.get("duration", 0)

    pdf = FPDF(orientation="portrait", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_title("DeepGuard BDD (Playwright) report")

    pdf.add_page()
    epw = float(pdf.w - pdf.l_margin - pdf.r_margin)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(epw, 10, _ascii("DeepGuard — Playwright BDD report"))
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 11)
    gen_ts = datetime.now(UTC).isoformat(timespec="seconds")
    pdf.multi_cell(epw, 6, _ascii(f"Generated (UTC): {gen_ts}"))
    pdf.multi_cell(epw, 6, _ascii(f"Run start (report): {start}"))
    pdf.multi_cell(epw, 6, _ascii(f"Run duration (ms): {duration_ms:.0f}"))
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(
        epw,
        5,
        _ascii(
            "Screenshots come from test.step attachments (e.g. bdd-step-screenshot). "
            "Order matches Playwright JSON attachment order per test."
        ),
    )

    for suite in report.get("suites") or []:
        for ancestors, spec, test in _walk_suites(suite, []):
            spec_title = (spec.get("title") or "").strip()
            breadcrumb = " / ".join(t for t in ancestors if t)
            for result in test.get("results") or []:
                status = (result.get("status") or "?").upper()
                dur = result.get("duration")
                project = (result.get("projectName") or "").strip()
                heading_parts = [p for p in (breadcrumb, spec_title, project) if p]
                if heading_parts:
                    block_title = " — ".join(heading_parts)
                else:
                    block_title = spec_title or "(untitled)"

                pdf.add_page()
                pdf.set_font("Helvetica", "B", 12)
                pdf.multi_cell(epw, 7, _ascii(block_title))
                pdf.set_font("Helvetica", "", 10)
                pdf.multi_cell(epw, 6, _ascii(f"Status: {status}  Duration: {dur} ms"))
                pdf.ln(2)

                raw_atts = result.get("attachments") or []
                attachments = [a for a in raw_atts if _is_image_attachment(a)]
                if not attachments:
                    pdf.set_font("Helvetica", "I", 10)
                    pdf.multi_cell(epw, 6, _ascii("(No image attachments for this test result.)"))
                    continue

                for att in attachments:
                    raw = _image_bytes(att)
                    if not raw:
                        pdf.set_font("Helvetica", "I", 9)
                        nm = att.get("name") or ""
                        skip_msg = f"[skip] {nm} — no inline body/path"
                        pdf.multi_cell(epw, 5, _ascii(skip_msg))
                        pdf.ln(2)
                        continue

                    stem = Path(att.get("name") or "screenshot").stem
                    caption = re.sub(r"[-_]+", " ", stem).strip()
                    pdf.set_font("Helvetica", "B", 10)
                    pdf.multi_cell(epw, 6, _ascii(caption or "Screenshot"))
                    pdf.ln(1)
                    try:
                        pdf.image(BytesIO(raw), x=pdf.l_margin, w=epw)
                    except (FPDFException, OSError, ValueError) as exc:
                        pdf.set_font("Helvetica", "", 9)
                        pdf.multi_cell(epw, 5, _ascii(f"[image error] {exc}"))
                    pdf.ln(4)

    output.parent.mkdir(parents=True, exist_ok=True)
    out = pdf.output()
    if isinstance(out, str):
        output.write_bytes(out.encode("latin-1"))
    else:
        output.write_bytes(bytes(out))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("apps/web/playwright-report"),
        help="Playwright HTML report folder (contains results.json and data/).",
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=None,
        help="Path to results.json (default: <report-dir>/results.json).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/playwright-bdd-report.pdf"),
        help="Output PDF path.",
    )
    args = parser.parse_args()
    report_dir = args.report_dir.resolve()
    results_path = (args.results or (report_dir / "results.json")).resolve()

    if not results_path.is_file():
        print(
            f"error: {results_path} not found. Run Playwright with the repo config "
            f"(JSON reporter writes results.json), e.g.:\n"
            f"  cd apps/web && npm run test:e2e\n"
            f"Do not pass --reporter=… on the CLI unless it includes `json` with outputFile.",
            file=sys.stderr,
        )
        return 1

    report = json.loads(results_path.read_text(encoding="utf-8"))
    try:
        build_pdf(report=report, output=args.output.resolve())
    except (OSError, ValueError, KeyError, FPDFException) as exc:
        print(f"error: failed to build PDF: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
