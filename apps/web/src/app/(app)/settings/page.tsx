"use client";

import { useEffect, useState } from "react";
import {
  loadConnectionSettings,
  saveConnectionSettings,
  type ConnectionSettings,
} from "@/lib/connection-settings";
import { fetchHealthz } from "@/lib/health";
import { apiFetch, parseJson } from "@/lib/api-client";
import { useToast } from "@/components/toast-context";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function SettingsPage() {
  const { push } = useToast();
  const [form, setForm] = useState<ConnectionSettings>(() => loadConnectionSettings());
  const [showKey, setShowKey] = useState(false);
  const [testing, setTesting] = useState(false);
  const [authError, setAuthError] = useState<string | null>(null);

  useEffect(() => {
    setForm(loadConnectionSettings());
  }, []);

  const persist = (next: ConnectionSettings) => {
    setForm(next);
    saveConnectionSettings(next);
  };

  const testAuthenticatedPing = async () => {
    setAuthError(null);
    const res = await apiFetch(form, "/v1/scans/00000000-0000-4000-8000-000000000099", {
      method: "GET",
    });
    if (res.status === 401) {
      setAuthError(
        "You don’t have access — check your API key or ask an admin for the correct role."
      );
      return;
    }
    /* 404 expected for random id — proves auth passed */
    if (!res.ok && res.status !== 404) {
      const body = await parseJson<{ detail?: unknown }>(res);
      const d = body?.detail;
      setAuthError(
        typeof d === "string" ? d : `Request failed (${res.status}).`
      );
    }
  };

  const testConnection = async () => {
    setTesting(true);
    setAuthError(null);
    try {
      const r = await fetchHealthz(form.baseUrl.trim());
      const next: ConnectionSettings = {
        ...form,
        baseUrl: form.baseUrl.trim(),
        lastHealthOkAt: r.ok ? new Date().toISOString() : form.lastHealthOkAt,
        lastHealthLatencyMs: r.ms,
      };
      persist(next);
      if (r.ok) {
        push({ kind: "success", title: "Connected", body: "GET /v1/healthz succeeded." });
        await testAuthenticatedPing();
      } else {
        push({
          kind: "error",
          title: "Health check failed",
          body: `HTTP ${r.status}`,
        });
      }
    } catch {
      push({
        kind: "error",
        title: "Something went wrong",
        body: "Check your connection and base URL.",
      });
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className="max-w-form">
      <h1 className="mb-6 text-[22px] font-semibold tracking-tight">API connection</h1>
      <Card>
        <div className="space-y-4">
          <div>
            <label className="mb-1 block text-sm text-dg-text-primary" htmlFor="base">
              Base URL
            </label>
            <Input
              id="base"
              name="baseUrl"
              className="font-mono text-[13px]"
              value={form.baseUrl}
              onChange={(e) => persist({ ...form, baseUrl: e.target.value })}
              autoComplete="url"
            />
          </div>
          <div>
            <div className="mb-1 flex items-center justify-between gap-2">
              <label className="text-sm text-dg-text-primary" htmlFor="key">
                API key
              </label>
              <Button variant="ghost" size="sm" type="button" onClick={() => setShowKey((v) => !v)}>
                {showKey ? "Hide" : "Show"}
              </Button>
            </div>
            <Input
              id="key"
              type={showKey ? "text" : "password"}
              value={form.apiKey}
              onChange={(e) => persist({ ...form, apiKey: e.target.value })}
              autoComplete="off"
            />
            <p className="mt-1 text-xs text-dg-text-muted">
              Sent as <code className="text-xs">X-API-Key</code> or Bearer per toggle below.
            </p>
          </div>
          <fieldset className="space-y-2">
            <legend className="text-sm font-medium text-dg-text-primary">Auth header</legend>
            <label className="flex items-center gap-2 text-sm">
              <input
                type="radio"
                name="auth"
                checked={form.authKind === "api-key"}
                onChange={() => persist({ ...form, authKind: "api-key" })}
              />
              X-API-Key
            </label>
            <label className="flex items-center gap-2 text-sm">
              <input
                type="radio"
                name="auth"
                checked={form.authKind === "bearer"}
                onChange={() => persist({ ...form, authKind: "bearer" })}
              />
              Authorization: Bearer
            </label>
          </fieldset>
          {authError ? (
            <div
              role="alert"
              className="rounded-dg-md border border-dg-error/40 bg-dg-error-bg px-3 py-2 text-sm text-dg-error"
            >
              {authError}
            </div>
          ) : null}
          <div className="flex flex-wrap items-center gap-3">
            <Button variant="primary" onClick={testConnection} disabled={testing}>
              {testing ? "Testing…" : "Test connection"}
            </Button>
            {form.lastHealthOkAt ? (
              <span className="text-xs text-dg-text-muted">
                Last OK: {new Date(form.lastHealthOkAt).toLocaleString()} —{" "}
                {form.lastHealthLatencyMs != null ? `${form.lastHealthLatencyMs} ms` : ""}
              </span>
            ) : null}
          </div>
          <p className="text-xs text-dg-text-muted">
            Keys are stored in browser local storage only (MVP). Do not use production
            secrets here.
          </p>
        </div>
      </Card>
    </div>
  );
}
