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
  zip_url: string;
  policy_ids: string[];
  scan_layers: { code: boolean; iac: boolean; cloud: boolean };
};

type BenchmarkManifest = {
  version: string;
  entries: BenchmarkEntry[];
};

const BENCHMARK_MANIFEST_PATH = path.resolve(
  __dirname,
  "../../..",
  "docs/benchmarks/deepguard-benchmark-manifest.json"
);

const MANIFEST: BenchmarkManifest = JSON.parse(
  fs.readFileSync(BENCHMARK_MANIFEST_PATH, "utf-8")
) as BenchmarkManifest;

/** Unused loopback port — avoids colliding with a real uvicorn on :8000. Playwright routes match path-only globs. */
const MOCK_API_BASE = "http://127.0.0.1:49998";

test.describe("Console BDD — benchmark campaign (mocked API)", () => {
  test.beforeEach(async ({ page }) => {
    const scansById = new Map<
      string,
      {
        scan_id: string;
        status: string;
        current_stage: string;
        percent_complete: number;
        benchmark_id: string;
        report_artifact_id: string;
        job_config: Record<string, unknown>;
      }
    >();
    let sequence = 0;

    await page.route("**/v1/healthz", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ status: "ok" }),
      });
    });

    await page.route("**/v1/scans", async (route) => {
      if (route.request().method() !== "POST") {
        await route.continue();
        return;
      }

      const raw = route.request().postData() ?? "{}";
      const body = JSON.parse(raw) as {
        policy_ids?: string[];
        scan_layers?: { code: boolean; iac: boolean; cloud: boolean };
        repo?: {
          source?: string;
          url?: string;
          ref?: string;
          format?: string;
        };
      };
      const repo = body.repo ?? {};

      const matched = MANIFEST.entries.find((e) => {
        if (e.source_mode === "git") {
          return repo.source === "git" && repo.url === e.repo_url;
        }
        // zip/archive mode in mocked flow uses archive source and zip URL
        return repo.source === "archive" && repo.url === e.zip_url;
      });
      expect(matched, "scan request should match a benchmark manifest entry").toBeTruthy();

      sequence += 1;
      const scanId = `00000000-0000-4000-8000-${String(sequence).padStart(12, "0")}`;
      const artifactId = `10000000-0000-4000-8000-${String(sequence).padStart(12, "0")}`;

      scansById.set(scanId, {
        scan_id: scanId,
        status: "COMPLETE",
        current_stage: "REPORTING",
        percent_complete: 100,
        benchmark_id: matched!.id,
        report_artifact_id: artifactId,
        job_config: {
          policy_ids: body.policy_ids ?? matched!.policy_ids,
          scan_layers: body.scan_layers ?? matched!.scan_layers,
          repo: body.repo,
        },
      });

      await route.fulfill({
        status: 201,
        contentType: "application/json",
        body: JSON.stringify({
          scan_id: scanId,
          status: "QUEUED",
          current_stage: "INGESTING",
          percent_complete: 0,
          job_config: {
            policy_ids: body.policy_ids ?? matched!.policy_ids,
            scan_layers: body.scan_layers ?? matched!.scan_layers,
            repo: body.repo,
          },
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        }),
      });
    });

    await page.route("**/v1/scans/*/artifacts/*", async (route) => {
      await route.fulfill({
        status: 302,
        headers: {
          location: "https://example.invalid/deepguard-report.pdf",
        },
      });
    });

    await page.route("**/v1/scans/*", async (route) => {
      if (route.request().method() !== "GET") {
        await route.continue();
        return;
      }
      const url = new URL(route.request().url());
      const scanId = url.pathname.split("/").pop()!;
      const found = scansById.get(scanId);
      if (!found) {
        await route.fulfill({
          status: 404,
          contentType: "application/json",
          body: JSON.stringify({ error_code: "SCAN_NOT_FOUND" }),
        });
        return;
      }
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          scan_id: found.scan_id,
          status: found.status,
          current_stage: found.current_stage,
          percent_complete: found.percent_complete,
          job_config: found.job_config,
          report_artifact_id: found.report_artifact_id,
          benchmark_id: found.benchmark_id,
        }),
      });
    });

    await page.addInitScript((baseUrl: string) => {
      localStorage.setItem(
        "deepguard:connection:v1",
        JSON.stringify({
          baseUrl,
          apiKey: "benchmark-mock-key",
          authKind: "api-key",
        })
      );
    }, MOCK_API_BASE);
  });

  test("BDD: create benchmark scans + validate report endpoints", async ({ page }) => {
    await stepScreenshot(page, "Given API settings and benchmark corpus loaded", async () => {
      await page.goto("/settings");
      await page.getByRole("button", { name: "Test connection" }).click();
      await expect(page.getByText("Connected")).toBeVisible();
      expect(MANIFEST.entries.length).toBe(10);
    });

    type CreatedRow = { id: string; scanId: string; source: string; reportArtifactId: string };
    let created: CreatedRow[] = [];

    await stepScreenshot(page, "When creating scans for all benchmark entries", async () => {
      created = await page.evaluate(
        async ({
          base,
          entries,
        }: {
          base: string;
          entries: BenchmarkEntry[];
        }) => {
          const out: CreatedRow[] = [];
          const headers: Record<string, string> = {
            "Content-Type": "application/json",
            "X-API-Key": "benchmark-mock-key",
          };
          for (const entry of entries) {
            const repo =
              entry.source_mode === "git"
                ? {
                    source: "git",
                    url: entry.repo_url,
                    ref: entry.default_ref,
                  }
                : {
                    source: "archive",
                    url: entry.zip_url,
                    format: "zip",
                  };
            const r = await fetch(`${base}/v1/scans`, {
              method: "POST",
              headers,
              body: JSON.stringify({
                repo,
                policy_ids: entry.policy_ids,
                scan_layers: entry.scan_layers,
              }),
            });
            if (r.status !== 201) {
              throw new Error(`POST /v1/scans → ${r.status} ${await r.text()}`);
            }
            const b = (await r.json()) as { scan_id: string };
            out.push({
              id: entry.id,
              scanId: b.scan_id,
              source: entry.source_mode,
              reportArtifactId: "",
            });
          }
          return out;
        },
        { base: MOCK_API_BASE, entries: MANIFEST.entries }
      );
      expect(created.length).toBe(10);
    });

    await stepScreenshot(page, "Then all scans complete and expose report artifact IDs", async () => {
      const updated = await page.evaluate(
        async ({ base, items }: { base: string; items: CreatedRow[] }) => {
          const next: CreatedRow[] = [];
          for (const item of items) {
            const g = await fetch(`${base}/v1/scans/${item.scanId}`, {
              headers: { "X-API-Key": "benchmark-mock-key" },
            });
            if (g.status !== 200) {
              throw new Error(`GET scan ${item.scanId} → ${g.status}`);
            }
            const row = (await g.json()) as {
              status: string;
              report_artifact_id?: string;
            };
            if (row.status !== "COMPLETE") {
              throw new Error(`Expected COMPLETE for ${item.id}, got ${row.status}`);
            }
            if (!row.report_artifact_id) {
              throw new Error(`Missing report_artifact_id for ${item.id}`);
            }
            next.push({ ...item, reportArtifactId: row.report_artifact_id });
          }
          return next;
        },
        { base: MOCK_API_BASE, items: created }
      );
      created.splice(0, created.length, ...updated);
    });

    await stepScreenshot(page, "And report retrieval endpoints are resolvable for publishing", async () => {
      await page.evaluate(
        async ({ base, items }: { base: string; items: CreatedRow[] }) => {
          for (const item of items) {
            const url = `${base}/v1/scans/${item.scanId}/artifacts/${item.reportArtifactId}`;
            const rr = await fetch(url, {
              method: "GET",
              redirect: "manual",
              headers: { "X-API-Key": "benchmark-mock-key" },
            });
            /* redirect: manual — cross-origin Location can surface as status 0 (opaque) in Chromium */
            if (rr.status !== 302 && rr.status !== 200 && rr.status !== 0) {
              throw new Error(`GET artifact → ${rr.status}`);
            }
          }
        },
        { base: MOCK_API_BASE, items: created }
      );
    });
  });
});
