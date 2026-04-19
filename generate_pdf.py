"""
Generate a professional PDF from the DeepGuard business case markdown file.
Uses ReportLab for PDF rendering with a clean enterprise report style.
"""

import re
import sys
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, Image as RLImage
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# Import diagram generator
import diagrams as _diag


# ── Brand colours ────────────────────────────────────────────────────────────
NAVY     = HexColor("#0D2137")
BLUE     = HexColor("#1A56DB")
LIGHT_BG = HexColor("#F0F4FA")
ACCENT   = HexColor("#E8F0FE")
MID_GREY = HexColor("#6B7280")
RED      = HexColor("#DC2626")
GREEN    = HexColor("#16A34A")
ORANGE   = HexColor("#D97706")
WHITE    = colors.white
BLACK    = colors.black
ROW_ALT  = HexColor("#F8FAFC")


# ── Page template with header/footer ─────────────────────────────────────────
class PageTemplate:
    def __init__(self, doc_title: str):
        self.doc_title = doc_title

    def on_page(self, canvas_obj, doc):
        canvas_obj.saveState()
        w, h = A4

        # Header bar
        canvas_obj.setFillColor(NAVY)
        canvas_obj.rect(0, h - 1.2 * cm, w, 1.2 * cm, fill=1, stroke=0)
        canvas_obj.setFillColor(WHITE)
        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.drawString(1.5 * cm, h - 0.8 * cm, "DEEPGUARD COMPLIANCE ENGINE")
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawRightString(w - 1.5 * cm, h - 0.8 * cm, self.doc_title)

        # Footer bar
        canvas_obj.setFillColor(NAVY)
        canvas_obj.rect(0, 0, w, 0.9 * cm, fill=1, stroke=0)
        canvas_obj.setFillColor(WHITE)
        canvas_obj.setFont("Helvetica", 7)
        canvas_obj.drawString(1.5 * cm, 0.3 * cm, "CONFIDENTIAL — Business Case v5.0 | April 2026")
        canvas_obj.drawRightString(w - 1.5 * cm, 0.3 * cm, f"Page {doc.page}")

        canvas_obj.restoreState()

    def on_first_page(self, canvas_obj, doc):
        self.on_page(canvas_obj, doc)


def cover_page(canvas_obj, doc):
    w, h = A4
    canvas_obj.saveState()

    # Full background
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 0, w, h, fill=1, stroke=0)

    # Decorative accent strip
    canvas_obj.setFillColor(BLUE)
    canvas_obj.rect(0, h * 0.38, w, 4, fill=1, stroke=0)

    # Title block
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont("Helvetica-Bold", 32)
    canvas_obj.drawCentredString(w / 2, h * 0.58, "DeepGuard")
    canvas_obj.setFont("Helvetica-Bold", 22)
    canvas_obj.drawCentredString(w / 2, h * 0.52, "Compliance Engine")

    canvas_obj.setFont("Helvetica", 14)
    canvas_obj.setFillColor(HexColor("#93C5FD"))
    canvas_obj.drawCentredString(
        w / 2, h * 0.46,
        "Autonomous AI-Powered Security Compliance Checker"
    )

    # Sub-title line
    canvas_obj.setFont("Helvetica", 11)
    canvas_obj.setFillColor(HexColor("#CBD5E1"))
    canvas_obj.drawCentredString(
        w / 2, h * 0.41,
        "Business Case · Commercial Viability · Technical Architecture"
    )

    # Metadata box
    canvas_obj.setFillColor(HexColor("#1E3A5F"))
    canvas_obj.roundRect(w * 0.25, h * 0.15, w * 0.5, h * 0.18, 8, fill=1, stroke=0)

    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont("Helvetica-Bold", 10)
    canvas_obj.drawCentredString(w / 2, h * 0.305, "Document Details")

    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.setFillColor(HexColor("#CBD5E1"))
    items = [
        ("Version",        "5.0"),
        ("Date",           "April 2026"),
        ("Classification", "Confidential"),
        ("Prepared by",    "DeepGuard Product Team"),
    ]
    y = h * 0.275
    for label, val in items:
        canvas_obj.drawString(w * 0.28, y, f"{label}:")
        canvas_obj.drawString(w * 0.44, y, val)
        y -= 0.45 * cm

    canvas_obj.restoreState()


