"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { loadConnectionSettings } from "@/lib/connection-settings";
import { upsertRecentScan } from "@/lib/recent-scans";
import { apiFetch, parseJson } from "@/lib/api-client";
import type { ScanResponse } from "@/lib/api-types";
import {
  defaultCreateScanForm,
  validateCreateScanForm,
  type CreateScanFormState,
  type CloudProfileForm,
} from "@/lib/validate-create-scan";
import { mapApiValidationToFormFields } from "@/lib/map-api-validation";
import { useToast } from "@/components/toast-context";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { UploadRepoModal } from "@/components/upload-repo-modal";

const PROVIDERS = ["aws", "azure", "gcp", "alibaba", "tencent", "huawei"] as const;

export function CreateScanForm() {
  const router = useRouter();
  const { push } = useToast();
  const [f, setF] = useState<CreateScanFormState>(defaultCreateScanForm);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [uploadOpen, setUploadOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const set = (patch: Partial<CreateScanFormState>) => setF((prev) => ({ ...prev, ...patch }));

  const addCloudProfile = () => {
    setF((prev) => ({
      ...prev,
      cloudProfiles: [
        ...prev.cloudProfiles,
        {
          profile_id: "",
          provider: "aws",
          connector_credential_ref: "",
          regionsText: "us-east-1",
        },
      ],
    }));
  };

  const updateCloud = (i: number, patch: Partial<CloudProfileForm>) => {
    setF((prev) => {
      const next = [...prev.cloudProfiles];
      next[i] = { ...next[i], ...patch };
      return { ...prev, cloudProfiles: next };
    });
  };

  const removeCloud = (i: number) => {
    setF((prev) => ({
      ...prev,
      cloudProfiles: prev.cloudProfiles.filter((_, j) => j !== i),
    }));
  };

  const submit = async () => {
    setFieldErrors({});
    const v = validateCreateScanForm(f);
    if (!v.ok || !v.payload) {
      setFieldErrors(v.errors);
      return;
    }
    const s = loadConnectionSettings();
    setSubmitting(true);
    try {
      const headers: Record<string, string> = {};
      if (f.idempotencyKey.trim()) {
        headers["Idempotency-Key"] = f.idempotencyKey.trim();
      }
      const res = await apiFetch(s, "/v1/scans", {
        method: "POST",
        headers,
        body: JSON.stringify(v.payload),
      });
      if (res.status === 422) {
        const body = await parseJson<{ detail?: unknown }>(res);
        setFieldErrors(mapApiValidationToFormFields(body.detail));
        push({
          kind: "error",
          title: "Fix the highlighted fields",
          body: "Review validation errors from the API.",
        });
        return;
      }
      if (!res.ok) {
        const body = await parseJson<{ detail?: unknown }>(res);
        const msg =
          typeof body.detail === "string"
            ? body.detail
            : `Create failed (${res.status})`;
        push({ kind: "error", title: "Something went wrong", body: msg });
        return;
      }
      const scan = await parseJson<ScanResponse>(res);
      upsertRecentScan({
        scan_id: scan.scan_id,
        updated_at: scan.updated_at,
        status: scan.status,
      });
      push({
        kind: "success",
        title: "Scan queued",
        body: "You will see status updates as the scan runs.",
      });
      router.push(`/scans/${scan.scan_id}`);
    } catch {
      push({
        kind: "error",
        title: "Something went wrong",
        body: "Network error.",
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-form space-y-6">
      <UploadRepoModal
        open={uploadOpen}
        onClose={() => setUploadOpen(false)}
        onUseUri={(uri) =>
          setF((prev) => ({ ...prev, storageUri: uri, repoSource: "archive" }))
        }
      />

      <Card>
        <h2 className="mb-4 text-base font-semibold">Source</h2>
        <div className="mb-4 flex flex-wrap gap-4">
          <label className="flex items-center gap-2 text-sm">
            <input
              type="radio"
              name="src"
              checked={f.repoSource === "git"}
              onChange={() => set({ repoSource: "git" })}
            />
            Git
          </label>
          <label className="flex items-center gap-2 text-sm">
            <input
              type="radio"
              name="src"
              checked={f.repoSource === "archive"}
              onChange={() => set({ repoSource: "archive" })}
            />
            Archive
          </label>
        </div>

        {f.repoSource === "git" ? (
          <div className="space-y-3">
            <div>
              <label className="mb-1 block text-sm" htmlFor="gitUrl">
                Repo URL
              </label>
              <Input
                id="gitUrl"
                className="font-mono text-[13px]"
                value={f.gitUrl}
                onChange={(e) => set({ gitUrl: e.target.value })}
              />
              {fieldErrors.gitUrl ? (
                <p className="mt-1 text-xs text-dg-error" role="alert">
                  {fieldErrors.gitUrl}
                </p>
              ) : null}
            </div>
            <div className="grid gap-3 md:grid-cols-2">
              <div>
                <label className="mb-1 block text-sm" htmlFor="ref">
                  Ref
                </label>
                <Input
                  id="ref"
                  value={f.gitRef}
                  onChange={(e) => set({ gitRef: e.target.value })}
                />
                {fieldErrors.gitRef ? (
                  <p className="mt-1 text-xs text-dg-error" role="alert">
                    {fieldErrors.gitRef}
                  </p>
                ) : null}
              </div>
              <div>
                <label className="mb-1 block text-sm" htmlFor="depth">
                  Clone depth (optional)
                </label>
                <Input
                  id="depth"
                  inputMode="numeric"
                  value={f.cloneDepth}
                  onChange={(e) => set({ cloneDepth: e.target.value })}
                />
                {fieldErrors.cloneDepth ? (
                  <p className="mt-1 text-xs text-dg-error" role="alert">
                    {fieldErrors.cloneDepth}
                  </p>
                ) : null}
              </div>
            </div>
            <div>
              <label className="mb-1 block text-sm" htmlFor="sub">
                Sub-path (optional)
              </label>
              <Input
                id="sub"
                value={f.subPath}
                onChange={(e) => set({ subPath: e.target.value })}
              />
              {fieldErrors.subPath ? (
                <p className="mt-1 text-xs text-dg-error" role="alert">
                  {fieldErrors.subPath}
                </p>
              ) : null}
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            <Button variant="secondary" type="button" onClick={() => setUploadOpen(true)}>
              Prepare upload
            </Button>
            <div>
              <label className="mb-1 block text-sm" htmlFor="su">
                Storage URI (s3://…)
              </label>
              <Input
                id="su"
                className="break-all font-mono text-[13px]"
                value={f.storageUri}
                onChange={(e) => set({ storageUri: e.target.value })}
              />
              {fieldErrors.storageUri ? (
                <p className="mt-1 text-xs text-dg-error" role="alert">
                  {fieldErrors.storageUri}
                </p>
              ) : null}
            </div>
          </div>
        )}

        <div className="mt-4">
          <label className="mb-1 block text-sm" htmlFor="sha">
            Checksum SHA-256 (optional)
          </label>
          <Input
            id="sha"
            value={f.checksumSha256}
            onChange={(e) => set({ checksumSha256: e.target.value })}
          />
        </div>
      </Card>

      <Card>
        <h2 className="mb-4 text-base font-semibold">Policies</h2>
        <label className="mb-1 block text-sm" htmlFor="pol">
          Policy IDs (comma-separated)
        </label>
        <Input
          id="pol"
          value={f.policyIdsText}
          onChange={(e) => set({ policyIdsText: e.target.value })}
        />
        {fieldErrors.policyIdsText ? (
          <p className="mt-1 text-xs text-dg-error" role="alert">
            {fieldErrors.policyIdsText}
          </p>
        ) : null}
      </Card>

      <Card>
        <h2 className="mb-4 text-base font-semibold">Layers</h2>
        <div className="space-y-2">
          <label className="flex items-center justify-between gap-4 text-sm">
            <span>Code</span>
            <input
              type="checkbox"
              checked={f.layerCode}
              onChange={(e) => set({ layerCode: e.target.checked })}
            />
          </label>
          <label className="flex items-center justify-between gap-4 text-sm">
            <span>IaC</span>
            <input
              type="checkbox"
              checked={f.layerIac}
              onChange={(e) => set({ layerIac: e.target.checked })}
            />
          </label>
          <label className="flex items-center justify-between gap-4 text-sm">
            <span>Cloud</span>
            <input
              type="checkbox"
              checked={f.layerCloud}
              onChange={(e) => set({ layerCloud: e.target.checked })}
            />
          </label>
        </div>
        {fieldErrors.scan_layers ? (
          <p className="mt-2 text-xs text-dg-error" role="alert">
            {fieldErrors.scan_layers}
          </p>
        ) : null}
        {fieldErrors.repo ? (
          <p className="mt-2 text-xs text-dg-error" role="alert">
            {fieldErrors.repo}
          </p>
        ) : null}
      </Card>

      {f.layerCloud ? (
        <Card>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-base font-semibold">Cloud profiles</h2>
            <Button variant="secondary" size="sm" type="button" onClick={addCloudProfile}>
              Add
            </Button>
          </div>
          <div className="space-y-4">
            {f.cloudProfiles.map((c, i) => (
              <div
                key={i}
                className="rounded-dg-md border border-dg-border bg-dg-subtle/40 p-4"
              >
                <div className="mb-2 flex justify-end">
                  <Button variant="ghost" size="sm" type="button" onClick={() => removeCloud(i)}>
                    Remove
                  </Button>
                </div>
                <div className="grid gap-2 md:grid-cols-2">
                  <div>
                    <label className="text-xs text-dg-text-muted">Profile ID</label>
                    <Input
                      value={c.profile_id}
                      onChange={(e) => updateCloud(i, { profile_id: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-xs text-dg-text-muted">Provider</label>
                    <select
                      className="w-full rounded-dg-sm border border-dg-border bg-dg-card px-2 py-2 text-sm"
                      value={c.provider}
                      onChange={(e) => updateCloud(i, { provider: e.target.value })}
                    >
                      {PROVIDERS.map((p) => (
                        <option key={p} value={p}>
                          {p}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="md:col-span-2">
                    <label className="text-xs text-dg-text-muted">Connector credential ref</label>
                    <Input
                      value={c.connector_credential_ref}
                      onChange={(e) =>
                        updateCloud(i, { connector_credential_ref: e.target.value })
                      }
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="text-xs text-dg-text-muted">Regions (comma-separated)</label>
                    <Input
                      value={c.regionsText}
                      onChange={(e) => updateCloud(i, { regionsText: e.target.value })}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      ) : null}

      <Card>
        <h2 className="mb-4 text-base font-semibold">Budget (optional)</h2>
        <div className="grid gap-3 md:grid-cols-2">
          <div>
            <label className="mb-1 block text-sm">Max LLM USD</label>
            <Input
              inputMode="decimal"
              value={f.budgetMaxUsd}
              onChange={(e) => set({ budgetMaxUsd: e.target.value })}
            />
            {fieldErrors.budgetMaxUsd ? (
              <p className="mt-1 text-xs text-dg-error" role="alert">
                {fieldErrors.budgetMaxUsd}
              </p>
            ) : null}
          </div>
          <div>
            <label className="mb-1 block text-sm">Wall seconds</label>
            <Input
              inputMode="numeric"
              value={f.budgetWallSec}
              onChange={(e) => set({ budgetWallSec: e.target.value })}
            />
            {fieldErrors.budgetWallSec ? (
              <p className="mt-1 text-xs text-dg-error" role="alert">
                {fieldErrors.budgetWallSec}
              </p>
            ) : null}
          </div>
        </div>
      </Card>

      <Card>
        <h2 className="mb-4 text-base font-semibold">Webhook (optional)</h2>
        <Input
          placeholder="https://example.com/hook"
          value={f.webhookUrl}
          onChange={(e) => set({ webhookUrl: e.target.value })}
        />
        <div className="mt-2 flex gap-4 text-sm">
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={f.webhookEvents.completed}
              onChange={(e) =>
                set({
                  webhookEvents: { ...f.webhookEvents, completed: e.target.checked },
                })
              }
            />
            completed
          </label>
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={f.webhookEvents.failed}
              onChange={(e) =>
                set({
                  webhookEvents: { ...f.webhookEvents, failed: e.target.checked },
                })
              }
            />
            failed
          </label>
        </div>
        {fieldErrors.webhookUrl ? (
          <p className="mt-1 text-xs text-dg-error" role="alert">
            {fieldErrors.webhookUrl}
          </p>
        ) : null}
      </Card>

      <Card>
        <label className="mb-1 block text-sm" htmlFor="idem">
          Idempotency-Key (optional, header)
        </label>
        <Input
          id="idem"
          className="font-mono text-[13px]"
          value={f.idempotencyKey}
          onChange={(e) => set({ idempotencyKey: e.target.value })}
        />
      </Card>

      {fieldErrors._form ? (
        <p className="text-sm text-dg-error" role="alert">
          {fieldErrors._form}
        </p>
      ) : null}

      <div className="flex flex-wrap justify-end gap-2">
        <Button variant="secondary" type="button" onClick={() => router.push("/scans")}>
          Cancel
        </Button>
        <Button variant="primary" type="button" onClick={submit} disabled={submitting}>
          {submitting ? "Creating…" : "Create scan"}
        </Button>
      </div>
    </div>
  );
}
