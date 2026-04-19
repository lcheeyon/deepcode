"""
Render architecture diagrams as high-resolution PNG files for embedding in the PDF.
Uses matplotlib with a dark-navy enterprise theme matching the DeepGuard brand palette.
"""

import io
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
import numpy as np

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
GREY_L    = "#F0F4FA"
WHITE     = "#FFFFFF"
SLATE     = "#1E3A5F"


def _box(ax, x, y, w, h, label, sublabel=None,
         fc=SLATE, ec=BLUE_MID, tc=WHITE, stc=BLUE_LITE,
         fontsize=8.5, radius=0.015, lw=1.2, bold=False):
    """Draw a rounded-rectangle box with an optional sub-label."""
    box = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3
    )
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    if sublabel:
        ax.text(x, y + h*0.12, label, ha="center", va="center",
                color=tc, fontsize=fontsize, fontweight=weight, zorder=4)
        ax.text(x, y - h*0.22, sublabel, ha="center", va="center",
                color=stc, fontsize=fontsize - 1.5, fontstyle="italic", zorder=4)
    else:
        ax.text(x, y, label, ha="center", va="center",
                color=tc, fontsize=fontsize, fontweight=weight, zorder=4)


def _arrow(ax, x0, y0, x1, y1, color=BLUE_LITE, lw=1.2, style="->", label=None):
    """Draw an annotated arrow."""
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color=color,
                                lw=lw, connectionstyle="arc3,rad=0"))
    if label:
        mx, my = (x0+x1)/2, (y0+y1)/2
        ax.text(mx + 0.01, my, label, ha="left", va="center",
                color=GREY_M, fontsize=6.5, fontstyle="italic", zorder=5)


def _section_label(ax, x, y, w, h, text, fc=NAVY, tc=BLUE_LITE):
    """Draw a section background panel with a label."""
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0,rounding_size=0.012",
        facecolor=fc, edgecolor=BLUE_MID, linewidth=0.8,
        alpha=0.55, zorder=1
    )
    ax.add_patch(rect)
    ax.text(x + 0.012, y + h - 0.022, text,
            ha="left", va="top", color=tc,
            fontsize=7.5, fontweight="bold", zorder=2,
            alpha=0.85)


