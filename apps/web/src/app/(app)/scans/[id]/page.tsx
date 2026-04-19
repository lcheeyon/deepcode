"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { loadConnectionSettings } from "@/lib/connection-settings";
import { upsertRecentScan } from "@/lib/recent-scans";
import { apiFetch, parseJson } from "@/lib/api-client";
import type { ArtifactsListResponse, ScanResponse, ScanWorkflowResponse } from "@/lib/api-types";
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
  const [artifacts, setArtifacts] = useState<ArtifactsListResponse["artifacts"] | null>(null);
  const [workflow, setWorkflow] = useState<ScanWorkflowResponse | null>(null);

  const load = useCallback(async () => {
    if (!scanId) return;
    const s = loadConnectionSettings();
    try {
      const res = await apiFetch(s, `/v1/scans/${scanId}`, { method: "GET" });
      if (res.status === 404) {
        setScan(null);
        setWorkflow(null);
        return;
      }
      if (!res.ok) {
        setScan(null);
        setWorkflow(null);
        return;
      }
      const body = await parseJson<ScanResponse>(res);
      setScan(body);
      upsertRecentScan({
        scan_id: body.scan_id,
        updated_at: body.updated_at,
        status: body.status,
      });
      if (body.status === "COMPLETE") {
        const ar = await apiFetch(s, `/v1/scans/${scanId}/artifacts`, { method: "GET" });
        if (ar.ok) {
          const aj = await parseJson<ArtifactsListResponse>(ar);
          setArtifacts(aj.artifacts ?? []);
        } else {
          setArtifacts(null);
        }
      } else {
        setArtifacts(null);
      }
      const wf = await apiFetch(s, `/v1/scans/${scanId}/workflow?include_events=true`, {
        method: "GET",
      });
      if (wf.ok) {
        setWorkflow(await parseJson<ScanWorkflowResponse>(wf));
      } else {
        setWorkflow(null);
      }
    } catch {
      setScan(null);
      setWorkflow(null);
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

      {scan.status === "COMPLETE" ? (
        <Card className="mb-6">
          <h2 className="mb-3 text-base font-semibold">Triage & reports</h2>
          <div className="flex flex-wrap gap-2">
            <Link href={`/findings?scan_id=${encodeURIComponent(scan.scan_id)}`}>
              <Button variant="secondary" size="sm" type="button">
                Open findings
              </Button>
            </Link>
            <Link href={`/reports?scan_id=${encodeURIComponent(scan.scan_id)}`}>
              <Button variant="secondary" size="sm" type="button">
                Open reports
              </Button>
            </Link>
          </div>
          {artifacts && artifacts.length ? (
            <p className="mt-3 text-xs text-dg-text-muted">
              Latest PDF checksum:{" "}
              <span className="font-mono">{artifacts[0]?.checksum_sha256.slice(0, 16)}…</span>
            </p>
          ) : null}
        </Card>
      ) : null}

      {workflow ? (
        <Card className="mb-6">
          <h2 className="mb-3 text-base font-semibold">Workflow (first-party)</h2>
          {workflow.correlation_id ? (
            <p className="mb-2 font-mono text-xs text-dg-text-muted">
              Correlation {workflow.correlation_id}
            </p>
          ) : null}
          <div className="mb-4 flex flex-wrap gap-2">
            {workflow.checklist.map((c) => (
              <span
                key={c.node}
                className="rounded-dg-sm border border-dg-border-subtle px-2 py-1 font-mono text-xs"
              >
                {c.node}: {c.state}
              </span>
            ))}
          </div>
          {workflow.handoffs.length ? (
            <div className="mb-3">
              <h3 className="mb-1 text-sm font-medium text-dg-text-muted">Handoffs</h3>
              <ul className="list-inside list-disc text-sm">
                {workflow.handoffs.slice(0, 12).map((h, i) => (
                  <li key={i} className="font-mono text-xs">
                    {h.from_agent} → {h.to_agent} ({h.message_type})
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
          {workflow.trace_links.some((t) => t.url) ? (
            <div className="mb-3 flex flex-wrap gap-2">
              {workflow.trace_links
                .filter((t) => t.url)
                .map((t) => (
                  <a
                    key={t.vendor}
                    href={t.url!}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-dg-brand-primary underline"
                  >
                    Open {t.vendor} trace
                  </a>
                ))}
            </div>
          ) : null}
          {workflow.events.length ? (
            <div>
              <h3 className="mb-1 text-sm font-medium text-dg-text-muted">Recent events</h3>
              <ul className="max-h-40 space-y-1 overflow-y-auto font-mono text-[11px] text-dg-text-muted">
                {workflow.events.slice(-12).map((e) => (
                  <li key={e.id}>
                    #{e.event_seq} {e.event_type}
                    {e.node ? ` ${e.node}` : ""}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </Card>
      ) : null}

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
