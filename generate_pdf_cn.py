"""
Generate the Chinese Xuanwu Compliance Engine business proposal PDF.
Uses STHeiti (Heiti SC) for headings and Songti SC for body text.
"""

import re
import subprocess
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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

import diagrams_cn as _diag

# ── Register CJK fonts ────────────────────────────────────────────────────────
_HEITI_PATH  = "/System/Library/Fonts/STHeiti Medium.ttc"
_SONGTI_PATH = "/System/Library/Fonts/Supplemental/Songti.ttc"
_ARIAL_PATH  = "/Library/Fonts/Arial Unicode.ttf"

def _register_fonts():
    registered = []
    # Heiti SC — headings (subfontIndex 0)
    for name, path, idx in [
        ("HeitiSC",  _HEITI_PATH,  0),
        ("SongtiSC", _SONGTI_PATH, 2),
        ("ArialUni", _ARIAL_PATH,  None),
    ]:
        try:
            if idx is not None:
                pdfmetrics.registerFont(TTFont(name, path, subfontIndex=idx))
            else:
                pdfmetrics.registerFont(TTFont(name, path))
            registered.append(name)
        except Exception:
            pass
    return registered

_REGISTERED = _register_fonts()
_HEADING_FONT = "HeitiSC"  if "HeitiSC"  in _REGISTERED else "Helvetica-Bold"
_BODY_FONT    = "SongtiSC" if "SongtiSC" in _REGISTERED else ("ArialUni" if "ArialUni" in _REGISTERED else "Helvetica")

# ── Brand colours ─────────────────────────────────────────────────────────────
NAVY     = HexColor("#0D2137")
BLUE     = HexColor("#1A56DB")
LIGHT_BG = HexColor("#F0F4FA")
ACCENT   = HexColor("#E8F0FE")
MID_GREY = HexColor("#6B7280")
RED      = HexColor("#DC2626")
GREEN    = HexColor("#16A34A")
ORANGE   = HexColor("#D97706")
GOLD     = HexColor("#B45309")
WHITE    = colors.white
BLACK    = colors.black
ROW_ALT  = HexColor("#F8FAFC")


# ── Page template ─────────────────────────────────────────────────────────────
class PageTemplate:
    def on_page(self, canvas_obj, doc):
        canvas_obj.saveState()
        w, h = A4

        # Header
        canvas_obj.setFillColor(NAVY)
        canvas_obj.rect(0, h - 1.2*cm, w, 1.2*cm, fill=1, stroke=0)
        canvas_obj.setFillColor(WHITE)
        canvas_obj.setFont(_HEADING_FONT, 8)
        canvas_obj.drawString(1.5*cm, h - 0.8*cm, "玄武合规引擎")
        canvas_obj.setFont(_BODY_FONT, 7.5)
        canvas_obj.drawRightString(w - 1.5*cm, h - 0.8*cm, "Xuanwu Compliance Engine")

        # Footer
        canvas_obj.setFillColor(NAVY)
        canvas_obj.rect(0, 0, w, 0.9*cm, fill=1, stroke=0)
        canvas_obj.setFillColor(WHITE)
        canvas_obj.setFont(_BODY_FONT, 7)
        canvas_obj.drawString(1.5*cm, 0.3*cm, "机密文件 — 商业计划书 v1.0 | 2026年4月")
        canvas_obj.drawRightString(w - 1.5*cm, 0.3*cm, f"第 {doc.page} 页")
        canvas_obj.restoreState()

    def on_first_page(self, canvas_obj, doc):
        self.on_page(canvas_obj, doc)


