"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useToast } from "@/components/toast-context";
import { apiFetch, parseJson } from "@/lib/api-client";
import type { ArtifactsListResponse, ArtifactSummary } from "@/lib/api-types";
import { loadConnectionSettings } from "@/lib/connection-settings";
import { loadRecentScans } from "@/lib/recent-scans";

function ReportsPageContent() {
  const router = useRouter();
  const sp = useSearchParams();
  const scanId = sp.get("scan_id")?.trim() ?? "";
  const { push } = useToast();
  const [scanInput, setScanInput] = useState(scanId);
  const [artifacts, setArtifacts] = useState<ArtifactSummary[] | null | "loading">("loading");
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!scanId) {
      setArtifacts(null);
      setError(null);
      return;
    }
    setArtifacts("loading");
    setError(null);
    const s = loadConnectionSettings();
    try {
      const res = await apiFetch(s, `/v1/scans/${encodeURIComponent(scanId)}/artifacts`, {
        method: "GET",
      });
      if (res.status === 404) {
        setError("Scan not found.");
        setArtifacts(null);
        return;
      }
      if (!res.ok) {
        setError(`Request failed (${res.status}).`);
        setArtifacts(null);
        return;
      }
      const body = await parseJson<ArtifactsListResponse>(res);
      setArtifacts(body.artifacts);
    } catch {
      setError("Network error.");
      setArtifacts(null);
    }
  }, [scanId]);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    setScanInput(scanId);
  }, [scanId]);

  const applyScan = () => {
    const id = scanInput.trim();
    const p = id ? `?scan_id=${encodeURIComponent(id)}` : "";
    router.replace(`/reports${p}`);
  };

  const copyChecksum = async (hex: string) => {
    try {
      await navigator.clipboard.writeText(hex);
      push({ kind: "success", title: "Copied", body: "Checksum copied to clipboard." });
    } catch {
      push({ kind: "error", title: "Copy failed", body: "Could not access clipboard." });
    }
  };

  const downloadPdf = async (artifactId: string) => {
    const s = loadConnectionSettings();
    const path = `/v1/scans/${encodeURIComponent(scanId)}/artifacts/${encodeURIComponent(artifactId)}`;
    try {
      const res = await apiFetch(s, path, { method: "GET", redirect: "follow" });
      if (!res.ok) {
        push({
          kind: "error",
          title: "Download failed",
          body: `HTTP ${res.status}`,
        });
        return;
      }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "report.pdf";
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      push({ kind: "error", title: "Download failed", body: "Network error." });
    }
  };

  const recent = loadRecentScans().slice(0, 8);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold tracking-tight">Reports</h1>
        <p className="mt-1 text-sm text-dg-text-muted">
          Completed scans expose PDF artifacts with checksum metadata. Download follows redirects
          when storage is presigned.
        </p>
      </div>

      <Card className="space-y-3 p-4">
        <label className="block text-xs text-dg-text-muted" htmlFor="rep-scan">
          Scan ID
        </label>
        <div className="flex flex-wrap gap-2">
          <input
            id="rep-scan"
            className="min-w-[240px] flex-1 rounded-dg-sm border border-dg-border bg-dg-card px-3 py-2 font-mono text-sm"
            value={scanInput}
            onChange={(e) => setScanInput(e.target.value)}
            placeholder="uuid"
          />
          <Button type="button" variant="primary" onClick={applyScan}>
            Load
          </Button>
        </div>
        {recent.length ? (
          <div className="text-xs text-dg-text-muted">
            Recent:{" "}
            {recent.map((e) => (
              <button
                key={e.scan_id}
                type="button"
                className="mr-2 font-mono text-dg-brand underline"
                onClick={() => {
                  setScanInput(e.scan_id);
                  router.replace(`/reports?scan_id=${encodeURIComponent(e.scan_id)}`);
                }}
              >
                {e.scan_id.slice(0, 8)}…
              </button>
            ))}
          </div>
        ) : null}
      </Card>

      {error ? <Card className="p-4 text-sm text-dg-warning">{error}</Card> : null}

      {scanId && artifacts === "loading" ? (
        <div className="h-32 animate-pulse rounded-dg-md bg-dg-subtle" />
      ) : null}

      {scanId && artifacts && artifacts !== "loading" ? (
        <div className="space-y-4">
          {artifacts.length === 0 ? (
            <Card className="p-4 text-sm text-dg-text-muted">
              No artifacts for this scan yet. Reports appear when the scan completes.
            </Card>
          ) : null}
          {artifacts.map((a) => (
            <Card key={a.artifact_id} className="space-y-3 p-4">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 className="text-base font-semibold">
                    {a.kind === "report_pdf" ? "Scan report (PDF)" : a.kind}
                  </h2>
                  <p className="mt-1 font-mono text-xs text-dg-text-muted">
                    Artifact {a.artifact_id}
                  </p>
                </div>
                <Link href={`/scans/${encodeURIComponent(scanId)}`}>
                  <Button variant="ghost" size="sm" type="button">
                    Scan detail
                  </Button>
                </Link>
              </div>
              <p className="text-sm">
                <span className="text-dg-text-muted">SHA-256:</span>{" "}
                <span className="font-mono text-[13px]">{a.checksum_sha256}</span>
              </p>
              <p className="text-sm text-dg-text-muted">
                Generated {new Date(a.created_at).toISOString()} · {a.size_bytes} bytes
              </p>
              <div className="flex flex-wrap gap-2">
                <Button type="button" variant="primary" onClick={() => void downloadPdf(a.artifact_id)}>
                  Download
                </Button>
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => void copyChecksum(a.checksum_sha256)}
                >
                  Copy checksum
                </Button>
              </div>
            </Card>
          ))}
        </div>
      ) : null}

      {!scanId ? (
        <Card className="p-4 text-sm text-dg-text-muted">
          Choose a completed scan. You can open{" "}
          <Link href="/scans" className="text-dg-brand underline">
            Scans
          </Link>{" "}
          and use the report shortcut from detail when available.
        </Card>
      ) : null}
    </div>
  );
}

export default function ReportsPage() {
  return (
    <Suspense
      fallback={<div className="h-40 animate-pulse rounded-dg-md bg-dg-subtle" />}
    >
      <ReportsPageContent />
    </Suspense>
  );
}
