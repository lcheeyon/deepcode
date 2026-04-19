"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useCallback, useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { apiFetch, parseJson } from "@/lib/api-client";
import type { FindingListItem, FindingsPage } from "@/lib/api-types";
import { loadConnectionSettings } from "@/lib/connection-settings";

const SEVERITIES = ["", "CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"] as const;

function FindingsPageContent() {
  const router = useRouter();
  const sp = useSearchParams();
  const scanId = sp.get("scan_id")?.trim() ?? "";
  const cursor = sp.get("cursor")?.trim() ?? "";
  const severity = sp.get("severity") ?? "";
  const framework = sp.get("framework") ?? "";

  const [scanInput, setScanInput] = useState(scanId);
  const [data, setData] = useState<FindingsPage | null | "loading">("loading");
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<Set<string>>(() => new Set());
  const [detail, setDetail] = useState<FindingListItem | null>(null);

  const queryString = useMemo(() => {
    const p = new URLSearchParams();
    if (scanId) p.set("scan_id", scanId);
    if (cursor) p.set("cursor", cursor);
    if (severity) p.set("severity", severity);
    if (framework) p.set("framework", framework);
    return p.toString();
  }, [scanId, cursor, severity, framework]);

  const load = useCallback(async () => {
    if (!scanId) {
      setData(null);
      setError(null);
      return;
    }
    setData("loading");
    setError(null);
    const s = loadConnectionSettings();
    const q = new URLSearchParams();
    if (cursor) q.set("cursor", cursor);
    q.set("limit", "20");
    if (severity) q.set("severity", severity);
    if (framework) q.set("framework", framework);
    const qs = q.toString();
    const path = `/v1/scans/${encodeURIComponent(scanId)}/findings${qs ? `?${qs}` : ""}`;
    try {
      const res = await apiFetch(s, path, { method: "GET" });
      if (res.status === 404) {
        setError("Scan not found.");
        setData(null);
        return;
      }
      if (!res.ok) {
        setError(`Request failed (${res.status}).`);
        setData(null);
        return;
      }
      const body = await parseJson<FindingsPage>(res);
      setData(body);
    } catch {
      setError("Network error.");
      setData(null);
    }
  }, [scanId, cursor, severity, framework]);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    setScanInput(scanId);
  }, [scanId]);

  useEffect(() => {
    if (!data || data === "loading" || !data.items.length) return;
    setDetail((d) => {
      if (d && data.items.some((x) => x.finding_id === d.finding_id)) return d;
      return data.items[0] ?? null;
    });
  }, [data]);

  const pushFilters = (next: { cursor?: string; severity?: string; framework?: string }) => {
    const p = new URLSearchParams();
    if (scanId) p.set("scan_id", scanId);
    const c = next.cursor !== undefined ? next.cursor : cursor;
    if (c) p.set("cursor", c);
    const sev = next.severity !== undefined ? next.severity : severity;
    if (sev) p.set("severity", sev);
    const fw = next.framework !== undefined ? next.framework : framework;
    if (fw) p.set("framework", fw);
    router.replace(`/findings?${p.toString()}`);
  };

  const applyScanId = () => {
    const id = scanInput.trim();
    const p = new URLSearchParams();
    if (id) p.set("scan_id", id);
    router.replace(`/findings?${p.toString()}`);
  };

  const runExport = async (format: "csv" | "json") => {
    const s = loadConnectionSettings();
    const q = new URLSearchParams();
    q.set("format", format);
    if (severity) q.set("severity", severity);
    if (framework) q.set("framework", framework);
    if (selected.size) q.set("ids", Array.from(selected).join(","));
    const path = `/v1/scans/${encodeURIComponent(scanId)}/findings/export?${q.toString()}`;
    const res = await apiFetch(s, path, { method: "GET" });
    if (!res.ok) return;
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = format === "csv" ? "findings_v1.csv" : "findings_v1.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold tracking-tight">Findings</h1>
        <p className="mt-1 text-sm text-dg-text-muted">
          Triage findings for a scan. Cursor and filters are reflected in the URL.
        </p>
      </div>

      <Card className="space-y-3 p-4">
        <label className="block text-xs text-dg-text-muted" htmlFor="scan-id">
          Scan ID
        </label>
        <div className="flex flex-wrap gap-2">
          <input
            id="scan-id"
            className="min-w-[240px] flex-1 rounded-dg-sm border border-dg-border bg-dg-card px-3 py-2 font-mono text-sm"
            value={scanInput}
            onChange={(e) => setScanInput(e.target.value)}
            placeholder="uuid"
          />
          <Button type="button" variant="primary" onClick={applyScanId}>
            Load
          </Button>
          {scanId ? (
            <Link href={`/scans/${encodeURIComponent(scanId)}`}>
              <Button variant="secondary" type="button">
                Open scan
              </Button>
            </Link>
          ) : null}
        </div>
      </Card>

      {scanId ? (
        <Card className="space-y-3 p-4">
          <div className="flex flex-wrap gap-3">
            <div>
              <label className="text-xs text-dg-text-muted" htmlFor="sev">
                Severity
              </label>
              <select
                id="sev"
                className="mt-1 block w-full min-w-[140px] rounded-dg-sm border border-dg-border bg-dg-card px-2 py-1.5 text-sm"
                value={severity}
                onChange={(e) => pushFilters({ severity: e.target.value, cursor: "" })}
              >
                {SEVERITIES.map((s) => (
                  <option key={s || "all"} value={s}>
                    {s || "All"}
                  </option>
                ))}
              </select>
            </div>
            <div className="min-w-[180px] flex-1">
              <label className="text-xs text-dg-text-muted" htmlFor="fw">
                Framework contains
              </label>
              <input
                id="fw"
                className="mt-1 w-full rounded-dg-sm border border-dg-border bg-dg-card px-2 py-1.5 text-sm"
                value={framework}
                onChange={(e) => pushFilters({ framework: e.target.value, cursor: "" })}
                placeholder="e.g. ISO"
              />
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button type="button" variant="secondary" size="sm" onClick={() => runExport("csv")}>
              Export CSV
            </Button>
            <Button type="button" variant="secondary" size="sm" onClick={() => runExport("json")}>
              Export JSON
            </Button>
            <span className="self-center text-xs text-dg-text-muted">
              {selected.size ? `${selected.size} selected` : "All rows if none selected"}
            </span>
          </div>
          <p className="text-xs text-dg-text-muted">
            Query: <span className="font-mono">{queryString || "(defaults)"}</span>
          </p>
        </Card>
      ) : null}

      {error ? (
        <Card className="p-4 text-sm text-dg-warning">{error}</Card>
      ) : null}

      {scanId && data === "loading" ? (
        <div className="h-40 animate-pulse rounded-dg-md bg-dg-subtle" />
      ) : null}

      {scanId && data && data !== "loading" ? (
        <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.1fr)]">
          <Card className="overflow-hidden p-0">
            <div className="max-h-[520px] overflow-y-auto">
              <table className="w-full text-left text-sm">
                <thead className="sticky top-0 bg-dg-card text-xs text-dg-text-muted">
                  <tr>
                    <th className="w-8 px-2 py-2" />
                    <th className="px-2 py-2">Sev</th>
                    <th className="px-2 py-2">Control</th>
                    <th className="px-2 py-2">Title</th>
                  </tr>
                </thead>
                <tbody>
                  {data.items.map((row) => (
                    <tr
                      key={row.finding_id}
                      className={`cursor-pointer border-t border-dg-border hover:bg-dg-subtle/60 ${
                        detail?.finding_id === row.finding_id ? "bg-dg-subtle/80" : ""
                      }`}
                      onClick={() => setDetail(row)}
                    >
                      <td className="px-2 py-2">
                        <input
                          type="checkbox"
                          checked={selected.has(row.finding_id)}
                          onChange={(e) => {
                            e.stopPropagation();
                            setSelected((prev) => {
                              const n = new Set(prev);
                              if (e.target.checked) n.add(row.finding_id);
                              else n.delete(row.finding_id);
                              return n;
                            });
                          }}
                          aria-label={`Select ${row.finding_id}`}
                        />
                      </td>
                      <td className="px-2 py-2 font-medium">{row.severity}</td>
                      <td className="px-2 py-2 font-mono text-xs">{row.control_id}</td>
                      <td className="px-2 py-2 text-dg-text-muted">{row.title}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="flex flex-wrap gap-2 border-t border-dg-border p-3">
              <Button
                type="button"
                variant="ghost"
                size="sm"
                disabled={!data.next_cursor}
                onClick={() => pushFilters({ cursor: data.next_cursor ?? "" })}
              >
                Next page
              </Button>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                disabled={!cursor}
                onClick={() => pushFilters({ cursor: "" })}
              >
                First page
              </Button>
            </div>
          </Card>

          <Card className="space-y-3 p-4">
            {detail ? (
              <>
                <h2 className="text-base font-semibold">{detail.title}</h2>
                <p className="text-sm text-dg-text-muted">
                  {detail.framework} · {detail.control_id} · status {detail.status} · confidence{" "}
                  {detail.confidence_score}
                </p>
                {detail.reasoning_summary ? (
                  <p className="text-sm">{detail.reasoning_summary}</p>
                ) : null}
                <div>
                  <h3 className="mb-1 text-xs font-medium uppercase text-dg-text-muted">
                    Evidence (read-only)
                  </h3>
                  <pre className="max-h-64 overflow-auto rounded-dg-sm bg-dg-subtle p-3 font-mono text-[12px]">
                    {JSON.stringify(detail.evidence_refs, null, 2)}
                  </pre>
                </div>
              </>
            ) : (
              <p className="text-sm text-dg-text-muted">Select a finding.</p>
            )}
          </Card>
        </div>
      ) : null}

      {!scanId ? (
        <Card className="p-4 text-sm text-dg-text-muted">
          Enter a scan UUID to load findings. Open a scan from{" "}
          <Link href="/scans" className="text-dg-brand underline">
            Scans
          </Link>{" "}
          and paste its id here.
        </Card>
      ) : null}
    </div>
  );
}

export default function FindingsPage() {
  return (
    <Suspense
      fallback={<div className="h-40 animate-pulse rounded-dg-md bg-dg-subtle" />}
    >
      <FindingsPageContent />
    </Suspense>
  );
}
