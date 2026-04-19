"use client";

import type { ReactNode } from "react";
import { ThemeProvider } from "./theme-context";
import { ToastProvider } from "./toast-context";
import { ToastRegion } from "./toast-region";

export function Providers({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      <ToastProvider>
        {children}
        <ToastRegion />
      </ToastProvider>
    </ThemeProvider>
  );
}