def cover_page(canvas_obj, doc):
    w, h = A4
    canvas_obj.saveState()

    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 0, w, h, fill=1, stroke=0)

    # Red-gold accent (Chinese auspicious colours)
    canvas_obj.setFillColor(HexColor("#8B0000"))
    canvas_obj.rect(0, h*0.38, w, 5, fill=1, stroke=0)
    canvas_obj.setFillColor(HexColor("#B45309"))
    canvas_obj.rect(0, h*0.38 - 3, w, 3, fill=1, stroke=0)

    # Large Chinese title
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont(_HEADING_FONT, 40)
    canvas_obj.drawCentredString(w/2, h*0.62, "玄武合规引擎")

    canvas_obj.setFont(_HEADING_FONT, 20)
    canvas_obj.setFillColor(HexColor("#93C5FD"))
    canvas_obj.drawCentredString(w/2, h*0.555, "自主 AI 驱动的安全合规检测平台")

    canvas_obj.setFont(_BODY_FONT, 13)
    canvas_obj.setFillColor(HexColor("#CBD5E1"))
    canvas_obj.drawCentredString(w/2, h*0.497,
        "商业计划书  ·  市场分析  ·  技术架构")

    canvas_obj.setFont(_BODY_FONT, 10)
    canvas_obj.setFillColor(HexColor("#B45309"))
    canvas_obj.drawCentredString(w/2, h*0.454,
        "Xuanwu Compliance Engine — Powered by the Odysseus Engine")

    # Metadata box
    canvas_obj.setFillColor(HexColor("#1E3A5F"))
    canvas_obj.roundRect(w*0.22, h*0.14, w*0.56, h*0.22, 8, fill=1, stroke=0)
    canvas_obj.setFillColor(HexColor("#B45309"))
    canvas_obj.setFont(_HEADING_FONT, 10)
    canvas_obj.drawCentredString(w/2, h*0.328, "文件信息")
    canvas_obj.setFont(_BODY_FONT, 9)
    canvas_obj.setFillColor(HexColor("#CBD5E1"))
    items = [
        ("版本",     "1.0"),
        ("日期",     "2026年4月"),
        ("密级",     "机密"),
        ("适用范围", "天使投资人（须签署保密协议）"),
        ("编制方",   "DeepGuard 产品团队"),
    ]
    y = h * 0.300
    for label, val in items:
        canvas_obj.drawString(w*0.26, y, f"{label}：")
        canvas_obj.drawString(w*0.40, y, val)
        y -= 0.43*cm

    canvas_obj.restoreState()


# ── Styles ────────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    def safe_add(name, **kw):
        if name not in base:
            base.add(ParagraphStyle(name=name, **kw))
        else:
            s = base[name]
            for k, v in kw.items():
                setattr(s, k, v)

    safe_add("CnH1", fontName=_HEADING_FONT, fontSize=17, textColor=NAVY,
             spaceAfter=6, spaceBefore=18, leading=26)
    safe_add("CnH2", fontName=_HEADING_FONT, fontSize=13, textColor=BLUE,
             spaceAfter=4, spaceBefore=14, leading=20)
    safe_add("CnH3", fontName=_HEADING_FONT, fontSize=10.5, textColor=NAVY,
             spaceAfter=3, spaceBefore=10, leading=16)
    safe_add("CnH4", fontName=_HEADING_FONT, fontSize=9.5, textColor=MID_GREY,
             spaceAfter=2, spaceBefore=8, leading=14)
    safe_add("CnBody", fontName=_BODY_FONT, fontSize=9.5, leading=17,
             spaceAfter=6, textColor=HexColor("#1F2937"), alignment=TA_LEFT)
    safe_add("CnBullet", fontName=_BODY_FONT, fontSize=9.5, leading=16,
             spaceAfter=3, textColor=HexColor("#1F2937"),
             leftIndent=16, firstLineIndent=0)
    safe_add("CnBullet2", fontName=_BODY_FONT, fontSize=9, leading=15,
             spaceAfter=2, textColor=HexColor("#374151"),
             leftIndent=30, firstLineIndent=0)
    safe_add("CnCode", fontName="Courier", fontSize=7.5, leading=11,
             spaceAfter=4, textColor=HexColor("#1F2937"),
             backColor=HexColor("#F0F4FA"), leftIndent=8, rightIndent=8)
    safe_add("CnQuote", fontName=_BODY_FONT, fontSize=9.5, leading=17,
             spaceAfter=6, textColor=HexColor("#374151"),
             leftIndent=20, rightIndent=20,
             backColor=HexColor("#F0F4FA"),
             borderColor=BLUE, borderWidth=2, borderPad=6)
    safe_add("CnCaption", fontName=_BODY_FONT, fontSize=8,
             textColor=MID_GREY, alignment=TA_CENTER, spaceAfter=8)

    # Reuse existing styles for tables
    safe_add("TableHeader", fontName=_HEADING_FONT, fontSize=8.5, textColor=WHITE,
             alignment=TA_CENTER, leading=13)
    safe_add("TableCell", fontName=_BODY_FONT, fontSize=8.5, textColor=BLACK,
             leading=13, spaceAfter=2)

    return base


