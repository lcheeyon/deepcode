"""
Chinese-language architecture diagrams for the Xuanwu Compliance Engine proposal.
Uses the same brand palette as diagrams.py but with Chinese labels.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.font_manager as fm
import os

# ── Brand palette ─────────────────────────────────────────────────────────────
NAVY      = "#0D2137"
BLUE      = "#1A56DB"
BLUE_MID  = "#2563EB"
BLUE_LITE = "#93C5FD"
TEAL      = "#0EA5E9"
GREEN     = "#16A34A"
GREEN_L   = "#BBF7D0"
ORANGE    = "#D97706"
ORANGE_L  = "#FDE68A"
RED       = "#DC2626"
RED_L     = "#FECACA"
PURPLE    = "#7C3AED"
PURPLE_L  = "#DDD6FE"
GREY_D    = "#374151"
GREY_M    = "#6B7280"
WHITE     = "#FFFFFF"
SLATE     = "#1E3A5F"
GOLD      = "#B45309"
GOLD_L    = "#FEF3C7"

# ── Register CJK fonts ────────────────────────────────────────────────────────
_HEITI  = "/System/Library/Fonts/STHeiti Medium.ttc"
_SONGTI = "/System/Library/Fonts/Supplemental/Songti.ttc"
_ARIAL  = "/Library/Fonts/Arial Unicode.ttf"

def _get_cjk_font(size=9):
    """Return a FontProperties object for Chinese text rendering."""
    for path in [_HEITI, _ARIAL]:
        if os.path.exists(path):
            return fm.FontProperties(fname=path, size=size)
    return fm.FontProperties(size=size)

def _get_song_font(size=9):
    for path in [_SONGTI, _ARIAL]:
        if os.path.exists(path):
            return fm.FontProperties(fname=path, size=size)
    return fm.FontProperties(size=size)


def _box(ax, x, y, w, h, label, sublabel=None,
         fc=SLATE, ec=BLUE_MID, tc=WHITE, stc=BLUE_LITE,
         fontsize=8, radius=0.015, lw=1.2, bold=False):
    box = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3
    )
    ax.add_patch(box)
    fp = _get_cjk_font(fontsize)
    fp_bold = _get_cjk_font(fontsize)
    if sublabel:
        ax.text(x, y + h*0.14, label, ha="center", va="center",
                color=tc, fontsize=fontsize, fontproperties=fp, zorder=4, fontweight="bold" if bold else "normal")
        ax.text(x, y - h*0.20, sublabel, ha="center", va="center",
                color=stc, fontsize=fontsize - 1.5, fontproperties=_get_cjk_font(fontsize-1.5),
                fontstyle="italic", zorder=4)
    else:
        ax.text(x, y, label, ha="center", va="center",
                color=tc, fontsize=fontsize, fontproperties=fp, zorder=4,
                fontweight="bold" if bold else "normal")


def _arrow(ax, x0, y0, x1, y1, color=BLUE_LITE, lw=1.2):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="->", color=color,
                                lw=lw, connectionstyle="arc3,rad=0"))


def _section_label(ax, x, y, w, h, text, fc=NAVY, tc=BLUE_LITE):
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0,rounding_size=0.012",
        facecolor=fc, edgecolor=BLUE_MID, linewidth=0.8,
        alpha=0.55, zorder=1
    )
    ax.add_patch(rect)
    ax.text(x + 0.012, y + h - 0.022, text,
            ha="left", va="top", color=tc,
            fontsize=7.5, fontproperties=_get_cjk_font(7.5),
            fontweight="bold", zorder=2, alpha=0.85)


# ─────────────────────────────────────────────────────────────────────────────
# Diagram 1 — System Architecture (Chinese)
# ─────────────────────────────────────────────────────────────────────────────
def draw_system_overview_cn(path: str, dpi: int = 180):
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fp_title = _get_cjk_font(13)
    fp_sub   = _get_cjk_font(8.5)

    ax.text(0.5, 0.968, "玄武合规引擎 — 系统架构总览",
            ha="center", va="top", color=WHITE, fontsize=13,
            fontproperties=fp_title, fontweight="bold")
    ax.text(0.5, 0.947, "多云原生 · VPC 私有化部署 · 离线信创就绪 · 姜子牙编排引擎",
            ha="center", va="top", color=BLUE_LITE, fontsize=8.5,
            fontproperties=fp_sub, fontstyle="italic")

    # Outer VPC boundary
    vpc = FancyBboxPatch((0.02, 0.03), 0.96, 0.89,
                         boxstyle="round,pad=0,rounding_size=0.018",
                         facecolor="#0A1929", edgecolor=BLUE_MID,
                         linewidth=1.5, linestyle="--", zorder=0)
    ax.add_patch(vpc)
    ax.text(0.05, 0.898, "阿里云 VPC / 腾讯云 VPC / 华为云 VPC / 企业自有 Kubernetes",
            ha="left", va="top", color=BLUE_LITE, fontsize=7.5,
            fontproperties=_get_cjk_font(7.5), fontweight="bold", alpha=0.9)

    # ── ROW 1: Ingestion Layer ────────────────────────────────────────────────
    _section_label(ax, 0.04, 0.73, 0.92, 0.14, "太白金星 — 数据摄取网关", fc="#0F2D4A")
    sources = [
        (0.13, "GitHub\nGitLab / Gitee"),
        (0.29, "ZIP 上传\n（OSS 预签名）"),
        (0.47, "Terraform / ROS\nRFS / CFN"),
        (0.65, "实时云 API\n阿里 · 腾讯 · 华为"),
        (0.83, "策略文档\nPDF / YAML"),
    ]
    for sx, sl in sources:
        _box(ax, sx, 0.808, 0.14, 0.075, sl,
             fc="#133152", ec=TEAL, tc=WHITE, fontsize=7)
    for sx, _ in sources:
        _arrow(ax, sx, 0.770, sx, 0.718, color=TEAL, lw=0.9)

    # ── ROW 2: Orchestration ──────────────────────────────────────────────────
    _section_label(ax, 0.04, 0.595, 0.92, 0.118, "姜子牙 — 玄武引擎（LangGraph 编排核心）", fc="#1A2744")
    _box(ax, 0.50, 0.660, 0.88, 0.056,
         "LangGraph 状态机  ·  DynamoDB 检查点  ·  按控制项并行展开",
         fc=SLATE, ec=BLUE_MID, tc=BLUE_LITE, fontsize=7.5)
    _arrow(ax, 0.50, 0.632, 0.50, 0.600, color=BLUE_LITE, lw=1.2)

    # ── ROW 3: Agent Layer ────────────────────────────────────────────────────
    _section_label(ax, 0.04, 0.415, 0.92, 0.180, "九天神将 — 分析代理图", fc="#1E2D40")
    agents = [
        (0.13, 0.535, "太白金星\n摄取代理",   "#133152", TEAL),
        (0.30, 0.535, "伏  羲\n策略解析器",    "#133152", BLUE_MID),
        (0.47, 0.535, "千里眼\n代码索引器",    "#133152", BLUE_MID),
        (0.65, 0.535, "钟  馗\nIaC 分析器",    "#133152", ORANGE),
        (0.83, 0.535, "比  干\n云配置检测",    "#133152", ORANGE),
    ]
    for ax_, ay_, al_, afc, aec in agents:
        _box(ax, ax_, ay_, 0.14, 0.075, al_, fc=afc, ec=aec, fontsize=7)
    for ax_, ay_, *_ in agents:
        _arrow(ax, ax_, ay_ - 0.0375, ax_, 0.462, color=GREY_M, lw=0.8)

    _box(ax, 0.50, 0.448, 0.88, 0.056,
         "观音菩萨 — 合规映射引擎  ·  RAG 检索 + LLM 推理  ·  通过 / 失败 / 部分 / 不适用",
         fc=PURPLE, ec="#A855F7", tc=WHITE, fontsize=7.5)
    _arrow(ax, 0.50, 0.420, 0.50, 0.395, color=PURPLE_L, lw=1.2)

    _box(ax, 0.50, 0.378, 0.88, 0.044,
         "神农氏 — 修复建议器  ·  代码补丁  ·  IaC 修复（ROS/RFS/CFN）  ·  CLI 命令",
         fc="#1C3830", ec=GREEN, tc=GREEN_L, fontsize=7.5)

    # ── ROW 4: Report Layer ───────────────────────────────────────────────────
    _arrow(ax, 0.50, 0.356, 0.50, 0.332, color=GREEN, lw=1.2)
    _section_label(ax, 0.04, 0.238, 0.92, 0.090, "织  女 — 报告层", fc="#1A2D20")
    _box(ax, 0.33, 0.292, 0.26, 0.058,
         "织女\n报告组装器",
         fc="#1C3830", ec=GREEN, tc=GREEN_L, fontsize=7.5)
    _arrow(ax, 0.46, 0.292, 0.56, 0.292, color=GREEN, lw=1.0)
    _box(ax, 0.69, 0.292, 0.24, 0.058,
         "PDF 生成器\nReportLab + Jinja2",
         fc="#1C3830", ec=GREEN, tc=GREEN_L, fontsize=7.5)

    # ── BOTTOM: Provider + LLM + Observability ────────────────────────────────
    _section_label(ax, 0.04, 0.085, 0.60, 0.105, "服务抽象层", fc="#251D0A")
    providers = [
        (0.13, "存  储\nOSS/COS/OBS/S3"),
        (0.30, "东海龙王\n密钥（KMS/DEW）"),
        (0.47, "门  神\n身份认证（IAM）"),
        (0.63, "风  伯\n队列（MNS/TDMQ）"),
    ]
    for px, pl in providers:
        _box(ax, px, 0.128, 0.14, 0.060, pl,
             fc="#2D1F06", ec=ORANGE, tc=ORANGE_L, fontsize=6.5)

    _section_label(ax, 0.66, 0.085, 0.30, 0.105, "大模型推理层", fc="#130E2A")
    _box(ax, 0.755, 0.113, 0.125, 0.056,
         "云端大模型\n通义/混元/盘古",
         fc="#1B1040", ec=PURPLE, tc=PURPLE_L, fontsize=6.5)
    _box(ax, 0.905, 0.113, 0.125, 0.056,
         "开源自托管\nQwen / DeepSeek",
         fc="#1B1040", ec=PURPLE, tc=PURPLE_L, fontsize=6.5)

    # Observability row
    obs_y = 0.048
    for bx, lbl in [(0.22, "LangSmith（自托管）"),
                    (0.50, "LangFuse（自托管）"),
                    (0.78, "OpenTelemetry → Grafana")]:
        _box(ax, bx, obs_y, 0.22 if bx < 0.5 else 0.34, 0.042, lbl,
             fc="#1A1A2E", ec=BLUE_MID, tc=BLUE_LITE, fontsize=6.8)
    ax.text(0.05, obs_y + 0.005, "可观测性", ha="left", va="center",
            color=GREY_M, fontsize=7, fontproperties=_get_cjk_font(7), fontweight="bold")

    plt.tight_layout(pad=0)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=NAVY, edgecolor="none")
    plt.close(fig)
    print(f"Saved: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# Diagram 2 — Agent Pipeline (Chinese)
# ─────────────────────────────────────────────────────────────────────────────
def draw_agent_pipeline_cn(path: str, dpi: int = 180):
    fig, ax = plt.subplots(figsize=(14, 11))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fp_title = _get_cjk_font(13)
    ax.text(0.5, 0.973, "玄武引擎 — 九天神将作战流水线",
            ha="center", va="top", color=WHITE, fontsize=13,
            fontproperties=fp_title, fontweight="bold")
    ax.text(0.5, 0.952, "有状态多智能体图  ·  按控制项并行展开  ·  DynamoDB 检查点  ·  跨层关联分析",
            ha="center", va="top", color=BLUE_LITE, fontsize=8,
            fontproperties=_get_cjk_font(8), fontstyle="italic")

    def node(cx, cy, w, h, title, bullets,
             fc=SLATE, ec=BLUE_MID, tc=WHITE, btc=BLUE_LITE):
        _box(ax, cx, cy, w, h, title, fc=fc, ec=ec, tc=tc, fontsize=8.5, bold=True)
        fp_b = _get_cjk_font(6.5)
        for i, b in enumerate(bullets):
            bx = cx - w/2 + 0.012
            by = cy + h/2 - 0.028 - i * 0.026
            ax.text(bx, by, f"• {b}", ha="left", va="center",
                    color=btc, fontsize=6.5, fontproperties=fp_b, zorder=5)

    # START
    _box(ax, 0.50, 0.918, 0.14, 0.036, "开  始",
         fc=GREEN, ec="#15803D", tc=WHITE, fontsize=8.5, bold=True)
    _arrow(ax, 0.50, 0.900, 0.50, 0.870)

    # Node 1: Hermes
    node(0.50, 0.822, 0.88, 0.082, "① 太白金星 — 数据摄取代理",
         ["克隆 GitHub / GitLab / Gitee 仓库或解压 ZIP → 对象存储",
          "检测：编程语言、框架、入口点、依赖清单",
          "IaC 文件：Terraform / 阿里云 ROS / 华为云 RFS / CloudFormation",
          "实时云：调用云连接器（阿里云 / 腾讯云 / 华为云 / AWS）"],
         fc=SLATE, ec=TEAL, btc=BLUE_LITE)
    _arrow(ax, 0.50, 0.781, 0.50, 0.754)

    # Node 2: Tiresias
    node(0.50, 0.716, 0.88, 0.072, "② 伏羲 — 策略解析器",
         ["解析合规文档：PDF · YAML · 预设框架选择器（等保 2.0 / OWASP / ISO 27001）",
          "分解为带范围标签的控制要求[]",
          "范围标签：[代码 | IaC | 云配置 | 全部]"],
         fc=SLATE, ec=BLUE_MID, btc=BLUE_LITE)
    _arrow(ax, 0.50, 0.680, 0.50, 0.651)

    # Node 3: Argus
    node(0.50, 0.613, 0.88, 0.072, "③ 千里眼 — 代码索引器",
         ["tree-sitter AST 解析：Python · Java · TypeScript · Go · C# · PHP",
          "依赖图与数据流图提取",
          "语义分块 → 向量嵌入 → pgvector 索引"],
         fc=SLATE, ec=BLUE_MID, btc=BLUE_LITE)
    _arrow(ax, 0.50, 0.577, 0.50, 0.551)

    # Fan-out label
    _box(ax, 0.50, 0.536, 0.88, 0.030,
         "并行展开  ·  每个控制要求范围独立子图",
         fc="#1A2744", ec=GREY_D, tc=GREY_M, fontsize=7.5)

    # Fan-out arrows
    fan_targets = [0.17, 0.50, 0.83]
    fan_labels  = ["代码范围\n控制项", "IaC 范围\n控制项", "云配置\n控制项"]
    fan_colors  = [BLUE_MID, ORANGE, GREEN]
    for tx, lbl, fc_ in zip(fan_targets, fan_labels, fan_colors):
        ax.annotate("", xy=(tx, 0.490), xytext=(0.50, 0.521),
                    arrowprops=dict(arrowstyle="->", color=fc_, lw=1.1,
                                   connectionstyle="arc3,rad=0"))
        ax.text(tx, 0.498, lbl, ha="center", va="top",
                color=fc_, fontsize=6.2, fontproperties=_get_cjk_font(6.2),
                fontstyle="italic")

    # Three parallel nodes
    parallel_specs = [
        (0.17, ["RAG 检索源代码\n向量索引",
                "语义相似度\n检索 + 重排序",
                "返回：相关\n代码片段"], BLUE_MID),
        (0.50, ["解析 Terraform / ROS\nRFS / CFN AST",
                "资源属性 vs\n策略控制对比",
                "漂移：IaC vs\n实时配置"], ORANGE),
        (0.83, ["调用云连接器\n.get_resources()",
                "规范化为标准\n资源快照 Schema",
                "阿里 · 腾讯 · 华为\n资源配置"], GREEN),
    ]
    p_titles = ["④a 代码分析器", "④b 钟馗 — IaC 分析", "④c 比干 — 云配置"]
    for (px, pbullets, pec), pt in zip(parallel_specs, p_titles):
        node(px, 0.428, 0.29, 0.10, pt, pbullets,
             fc=SLATE, ec=pec, btc=WHITE)

    # Converge to compliance mapper
    for px, pc in zip(fan_targets, fan_colors):
        ax.annotate("", xy=(0.50, 0.355), xytext=(px, 0.378),
                    arrowprops=dict(arrowstyle="->", color=pc, lw=1.1,
                                   connectionstyle="arc3,rad=0"))

    # Node 5: Athena
    node(0.50, 0.317, 0.88, 0.072, "⑤ 观音菩萨 — 合规映射代理",
         ["RAG 检索三层全部证据，对每项控制要求逐一分析",
          "LLM 推理：通过 / 失败 / 部分通过 / 不适用",
          "跨层关联：基础设施承诺 vs. 代码实现缺口",
          "生成发现项：证据 · 严重性 · CVSS 评分 · 推理链"],
         fc=PURPLE, ec="#A855F7", tc=WHITE, btc=PURPLE_L)
    _arrow(ax, 0.50, 0.281, 0.50, 0.255, color=PURPLE_L)

    # Node 6: Circe
    node(0.50, 0.217, 0.88, 0.072, "⑥ 神农氏 — 修复建议代理",
         ["源代码发现的代码补丁（diff 格式）",
          "IaC 修复（Terraform / 阿里云 ROS / 华为云 RFS / CloudFormation）",
          "云 CLI 修复命令（aliyun CLI / tccli / huaweicloud CLI / aws CLI）"],
         fc="#1C3830", ec=GREEN, tc=GREEN_L, btc=GREEN_L)
    _arrow(ax, 0.50, 0.181, 0.50, 0.154, color=GREEN)

    # Node 7: Penelope
    node(0.50, 0.116, 0.88, 0.072, "⑦ 织女 — 报告组装器 → PDF 生成器",
         ["按层次（代码 / IaC / 云配置）和严重性整理发现项",
          "生成跨层关联洞察与管理层摘要",
          "渲染专业 PDF（ReportLab + Jinja2）→ OSS/COS/OBS 加密归档 → 通知"],
         fc="#1C3830", ec=GREEN, tc=GREEN_L, btc=GREEN_L)
    _arrow(ax, 0.50, 0.080, 0.50, 0.054, color=GREEN)

    # END
    _box(ax, 0.50, 0.040, 0.14, 0.030, "结  束",
         fc=RED, ec="#B91C1C", tc=WHITE, fontsize=8.5, bold=True)

    # Legend
    legend_items = [
        mpatches.Patch(facecolor=SLATE,    edgecolor=TEAL,     label="太白金星（摄取）"),
        mpatches.Patch(facecolor=SLATE,    edgecolor=BLUE_MID, label="伏羲 / 千里眼（解析 / 索引）"),
        mpatches.Patch(facecolor=PURPLE,   edgecolor="#A855F7",label="观音菩萨（LLM 推理）"),
        mpatches.Patch(facecolor="#1C3830",edgecolor=GREEN,    label="神农 / 织女（修复 / 报告）"),
        mpatches.Patch(facecolor=SLATE,    edgecolor=ORANGE,   label="钟馗 / 比干（IaC / 云配置）"),
    ]
    ax.legend(handles=legend_items, loc="lower right",
              facecolor="#0F2030", edgecolor=BLUE_MID,
              labelcolor=WHITE, fontsize=7, framealpha=0.85,
              prop=_get_cjk_font(7))

    plt.tight_layout(pad=0)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=NAVY, edgecolor="none")
    plt.close(fig)
    print(f"Saved: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# Diagram 3 — Three-Cloud Deployment Architecture (Chinese)
# ─────────────────────────────────────────────────────────────────────────────
def draw_three_cloud_deployment(path: str, dpi: int = 180):
    fig, ax = plt.subplots(figsize=(15, 9))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fp_title = _get_cjk_font(12)
    ax.text(0.5, 0.968, "玄武合规引擎 — 三大国内云专属部署架构",
            ha="center", va="top", color=WHITE, fontsize=12,
            fontproperties=fp_title, fontweight="bold")
    ax.text(0.5, 0.946, "阿里云 · 腾讯云 · 华为云  |  私有 VPC 部署  |  代码永不离境",
            ha="center", va="top", color=BLUE_LITE, fontsize=8,
            fontproperties=_get_cjk_font(8), fontstyle="italic")

    # Three cloud columns
    clouds = [
        {"x": 0.17, "color": ORANGE, "light": ORANGE_L, "bg": "#2D1A06",
         "title": "[ 阿里云 ] Alibaba Cloud",
         "subtitle": "互联网 · 金融科技 · 电商",
         "k8s": "容器服务 ACK",
         "db": "云原生数据库 PolarDB\n（pgvector）",
         "storage": "对象存储 OSS\n（KMS 加密）",
         "keys": "密钥管理 KMS",
         "auth": "访问控制 RAM\n+ IDaaS",
         "queue": "消息服务 MNS",
         "llm": "阿里云百炼\n通义千问 Qwen3",
         "audit": "ActionTrail\n+ 日志服务 SLS",
         "iac": "Terraform alicloud\n+ 阿里云 ROS",
         "badge": "互联网领先"},
        {"x": 0.50, "color": TEAL, "light": BLUE_LITE, "bg": "#061D2D",
         "title": "[ 腾讯云 ] Tencent Cloud",
         "subtitle": "互联网 · 游戏 · 微信生态",
         "k8s": "容器服务 TKE",
         "db": "云数据库 TDSQL-C\n（pgvector）",
         "storage": "对象存储 COS\n（SSE-KMS 加密）",
         "keys": "密钥管理 KMS",
         "auth": "访问管理 CAM\n+ 身份认证",
         "queue": "消息队列 TDMQ\n（Pulsar）",
         "llm": "混元大模型\nHunyuan-Code",
         "audit": "云审计 CloudAudit\n+ 日志服务 CLS",
         "iac": "Terraform tencentcloud\n+ 腾讯云 TIC",
         "badge": "微信生态优势"},
        {"x": 0.83, "color": "#CC0000", "light": "#FECACA", "bg": "#2D0606",
         "title": "[ 华为云 ] Huawei Cloud",
         "subtitle": "政务 · 央企 · 信创首选",
         "k8s": "云容器引擎 CCE",
         "db": "GaussDB（国产自研\npgvector）",
         "storage": "对象存储 OBS\n（DEW 国密加密）",
         "keys": "数据加密 DEW\n（SM2/SM3/SM4）",
         "auth": "统一身份 IAM\n+ OneAccess",
         "queue": "分布式消息 DMS\nKafka",
         "llm": "华为盘古大模型\nPanGu-Code",
         "audit": "云审计 CTS\n+ 日志存储 LTS",
         "iac": "Terraform huaweicloud\n+ 华为云 RFS",
         "badge": "★ 信创认证 ★"},
    ]

    col_w = 0.26
    for c in clouds:
        cx = c["x"]
        col_color = c["color"]
        bg = c["bg"]
        light = c["light"]

        # Column background
        col_bg = FancyBboxPatch((cx - col_w/2, 0.05), col_w, 0.845,
                                boxstyle="round,pad=0,rounding_size=0.012",
                                facecolor=bg, edgecolor=col_color,
                                linewidth=1.8, alpha=0.6, zorder=1)
        ax.add_patch(col_bg)

        # Title
        ax.text(cx, 0.878, c["title"], ha="center", va="center",
                color=col_color, fontsize=8, fontproperties=_get_cjk_font(8),
                fontweight="bold", zorder=4)
        ax.text(cx, 0.857, c["subtitle"], ha="center", va="center",
                color=light, fontsize=6.8, fontproperties=_get_cjk_font(6.8),
                fontstyle="italic", zorder=4)

        # Service rows
        rows = [
            ("Kubernetes 容器", c["k8s"],     BLUE_MID,  "#1A2744"),
            ("向量数据库",      c["db"],       BLUE_MID,  "#1A2744"),
            ("对象存储",        c["storage"],  TEAL,      "#0F2D3D"),
            ("密钥管理",        c["keys"],     ORANGE,    "#2D1A06"),
            ("身份认证",        c["auth"],     ORANGE,    "#2D1A06"),
            ("任务队列",        c["queue"],    GREY_D,    "#1A1A2E"),
            ("大模型（LLM）",   c["llm"],      PURPLE,    "#1B1040"),
            ("审计日志",        c["audit"],    GREEN,     "#0D2318"),
            ("IaC 支持",        c["iac"],      col_color, bg),
        ]

        row_heights = [0.064, 0.064, 0.058, 0.052, 0.058, 0.052, 0.058, 0.058, 0.052]
        ys = [0.790, 0.720, 0.656, 0.598, 0.536, 0.479, 0.416, 0.354, 0.292]

        for (label, val, ec, fc_), y, rh in zip(rows, ys, row_heights):
            box = FancyBboxPatch((cx - col_w/2 + 0.008, y - rh/2),
                                  col_w - 0.016, rh,
                                  boxstyle="round,pad=0,rounding_size=0.008",
                                  facecolor=fc_, edgecolor=ec,
                                  linewidth=0.8, zorder=3)
            ax.add_patch(box)
            ax.text(cx - col_w/2 + 0.018, y + rh/2 - 0.012, label,
                    ha="left", va="top", color=ec,
                    fontsize=5.8, fontproperties=_get_cjk_font(5.8),
                    fontweight="bold", zorder=4)
            ax.text(cx, y - 0.004, val, ha="center", va="center",
                    color=WHITE, fontsize=6.2, fontproperties=_get_cjk_font(6.2),
                    zorder=4)

        # Badge
        badge_color = col_color
        badge = FancyBboxPatch((cx - col_w/2 + 0.01, 0.065), col_w - 0.02, 0.048,
                               boxstyle="round,pad=0,rounding_size=0.010",
                               facecolor=badge_color, edgecolor=badge_color,
                               linewidth=0, alpha=0.25, zorder=2)
        ax.add_patch(badge)
        ax.text(cx, 0.089, c["badge"],
                ha="center", va="center", color=light,
                fontsize=7.5, fontproperties=_get_cjk_font(7.5),
                fontweight="bold", zorder=4)

    # Shared bottom row
    bottom_items = [
        (0.17, "数据永不离开\n企业安全边界", TEAL),
        (0.50, "等保 2.0 全覆盖\n统一合规报告", GREEN),
        (0.83, "开源大模型备选\nQwen3 / DeepSeek", PURPLE),
    ]
    for bx, bl, bc in bottom_items:
        ax.text(bx, 0.027, bl, ha="center", va="center",
                color=bc, fontsize=7, fontproperties=_get_cjk_font(7),
                fontweight="bold", zorder=5)

    plt.tight_layout(pad=0)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=NAVY, edgecolor="none")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    draw_system_overview_cn("diagram_cn_system_overview.png")
    draw_agent_pipeline_cn("diagram_cn_agent_pipeline.png")
    draw_three_cloud_deployment("diagram_cn_three_cloud.png")
