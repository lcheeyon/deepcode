import { test, expect } from "@playwright/test";
import { stepScreenshot } from "./helpers/bdd-step-screenshot";

const hasRealApi = !!process.env.E2E_REAL_API;

test.describe("Real MinIO repo-upload (compose + uvicorn)", () => {
  test.skip(!hasRealApi, "Set E2E_REAL_API=1 with MinIO + API (see CI job web-console-e2e-compose)");

  test.beforeEach(async ({ page }) => {
    const cfg = JSON.stringify({
      baseUrl: process.env.E2E_API_BASE_URL ?? "http://127.0.0.1:8000",
      apiKey: process.env.E2E_API_KEY ?? "dev",
      authKind: "api-key",
    });
    await page.addInitScript((raw) => {
      localStorage.setItem("deepguard:connection:v1", raw as string);
    }, cfg);
  });

  test("prepare-only fills s3:// storage URI from presigned flow", async ({ page }) => {
    await stepScreenshot(page, "MinIO prepare-only: archive flow and presign", async () => {
      await page.goto("/scans/new");
      await page.getByRole("radio", { name: "Archive", exact: true }).check();
      await page.getByRole("button", { name: "Prepare upload" }).click();
      await page.getByRole("button", { name: "Prepare only" }).click();
      await expect(page.getByText("Prepared")).toBeVisible();
    });
    await stepScreenshot(page, "MinIO prepare-only: storage URI on form", async () => {
      await expect(page.locator("#su")).toHaveValue(/^s3:\/\/deepguard-dev\//);
    });
  });

  test("PUT small payload through presigned URL succeeds", async ({ page }) => {
    await stepScreenshot(page, "MinIO upload: attach stub file and PUT", async () => {
      await page.goto("/scans/new");
      await page.getByRole("radio", { name: "Archive", exact: true }).check();
      await page.getByRole("button", { name: "Prepare upload" }).click();
      await page.getByLabel("Archive file (optional)").setInputFiles({
        name: "stub.tgz",
        mimeType: "application/gzip",
        buffer: Buffer.from("stub-bytes-not-a-real-tar"),
      });
      await page.getByRole("button", { name: "Prepare and upload" }).click();
      await expect(page.getByText("Upload complete")).toBeVisible();
    });
    await stepScreenshot(page, "MinIO upload: URI populated", async () => {
      await expect(page.locator("#su")).toHaveValue(/^s3:\/\/deepguard-dev\//);
    });
  });
});
