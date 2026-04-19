/**
 * **Live E2E** — browser exercises a **real** control plane (`/v1`). **No `page.route` mocks.**
 *
 * Use this to prove FastAPI + DB (and optional worker) behave correctly behind the console,
 * without the long-running **power-rag** worker scenario (`E2E_POWER_RAG_BACKEND`) or **MinIO**
 * compose (`E2E_REAL_API`).
 *
 * **Enable:** `E2E_LIVE_BACKEND=1`  
 * **Optional:** `E2E_API_BASE_URL` (default `http://127.0.0.1:8000`), `E2E_API_KEY` (default `dev`)
 *
 * **Prerequisites:** API reachable from the machine running Playwright; CORS allows the Next
 * origin (e.g. `http://127.0.0.1:3000`). Same baseline as local dev (`DEEPGUARD_DEV_API_KEY`, DB,
 * migrations, seed tenant, etc.).
 */

import { test, expect } from "@playwright/test";
import { stepScreenshot } from "./helpers/bdd-step-screenshot";

const enabled = !!process.env.E2E_LIVE_BACKEND;
const describeLive = enabled ? test.describe : test.describe.skip;

function apiBase(): string {
  return (process.env.E2E_API_BASE_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");
}

function apiKey(): string {
  return process.env.E2E_API_KEY ?? "dev";
}

async function seedLiveConnection(page: import("@playwright/test").Page) {
  await page.addInitScript(
    (cfg: { baseUrl: string; apiKey: string; authKind: "api-key" | "bearer" }) => {
      localStorage.setItem("deepguard:connection:v1", JSON.stringify(cfg));
    },
    { baseUrl: apiBase(), apiKey: apiKey(), authKind: "api-key" }
  );
}

describeLive("E2E — live control plane (no HTTP mocks)", () => {
  test.describe.configure({ mode: "parallel" });

  test.beforeEach(async ({ request }) => {
    if (!enabled) return;
    try {
      const h = await request.get(`${apiBase()}/v1/healthz`, { timeout: 15_000 });
      test.skip(!h.ok(), `GET /v1/healthz returned ${h.status()} — start API at ${apiBase()}`);
    } catch (e) {
      test.skip(true, `API not reachable at ${apiBase()}: ${String(e)}`);
    }
  });

  test("E2E: Settings → Test connection uses live GET /v1/healthz", async ({ page }) => {
    await seedLiveConnection(page);
    await stepScreenshot(page, "Given: Settings with live base URL", async () => {
      await page.goto("/settings");
      await expect(page.getByRole("heading", { name: "API connection", exact: true })).toBeVisible();
    });
    await stepScreenshot(page, "When: Test connection", async () => {
      await page.getByRole("button", { name: "Test connection" }).click();
    });
    await stepScreenshot(page, "Then: Connected toast and last OK metadata", async () => {
      await expect(page.getByText("Connected")).toBeVisible({ timeout: 30_000 });
      await expect(page.getByText(/Last OK:/)).toBeVisible();
    });
  });

  test("E2E: Dashboard → Refresh probes live healthz", async ({ page }) => {
    await seedLiveConnection(page);
    await stepScreenshot(page, "Given: Dashboard", async () => {
      await page.goto("/dashboard");
      await expect(page.getByRole("heading", { name: "Dashboard", exact: true })).toBeVisible();
    });
    await stepScreenshot(page, "When: Refresh control plane", async () => {
      await page.getByRole("button", { name: "Refresh" }).click();
    });
    await stepScreenshot(page, "Then: OK badge and latency line from real API", async () => {
      await expect(page.getByText("OK").first()).toBeVisible({ timeout: 30_000 });
      await expect(page.getByText(/GET \/v1\/healthz/i)).toBeVisible();
    });
  });

  test("E2E: New scan (defaults) → live POST /v1/scans → detail + API cross-check", async ({
    page,
    request,
  }) => {
    test.setTimeout(120_000);
    await seedLiveConnection(page);
    const base = apiBase();
    const key = apiKey();
    const headers = { "X-API-Key": key };

    await stepScreenshot(page, "Given: New scan with default Hello-World payload", async () => {
      await page.goto("/scans/new");
      await expect(page.getByRole("heading", { name: "New scan" })).toBeVisible();
      await expect(page.getByLabel("Repo URL")).toHaveValue(/octocat\/Hello-World/);
    });

    await stepScreenshot(page, "When: Create scan (real POST from browser)", async () => {
      await page.getByRole("button", { name: "Create scan" }).click();
      await expect(page).toHaveURL(/\/scans\/[0-9a-f-]{36}$/i, { timeout: 60_000 });
    });

    const scanId = new URL(page.url()).pathname.split("/").pop()!;
    expect(scanId).toMatch(/^[0-9a-f-]{36}$/i);

    await stepScreenshot(page, "Then: detail heading and scan id from live GET", async () => {
      await expect(page.getByRole("heading", { name: `Scan ${scanId}` })).toBeVisible({
        timeout: 30_000,
      });
    });

    await stepScreenshot(page, "Then: control plane GET matches UI scan_id", async () => {
      const res = await request.get(`${base}/v1/scans/${scanId}`, { headers });
      expect(res.ok(), `GET /v1/scans/${scanId} → ${res.status()}`).toBeTruthy();
      const row = (await res.json()) as { scan_id: string; status: string; job_config?: unknown };
      expect(row.scan_id).toBe(scanId);
      expect(row.status.length).toBeGreaterThan(0);
      expect(row.job_config).toBeDefined();
    });
  });

  test("E2E: Bearer auth → Test connection + authenticated probe", async ({ page, request }) => {
    await seedLiveConnection(page);
    const base = apiBase();
    const key = apiKey();

    await stepScreenshot(page, "Given: Bearer selected in Settings", async () => {
      await page.goto("/settings");
      await page.getByRole("radio", { name: /Bearer/i }).check();
    });

    await stepScreenshot(page, "When: Test connection", async () => {
      await page.getByRole("button", { name: "Test connection" }).click();
      await expect(page.getByText("Connected")).toBeVisible({ timeout: 30_000 });
    });

    await stepScreenshot(page, "Then: no inline auth error (404 probe is success for auth)", async () => {
      await expect(
        page.getByRole("alert").filter({ hasText: /don’t have access|don't have access/i })
      ).toHaveCount(0);
    });

    await stepScreenshot(page, "Then: random scan GET accepts Bearer from server", async () => {
      const ping = "00000000-0000-4000-8000-000000000099";
      const res = await request.get(`${base}/v1/scans/${ping}`, {
        headers: { Authorization: `Bearer ${key}` },
      });
      expect([200, 404]).toContain(res.status());
    });
  });

  test("E2E: After live create, Scans hub lists recent entry", async ({ page, request }) => {
    test.setTimeout(120_000);
    await seedLiveConnection(page);
    const base = apiBase();
    const key = apiKey();
    const headers = { "X-API-Key": key };

    await page.goto("/scans/new");
    await page.getByRole("button", { name: "Create scan" }).click();
    await expect(page).toHaveURL(/\/scans\/[0-9a-f-]{36}$/i, { timeout: 60_000 });
    const scanId = new URL(page.url()).pathname.split("/").pop()!;

    const res = await request.get(`${base}/v1/scans/${scanId}`, { headers });
    expect(res.ok()).toBeTruthy();

    await stepScreenshot(page, "Given: returning to Scans hub after live create", async () => {
      await page.getByRole("navigation", { name: "Main" }).getByRole("link", { name: "Scans" }).click();
      await expect(page).toHaveURL(/\/scans$/);
    });

    await stepScreenshot(page, "Then: recent list shows truncated id and View", async () => {
      await expect(page.getByText(new RegExp(scanId.slice(0, 8)))).toBeVisible();
      await expect(page.getByRole("link", { name: "View" }).first()).toBeVisible();
    });
  });
});
