import { test, expect } from "@playwright/test";
import { stepScreenshot } from "./helpers/bdd-step-screenshot";

const SCAN_ID = "3fa2f2f2-f2f2-4002-8002-000000000001";
const TENANT_ID = "00000000-0000-4000-8000-000000000001";

const scanJson = (over: Partial<Record<string, unknown>> = {}) =>
  JSON.stringify({
    scan_id: SCAN_ID,
    tenant_id: TENANT_ID,
    status: "QUEUED",
    current_stage: "INGESTING",
    percent_complete: 0,
    job_config: {
      policy_ids: ["ISO-27001-2022"],
      scan_layers: { code: true, iac: false, cloud: false },
      repo: { source: "git", url: "https://github.com/octocat/Hello-World", ref: "main" },
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    idempotency_key: null,
    repo_commit_sha: null,
    cancellation_requested: false,
    ...over,
  });

test.beforeEach(async ({ page }) => {
  await page.route("**/v1/healthz", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ status: "ok" }),
    });
  });
  await page.route("**/v1/scans/00000000-0000-4000-8000-000000000099", async (route) => {
    await route.fulfill({ status: 404, contentType: "application/json", body: "{}" });
  });
  await page.route("**/v1/scans", async (route) => {
    if (route.request().method() !== "POST") {
      await route.continue();
      return;
    }
    await route.fulfill({
      status: 201,
      contentType: "application/json",
      body: scanJson(),
    });
  });
  await page.route(`**/v1/scans/${SCAN_ID}`, async (route) => {
    if (route.request().method() !== "GET") {
      await route.continue();
      return;
    }
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: scanJson({ percent_complete: 12 }),
    });
  });
  await page.route(`**/v1/scans/${SCAN_ID}/cancel`, async (route) => {
    if (route.request().method() !== "POST") {
      await route.continue();
      return;
    }
    await route.fulfill({
      status: 202,
      contentType: "application/json",
      body: JSON.stringify({ scan_id: SCAN_ID, cancellation_requested: true }),
    });
  });

  await page.addInitScript(() => {
    localStorage.setItem(
      "deepguard:connection:v1",
      JSON.stringify({
        baseUrl: "http://mock-api.local",
        apiKey: "test-key",
        authKind: "api-key",
      })
    );
  });
});

test.describe("Console MVP (EPIC-DG-14)", () => {
  test("health check then create git scan and see scan id on detail", async ({ page }) => {
    await stepScreenshot(page, "Open settings and test connection", async () => {
      await page.goto("/settings");
      await page.getByRole("button", { name: "Test connection" }).click();
      await expect(page.getByText("Connected")).toBeVisible();
    });

    await stepScreenshot(page, "Create scan from defaults", async () => {
      await page.goto("/scans/new");
      await page.getByRole("button", { name: "Create scan" }).click();
    });

    await stepScreenshot(page, "Land on scan detail with id visible", async () => {
      await expect(page).toHaveURL(new RegExp(`/scans/${SCAN_ID}`));
      await expect(page.getByText(SCAN_ID)).toBeVisible();
    });
  });

  test("request cancel shows success toast", async ({ page }) => {
    await stepScreenshot(page, "Open scan detail", async () => {
      await page.goto(`/scans/${SCAN_ID}`);
      await expect(page.getByText(SCAN_ID)).toBeVisible();
    });
    await stepScreenshot(page, "Open cancel dialog", async () => {
      await page.getByRole("button", { name: "Request cancel" }).first().click();
      await expect(page.getByRole("dialog", { name: "Cancel scan?" })).toBeVisible();
    });
    await stepScreenshot(page, "Confirm cancel and see toast", async () => {
      await page
        .getByRole("dialog", { name: "Cancel scan?" })
        .getByRole("button", { name: "Request cancel" })
        .click();
      await expect(page.getByText("Cancellation requested")).toBeVisible();
    });
  });
});