# ── Style sheet ───────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    def add(name, **kw):
        pass  # replaced by safe_add below

    def safe_add(name, **kw):
        if name not in base:
            base.add(ParagraphStyle(name=name, **kw))
        else:
            # Override existing style properties
            s = base[name]
            for k, v in kw.items():
                setattr(s, k, v)

    safe_add("H1", fontName="Helvetica-Bold", fontSize=18, textColor=NAVY,
        spaceAfter=6, spaceBefore=18, leading=22)
    safe_add("H2", fontName="Helvetica-Bold", fontSize=14, textColor=BLUE,
        spaceAfter=4, spaceBefore=14, leading=18,
        borderPad=4)
    safe_add("H3", fontName="Helvetica-Bold", fontSize=11, textColor=NAVY,
        spaceAfter=3, spaceBefore=10, leading=14)
    safe_add("H4", fontName="Helvetica-Bold", fontSize=10, textColor=MID_GREY,
        spaceAfter=2, spaceBefore=8, leading=13)
    safe_add("Body", fontName="Helvetica", fontSize=9.5, leading=14,
        spaceAfter=6, textColor=HexColor("#1F2937"), alignment=TA_JUSTIFY)
    safe_add("Bullet", fontName="Helvetica", fontSize=9.5, leading=13,
        spaceAfter=3, textColor=HexColor("#1F2937"),
        leftIndent=14, bulletIndent=4, bulletFontSize=10)
    safe_add("CodeBlock", fontName="Courier", fontSize=8, leading=11,
        spaceAfter=6, textColor=HexColor("#1F2937"),
        backColor=HexColor("#F1F5F9"), leftIndent=10, rightIndent=10,
        borderPad=6)
    safe_add("Caption", fontName="Helvetica-Oblique", fontSize=8,
        textColor=MID_GREY, spaceAfter=4, alignment=TA_CENTER)
    safe_add("RefItem", fontName="Helvetica", fontSize=8, leading=11,
        spaceAfter=2, textColor=MID_GREY, leftIndent=20)

    return base