# ── Table helpers ─────────────────────────────────────────────────────────────
def _make_table(rows, col_widths=None, header=True):
    styles_obj = build_styles()
    data = []
    for ri, row in enumerate(rows):
        is_header_row = (ri == 0 and header)
        data.append([
            Paragraph(
                str(cell).strip() if is_header_row else _inline(str(cell).strip(), styles_obj),
                styles_obj["TableHeader"] if is_header_row else styles_obj["TableCell"]
            )
            for cell in row
        ])
    page_w = A4[0] - 4*cm
    if col_widths is None:
        ncols = max(len(r) for r in rows)
        col_widths = [page_w / ncols] * ncols

    tbl = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("BACKGROUND",  (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",   (0,0), (-1,0), WHITE),
        ("FONTNAME",    (0,0), (-1,0), _HEADING_FONT),
        ("FONTSIZE",    (0,0), (-1,0), 8.5),
        ("ALIGN",       (0,0), (-1,0), "CENTER"),
        ("GRID",        (0,0), (-1,-1), 0.4, HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, ROW_ALT]),
        ("FONTNAME",    (0,1), (-1,-1), _BODY_FONT),
        ("FONTSIZE",    (0,1), (-1,-1), 8.5),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING",(0,0), (-1,-1), 6),
    ]
    tbl.setStyle(TableStyle(style))
    return tbl


def _section_banner(text, styles):
    data = [[Paragraph(text, ParagraphStyle(
        "SBanner", fontName=_HEADING_FONT, fontSize=11,
        textColor=WHITE, leading=16))]]
    tbl = Table(data, colWidths=[A4[0] - 4*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
    ]))
    return tbl


# ── Markdown → flowables ──────────────────────────────────────────────────────
def _escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def _inline(text, styles):
    """Handle bold (**text**) and inline code (`code`) in Chinese text."""
    text = _escape(text)
    text = re.sub(r"\*\*(.+?)\*\*",
                  lambda m: f'<font name="{_HEADING_FONT}"><b>{m.group(1)}</b></font>', text)
    text = re.sub(r"`([^`]+)`",
                  lambda m: f'<font name="Courier" size="8">{m.group(1)}</font>', text)
    return text

