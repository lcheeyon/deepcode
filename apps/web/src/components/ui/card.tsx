"use client";

import type { ReactNode } from "react";

export function Card({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`rounded-dg-md border border-dg-border bg-dg-card p-6 shadow-dg-sm ${className}`}
    >
      {children}
    </div>
  );
}
