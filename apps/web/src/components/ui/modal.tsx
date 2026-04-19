"use client";

import { useEffect, useRef, type ReactNode } from "react";
import { Button } from "./button";

export function Modal({
  open,
  title,
  children,
  onClose,
  footer,
}: {
  open: boolean;
  title: string;
  children: ReactNode;
  onClose: () => void;
  footer?: ReactNode;
}) {
  const ref = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (open) {
      if (!el.open) el.showModal();
    } else if (el.open) {
      el.close();
    }
  }, [open]);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const onCancel = (e: Event) => {
      e.preventDefault();
      onClose();
    };
    el.addEventListener("cancel", onCancel);
    return () => el.removeEventListener("cancel", onCancel);
  }, [onClose]);

  return (
    <dialog
      ref={ref}
      className="z-modal w-full max-w-form rounded-dg-lg border border-dg-border bg-dg-card p-0 text-dg-text-primary shadow-dg-lg backdrop:bg-black/40"
      aria-labelledby="modal-title"
    >
      <div className="border-b border-dg-border px-6 py-4">
        <h2 id="modal-title" className="text-lg font-semibold tracking-tight">
          {title}
        </h2>
      </div>
      <div className="max-h-[70vh] overflow-y-auto px-6 py-4">{children}</div>
      {footer ? (
        <div className="flex justify-end gap-2 border-t border-dg-border px-6 py-4">
          {footer}
        </div>
      ) : (
        <div className="flex justify-end border-t border-dg-border px-6 py-4">
          <Button variant="secondary" onClick={onClose}>
            Close
          </Button>
        </div>
      )}
    </dialog>
  );
}
