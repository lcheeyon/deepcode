"use client";

import { STORAGE_CONNECTION } from "./storage-keys";

export type AuthKind = "api-key" | "bearer";

export interface ConnectionSettings {
  baseUrl: string;
  apiKey: string;
  authKind: AuthKind;
  lastHealthOkAt?: string;
  lastHealthLatencyMs?: number;
}

const defaultSettings = (): ConnectionSettings => ({
  baseUrl: "http://127.0.0.1:8000",
  apiKey: "",
  authKind: "api-key",
});

export function loadConnectionSettings(): ConnectionSettings {
  if (typeof window === "undefined") return defaultSettings();
  try {
    const raw = localStorage.getItem(STORAGE_CONNECTION);
    if (!raw) return defaultSettings();
    const p = JSON.parse(raw) as Partial<ConnectionSettings>;
    return {
      ...defaultSettings(),
      ...p,
      authKind: p.authKind === "bearer" ? "bearer" : "api-key",
    };
  } catch {
    return defaultSettings();
  }
}

export function saveConnectionSettings(s: ConnectionSettings): void {
  localStorage.setItem(STORAGE_CONNECTION, JSON.stringify(s));
}
