"""
DeepGuard Compliance Engine — Executive Summary One-Pager  v4
Fixes: logo clear of headline · spread vertical spacing · cloud rows · tagline updated
"""
from pathlib import Path as FilePath
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math

# ── Fonts ──────────────────────────────────────────────────────────────────────
for _n, _p, _i in [
    ("DGBold", "/System/Library/Fonts/STHeiti Medium.ttc",       0),
    ("DGBody", "/System/Library/Fonts/Supplemental/Songti.ttc",  2),
]:
    try: pdfmetrics.registerFont(TTFont(_n, _p, subfontIndex=_i))
    except Exception: pass

BOLD = "DGBold" if "DGBold" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"
BODY = "DGBody" if "DGBody" in pdfmetrics.getRegisteredFontNames() else "Helvetica"

# ── Palette ────────────────────────────────────────────────────────────────────
NAVY    = HexColor("#0B1C2E");  NAVY2   = HexColor("#112438")
BLUE    = HexColor("#1A56DB");  BLUE2   = HexColor("#1E3A8A");  BLUE_L  = HexColor("#DBEAFE")
TEAL    = HexColor("#0891B2");  TEAL_L  = HexColor("#CFFAFE")
AMBER   = HexColor("#B45309");  AMBER2  = HexColor("#D97706");  AMBER_L = HexColor("#FEF3C7")
RED     = HexColor("#991B1B");  RED2    = HexColor("#DC2626");  RED_L   = HexColor("#FEE2E2")
GREEN   = HexColor("#065F46");  GREEN2  = HexColor("#10B981");  GREEN_L = HexColor("#D1FAE5")
SLATE   = HexColor("#334155");  SLATE2  = HexColor("#475569");  SLATE_L = HexColor("#F1F5F9")
STEEL   = HexColor("#94A3B8");  PURPLE  = HexColor("#6D28D9");  PURPLE_L= HexColor("#EDE9FE")
W, H    = A4   # 595.3 × 841.9

# ── Primitives ─────────────────────────────────────────────────────────────────
def box(c, x, y, w, h, fill, radius=0, stroke=None, sw=0.5):
    c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(sw)
    if radius: c.roundRect(x, y, w, h, radius, fill=1, stroke=1 if stroke else 0)
    else:      c.rect(x, y, w, h, fill=1, stroke=1 if stroke else 0)

def txt(c, s, x, y, font, size, color, align="left"):
    c.setFillColor(color); c.setFont(font, size)
    {"left": lambda: c.drawString(x, y, s),
     "center": lambda: c.drawCentredString(x, y, s),
     "right":  lambda: c.drawRightString(x, y, s)}[align]()

def hline(c, x1, x2, y, color, lw=0.5):
    c.saveState(); c.setStrokeColor(color); c.setLineWidth(lw)
    c.line(x1, y, x2, y); c.restoreState()

def wrap(c, s, font, size, max_w):
    words = s.split(); lines, cur = [], []
    for w in words:
        probe = " ".join(cur + [w])
        if c.stringWidth(probe, font, size) <= max_w: cur.append(w)
        else:
            if cur: lines.append(" ".join(cur))
            cur = [w]
    if cur: lines.append(" ".join(cur))
    return lines

def wtext(c, s, x, y, font, size, color, max_w, lead):
    for ln in wrap(c, s, font, size, max_w):
        txt(c, ln, x, y, font, size, color); y -= lead
    return y

