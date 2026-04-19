"""Minimal PDF report (Phase L11 — cover + finding section)."""

from __future__ import annotations

from fpdf import FPDF
from jinja2 import Template


def render_report_html(template_str: str, context: dict[str, object]) -> str:
    """Render Jinja HTML (intermediate for PDF engines that accept HTML)."""

    return Template(template_str).render(**context)


def build_scan_pdf_bytes(*, scan_id: str, finding_titles: list[str]) -> bytes:
    """Emit a small valid PDF with a cover line and at least one finding section."""

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=16)
    pdf.cell(0, 10, "DeepGuard - Compliance Scan Report")
    pdf.ln(12)
    pdf.set_font(size=11)
    pdf.multi_cell(0, 8, f"Scan ID: {scan_id}")
    pdf.ln(6)
    pdf.set_font(size=14)
    pdf.cell(0, 10, "Findings")
    pdf.ln(8)
    pdf.set_font(size=11)
    # After ``multi_cell``, x can sit past the right margin; reset before listing findings.
    pdf.set_x(pdf.l_margin)
    usable = getattr(pdf, "epw", pdf.w - pdf.l_margin - pdf.r_margin)
    for t in finding_titles[:20]:
        line = (t or "(empty)")[:200]
        pdf.multi_cell(usable, 7, f"- {line}")
    raw = pdf.output()
    if isinstance(raw, (bytes, bytearray)):
        return bytes(raw)
    if isinstance(raw, str):
        return raw.encode("latin-1")
    return bytes(bytearray(raw))
