"use client";

import { STORAGE_RECENT_SCANS } from "./storage-keys";

export const RECENT_SCANS_MAX = 50;

export interface RecentScanEntry {
  scan_id: string;
  updated_at: string;
  status?: string;
  label?: string;
}

function parse(raw: string | null): RecentScanEntry[] {
  if (!raw) return [];
  try {
    const arr = JSON.parse(raw) as unknown;
    if (!Array.isArray(arr)) return [];
    return arr
      .filter(
        (x): x is RecentScanEntry =>
          typeof x === "object" &&
          x !== null &&
          typeof (x as RecentScanEntry).scan_id === "string" &&
          typeof (x as RecentScanEntry).updated_at === "string"
      )
      .slice(0, RECENT_SCANS_MAX);
  } catch {
    return [];
  }
}

export function loadRecentScans(): RecentScanEntry[] {
  if (typeof window === "undefined") return [];
  return parse(localStorage.getItem(STORAGE_RECENT_SCANS));
}

export function saveRecentScans(entries: RecentScanEntry[]): void {
  localStorage.setItem(
    STORAGE_RECENT_SCANS,
    JSON.stringify(entries.slice(0, RECENT_SCANS_MAX))
  );
}

export function upsertRecentScan(entry: RecentScanEntry): void {
  const cur = loadRecentScans().filter((e) => e.scan_id !== entry.scan_id);
  cur.unshift(entry);
  saveRecentScans(cur);
}

export function clearRecentScans(): void {
  localStorage.removeItem(STORAGE_RECENT_SCANS);
}
