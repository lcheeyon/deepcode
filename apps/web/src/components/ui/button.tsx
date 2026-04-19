"use client";

import type { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "primary" | "secondary" | "ghost" | "destructive";

const variants: Record<Variant, string> = {
  primary:
    "bg-dg-brand text-dg-inverse hover:bg-dg-brand-hover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-dg-brand disabled:opacity-50",
  secondary:
    "border border-dg-border bg-dg-card text-dg-text-primary hover:bg-dg-subtle focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-dg-brand disabled:opacity-50",
  ghost:
    "text-dg-text-primary hover:bg-dg-subtle focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-dg-brand disabled:opacity-50",
  destructive:
    "bg-dg-error text-dg-inverse hover:opacity-90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-dg-error disabled:opacity-50",
};

export function Button({
  variant = "secondary",
  size = "md",
  className = "",
  children,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: Variant;
  size?: "sm" | "md";
  children: ReactNode;
}) {
  const sz =
    size === "sm" ? "min-h-8 px-3 text-sm" : "min-h-10 px-4 text-sm font-medium";
  return (
    <button
      type="button"
      className={`inline-flex items-center justify-center rounded-dg-md transition ${variants[variant]} ${sz} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
