import { test, expect } from "@playwright/test";
import { stepScreenshot } from "./helpers/bdd-step-screenshot";

test.describe("API error surfaces (mocked)", () => {
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
    await page.addInitScript(() => {
      localStorage.setItem(
        "deepguard:connection:v1",
        JSON.stringify({
          baseUrl: "http://mock-validation.local",
          apiKey: "k",
          authKind: "api-key",
        })
      );
    });
  });

  test("repo-upload 503 shows REPO_UPLOAD inline alert in modal", async ({ page }) => {
    await page.route("**/v1/repo-uploads", async (route) => {
      if (route.request().method() !== "POST") {
        await route.continue();
        return;
      }
      await route.fulfill({
        status: 503,
        contentType: "application/json",
        body: JSON.stringify({
          detail: {
            error_code: "REPO_UPLOAD_S3_UNCONFIGURED",
            message: "S3/MinIO settings are not configured for presigned repo uploads.",
          },
        }),
      });
    });

    await stepScreenshot(page, "503 repo-upload: open archive upload modal", async () => {
      await page.goto("/scans/new");
      await page.getByRole("radio", { name: "Archive", exact: true }).check();
      await page.getByRole("button", { name: "Prepare upload" }).click();
    });
    await stepScreenshot(page, "503 repo-upload: trigger prepare and see alert", async () => {
      await page.getByRole("button", { name: "Prepare only" }).click();
      await expect(
        page.getByRole("alert").filter({ hasText: /REPO_UPLOAD_S3_UNCONFIGURED|\.env\.example/i })
      ).toBeVisible();
    });
  });

  test("POST scan 422 maps repo.url onto Git URL field", async ({ page }) => {
    await page.route("**/v1/scans", async (route) => {
      if (route.request().method() !== "POST") {
        await route.continue();
        return;
      }
      await route.fulfill({
        status: 422,
        contentType: "application/json",
        body: JSON.stringify({
          detail: [
            {
              type: "value_error",
              loc: ["body", "repo", "url"],
              msg: "API validation: repo.url rejected for this test",
            },
          ],
        }),
      });
    });

    await stepScreenshot(page, "422 create scan: submit and see field mapping", async () => {
      await page.goto("/scans/new");
      await page.getByRole("button", { name: "Create scan" }).click();
      await expect(page.getByText("Fix the highlighted fields")).toBeVisible();
      await expect(
        page.getByText("API validation: repo.url rejected for this test")
      ).toBeVisible();
    });
  });
});
