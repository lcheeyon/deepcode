"""Phase L11 — Penelope PDF + Circe remediation."""

from __future__ import annotations

import uuid

from deepguard_reporting.circe_stub import build_remediation_diff_only
from deepguard_reporting.penelope_pdf import build_scan_pdf_bytes, render_report_html


def test_pdf_contains_cover_and_finding_section() -> None:
    pdf = build_scan_pdf_bytes(
        scan_id="00000000-0000-4000-8000-000000000099",
        finding_titles=["S3 bucket lacks encryption"],
    )
    assert pdf.startswith(b"%PDF")


def test_jinja_render() -> None:
    html = render_report_html("<p>{{ title }}</p>", {"title": "Report"})
    assert "Report" in html


def test_circe_remediation_is_diff_only() -> None:
    sid = uuid.UUID("00000000-0000-4000-8000-0000000000aa")
    r = build_remediation_diff_only(
        scan_id=sid,
        finding_id=None,
        title="Harden bucket",
    )
    assert "--- a/" in r.diff_preview
    assert r.terraform_validate_exit_code is None
