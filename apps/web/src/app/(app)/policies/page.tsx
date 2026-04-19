"use client";

import { useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { apiFetch, parseJson } from "@/lib/api-client";
import type { PolicyUploadListResponse, PolicyUploadResponse } from "@/lib/api-types";
import { loadConnectionSettings } from "@/lib/connection-settings";

export default function PoliciesPage() {
  const [list, setList] = useState<PolicyUploadListResponse["uploads"]>([]);
  const [loading, setLoading] = useState(true);
  const [last, setLast] = useState<PolicyUploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const refresh = useCallback(async () => {
    const s = loadConnectionSettings();
    setLoading(true);
    try {
      const res = await apiFetch(s, "/v1/policies", { method: "GET" });
      if (!res.ok) {
        setError(`List failed (${res.status}).`);
        setList([]);
        return;
      }
      const body = await parseJson<PolicyUploadListResponse>(res);
      setList(body.uploads);
      setError(null);
    } catch {
      setError("Network error.");
      setList([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const onUpload = async (file: File | null) => {
    if (!file) return;
    setBusy(true);
    setError(null);
    const s = loadConnectionSettings();
    const fd = new FormData();
    fd.set("file", file);
    try {
      const res = await apiFetch(s, "/v1/policies:upload", { method: "POST", body: fd });
      const text = await res.text();
      if (!res.ok) {
        let msg = text.slice(0, 500);
        try {
          const j = JSON.parse(text) as { detail?: unknown };
          if (typeof j.detail === "string") msg = j.detail;
        } catch {
          /* ignore */
        }
        setError(msg);
        return;
      }
      const body = JSON.parse(text) as PolicyUploadResponse;
      setLast(body);
      await refresh();
    } catch {
      setError("Network error.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold tracking-tight">Policies</h1>
        <p className="mt-1 text-sm text-dg-text-muted">
          Upload DeepGuard YAML policy fixtures. Parse summary is returned immediately.
        </p>
      </div>

      <Card className="space-y-3 p-4">
        <label className="text-sm font-medium" htmlFor="policy-file">
          Upload YAML
        </label>
        <input
          id="policy-file"
          type="file"
          accept=".yaml,.yml"
          className="block w-full text-sm"
          disabled={busy}
          onChange={(e) => void onUpload(e.target.files?.[0] ?? null)}
        />
        <p className="text-xs text-dg-text-muted">Endpoint: POST /v1/policies:upload</p>
      </Card>

      {error ? <Card className="p-4 text-sm text-dg-warning">{error}</Card> : null}

      {last ? (
        <Card className="space-y-2 p-4">
          <h2 className="text-base font-semibold">Parse summary</h2>
          <p className="text-sm">
            <span className="text-dg-text-muted">Policy version:</span>{" "}
            <span className="font-mono">{last.policy_version}</span>
          </p>
          <p className="text-sm">
            <span className="text-dg-text-muted">Controls extracted:</span>{" "}
            {last.controls_extracted}
            {last.warnings.length ? (
              <>
                {" "}
                · <span className="text-dg-warning">Warnings: {last.warnings.length}</span>
              </>
            ) : null}
          </p>
          {last.warnings.length ? (
            <ul className="list-inside list-disc text-sm text-dg-text-muted">
              {last.warnings.map((w, i) => (
                <li key={i}>{w.detail}</li>
              ))}
            </ul>
          ) : null}
        </Card>
      ) : null}

      <Card className="p-4">
        <h2 className="mb-3 text-base font-semibold">Recent uploads</h2>
        {loading ? (
          <div className="h-24 animate-pulse rounded-dg-sm bg-dg-subtle" />
        ) : list.length === 0 ? (
          <p className="text-sm text-dg-text-muted">No uploads yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="text-xs text-dg-text-muted">
                <tr>
                  <th className="py-2 pr-3">Version</th>
                  <th className="py-2 pr-3">File</th>
                  <th className="py-2 pr-3">Controls</th>
                  <th className="py-2">When</th>
                </tr>
              </thead>
              <tbody>
                {list.map((u) => (
                  <tr key={u.upload_id} className="border-t border-dg-border">
                    <td className="py-2 pr-3 font-mono text-xs">{u.policy_version}</td>
                    <td className="py-2 pr-3">{u.source_filename}</td>
                    <td className="py-2 pr-3">{u.controls_extracted}</td>
                    <td className="py-2 text-dg-text-muted">
                      {new Date(u.created_at).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        <Button type="button" variant="secondary" size="sm" className="mt-3" onClick={() => void refresh()}>
          Refresh list
        </Button>
      </Card>
    </div>
  );
}
