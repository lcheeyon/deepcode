"use client";

import { useCallback, useState } from "react";
import { loadConnectionSettings } from "@/lib/connection-settings";
import { fetchHealthz } from "@/lib/health";
import { useToast } from "@/components/toast-context";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function DashboardPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(false);
  const [last, setLast] = useState<{
    ok: boolean;
    ms: number;
    at: string;
  } | null>(null);
  const refresh = useCallback(async () => {
    const s = loadConnectionSettings();
    setLoading(true);
    try {
      const r = await fetchHealthz(s.baseUrl);
      const at = new Date().toLocaleTimeString();
      setLast({ ok: r.ok, ms: r.ms, at });
      if (!r.ok) {
        const msg = `Health check failed (${r.status}).`;
        push({
          kind: "error",
          title: "Control plane unreachable",
          body: msg,
          sticky: true,
        });
      }
    } catch {
      const msg = "Network error calling health endpoint.";
      push({
        kind: "error",
        title: "Something went wrong",
        body: msg,
        sticky: true,
      });
      setLast(null);
    } finally {
      setLoading(false);
    }
  }, [push]);

  return (
    <div>
      <h1 className="mb-6 text-[22px] font-semibold tracking-tight">Dashboard</h1>
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-base font-semibold">Control plane</h2>
            <Button variant="secondary" size="sm" onClick={refresh} disabled={loading}>
              {loading ? "Loading…" : "Refresh"}
            </Button>
          </div>
          {loading && !last ? (
            <div className="h-16 animate-pulse rounded-dg-sm bg-dg-subtle" aria-hidden />
          ) : last ? (
            <div className="space-y-2 text-sm">
              <p className="flex items-center gap-2">
                <span
                  className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-semibold ${
                    last.ok
                      ? "bg-dg-success-bg text-dg-success"
                      : "bg-dg-error-bg text-dg-error"
                  }`}
                >
                  <span
                    className={`h-2 w-2 rounded-full ${last.ok ? "bg-dg-success" : "bg-dg-error"}`}
                  />
                  {last.ok ? "OK" : "Error"}
                </span>
                <span className="text-dg-text-muted">
                  GET /v1/healthz — {last.ms} ms — {last.at}
                </span>
              </p>
            </div>
          ) : (
            <p className="text-sm text-dg-text-muted">Press Refresh to probe the API.</p>
          )}
        </Card>
        <Card>
          <h2 className="mb-2 text-base font-semibold">Background jobs</h2>
          <p className="text-sm text-dg-text-muted">
            When Redis is configured alongside Postgres, new scans enqueue to the
            worker stream after <code className="text-xs">POST /v1/scans</code>.
          </p>
          <p className="mt-2 text-xs text-dg-text-muted">
            See <code>.env.example</code> for <code>REDIS_URL</code>.
          </p>
        </Card>
      </div>
    </div>
  );
}