# ── Markdown parser → ReportLab flowables ────────────────────────────────────
def md_to_flowables(md_text: str, styles) -> list:
    flowables = []
    lines = md_text.splitlines()
    i = 0
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal table_rows, in_table
        if not table_rows:
            return
        col_count = max(len(r) for r in table_rows)
        # Normalise row lengths
        norm = [r + [""] * (col_count - len(r)) for r in table_rows]
        # Detect separator row (---|---|---)
        data = [r for r in norm if not all(re.match(r"^[-:| ]+$", c) for c in r)]
        if not data:
            in_table = False
            table_rows = []
            return

        # Build paragraph cells
        cell_rows = []
        for ridx, row in enumerate(data):
            cell_row = []
            for cidx, cell in enumerate(row):
                txt = cell.strip()
                if ridx == 0:
                    style = ParagraphStyle(
                        "TH", fontName="Helvetica-Bold", fontSize=8.5,
                        textColor=WHITE, leading=11
                    )
                else:
                    style = ParagraphStyle(
                        "TD", fontName="Helvetica", fontSize=8.5,
                        textColor=HexColor("#1F2937"), leading=11
                    )
                cell_row.append(Paragraph(inline_md(txt), style))
            cell_rows.append(cell_row)

        col_w = (A4[0] - 4 * cm) / col_count
        col_widths = [col_w] * col_count

        tbl = Table(cell_rows, colWidths=col_widths, repeatRows=1)
        ts = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, ROW_ALT]),
            ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#D1D5DB")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
        tbl.setStyle(ts)
        flowables.append(Spacer(1, 4))
        flowables.append(tbl)
        flowables.append(Spacer(1, 8))
        in_table = False
        table_rows = []

    def inline_md(text: str) -> str:
        # Bold
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)
        # Italic
        text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
        text = re.sub(r"_(.+?)_", r"<i>\1</i>", text)
        # Inline code
        text = re.sub(r"`(.+?)`", r'<font name="Courier" size="8">\1</font>', text)
        return text

    while i < len(lines):
        line = lines[i]

        # ── Skip YAML front-matter / horizontal rules ─────────────────────
        if line.strip() in ("---", "==="):
            if not in_table:
                flowables.append(HRFlowable(
                    width="100%", thickness=0.5,
                    color=HexColor("#D1D5DB"), spaceAfter=6, spaceBefore=6
                ))
            i += 1
            continue

        # ── Table detection ───────────────────────────────────────────────
        if "|" in line:
            in_table = True
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            table_rows.append(cells)
            i += 1
            continue
        else:
            if in_table:
                flush_table()

        stripped = line.strip()

        # ── Skip table-of-contents anchor links ──────────────────────────
        if re.match(r"^\d+\.\s+\[.*\]\(#.*\)$", stripped):
            i += 1
            continue

        # ── Headings ──────────────────────────────────────────────────────
        if stripped.startswith("#### "):
            flowables.append(Paragraph(inline_md(stripped[5:]), styles["H4"]))
        elif stripped.startswith("### "):
            flowables.append(Paragraph(inline_md(stripped[4:]), styles["H3"]))
        elif stripped.startswith("## "):
            flowables.append(Spacer(1, 4))
            text = stripped[3:]
            # Draw a coloured left-bar heading
            tbl = Table(
                [[Paragraph(inline_md(text), styles["H2"])]],
                colWidths=[A4[0] - 4 * cm]
            )
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LINEAFTER", (0, 0), (0, 0), 0, WHITE),
                ("LINEBEFORE", (0, 0), (0, 0), 4, BLUE),
            ]))
            flowables.append(tbl)
            flowables.append(Spacer(1, 4))
        elif stripped.startswith("# "):
            flowables.append(PageBreak())
            flowables.append(Paragraph(inline_md(stripped[2:]), styles["H1"]))
            flowables.append(HRFlowable(
                width="100%", thickness=1.5, color=BLUE,
                spaceAfter=8, spaceBefore=2
            ))

        # ── Bullet lists ──────────────────────────────────────────────────
        elif stripped.startswith("- ") or stripped.startswith("* "):
            text = stripped[2:].strip()
            flowables.append(Paragraph(
                f"\u2022&nbsp;&nbsp;{inline_md(text)}", styles["Bullet"]
            ))

        # ── Numbered lists ────────────────────────────────────────────────
        elif re.match(r"^\d+\.\s", stripped):
            text = re.sub(r"^\d+\.\s", "", stripped)
            flowables.append(Paragraph(
                f"&nbsp;&nbsp;&nbsp;{inline_md(text)}", styles["Bullet"]
            ))

        # ── Code blocks ───────────────────────────────────────────────────
        elif stripped.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            block_text = "\n".join(code_lines)

            # ── Replace specific architecture blocks with pre-rendered PNGs ──
            _is_sysdiag = ("Ingestion Gateway" in block_text or
                           "LangGraph Orchestration Engine" in block_text or
                           "ODYSSEUS ENGINE" in block_text.upper() or
                           "LANGGRAPH" in block_text.upper())
            _is_pipeline = ("[START]" in block_text and
                            ("IngestionAgent]" in block_text or
                             "HERMES" in block_text))

            if _is_sysdiag:
                img_path = str(Path(__file__).parent / "diagram_system_overview.png")
                if Path(img_path).exists():
                    page_w = A4[0] - 4 * cm
                    img = RLImage(img_path, width=page_w, height=page_w * 9/13)
                    cap_sty = ParagraphStyle(
                        "DiagCap", fontName="Helvetica-Oblique", fontSize=8,
                        textColor=MID_GREY, alignment=1, spaceAfter=8
                    )
                    flowables.append(Spacer(1, 8))
                    flowables.append(img)
                    flowables.append(Paragraph(
                        "Figure 1: DeepGuard — Odysseus Engine System Architecture · Cloud-Agnostic · VPC-Native",
                        cap_sty))
            elif _is_pipeline:
                img_path = str(Path(__file__).parent / "diagram_agent_pipeline.png")
                if Path(img_path).exists():
                    page_w = A4[0] - 4 * cm
                    img = RLImage(img_path, width=page_w, height=page_w * 10/13)
                    cap_sty = ParagraphStyle(
                        "DiagCap2", fontName="Helvetica-Oblique", fontSize=8,
                        textColor=MID_GREY, alignment=1, spaceAfter=8
                    )
                    flowables.append(Spacer(1, 8))
                    flowables.append(img)
                    flowables.append(Paragraph(
                        "Figure 2: Odysseus Engine Agent Pipeline — Hermes · Tiresias · Argus · Laocoon · Cassandra · Athena · Circe · Penelope",
                        cap_sty))
            else:
                code_text = "<br/>".join(
                    l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    for l in code_lines
                )
                flowables.append(Paragraph(code_text, styles["CodeBlock"]))

        # ── Block quotes / callouts ───────────────────────────────────────
        elif stripped.startswith("> "):
            text = stripped[2:]
            tbl = Table(
                [[Paragraph(inline_md(text), styles["Body"])]],
                colWidths=[A4[0] - 4.5 * cm]
            )
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
                ("LINEBEFORE", (0, 0), (0, -1), 4, BLUE),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            flowables.append(tbl)
            flowables.append(Spacer(1, 4))

        # ── Reference items (lines starting with digit + period in refs) ──
        elif re.match(r"^\d+\.\s+(Grand|Market|IDC|Allied|OWASP|ISO|European|NIST|Monetary|PCI|Center|Flexera|Google|Anthropic|Fortune|Axios|CNBC|Council|UK AI|IANS|Cloud Security|DarkReading|VentureBeat|Scientific|Schneier|Noma|Silicon|Pinggy|DeepSeek|Qwen)", stripped):
            flowables.append(Paragraph(inline_md(stripped), styles["RefItem"]))

        # ── Regular body paragraph ────────────────────────────────────────
        elif stripped:
            flowables.append(Paragraph(inline_md(stripped), styles["Body"]))

        # ── Blank line → small spacer ─────────────────────────────────────
        else:
            flowables.append(Spacer(1, 3))

        i += 1

    if in_table:
        flush_table()

    return flowables


