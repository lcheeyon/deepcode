"""Reporting (Penelope PDF) + Circe remediation stubs (Phase L11)."""

from deepguard_reporting.circe_stub import build_remediation_diff_only
from deepguard_reporting.penelope_pdf import build_scan_pdf_bytes, render_report_html

__all__ = [
    "build_remediation_diff_only",
    "build_scan_pdf_bytes",
    "render_report_html",
]