# ─────────────────────────────────────────────────────────────────────────────
# Diagram 1 — System Overview (11.2)
# ─────────────────────────────────────────────────────────────────────────────
def draw_system_overview(path: str, dpi: int = 180):
    fig, ax = plt.subplots(figsize=(13, 9))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ── Title ─────────────────────────────────────────────────────────────────
    ax.text(0.5, 0.965, "DeepGuard — Odysseus Engine System Architecture",
            ha="center", va="top", color=WHITE, fontsize=13, fontweight="bold")
    ax.text(0.5, 0.945, "Cloud-Agnostic · VPC-Native · Air-Gapped Ready · Powered by the Odysseus Engine",
            ha="center", va="top", color=BLUE_LITE, fontsize=8.5, fontstyle="italic")

    # ── Outer VPC boundary ───────────────────────────────────────────────────
    vpc = FancyBboxPatch((0.02, 0.03), 0.96, 0.88,
                         boxstyle="round,pad=0,rounding_size=0.018",
                         facecolor="#0A1929", edgecolor=BLUE_MID,
                         linewidth=1.5, linestyle="--", zorder=0)
    ax.add_patch(vpc)
    ax.text(0.05, 0.895, "Customer AWS VPC  /  AKS VNet  /  GKE VPC  /  Air-Gapped Kubernetes",
            ha="left", va="top", color=BLUE_LITE, fontsize=7.5,
            fontweight="bold", alpha=0.9)

    # ══════════════════════════════════════════════════════════════
    # ROW 1 — Ingestion sources  (y ≈ 0.82)
    # ══════════════════════════════════════════════════════════════
    _section_label(ax, 0.04, 0.72, 0.92, 0.14, "HERMES — INGESTION GATEWAY", fc="#0F2D4A")
    sources = [
        (0.15, "GitHub / GitLab\nBitbucket"),
        (0.35, "ZIP Upload\n(S3 Pre-signed)"),
        (0.55, "Terraform / CFN\nBicep / Pulumi"),
        (0.75, "Live Cloud API\nAWS · Azure · GCP"),
        (0.90, "Policy Doc\nPDF / YAML"),
    ]
    for sx, sl in sources:
        _box(ax, sx, 0.80, 0.14, 0.072, sl,
             fc="#133152", ec=TEAL, tc=WHITE, fontsize=7.2)

    # Arrow down to orchestration
    for sx, _ in sources:
        _arrow(ax, sx, 0.764, sx, 0.715, color=TEAL, lw=0.9)

    # ══════════════════════════════════════════════════════════════
    # ROW 2 — LangGraph Orchestration  (y ≈ 0.66)
    # ══════════════════════════════════════════════════════════════
    _section_label(ax, 0.04, 0.58, 0.92, 0.125, "ODYSSEUS ENGINE — LangGraph Orchestration Core", fc="#1A2744")
    _box(ax, 0.50, 0.655, 0.88, 0.058,
         "LangGraph State Machine  ·  DynamoDB Checkpointing  ·  Parallel Fan-out per ControlRequirement",
         fc=SLATE, ec=BLUE_MID, tc=BLUE_LITE, fontsize=7.8, bold=False)
    _arrow(ax, 0.50, 0.626, 0.50, 0.595, color=BLUE_LITE, lw=1.2)

    # ══════════════════════════════════════════════════════════════
    # ROW 3 — Agent layer  (y ≈ 0.50)
    # ══════════════════════════════════════════════════════════════
    _section_label(ax, 0.04, 0.40, 0.92, 0.185, "ODYSSEUS CREW — ANALYSIS AGENT GRAPH", fc="#1E2D40")
    agents = [
        (0.14, 0.52, "Hermes\nIngestion",    "#133152", TEAL),
        (0.30, 0.52, "Tiresias\nPolicy",      "#133152", BLUE_MID),
        (0.46, 0.52, "Argus\nCode Index",       "#133152", BLUE_MID),
        (0.62, 0.52, "Laocoon\nIaC Analyzer",       "#133152", ORANGE),
        (0.78, 0.52, "Cassandra\nCloud Config", "#133152", ORANGE),
    ]
    for ax_, ay_, al_, afc, aec in agents:
        _box(ax, ax_, ay_, 0.13, 0.072, al_, fc=afc, ec=aec, fontsize=7.5)

    # Converge arrows to Compliance Mapper
    for ax_, ay_, *_ in agents:
        _arrow(ax, ax_, ay_ - 0.036, ax_, 0.455, color=GREY_M, lw=0.8)

    _box(ax, 0.50, 0.44, 0.88, 0.056,
         "ATHENA — Policy Compliance Mapper  ·  RAG Retrieval + LLM Reasoning  ·  PASS / FAIL / PARTIAL per Control",
         fc=PURPLE, ec="#A855F7", tc=WHITE, fontsize=7.8, bold=False)
    _arrow(ax, 0.50, 0.412, 0.50, 0.388, color=PURPLE_L, lw=1.2)

    _box(ax, 0.50, 0.37, 0.88, 0.044,
         "CIRCE — Remediation Advisor  ·  Code Diffs  ·  IaC Patches  ·  CLI Remediation Commands",
         fc="#1C3830", ec=GREEN, tc=GREEN_L, fontsize=7.8)

    # ══════════════════════════════════════════════════════════════
    # ROW 4 — Report layer  (y ≈ 0.30)
    # ══════════════════════════════════════════════════════════════
    _arrow(ax, 0.50, 0.348, 0.50, 0.325, color=GREEN, lw=1.2)
    _section_label(ax, 0.04, 0.23, 0.92, 0.09, "REPORT LAYER", fc="#1A2D20")
    _box(ax, 0.34, 0.285, 0.26, 0.058,
         "Penelope\nReport Assembler",
         fc="#1C3830", ec=GREEN, tc=GREEN_L, fontsize=7.5)
    _arrow(ax, 0.47, 0.285, 0.56, 0.285, color=GREEN, lw=1.0)
    _box(ax, 0.69, 0.285, 0.24, 0.058,
         "PDF Generator\nReportLab · Jinja2",
         fc="#1C3830", ec=GREEN, tc=GREEN_L, fontsize=7.5)

    # ══════════════════════════════════════════════════════════════
    # BOTTOM — Provider Abstraction + LLM + Observability
    # ══════════════════════════════════════════════════════════════
    _section_label(ax, 0.04, 0.085, 0.60, 0.10, "PROVIDER ABSTRACTION LAYER", fc="#251D0A")
    providers = [
        (0.13, "Storage\nS3 / MinIO\nAzure Blob / GCS"),
        (0.29, "Calypso\nSecrets\nAWS SM · KV · Vault"),
        (0.46, "Eumaeus\nAuth\nCognito · Entra · IAP"),
        (0.62, "Aeolus\nQueue\nSQS · Bus · Pub/Sub"),
    ]
    for px, pl in providers:
        _box(ax, px, 0.128, 0.13, 0.058, pl,
             fc="#2D1F06", ec=ORANGE, tc=ORANGE_L, fontsize=6.5)

    _section_label(ax, 0.66, 0.085, 0.30, 0.10, "LLM INFERENCE LAYER", fc="#130E2A")
    _box(ax, 0.76, 0.108, 0.12, 0.052,
         "Bedrock\nClaude",
         fc="#1B1040", ec=PURPLE, tc=PURPLE_L, fontsize=6.5)
    _box(ax, 0.895, 0.108, 0.12, 0.052,
         "Open-Source\nOllama / vLLM",
         fc="#1B1040", ec=PURPLE, tc=PURPLE_L, fontsize=6.5)

    # Observability row
    obs_y = 0.046
    _box(ax, 0.22, obs_y, 0.18, 0.042,
         "LangSmith  (self-hosted)",
         fc="#1A1A2E", ec=BLUE_MID, tc=BLUE_LITE, fontsize=7)
    _box(ax, 0.50, obs_y, 0.18, 0.042,
         "LangFuse  (self-hosted)",
         fc="#1A1A2E", ec=BLUE_MID, tc=BLUE_LITE, fontsize=7)
    _box(ax, 0.78, obs_y, 0.28, 0.042,
         "OpenTelemetry → Grafana / Jaeger",
         fc="#1A1A2E", ec=BLUE_MID, tc=BLUE_LITE, fontsize=7)
    ax.text(0.05, obs_y + 0.005, "OBSERVABILITY", ha="left", va="center",
            color=GREY_M, fontsize=6.8, fontweight="bold")

    plt.tight_layout(pad=0)
    fig.savefig(path, dpi=dpi, bbox_inches="tight",
                facecolor=NAVY, edgecolor="none")
    plt.close(fig)
    print(f"Saved: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# Diagram 2 — LangGraph Agent Pipeline (11.3)
# ─────────────────────────────────────────────────────────────────────────────
def draw_agent_pipeline(path: str, dpi: int = 180):
    fig, ax = plt.subplots(figsize=(13, 10))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.972, "DeepGuard — Odysseus Engine: Agent Pipeline",
            ha="center", va="top", color=WHITE, fontsize=13, fontweight="bold")
    ax.text(0.5, 0.952, "Stateful multi-agent graph  ·  Parallel fan-out  ·  DynamoDB checkpointing  ·  Odysseus Crew",
            ha="center", va="top", color=BLUE_LITE, fontsize=8.5, fontstyle="italic")

    # ── Helper: vertical node with I/O callouts ───────────────────────────────
    def node(cx, cy, w, h, title, bullets,
             fc=SLATE, ec=BLUE_MID, tc=WHITE, btc=BLUE_LITE):
        _box(ax, cx, cy, w, h, title, fc=fc, ec=ec, tc=tc,
             fontsize=8.5, bold=True)
        for i, b in enumerate(bullets):
            bx = cx - w/2 + 0.012
            by = cy + h/2 - 0.028 - i * 0.026
            ax.text(bx, by, f"• {b}", ha="left", va="center",
                    color=btc, fontsize=6.5, zorder=5)

    # ── START ─────────────────────────────────────────────────────────────────
    _box(ax, 0.50, 0.915, 0.12, 0.036, "START",
         fc=GREEN, ec="#15803D", tc=WHITE, fontsize=8, bold=True)
    _arrow(ax, 0.50, 0.897, 0.50, 0.867)

    # ── Node 1: Ingestion ─────────────────────────────────────────────────────
    node(0.50, 0.820, 0.88, 0.082, "① Hermes — Ingestion Agent",
         ["Clone GitHub / GitLab repo or extract ZIP → object store",
          "Detect: languages, frameworks, entry points, dependency manifests",
          "IaC files: Terraform / CloudFormation / Bicep / Pulumi detected",
          "Live cloud: invoke CloudConnector for target provider (AWS / Azure / GCP)"],
         fc=SLATE, ec=TEAL, btc=BLUE_LITE)
    _arrow(ax, 0.50, 0.779, 0.50, 0.752)

    # ── Node 2: Policy Parser ──────────────────────────────────────────────────
    node(0.50, 0.713, 0.88, 0.072, "② Tiresias — Policy Parser",
         ["Parse compliance document: PDF · YAML · predefined framework selector",
          "Decompose into typed ControlRequirement[] with scope tags",
          "Scope tags: [code | iac | cloud_config | all]"],
         fc=SLATE, ec=BLUE_MID, btc=BLUE_LITE)
    _arrow(ax, 0.50, 0.677, 0.50, 0.648)

    # ── Node 3: Code Indexer ──────────────────────────────────────────────────
    node(0.50, 0.610, 0.88, 0.072, "③ Argus — Code Indexer",
         ["AST parsing via tree-sitter: Python · Java · TypeScript · Go · C# · PHP",
          "Dependency and data-flow graph extraction",
          "Semantic chunking → embeddings → pgvector index"],
         fc=SLATE, ec=BLUE_MID, btc=BLUE_LITE)
    _arrow(ax, 0.50, 0.574, 0.50, 0.548)

    # ── Fan-out label ─────────────────────────────────────────────────────────
    _box(ax, 0.50, 0.533, 0.88, 0.030,
         "Parallel Fan-out  ·  One sub-graph per ControlRequirement scope",
         fc="#1A2744", ec=GREY_D, tc=GREY_M, fontsize=7.5)

    # Fan-out arrows to three parallel agents
    fan_targets = [0.17, 0.50, 0.83]
    fan_labels  = ["code-scoped\ncontrols", "iac-scoped\ncontrols", "cloud-scoped\ncontrols"]
    fan_colors  = [BLUE_MID, ORANGE, GREEN]
    for tx, lbl, fc_ in zip(fan_targets, fan_labels, fan_colors):
        ax.annotate("", xy=(tx, 0.488), xytext=(0.50, 0.518),
                    arrowprops=dict(arrowstyle="->", color=fc_, lw=1.1,
                                   connectionstyle=f"arc3,rad=0"))
        ax.text(tx, 0.496, lbl, ha="center", va="top",
                color=fc_, fontsize=6.2, fontstyle="italic")

    # ── Three parallel nodes ──────────────────────────────────────────────────
    parallel_specs = [
        (0.17, ["RAG over source code\nvector index",
                "Semantic similarity\nsearch + rerank",
                "Returns: relevant\ncode snippets"], BLUE_MID),
        (0.50, ["Parse Terraform / CFN /\nBicep / Pulumi AST",
                "Check resource attrs\nvs policy controls",
                "Drift: IaC vs live state"], ORANGE),
        (0.83, ["CloudConnector\n.get_resources()",
                "Normalise to canonical\nResourceSnapshot schema",
                "AWS · Azure · GCP\nresource config"], GREEN),
    ]
    p_titles = ["④a Code Analyzer", "④b Laocoon — IaC", "④c Cassandra — Cloud"]
    p_colors = [BLUE_MID, ORANGE, GREEN]
    for (px, pbullets, pec), pt, pc in zip(parallel_specs, p_titles, p_colors):
        node(px, 0.426, 0.29, 0.10, pt, pbullets,
             fc=SLATE, ec=pec, btc=WHITE)

    # Converge arrows from three parallel nodes to mapper
    for px, pc in zip(fan_targets, fan_colors):
        ax.annotate("", xy=(0.50, 0.353), xytext=(px, 0.376),
                    arrowprops=dict(arrowstyle="->", color=pc, lw=1.1,
                                   connectionstyle="arc3,rad=0"))

    # ── Node 5: Compliance Mapper ─────────────────────────────────────────────
    node(0.50, 0.315, 0.88, 0.072, "⑤ Athena — Compliance Mapper",
         ["RAG retrieves evidence across all three layers for each ControlRequirement",
          "LLM reasons: PASS / FAIL / PARTIAL / NOT_APPLICABLE",
          "Cross-layer correlation: infra promise vs. code delivery gaps",
          "Generates Finding: evidence · severity · CVSS · reasoning chain"],
         fc=PURPLE, ec="#A855F7", tc=WHITE, btc=PURPLE_L)
    _arrow(ax, 0.50, 0.279, 0.50, 0.253, color=PURPLE_L)

    # ── Node 6: Remediation ───────────────────────────────────────────────────
    node(0.50, 0.215, 0.88, 0.072, "⑥ Circe — Remediation Advisor",
         ["Code diffs for source code findings",
          "IaC patches (Terraform / CloudFormation / Bicep) for infrastructure findings",
          "AWS CLI / Azure CLI / gcloud commands for live config findings"],
         fc="#1C3830", ec=GREEN, tc=GREEN_L, btc=GREEN_L)
    _arrow(ax, 0.50, 0.179, 0.50, 0.152, color=GREEN)

    # ── Node 7: Report ────────────────────────────────────────────────────────
    node(0.50, 0.115, 0.88, 0.072, "⑦ Penelope — Report Assembler  →  PDF",
         ["Structure findings by layer (code / IaC / cloud) and severity",
          "Generate cross-layer correlation insights and executive summary",
          "Render professional PDF (ReportLab + Jinja2) → S3 (KMS-encrypted) → notify"],
         fc="#1C3830", ec=GREEN, tc=GREEN_L, btc=GREEN_L)
    _arrow(ax, 0.50, 0.079, 0.50, 0.055, color=GREEN)

    # ── END ───────────────────────────────────────────────────────────────────
    _box(ax, 0.50, 0.040, 0.12, 0.030, "END",
         fc=RED, ec="#B91C1C", tc=WHITE, fontsize=8, bold=True)

    # ── Legend ────────────────────────────────────────────────────────────────
    legend_items = [
        mpatches.Patch(facecolor=SLATE,   edgecolor=TEAL,    label="Hermes (Ingestion)"),
        mpatches.Patch(facecolor=SLATE,   edgecolor=BLUE_MID,label="Tiresias / Argus (Parse / Index)"),
        mpatches.Patch(facecolor=PURPLE,  edgecolor="#A855F7",label="Athena (LLM Reasoning)"),
        mpatches.Patch(facecolor="#1C3830",edgecolor=GREEN,  label="Circe / Penelope (Remediate / Report)"),
        mpatches.Patch(facecolor=SLATE,   edgecolor=ORANGE,  label="Laocoon / Cassandra (IaC / Cloud)"),
    ]
    ax.legend(handles=legend_items, loc="lower right",
              facecolor="#0F2030", edgecolor=BLUE_MID,
              labelcolor=WHITE, fontsize=7, framealpha=0.85)

    plt.tight_layout(pad=0)
    fig.savefig(path, dpi=dpi, bbox_inches="tight",
                facecolor=NAVY, edgecolor="none")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    draw_system_overview("diagram_system_overview.png")
    draw_agent_pipeline("diagram_agent_pipeline.png")
