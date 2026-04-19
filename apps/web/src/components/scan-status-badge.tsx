"use client";

const STATUS_TOKENS: Record<string, { bg: string; fg: string; dot: string }> = {
  PENDING: { bg: "bg-dg-subtle", fg: "text-dg-text-muted", dot: "bg-dg-text-muted" },
  QUEUED: { bg: "bg-dg-info-bg", fg: "text-dg-info", dot: "bg-dg-info" },
  INGESTING: { bg: "bg-dg-info-bg", fg: "text-dg-info", dot: "bg-dg-info" },
  INDEXING: { bg: "bg-dg-info-bg", fg: "text-dg-info", dot: "bg-dg-info" },
  ANALYZING: { bg: "bg-dg-warning-bg", fg: "text-dg-warning", dot: "bg-dg-warning" },
  MAPPING: { bg: "bg-dg-warning-bg", fg: "text-dg-warning", dot: "bg-dg-warning" },
  REMEDIATING: { bg: "bg-dg-warning-bg", fg: "text-dg-warning", dot: "bg-dg-warning" },
  REPORTING: { bg: "bg-dg-warning-bg", fg: "text-dg-warning", dot: "bg-dg-warning" },
  COMPLETE: { bg: "bg-dg-success-bg", fg: "text-dg-success", dot: "bg-dg-success" },
  FAILED: { bg: "bg-dg-error-bg", fg: "text-dg-error", dot: "bg-dg-error" },
  CANCELLED: { bg: "bg-dg-subtle", fg: "text-dg-text-muted", dot: "bg-dg-text-muted" },
  AWAITING_REVIEW: {
    bg: "bg-dg-warning-bg",
    fg: "text-dg-warning",
    dot: "bg-dg-warning",
  },
};

export function ScanStatusBadge({ status }: { status: string }) {
  const t = STATUS_TOKENS[status] ?? STATUS_TOKENS.PENDING;
  return (
    <span
      className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${t.bg} ${t.fg}`}
    >
      <span
        className={`h-2 w-2 shrink-0 rounded-full ${t.dot}`}
        aria-hidden
      />
      {status}
    </span>
  );
}
