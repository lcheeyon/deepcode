"use client";

import { useToast } from "./toast-context";

const kindStyles: Record<string, string> = {
  success: "bg-dg-success-bg text-dg-success border-dg-success/30",
  error: "bg-dg-error-bg text-dg-error border-dg-error/30",
  warning: "bg-dg-warning-bg text-dg-warning border-dg-warning/30",
  info: "bg-dg-info-bg text-dg-info border-dg-info/30",
};

export function ToastRegion() {
  const { toasts, dismiss } = useToast();

  return (
    <div
      className="pointer-events-none fixed bottom-4 right-4 z-[80] flex max-w-sm flex-col gap-2"
      aria-live="polite"
    >
      {toasts.map((t) => (
        <div
          key={t.id}
          role={t.kind === "error" ? "alert" : "status"}
          className={`pointer-events-auto rounded-dg-md border px-4 py-3 shadow-dg-md ${kindStyles[t.kind] ?? kindStyles.info}`}
        >
          <div className="flex items-start justify-between gap-2">
            <div>
              <p className="text-sm font-semibold">{t.title}</p>
              {t.body ? (
                <p className="mt-1 text-xs opacity-90">{t.body}</p>
              ) : null}
            </div>
            <button
              type="button"
              onClick={() => dismiss(t.id)}
              className="min-h-[24px] min-w-[24px] rounded-dg-sm text-xs underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-dg-brand"
              aria-label="Dismiss notification"
            >
              ×
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