# ── Logo (hexagonal DG) ────────────────────────────────────────────────────────
def logo(c, cx, cy, r=30):
    def pts(r, off=0):
        return [(cx + r*math.cos(math.radians(60*i+off)),
                 cy + r*math.sin(math.radians(60*i+off))) for i in range(6)]
    for verts, fill, sc, lw in [(pts(r,30), NAVY, BLUE, 1.5),
                                  (pts(r*0.70,30), BLUE, HexColor("#60A5FA"), 0.5)]:
        p = c.beginPath(); p.moveTo(*verts[0])
        for v in verts[1:]: p.lineTo(*v)
        p.close(); c.setFillColor(fill); c.setStrokeColor(sc); c.setLineWidth(lw)
        c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(HexColor("#93C5FD"))
    for px, py in pts(r,30)[::2]: c.circle(px, py, 1.4, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#93C5FD")); c.setLineWidth(0.35)
    for dy in [-r*0.16, 0, r*0.16]:
        c.line(cx-r*0.52, cy+dy+r*0.05, cx+r*0.52, cy+dy+r*0.05)
    c.setFillColor(white); c.setFont(BOLD, r*0.42)
    c.drawCentredString(cx, cy - r*0.14, "DG")

# ── Metric card ────────────────────────────────────────────────────────────────
def metric(c, x, y, w, h, value, label, sub, vc):
    box(c, x, y, w, h, SLATE_L, radius=6, stroke=HexColor("#CBD5E1"), sw=0.4)
    box(c, x, y+h-5, w, 5, vc, radius=6)
    box(c, x, y+h-9, w, 4, vc)                      # square-off bottom of accent
    txt(c, value,  x+w/2, y+h-26, BOLD, 16, vc,    "center")
    txt(c, label,  x+w/2, y+h-39, BOLD,  7.5, NAVY, "center")
    txt(c, sub,    x+w/2, y+8,    BODY,  7,   STEEL,"center")

# ── Bullet ─────────────────────────────────────────────────────────────────────
def bullet(c, x, y, num, dc, title, body_s, cw):
    R = 7
    c.setFillColor(dc); c.circle(x+R, y+4, R, fill=1, stroke=0)
    c.setFillColor(white); c.setFont(BOLD, 7); c.drawCentredString(x+R, y+1.5, str(num))
    tx = x + R*2 + 5
    txt(c, title, tx, y+6, BOLD, 9, NAVY)
    lines = wrap(c, body_s, BODY, 8.2, cw - (tx-x))
    ny = y - 6
    for ln in lines:
        txt(c, ln, tx, ny, BODY, 8.2, SLATE2); ny -= 11
    return ny - 8     # generous bottom padding

# ── Value prop ─────────────────────────────────────────────────────────────────
def vp(c, x, y, accent, icon, title, body_s, cw):
    tx = x + 13
    lines = wrap(c, body_s, BODY, 8.2, cw - 15)
    bar_h = 16 + len(lines)*12
    box(c, x, y - bar_h + 16, 3, bar_h, accent)
    txt(c, icon + "  " + title, tx, y+4, BOLD, 9, NAVY)
    ny = y - 8
    for ln in lines:
        txt(c, ln, tx, ny, BODY, 8.2, SLATE2); ny -= 12
    return ny - 9     # generous bottom padding

# ── Customer segment ───────────────────────────────────────────────────────────
def segment(c, x, y, title, body_s, cw):
    c.setFillColor(BLUE); c.circle(x+4, y+4, 3.5, fill=1, stroke=0)
    txt(c, title, x+13, y+6, BOLD, 9, NAVY)
    lines = wrap(c, body_s, BODY, 8.2, cw - 13)
    ny = y - 6
    for ln in lines:
        txt(c, ln, tx:=x+13, ny, BODY, 8.2, SLATE2); ny -= 11
    return ny - 8

# ── Section label ──────────────────────────────────────────────────────────────
def section(c, label_s, x, y, color, w):
    txt(c, label_s, x, y, BOLD, 7, color)
    hline(c, x, x+w, y-4, color, 0.8)
    return y - 18    # generous section spacing

# ══════════════════════════════════════════════════════════════════════════════
#  LAYOUT CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
HDR_H    = 210
HDR_Y    = H - HDR_H      # 631.9
STRIP_H  = 40
STRIP_Y  = HDR_Y - STRIP_H  # 591.9
BODY_TOP = STRIP_Y - 16     # 575.9
FOOT_H   = 70
PAD      = 28
L_X      = PAD
L_W      = 320
R_X      = L_X + L_W + 16
R_W      = W - R_X - PAD   # ≈ 203

# ── BRAND BAR geometry (top of header, logo fully above headline) ─────────────
BRAND_CY  = H - 44          # logo centre Y       → logo spans H-74 .. H-14
BRAND_R   = 28              # logo radius
BRAND_BOT = BRAND_CY - BRAND_R  # = H-72  (lowest point of logo)

# headline must start at least 12pt below BRAND_BOT
HEADLINE_Y1 = BRAND_BOT - 14   # H-86
HEADLINE_Y2 = HEADLINE_Y1 - 24 # H-110
TAGLINE_Y1  = HEADLINE_Y2 - 18 # H-128
TAGLINE_Y2  = TAGLINE_Y1  - 14 # H-142

def draw_page(c):
    # ── Background ─────────────────────────────────────────────────────────────
    box(c, 0, 0, W, H, HexColor("#F8FAFD"))

    # ══════════════════════════════════════════════════════════════════════════
    # HEADER
    # ══════════════════════════════════════════════════════════════════════════
    box(c, 0, HDR_Y, W, HDR_H, NAVY)

    # diagonal accent shape (top-right)
    c.saveState(); c.setFillColor(NAVY2)
    p = c.beginPath()
    p.moveTo(W*0.60, H); p.lineTo(W, H - HDR_H*0.62); p.lineTo(W, H); p.close()
    c.drawPath(p, fill=1, stroke=0); c.restoreState()
    box(c, 0, H-4, W, 4, BLUE)   # top stripe

    # ── Brand bar: logo + name (all above BRAND_BOT = H-72) ──────────────────
    LOGO_CX = PAD + BRAND_R + 2   # 58
    logo(c, LOGO_CX, BRAND_CY, r=BRAND_R)
    NAME_X = LOGO_CX + BRAND_R + 12   # clear of logo right edge
    txt(c, "DEEPGUARD",          NAME_X, H-36, BOLD, 18, white)
    txt(c, "COMPLIANCE ENGINE",  NAME_X, H-52, BOLD,  9, HexColor("#93C5FD"))

    # ── Headline (starts 14pt below logo bottom — no overlap) ─────────────────
    txt(c, "Enterprise Security Compliance,",
        L_X, HEADLINE_Y1, BOLD, 19, white)
    txt(c, "Automated by AI — SaaS or On-Premise Options Available.",
        L_X, HEADLINE_Y2, BOLD, 15, HexColor("#93C5FD"))

    # ── Tagline ────────────────────────────────────────────────────────────────
    txt(c, "Agentic scanning of source code, cloud infrastructure & IaC —",
        L_X, TAGLINE_Y1, BODY, 9.5, HexColor("#CBD5E1"))
    txt(c, "one AI-generated audit report, CVSS-scored, in under 10 minutes.",
        L_X, TAGLINE_Y2, BODY, 9.5, HexColor("#CBD5E1"))

    # ── Threat Context badge (right side — fully inside header) ───────────────
    BX  = 368
    BW  = W - BX - 10            # ≈ 217
    BH  = HDR_H - 16             # 194
    BY  = HDR_Y + 8              # badge bottom
    box(c, BX, BY, BW, BH, HexColor("#111E30"), radius=6)
    # red title bar
    box(c, BX, BY+BH-22, BW, 22, RED, radius=6)
    box(c, BX, BY+BH-22, BW, 11, RED)
    txt(c, "THREAT CONTEXT — MARCH 2026",
        BX+BW/2, BY+BH-14, BOLD, 7, white, "center")

    badge_lines = [
        (HexColor("#FCA5A5"), 7.5, "Anthropic's Mythos AI model autonomously"),
        (HexColor("#FCA5A5"), 7.5, "discovered thousands of zero-day flaws"),
        (HexColor("#FCA5A5"), 7.5, "across all major OS & browsers — 99%"),
        (HexColor("#FCA5A5"), 7.5, "unpatched at time of public disclosure."),
    ]
    bty = BY + BH - 40
    for col, sz, line in badge_lines:
        txt(c, line, BX+10, bty, BODY, sz, col); bty -= 13
    hline(c, BX+10, BX+BW-10, bty-3, HexColor("#2D3F55"), 0.6)
    bty -= 15
    txt(c, "Project Glasswing scope: open-source only.", BX+10, bty, BODY, 7.5, AMBER2)
    bty -= 13
    txt(c, "Enterprise proprietary code and cloud",     BX+10, bty, BODY, 7.5, AMBER2)
    bty -= 13
    txt(c, "configuration: completely unprotected.",    BX+10, bty, BODY, 7.5, AMBER2)
    bty -= 13
    txt(c, "DeepGuard fills that gap.",                 BX+10, bty, BOLD, 8,   AMBER2)

    box(c, 0, HDR_Y-3, W, 3, BLUE2)   # bottom of header accent

    # ══════════════════════════════════════════════════════════════════════════
    # ALERT STRIP (two distinct lines, no overlap)
    # ══════════════════════════════════════════════════════════════════════════
    box(c, 0, STRIP_Y, W, STRIP_H, HexColor("#431407"))
    # line 1 — label + short description
    L1Y = STRIP_Y + STRIP_H - 14
    txt(c, "THE BLIND SPOT", L_X, L1Y, BOLD, 9, AMBER2)
    sep = L_X + c.stringWidth("THE BLIND SPOT", BOLD, 9) + 10
    hline(c, sep, sep+8, L1Y+4, AMBER2, 1.5)
    txt(c, "Glasswing does not cover proprietary code, cloud config, or AI integrations.",
        sep+14, L1Y, BODY, 8.5, HexColor("#FDE68A"))
    # line 2 — consequence
    L2Y = STRIP_Y + 9
    txt(c, "These are the three highest-risk enterprise layers — and DeepGuard scans all three, "
           "with AI-powered cross-layer reasoning.",
        L_X, L2Y, BODY, 8.5, HexColor("#FED7AA"))

    # ══════════════════════════════════════════════════════════════════════════
    # BODY
    # ══════════════════════════════════════════════════════════════════════════
    ly = BODY_TOP
    ry = BODY_TOP

    # ── LEFT COLUMN ────────────────────────────────────────────────────────────

    ly = section(c, "THE PROBLEM", L_X, ly, RED2, L_W)

    ly = wtext(c,
        "Security compliance is manual, slow, and catastrophically incomplete. "
        "An ISO 27001 or MAS TRM audit consumes 3-6 months and costs SGD 80K-500K — "
        "yet captures only a point-in-time snapshot. With AI-powered adversaries "
        "autonomously discovering zero-day vulnerabilities at scale, that cycle "
        "is no longer acceptable.",
        L_X, ly, BODY, 9, SLATE, L_W, 14) - 8

    for num, dc, t, d in [
        (1, RED2,  "Proprietary code is invisible to Glasswing.",
                   "App logic, auth flows, and LLM integrations remain completely unscanned."),
        (2, AMBER, "Cloud configuration drifts faster than any audit.",
                   "IAM policies, storage ACLs, and network rules change daily — reports are instantly stale."),
        (3, BLUE,  "Compliance is siloed — code vs. IaC vs. cloud.",
                   "No existing tool correlates all three layers into a single evidence-backed finding."),
    ]:
        ly = bullet(c, L_X, ly, num, dc, t, d, L_W)

    ly -= 10
    ly = section(c, "THE SOLUTION", L_X, ly, GREEN2, L_W)

    ly = wtext(c,
        "DeepGuard deploys entirely inside the customer's environment — VPC, private "
        "cloud, or on-premise data centre. The Odysseus Engine, a LangGraph "
        "multi-agent orchestrator, dispatches nine specialised AI agents that "
        "simultaneously scan source code, IaC templates, and live cloud "
        "configuration. Cross-layer correlation reasoning surfaces compound "
        "vulnerabilities no rule-based scanner can detect. Output: a board-ready "
        "PDF audit report with CVSS-scored findings, code-level evidence, and "
        "diff-ready patches — in under 10 minutes.",
        L_X, ly, BODY, 9, SLATE, L_W, 14) - 10

    ly = section(c, "KEY VALUE PROPOSITIONS", L_X, ly, BLUE, L_W)

    for accent, icon, title, body_s in [
        (GREEN2, "▶", "Data Sovereignty by Design",
                      "Code never leaves the customer's environment. Full air-gap support for "
                      "Xinchuang and offline data centre deployments."),
        (BLUE,   "▶", "AI Reasoning, Not Rule Matching",
                      "LLM inference uncovers logic-layer vulnerabilities invisible to "
                      "signature-based or regex-pattern scanners."),
        (TEAL,   "▶", "Three-Layer Unified Audit",
                      "One report covers application code, IaC templates, and live cloud "
                      "configuration with cross-layer correlation analysis."),
        (AMBER,  "▶", "Comprehensive Regulatory Coverage",
                      "ISO 27001, SOC 2, MAS TRM, PCI-DSS, HIPAA, GDPR, GB/T 22239 "
                      "— all built in, no custom configuration required."),
        (RED2,   "▶", "Minutes, Not Months",
                      "P95 full-stack scan under 10 minutes. Incremental delta cache "
                      "cuts LLM cost by 60-80% for active repositories."),
    ]:
        ly = vp(c, L_X, ly, accent, icon, title, body_s, L_W)

    # ── RIGHT COLUMN ───────────────────────────────────────────────────────────

    ry = section(c, "INVESTMENT HIGHLIGHTS", R_X, ry, BLUE, R_W)

    MH  = 54
    MGX = 6
    MW  = (R_W - MGX) / 2

    for i, (val, lbl, sub, vc) in enumerate([
        ("SGD 1.6M",  "Angel Round",      "Seeking now",         BLUE),
        ("SGD 3.4M",  "18-Month ARR",     "Revenue target",      GREEN2),
        ("< 10 min",  "Full-Stack Scan",  "P95 latency",         TEAL),
        ("SGD 270M+", "Exit Valuation",   "5-year projection",   AMBER2),
    ]):
        mx = R_X + (i % 2) * (MW + MGX)
        my = ry - (i // 2) * (MH + 7) - MH
        metric(c, mx, my, MW, MH, val, lbl, sub, vc)

    ry -= 2*(MH+7) + 14

    ry = section(c, "TARGET ENTERPRISE CUSTOMERS", R_X, ry, BLUE, R_W)
    ry -= 6

    for seg_t, seg_d in [
        ("Financial Services",
         "Banks, insurers, payment platforms — MAS TRM, PCI-DSS, SOC 2 Type II."),
        ("Government & Defence",
         "Public sector MLPS Level-3 mandates; Xinchuang IT substitution environments."),
        ("Healthcare & Life Sciences",
         "HIPAA, PDPA; hospital and pharma IT with strict audit trail requirements."),
        ("Technology & SaaS",
         "Cloud-native teams shipping AI features; SOC 2 Type II certification pipelines."),
        ("Energy & Critical Infrastructure",
         "ICS/SCADA operators; critical information infrastructure compliance."),
    ]:
        ry = segment(c, R_X, ry, seg_t, seg_d, R_W)

    ry -= 8

    # ── SUPPORTED PLATFORMS (explicit two rows) ────────────────────────────────
    ry = section(c, "SUPPORTED CLOUD PLATFORMS", R_X, ry, BLUE, R_W)

    TAG_H = 20
    TAG_GAP = 5

    # Row label helper
    def tag_row_label(y, label_s):
        txt(c, label_s, R_X, y, BOLD, 6.5, STEEL)
        return y - 14

    def tag_row(tags_list, start_x, start_y):
        tx = start_x
        for label, bg, fg in tags_list:
            tw = c.stringWidth(label, BODY, 8) + 16
            box(c, tx, start_y, tw, TAG_H, bg, radius=4, stroke=fg, sw=0.6)
            txt(c, label, tx+8, start_y+6, BODY, 8, fg)
            tx += tw + TAG_GAP
        return start_y - TAG_H - 8

    # Row 1 — Global cloud providers
    ry = tag_row_label(ry, "GLOBAL")
    global_clouds = [
        ("AWS",           AMBER_L,  AMBER),
        ("Microsoft Azure",BLUE_L,  BLUE2),
        ("Google Cloud",  GREEN_L,  GREEN),
    ]
    ry = tag_row(global_clouds, R_X, ry)
    ry = tag_row([("Air-Gap / DC",  PURPLE_L, PURPLE)], R_X, ry)

    # Row 2 — Asia-Pacific cloud providers
    ry = tag_row_label(ry, "ASIA-PACIFIC")
    china_clouds = [
        ("Alibaba Cloud", GREEN_L,  GREEN),
        ("Tencent Cloud", BLUE_L,   BLUE2),
        ("Huawei Cloud",  RED_L,    RED),
    ]
    ry = tag_row(china_clouds, R_X, ry)

    # ── Divider ────────────────────────────────────────────────────────────────
    hline(c, 20, W-20, FOOT_H+4, HexColor("#CBD5E1"), 0.5)

    # ══════════════════════════════════════════════════════════════════════════
    # FOOTER
    # ══════════════════════════════════════════════════════════════════════════
    box(c, 0, 0, W, FOOT_H, NAVY)
    box(c, 0, FOOT_H, W, 3, BLUE)

    logo(c, 44, FOOT_H/2, r=22)

    txt(c, "REQUEST A DEMO — SEE YOUR COMPLIANCE POSTURE IN 10 MINUTES",
        82, FOOT_H-16, BOLD, 8.5, white)
    txt(c, "Scan your own repository. Zero code egress. Board-ready PDF audit report delivered in minutes.",
        82, FOOT_H-29, BODY, 8, HexColor("#93C5FD"))
    txt(c, "Powered by the Odysseus Engine  ·  LangGraph Multi-Agent Orchestration  ·  Singapore & Global",
        82, FOOT_H-43, BODY, 7.5, STEEL)

    box(c, W-168, 12, 146, 44, HexColor("#0D2137"), radius=5,
        stroke=BLUE, sw=0.6)
    txt(c, "CONFIDENTIAL",           W-95, FOOT_H-18, BOLD, 7.5, AMBER2,             "center")
    txt(c, "For qualified investors", W-95, FOOT_H-29, BODY, 7,   STEEL,             "center")
    txt(c, "and enterprise prospects",W-95, FOOT_H-39, BODY, 7,   STEEL,             "center")
    txt(c, "DeepGuard · April 2026",  W-95, FOOT_H-51, BODY, 6.5, HexColor("#64748B"),"center")


# ── Generate ───────────────────────────────────────────────────────────────────
def generate(out_path: str):
    c = canvas.Canvas(out_path, pagesize=A4)
    c.setTitle("DeepGuard Compliance Engine — Executive Summary")
    c.setAuthor("DeepGuard Product Team")
    draw_page(c)
    c.save()
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    out = FilePath(__file__).parent / "DeepGuard_Executive_Summary.pdf"
    generate(str(out))
