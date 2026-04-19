"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import {
  clearRecentScans,
  loadRecentScans,
  type RecentScanEntry,
} from "@/lib/recent-scans";
import { isUuid } from "@/lib/uuid";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Modal } from "@/components/ui/modal";

export default function ScansHubPage() {
  const router = useRouter();
  const [recent, setRecent] = useState<RecentScanEntry[]>([]);
  const [openId, setOpenId] = useState("");
  const [clearOpen, setClearOpen] = useState(false);

  const reload = useCallback(() => {
    setRecent(loadRecentScans());
  }, []);

  useEffect(() => {
    reload();
  }, [reload]);

  const openById = () => {
    const id = openId.trim();
    if (!isUuid(id)) return;
    router.push(`/scans/${id}`);
  };

  return (
    <div>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-[22px] font-semibold tracking-tight">Scans</h1>
        <Link href="/scans/new">
          <Button variant="primary">New scan</Button>
        </Link>
      </div>

      <Card className="mb-6">
        <h2 className="mb-2 text-base font-semibold">Open by ID</h2>
        <div className="flex max-w-form flex-wrap gap-2">
          <Input
            className="font-mono text-[13px]"
            placeholder="00000000-0000-4000-8000-000000000000"
            value={openId}
            onChange={(e) => setOpenId(e.target.value)}
            aria-invalid={openId.length > 0 && !isUuid(openId)}
          />
          <Button variant="secondary" onClick={openById} disabled={!isUuid(openId.trim())}>
            Open
          </Button>
        </div>
        {openId.length > 0 && !isUuid(openId.trim()) ? (
          <p className="mt-2 text-xs text-dg-error" role="alert">
            Enter a valid UUID.
          </p>
        ) : null}
      </Card>

      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-base font-semibold">Recent (this browser)</h2>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setClearOpen(true)}
          disabled={recent.length === 0}
        >
          Clear list
        </Button>
      </div>

      <Modal
        open={clearOpen}
        title="Clear recent scans?"
        onClose={() => setClearOpen(false)}
        footer={
          <>
            <Button variant="secondary" onClick={() => setClearOpen(false)}>
              Keep list
            </Button>
            <Button
              variant="destructive"
              onClick={() => {
                clearRecentScans();
                setRecent([]);
                setClearOpen(false);
              }}
            >
              Clear list
            </Button>
          </>
        }
      >
        <p className="text-sm text-dg-text-muted">
          This removes locally stored scan IDs from this browser only.
        </p>
      </Modal>

      {recent.length === 0 ? (
        <Card>
          <p className="mb-4 text-sm text-dg-text-muted">No scans yet.</p>
          <Link href="/scans/new">
            <Button variant="primary">Create scan</Button>
          </Link>
        </Card>
      ) : (
        <ul className="divide-y divide-dg-border rounded-dg-md border border-dg-border bg-dg-card">
          {recent.map((r) => (
            <li
              key={r.scan_id}
              className="flex flex-wrap items-center justify-between gap-2 px-4 py-3"
            >
              <div>
                <span className="font-mono text-[13px]">{r.scan_id.slice(0, 8)}…</span>
                <span className="ml-2 text-sm text-dg-text-muted">
                  {r.status ?? "—"} · {new Date(r.updated_at).toLocaleString()}
                </span>
              </div>
              <Link href={`/scans/${r.scan_id}`}>
                <Button variant="ghost" size="sm">
                  View
                </Button>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