def md_to_flowables(md_text: str, styles) -> list:
    flowables = []
    lines = md_text.splitlines()
    i = 0
    in_code = False
    code_lines = []
    in_table = False
    table_rows = []

    # Diagram detection flags
    _SYSDIAG_TOKENS  = ("太白金星 — 数据摄取网关", "姜子牙", "ODYSSEUS")
    _PIPEDAG_TOKENS  = ("太白金星 — 摄取代理", "太白金星 — 数据摄取代理", "① 太白金星")
    _CLOUDDAG_TOKENS = ("阿里云 VPC / 腾讯云 VPC",)

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ── Code block ──────────────────────────────────────────────────────
        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                block_text = "\n".join(code_lines)

                _is_sysdiag  = any(t in block_text for t in _SYSDIAG_TOKENS)
                _is_pipedag  = any(t in block_text for t in _PIPEDAG_TOKENS)
                _is_clouddag = any(t in block_text for t in _CLOUDDAG_TOKENS)

                page_w = A4[0] - 4*cm

                if _is_sysdiag and not _is_pipedag:
                    img_p = str(Path(__file__).parent / "diagram_cn_system_overview.png")
                    if Path(img_p).exists():
                        flowables.append(Spacer(1, 8))
                        flowables.append(RLImage(img_p, width=page_w, height=page_w*10/14))
                        flowables.append(Paragraph(
                            "图1：玄武合规引擎 — 系统架构总览（姜子牙编排引擎 · 九天神将代理图）",
                            styles["CnCaption"]))
                elif _is_pipedag:
                    img_p = str(Path(__file__).parent / "diagram_cn_pipeline_mermaid.png")
                    if Path(img_p).exists():
                        # Aspect ratio ~1.38 (732×1010). Fit within page width.
                        img_w = page_w * 0.92
                        flowables.append(Spacer(1, 8))
                        flowables.append(RLImage(img_p, width=img_w, height=img_w*1.38))
                        flowables.append(Paragraph(
                            "图2：九天神将作战流水线 — 按控制项并行展开 · 跨层关联分析",
                            styles["CnCaption"]))
                elif _is_clouddag:
                    img_p = str(Path(__file__).parent / "diagram_cn_three_cloud.png")
                    if Path(img_p).exists():
                        flowables.append(Spacer(1, 8))
                        flowables.append(RLImage(img_p, width=page_w, height=page_w*9/15))
                        flowables.append(Paragraph(
                            "图3：三大国内云专属部署架构 — 阿里云 · 腾讯云 · 华为云",
                            styles["CnCaption"]))
                else:
                    escaped = "<br/>".join(_escape(l) for l in code_lines)
                    flowables.append(Paragraph(
                        f'<font name="Courier" size="7">{escaped}</font>',
                        styles["CnCode"]))
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # ── Table ───────────────────────────────────────────────────────────
        if stripped.startswith("|") and "|" in stripped[1:]:
            if not in_table:
                in_table = True
                table_rows = []
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if not all(re.match(r"^[-: ]+$", c) for c in cells):
                table_rows.append(cells)
            i += 1
            continue
        else:
            if in_table:
                in_table = False
                if table_rows:
                    ncols = max(len(r) for r in table_rows)
                    norm = [r + [""]*(ncols - len(r)) for r in table_rows]
                    page_w = A4[0] - 4*cm
                    cw = [page_w / ncols] * ncols
                    # Widen first column
                    if ncols >= 3:
                        cw[0] = page_w * 0.30
                        rest = (page_w - cw[0]) / (ncols - 1)
                        cw[1:] = [rest] * (ncols - 1)
                    flowables.append(_make_table(norm, col_widths=cw))
                    flowables.append(Spacer(1, 6))
                table_rows = []

        # ── Horizontal rule ─────────────────────────────────────────────────
        if stripped in ("---", "___", "***"):
            flowables.append(HRFlowable(width="100%", thickness=0.5,
                                         color=HexColor("#CBD5E1"), spaceAfter=4))
            i += 1
            continue

        # ── Headings ────────────────────────────────────────────────────────
        m = re.match(r"^(#{1,4})\s+(.+)", stripped)
        if m:
            level = len(m.group(1))
            txt   = _inline(m.group(2), styles)
            sty_map = {1: "CnH1", 2: "CnH2", 3: "CnH3", 4: "CnH4"}
            sname = sty_map.get(level, "CnH3")
            if level == 1:
                flowables.append(PageBreak())
                flowables.append(_section_banner(m.group(2), styles))
                flowables.append(Spacer(1, 8))
            elif level == 2:
                flowables.append(Spacer(1, 4))
                flowables.append(Paragraph(txt, styles[sname]))
                flowables.append(HRFlowable(width="100%", thickness=1,
                                             color=BLUE, spaceAfter=4))
            else:
                flowables.append(Paragraph(txt, styles[sname]))
            i += 1
            continue

        # ── Block quote ─────────────────────────────────────────────────────
        if stripped.startswith("> "):
            flowables.append(Paragraph(_inline(stripped[2:], styles), styles["CnQuote"]))
            i += 1
            continue

        # ── Bullet / numbered list ───────────────────────────────────────────
        m_bullet = re.match(r"^(\s*)[-*+]\s+(.+)", line)
        m_numlist = re.match(r"^(\s*)\d+\.\s+(.+)", line)
        if m_bullet or m_numlist:
            m = m_bullet or m_numlist
            indent = len(m.group(1))
            txt = _inline(m.group(2), styles)
            prefix = "•  " if m_bullet else "    "
            sty = "CnBullet2" if indent >= 4 else "CnBullet"
            flowables.append(Paragraph(f"{prefix}{txt}", styles[sty]))
            i += 1
            continue

        # ── Bold-only paragraph (used as sub-heading) ────────────────────────
        if stripped.startswith("**") and stripped.endswith("**") and stripped.count("**") == 2:
            inner = stripped[2:-2]
            flowables.append(Paragraph(
                f'<font name="{_HEADING_FONT}"><b>{_escape(inner)}</b></font>',
                styles["CnH4"]))
            i += 1
            continue

        # ── Normal paragraph ─────────────────────────────────────────────────
        if stripped:
            flowables.append(Paragraph(_inline(stripped, styles), styles["CnBody"]))

        i += 1

    return flowables


