"use client";

import { useState } from "react";
import { loadConnectionSettings } from "@/lib/connection-settings";
import { apiFetch } from "@/lib/api-client";
import type { PrepareRepoUploadResponse } from "@/lib/api-types";
import { useToast } from "@/components/toast-context";
import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";

export function UploadRepoModal({
  open,
  onClose,
  onUseUri,
}: {
  open: boolean;
  onClose: () => void;
  onUseUri: (storageUri: string) => void;
}) {
  const { push } = useToast();
  const [file, setFile] = useState<File | null>(null);
  const [statusLine, setStatusLine] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [s3Error, setS3Error] = useState<string | null>(null);

  const runUpload = async () => {
    const s = loadConnectionSettings();
    setBusy(true);
    setS3Error(null);
    setStatusLine(null);
    try {
      setStatusLine("Requesting presigned URL…");
      const prep = await apiFetch(s, "/v1/repo-uploads", {
        method: "POST",
        body: JSON.stringify({
          filename: file?.name || "repo.tar.gz",
          content_type: file?.type || "application/gzip",
        }),
      });
      const raw = (await prep.json().catch(() => ({}))) as Record<string, unknown>;
      if (prep.status === 503) {
        const detail = raw.detail as { message?: string; error_code?: string } | undefined;
        setS3Error(
          `${detail?.error_code ?? "REPO_UPLOAD_S3_UNCONFIGURED"}: ${detail?.message ?? "Configure S3/MinIO (see repository .env.example)."}.`
        );
        return;
      }
      if (!prep.ok) {
        setS3Error(`Prepare upload failed (HTTP ${prep.status}).`);
        return;
      }
      const body = raw as unknown as PrepareRepoUploadResponse;
      if (file) {
        setStatusLine("Uploading bytes…");
        const put = await fetch(body.upload_url, {
          method: "PUT",
          headers: body.upload_headers,
          body: file,
        });
        if (!put.ok) {
          push({
            kind: "error",
            title: "Something went wrong",
            body: `PUT failed (${put.status}). Check CORS on the object store.`,
          });
          return;
        }
      }
      onUseUri(body.storage_uri);
      push({
        kind: "success",
        title: file ? "Upload complete" : "Prepared",
        body: "Storage URI applied to the form.",
      });
      onClose();
    } catch {
      push({
        kind: "error",
        title: "Something went wrong",
        body: "Network error during upload.",
      });
    } finally {
      setBusy(false);
      setStatusLine(null);
    }
  };

  return (
    <Modal
      open={open}
      title="Upload repo archive"
      onClose={onClose}
      footer={
        <>
          <Button variant="secondary" onClick={onClose} disabled={busy}>
            Cancel
          </Button>
          <Button variant="primary" onClick={runUpload} disabled={busy}>
            {busy ? "Working…" : file ? "Prepare and upload" : "Prepare only"}
          </Button>
        </>
      }
    >
      <ol className="mb-4 list-decimal space-y-1 pl-4 text-sm text-dg-text-muted">
        <li>POST /v1/repo-uploads → presigned URL + storage_uri</li>
        <li>Optional: PUT file using upload_headers from the response</li>
      </ol>
      {s3Error ? (
        <div
          role="alert"
          className="mb-3 rounded-dg-md border border-dg-error/40 bg-dg-error-bg px-3 py-2 text-sm text-dg-error"
        >
          {s3Error}
        </div>
      ) : null}
      <label className="mb-1 block text-sm" htmlFor="archive-file">
        Archive file (optional)
      </label>
      <input
        id="archive-file"
        type="file"
        className="mb-2 w-full text-sm"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
      />
      {statusLine ? <p className="text-sm text-dg-text-muted">{statusLine}</p> : null}
    </Modal>
  );
}
