"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { loadConnectionSettings } from "@/lib/connection-settings";
import { upsertRecentScan } from "@/lib/recent-scans";
import { apiFetch, parseJson } from "@/lib/api-client";
import type { ScanResponse } from "@/lib/api-types";
import { useToast } from "@/components/toast-context";
import { ScanStatusBadge } from "@/components/scan-status-badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Modal } from "@/components/ui/modal";

export default function ScanDetailPage() {
  const params = useParams();
  const scanId = typeof params.id === "string" ? params.id : "";
  const { push } = useToast();
  const [scan, setScan] = useState<ScanResponse | null | "loading">("loading");
  const [expanded, setExpanded] = useState(false);
  const [cancelOpen, setCancelOpen] = useState(false);
  const [cancelling, setCancelling] = useState(false);

  const load = useCallback(async () => {
    if (!scanId) return;
    const s = loadConnectionSettings();
    try {
      const res = await apiFetch(s, `/v1/scans/${scanId}`, { method: "GET" });
      if (res.status === 404) {
        setScan(null);
        return;
      }
      if (!res.ok) {
        setScan(null);
        return;
      }
      const body = await parseJson<ScanResponse>(res);
      setScan(body);
      upsertRecentScan({
        scan_id: body.scan_id,
        updated_at: body.updated_at,
        status: body.status,
      });
    } catch {
      setScan(null);
    }
  }, [scanId]);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    if (!scanId) return;
    const id = window.setInterval(() => {
      if (document.visibilityState === "hidden") return;
      void load();
    }, 5000);
    return () => window.clearInterval(id);
  }, [scanId, load]);

  const doCancel = async () => {
    const s = loadConnectionSettings();
    setCancelling(true);
    try {
      const res = await apiFetch(s, `/v1/scans/${scanId}/cancel`, { method: "POST" });
      if (res.status === 202) {
        push({
          kind: "success",
          title: "Cancellation requested",
          body: "The worker will stop when safe.",
        });
        setCancelOpen(false);
        await load();
        return;
      }
      if (res.status === 404) {
        const body = await parseJson<{ detail?: string }>(res);
        push({
          kind: "error",
          title: "Scan not found",
          body: typeof body.detail === "string" ? body.detail : "404",
        });
        return;
      }
      push({
        kind: "error",
        title: "Something went wrong",
        body: `HTTP ${res.status}`,
      });
    } catch {
      push({ kind: "error", title: "Something went wrong", body: "Network error." });
    } finally {
      setCancelling(false);
    }
  };

  if (scan === "loading") {
    return (
      <div className="space-y-4">
        <div className="h-8 w-48 animate-pulse rounded-dg-sm bg-dg-subtle" />
        <div className="h-40 animate-pulse rounded-dg-md bg-dg-subtle" />
      </div>
    );
  }

  if (scan === null) {
    return (
      <Card>
        <h1 className="mb-2 text-lg font-semibold">Scan not found</h1>
        <p className="mb-4 text-sm text-dg-text-muted">
          No scan exists for this ID, or you do not have access.
        </p>
        <Link href="/scans">
          <Button variant="primary">Back to scans</Button>
        </Link>
      </Card>
    );
  }

  const jsonStr = JSON.stringify(scan.job_config, null, 2);

  return (
    <div>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <h1 className="font-mono text-lg font-semibold tracking-tight">
          Scan {scan.scan_id}
        </h1>
        <Button variant="secondary" size="sm" type="button" onClick={() => void load()}>
          Refresh
        </Button>
      </div>

      <Card className="mb-6">
        <div className="mb-4 flex flex-wrap items-center gap-4">
          <ScanStatusBadge status={scan.status} />
          <span className="text-sm text-dg-text-muted">Stage {scan.current_stage}</span>
          <span className="font-tabular text-sm font-medium">
            {scan.percent_complete}%
          </span>
        </div>
        {scan.repo_commit_sha ? (
          <p className="font-mono text-[13px] text-dg-text-muted">
            Repo commit {scan.repo_commit_sha}
          </p>
        ) : null}
        {scan.cancellation_requested ? (
          <p className="mt-2 text-sm text-dg-warning">Cancellation requested.</p>
        ) : null}
      </Card>

      <Card className="mb-6">
        <div className="mb-2 flex items-center justify-between">
          <h2 className="text-base font-semibold">job_config</h2>
          <Button
            variant="ghost"
            size="sm"
            type="button"
            aria-expanded={expanded}
            onClick={() => setExpanded((e) => !e)}
          >
            {expanded ? "Collapse" : "Expand"}
          </Button>
        </div>
        <pre
          className={`overflow-x-auto rounded-dg-sm bg-dg-subtle p-3 font-mono text-[13px] text-dg-text-primary ${
            expanded ? "max-h-[480px]" : "max-h-32"
          }`}
        >
          {jsonStr}
        </pre>
      </Card>

      <Button variant="destructive" type="button" onClick={() => setCancelOpen(true)}>
        Request cancel
      </Button>

      <Modal
        open={cancelOpen}
        title="Cancel scan?"
        onClose={() => setCancelOpen(false)}
        footer={
          <>
            <Button variant="secondary" onClick={() => setCancelOpen(false)}>
              Keep scan
            </Button>
            <Button variant="destructive" onClick={doCancel} disabled={cancelling}>
              {cancelling ? "Sending…" : "Request cancel"}
            </Button>
          </>
        }
      >
        <p className="text-sm text-dg-text-muted">
          This requests cooperative cancel. Running work may stop soon.
        </p>
      </Modal>
    </div>
  );
}