# ── Mermaid pipeline renderer ─────────────────────────────────────────────────
_MERMAID_PIPELINE = """\
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1A3A5C', 'primaryTextColor': '#ffffff', 'primaryBorderColor': '#1A56DB', 'lineColor': '#1A56DB', 'fontFamily': 'Arial Unicode MS, PingFang SC, Microsoft YaHei, sans-serif', 'fontSize': '11px'}, 'flowchart': {'rankSpacing': 30, 'nodeSpacing': 10, 'padding': 8}}}%%
flowchart TD
    A([开始]) --> B["太白金星 — 摄取代理  克隆仓库·解压ZIP·调用云连接器  GitHub·GitLab·Gitee·Bitbucket"]
    B --> C["伏羲 — 策略解析器  解析合规文档→控制要求含范围标签  等保2.0·网络安全法·PIPL·DSMM"]
    C --> D["千里眼 — 代码索引器  AST解析+依赖图+pgvector索引  Python·Go·Java·TypeScript"]
    D --> PAR{"按控制要求范围并行展开"}
    PAR --> F["代码分析器  RAG检索源代码向量索引  跨语言深度推理"]
    PAR --> G["钟馗 — IaC分析器  Terraform/阿里云ROS/CFN  Bicep/Pulumi/Helm"]
    PAR --> H["比干 — 云配置代理  CloudConnector→标准资源快照  阿里云·腾讯云·华为云·AWS"]
    F --> I["观音菩萨 — 合规映射代理  LLM推理：通过/失败/部分通过/不适用  跨层关联：基础设施承诺vs代码实现缺口  生成发现项：证据·严重性·CVSS·推理链"]
    G --> I
    H --> I
    I --> J["神农氏 — 修复建议代理  代码补丁（diff格式）/IaC修复/云CLI命令  阿里云CLI·腾讯云CLI·AWS CLI·huaweicloud"]
    J --> K["织女 — 报告组装器→PDF生成器  等保2.0映射表·发现汇总·CVSS评分·修复建议"]
    K --> L["OSS/COS/OBS加密存储  通知→钉钉/企业微信/Slack/邮件"]
    L --> M([结束])
    style A fill:#16A34A,color:#fff,stroke:#16A34A
    style M fill:#16A34A,color:#fff,stroke:#16A34A
    style B fill:#0D2137,color:#fff,stroke:#1A56DB
    style C fill:#0D2137,color:#fff,stroke:#1A56DB
    style D fill:#0D2137,color:#fff,stroke:#1A56DB
    style PAR fill:#B45309,color:#fff,stroke:#D97706
    style F fill:#1E3A5F,color:#fff,stroke:#1A56DB
    style G fill:#1E3A5F,color:#fff,stroke:#1A56DB
    style H fill:#1E3A5F,color:#fff,stroke:#1A56DB
    style I fill:#7C2D12,color:#fff,stroke:#DC2626
    style J fill:#0D2137,color:#fff,stroke:#1A56DB
    style K fill:#14532D,color:#fff,stroke:#16A34A
    style L fill:#1E3A5F,color:#fff,stroke:#1A56DB
"""

def _render_mermaid_pipeline(base: Path):
    mmd_path = base / "diagram_cn_pipeline_mermaid.mmd"
    png_path = base / "diagram_cn_pipeline_mermaid.png"
    mmd_path.write_text(_MERMAID_PIPELINE, encoding="utf-8")
    try:
        subprocess.run(
            ["npx", "@mermaid-js/mermaid-cli", "-i", str(mmd_path),
             "-o", str(png_path), "-w", "1100", "-H", "900"],
            check=True, capture_output=True
        )
        print(f"Saved: {png_path}")
    except subprocess.CalledProcessError as e:
        print(f"Warning: mermaid render failed — {e.stderr.decode()[:200]}")


# ── Main generator ────────────────────────────────────────────────────────────
def generate_pdf(md_path: str, out_path: str):
    base = Path(md_path).parent

    print("渲染架构图表...")
    _diag.draw_system_overview_cn(str(base / "diagram_cn_system_overview.png"), dpi=200)
    _diag.draw_agent_pipeline_cn(str(base / "diagram_cn_agent_pipeline.png"), dpi=200)
    _diag.draw_three_cloud_deployment(str(base / "diagram_cn_three_cloud.png"), dpi=200)

    # Render section 11.3 mermaid pipeline diagram
    _render_mermaid_pipeline(base)

    md_text = Path(md_path).read_text(encoding="utf-8")
    styles  = build_styles()

    pt = PageTemplate()
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
        title="玄武合规引擎 — 商业计划书",
        author="DeepGuard 产品团队",
        subject="自主AI安全合规检测平台",
    )

    # Cover page — content starts on page 2
    story = [PageBreak()]

    def first_page(c, d):
        cover_page(c, d)  # cover only, no header/footer bar

    def later_pages(c, d):
        pt.on_page(c, d)

    # Skip front-matter (title / version lines / TOC) and parse body
    # Find the first ## heading that's not 目录
    lines = md_text.splitlines()
    start = 0
    for j, ln in enumerate(lines):
        if ln.strip().startswith("## 1."):
            start = j
            break

    body_md = "\n".join(lines[start:])
    story += md_to_flowables(body_md, styles)

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    print(f"PDF 已生成：{out_path}")


if __name__ == "__main__":
    base = Path(__file__).parent
    md   = base / "玄武合规引擎_商业计划书.md"
    out  = base / "玄武合规引擎_商业计划书.pdf"
    generate_pdf(str(md), str(out))
