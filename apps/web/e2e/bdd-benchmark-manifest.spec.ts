/**
 * End-to-end BDD against a real local API/worker stack for benchmark campaign.
 *
 * Enable with:
 *   E2E_BENCHMARK_BACKEND=1
 *
 * Optional:
 *   E2E_BENCHMARK_LIMIT=3
 *   E2E_API_BASE_URL=http://127.0.0.1:8000
 *   E2E_API_KEY=dev
 *
 * Note:
 * - This suite only submits `git` source entries from benchmark manifest by default.
 * - zip/archive entries are covered in mocked benchmark suite.
 */

import { test, expect } from "@playwright/test";
import { stepScreenshot } from "./helpers/bdd-step-screenshot";
import path from "node:path";
import fs from "node:fs";

type BenchmarkEntry = {
  id: string;
  name: string;
  source_mode: "git" | "zip_archive";
  repo_url: string;
  default_ref: string;
  policy_ids: string[];
  scan_layers: { code: boolean; iac: boolean; cloud: boolean };
};

type Manifest = { entries: BenchmarkEntry[] };

const enabled = !!process.env.E2E_BENCHMARK_BACKEND;
const describeBackend = enabled ? test.describe : test.describe.skip;

const MANIFEST_PATH = path.resolve(
  __dirname,
  "../../..",
  "docs/benchmarks/deepguard-benchmark-manifest.json"
);
const MANIFEST = JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf-8")) as Manifest;

describeBackend("Console BDD — benchmark campaign (real API + worker)", () => {
  test.describe.configure({ mode: "serial" });
  test.setTimeout(900_000);

  test("BDD: create benchmark scans (git subset) -> wait terminal -> verify report endpoint if present", async ({
    page,
    request,
  }) => {
    const base = (process.env.E2E_API_BASE_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");
    const key = process.env.E2E_API_KEY ?? "dev";
    const headers = { "X-API-Key": key };
    const limit = Number(process.env.E2E_BENCHMARK_LIMIT ?? "3");

    const h = await request.get(`${base}/v1/healthz`, { timeout: 20_000 });
    test.skip(!h.ok(), `API health check failed at ${base} with ${h.status()}`);

    await page.addInitScript(
      (cfg: { baseUrl: string; apiKey: string; authKind: string }) => {
        localStorage.setItem("deepguard:connection:v1", JSON.stringify(cfg));
      },
      { baseUrl: base, apiKey: key, authKind: "api-key" }
    );

    await stepScreenshot(page, "Given connected settings and benchmark plan", async () => {
      await page.goto("/settings");
      await page.getByRole("button", { name: "Test connection" }).click();
      await expect(page.getByText("Connected")).toBeVisible({ timeout: 30_000 });
    });

    const gitEntries = MANIFEST.entries.filter((e) => e.source_mode === "git").slice(0, Math.max(1, limit));
    const scans: Array<{ entry: BenchmarkEntry; scanId: string }> = [];

    await stepScreenshot(page, "When creating git benchmark scans via API", async () => {
      for (const entry of gitEntries) {
        const r = await request.post(`${base}/v1/scans`, {
          headers,
          data: {
            repo: {
              source: "git",
              url: entry.repo_url,
              ref: entry.default_ref,
            },
            policy_ids: entry.policy_ids,
            scan_layers: entry.scan_layers,
          },
        });
        expect([200, 201]).toContain(r.status());
        const body = (await r.json()) as { scan_id: string };
        expect(body.scan_id).toMatch(/^[0-9a-f-]{36}$/i);
        scans.push({ entry, scanId: body.scan_id });
      }
    });

    await stepScreenshot(page, "Then each scan reaches terminal state and report retrieval is checked", async () => {
      for (const item of scans) {
        const deadline = Date.now() + 12 * 60_000;
        let row: Record<string, unknown> | null = null;
        // poll every 5s
        while (Date.now() < deadline) {
          const g = await request.get(`${base}/v1/scans/${item.scanId}`, { headers });
          expect(g.ok()).toBeTruthy();
          row = (await g.json()) as Record<string, unknown>;
          const status = String(row.status ?? "");
          if (["COMPLETE", "FAILED", "CANCELLED"].includes(status)) break;
          await page.waitForTimeout(5000);
        }

        expect(row, `scan row missing for ${item.entry.id}`).toBeTruthy();
        const status = String(row!.status ?? "");
        expect(["COMPLETE", "FAILED", "CANCELLED"]).toContain(status);

        // Compliance report endpoint verification only if complete + artifact id available.
        if (status === "COMPLETE") {
          const reportArtifactId =
            (row!.report_artifact_id as string | undefined) ??
            ((row!.report_artifact_ref as { artifact_id?: string } | undefined)?.artifact_id ??
              undefined);

          if (reportArtifactId) {
            const rr = await request.get(
              `${base}/v1/scans/${item.scanId}/artifacts/${reportArtifactId}`,
              {
                headers,
                maxRedirects: 0,
              }
            );
            expect([200, 302]).toContain(rr.status());
          } else {
            test.info().annotations.push({
              type: "benchmark-note",
              description: `${item.entry.id}: COMPLETE but no report artifact field in API response`,
            });
          }
        }
      }
    });
  });
});