# ── Main ──────────────────────────────────────────────────────────────────────
def generate_pdf(md_path: str, pdf_path: str):
    # Pre-render architecture diagrams
    base = Path(__file__).parent
    print("Rendering architecture diagrams...")
    _diag.draw_system_overview(str(base / "diagram_system_overview.png"), dpi=200)
    _diag.draw_agent_pipeline(str(base / "diagram_agent_pipeline.png"), dpi=200)

    md_text = Path(md_path).read_text(encoding="utf-8")

    # Remove title block (first 6 lines — rendered on cover page)
    body_lines = md_text.splitlines()
    # Find first ## heading index to skip the cover metadata
    start = 0
    for idx, l in enumerate(body_lines):
        if l.startswith("## Table of Contents"):
            start = idx
            break
    body_md = "\n".join(body_lines[start:])

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=1.8 * cm,
        title="DeepGuard Compliance Engine — Business Case v4.0",
        author="DeepGuard Product Team",
        subject="Business Case, Commercial Viability & Technical Architecture",
    )

    template = PageTemplate("Business Case & Architecture v4.0")
    styles = build_styles()
    story = []

    # ── Cover page ───────────────────────────────────────────────────────
    story.append(PageBreak())  # triggers cover_page on first page

    # ── Body content ─────────────────────────────────────────────────────
    flowables = md_to_flowables(body_md, styles)
    story.extend(flowables)

    doc.build(
        story,
        onFirstPage=cover_page,
        onLaterPages=template.on_page,
    )
    print(f"PDF generated: {pdf_path}")


if __name__ == "__main__":
    base = Path(__file__).parent
    generate_pdf(
        str(base / "DeepGuard_Compliance_Engine.md"),
        str(base / "DeepGuard_Compliance_Engine.pdf"),
    )
