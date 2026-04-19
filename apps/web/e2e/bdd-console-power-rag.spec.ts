/**
 * End-to-end BDD against a **real** local control plane (no `page.route` mocks).
 *
 * Prerequisites (see `scripts/run_web_e2e_power_rag_bdd.sh` and `documentation/testing-ci.md`):
 * - Postgres + Redis (e.g. `docker compose -f docker/compose.dev.yml up -d`)
 * - `alembic upgrade head` + `python3 scripts/seed_dev_tenant.py`
 * - API: `DATABASE_URL`, `REDIS_URL`, `DEEPGUARD_DEV_API_KEY`, `DEEPGUARD_CORS_ORIGINS` (Next on :3000)
 * - Worker: same `DATABASE_URL` / `REDIS_URL`, plus **Hermes** for real git clone:
 *   `DEEPGUARD_HERMES_ENABLED=1` and `DEEPGUARD_S3_*` pointing at MinIO (host port 9000)
 *
 * Enable this suite with **`E2E_POWER_RAG_BACKEND=1`**. Optional: `E2E_API_BASE_URL`, `E2E_API_KEY`.
 */

import { test, expect } from "@playwright/test";
import { stepScreenshot } from "./helpers/bdd-step-screenshot";

const POWER_RAG_GIT_URL = "https://github.com/lcheeyon/power-rag";
const POWER_RAG_REF = "main";

const enabled = !!process.env.E2E_POWER_RAG_BACKEND;
const describeBackend = enabled ? test.describe : test.describe.skip;

describeBackend("Console BDD — power-rag (local API + real worker)", () => {
  test.describe.configure({ mode: "serial" });
  test.setTimeout(600_000);

  test.beforeEach(async ({ page, request }) => {
    if (!enabled) return;
    const base = (process.env.E2E_API_BASE_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");
    const key = process.env.E2E_API_KEY ?? "dev";
    try {
      const h = await request.get(`${base}/v1/healthz`, { timeout: 15_000 });
      test.skip(
        !h.ok(),
        `GET /v1/healthz returned ${h.status()} — start the API on ${base}`
      );
    } catch (e) {
      test.skip(true, `API not reachable at ${base}: ${String(e)}`);
    }

    await page.addInitScript(
      (cfg: { baseUrl: string; apiKey: string; authKind: string }) => {
        localStorage.setItem("deepguard:connection:v1", JSON.stringify(cfg));
      },
      { baseUrl: base, apiKey: key, authKind: "api-key" }
    );
  });

  test("BDD: settings → create Git scan for power-rag → wait COMPLETE → assert clone + job_config", async ({
    page,
    request,
  }) => {
    const base = (process.env.E2E_API_BASE_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");
    const key = process.env.E2E_API_KEY ?? "dev";
    const headers = { "X-API-Key": key };

    await stepScreenshot(page, "UI: Settings → Test connection to real API", async () => {
      await page.goto("/settings");
      await page.getByRole("button", { name: "Test connection" }).click();
      await expect(page.getByText("Connected")).toBeVisible({ timeout: 30_000 });
    });

    await stepScreenshot(page, "UI: New scan — power-rag + clone depth 1", async () => {
      await page.goto("/scans/new");
      await page.getByLabel("Repo URL").fill(POWER_RAG_GIT_URL);
      await page.getByLabel("Ref").fill(POWER_RAG_REF);
      await page.getByLabel("Clone depth (optional)").fill("1");
      await page.getByRole("button", { name: "Create scan" }).click();
      await expect(page).toHaveURL(/\/scans\/[0-9a-f-]{36}$/i, { timeout: 30_000 });
    });

    const scanId = new URL(page.url()).pathname.split("/").pop()!;
    expect(scanId).toMatch(/^[0-9a-f-]{36}$/i);

    await stepScreenshot(page, "Wait for worker: status COMPLETE (polls every 5s)", async () => {
      await expect(page.getByText("COMPLETE", { exact: true })).toBeVisible({ timeout: 600_000 });
    });

    await stepScreenshot(page, "Assert resolved commit + Hermes archive metadata when present", async () => {
      const g = await request.get(`${base}/v1/scans/${scanId}`, { headers });
      expect(g.ok()).toBeTruthy();
      const row = (await g.json()) as {
        status: string;
        repo_commit_sha?: string | null;
        job_config: Record<string, unknown>;
      };
      expect(row.status).toBe("COMPLETE");
      expect(JSON.stringify(row.job_config)).toContain("lcheeyon/power-rag");

      if (row.repo_commit_sha) {
        expect(row.repo_commit_sha.length).toBeGreaterThanOrEqual(7);
        await expect(page.getByText(`Repo commit ${row.repo_commit_sha}`)).toBeVisible();
      }

      await page.getByRole("button", { name: "Expand" }).click();
      await expect(page.locator("pre").first()).toContainText("lcheeyon/power-rag");
      const jc = JSON.stringify(row.job_config);
      if (jc.includes('"hermes"')) {
        await expect(page.locator("pre").first()).toContainText("hermes");
      }
    });
  });
});
