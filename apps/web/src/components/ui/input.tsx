"use client";

import type { InputHTMLAttributes } from "react";

export function Input({
  className = "",
  ...props
}: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={`w-full rounded-dg-sm border border-dg-border bg-dg-card px-3 py-2 text-sm text-dg-text-primary placeholder:text-dg-text-muted focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-dg-brand ${className}`}
      {...props}
    />
  );
}
