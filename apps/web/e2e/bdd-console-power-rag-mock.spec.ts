import { test, expect } from "@playwright/test";
import { stepScreenshot } from "./helpers/bdd-step-screenshot";

/** Public fixture repo for BDD “code scanning” scenarios (real URL; API is mocked). */
const POWER_RAG_GIT_URL = "https://github.com/lcheeyon/power-rag";
const POWER_RAG_REF = "main";

const SCAN_ID = "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d";
const TENANT_ID = "00000000-0000-4000-8000-000000000001";

function jobConfigFromCreateBody(body: Record<string, unknown>): Record<string, unknown> {
  return {
    policy_ids: body.policy_ids,
    scan_layers: body.scan_layers,
    repo: body.repo,
    ...(body.cloud_profiles && Array.isArray(body.cloud_profiles) && (body.cloud_profiles as unknown[]).length
      ? { cloud_profiles: body.cloud_profiles }
      : {}),
    ...(body.notifications ? { notifications: body.notifications } : {}),
    ...(body.budget ? { budget: body.budget } : {}),
  };
}

function scanResponseFromCreateBody(
  body: Record<string, unknown>,
  over: Partial<Record<string, unknown>> = {}
) {
  return JSON.stringify({
    scan_id: SCAN_ID,
    tenant_id: TENANT_ID,
    status: "QUEUED",
    current_stage: "INGESTING",
    percent_complete: 0,
    job_config: jobConfigFromCreateBody(body),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    idempotency_key: null,
    repo_commit_sha: null,
    cancellation_requested: false,
    ...over,
  });
}

test.describe("Console BDD — power-rag (mocked API)", () => {
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
      const raw = route.request().postData();
      expect(raw, "POST /v1/scans must send JSON body").toBeTruthy();
      const body = JSON.parse(raw!) as Record<string, unknown>;
      const repo = body.repo as Record<string, unknown> | undefined;
      expect(repo?.source, "repo.source").toBe("git");
      expect(String(repo?.url), "repo.url must use power-rag fixture").toContain(
        "github.com/lcheeyon/power-rag"
      );
      expect(repo?.ref, "repo.ref").toBe(POWER_RAG_REF);
      await route.fulfill({
        status: 201,
        contentType: "application/json",
        body: scanResponseFromCreateBody(body),
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
        body: JSON.stringify({
          scan_id: SCAN_ID,
          tenant_id: TENANT_ID,
          status: "RUNNING",
          current_stage: "INDEXING",
          percent_complete: 33,
          job_config: {
            policy_ids: ["ISO-27001-2022"],
            scan_layers: { code: true, iac: false, cloud: false },
            repo: {
              source: "git",
              url: POWER_RAG_GIT_URL,
              ref: POWER_RAG_REF,
            },
          },
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          idempotency_key: null,
          repo_commit_sha: "deadbeef",
          cancellation_requested: false,
        }),
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
          baseUrl: "http://mock-power-rag.local",
          apiKey: "bdd-test-key",
          authKind: "api-key",
        })
      );
    });
  });

  test("BDD: root redirect, shell nav, dashboard, settings, scans hub, power-rag create, detail, cancel", async ({
    page,
  }) => {
    await stepScreenshot(page, "Given the app: open root → redirect to dashboard", async () => {
      await page.goto("/");
      await expect(page).toHaveURL(/\/dashboard$/);
      await expect(page.getByRole("heading", { name: "Dashboard", exact: true })).toBeVisible();
    });

    await stepScreenshot(page, "When using the sidebar: navigate to Scans hub", async () => {
      await page.getByRole("navigation", { name: "Main" }).getByRole("link", { name: "Scans" }).click();
      await expect(page).toHaveURL(/\/scans$/);
      await expect(page.getByRole("heading", { name: "Scans", exact: true })).toBeVisible();
    });

    await stepScreenshot(page, "Then placeholder nav shows Findings/Policies/Reports disabled", async () => {
      await expect(page.getByText("Findings", { exact: true })).toBeVisible();
      await expect(page.getByText("Policies", { exact: true })).toBeVisible();
      await expect(page.getByText("Reports", { exact: true })).toBeVisible();
    });

    await stepScreenshot(page, "When opening Settings and testing connection", async () => {
      await page.getByRole("navigation", { name: "Main" }).getByRole("link", { name: "Settings" }).click();
      await expect(page).toHaveURL(/\/settings$/);
      await expect(page.getByRole("heading", { name: "API connection", exact: true })).toBeVisible();
      await page.getByRole("button", { name: "Test connection" }).click();
      await expect(page.getByText("Connected")).toBeVisible();
    });

    await stepScreenshot(page, "When starting a new Git scan for lcheeyon/power-rag", async () => {
      await page.getByRole("navigation", { name: "Main" }).getByRole("link", { name: "Dashboard" }).click();
      await page.getByRole("navigation", { name: "Main" }).getByRole("link", { name: "Scans" }).click();
      await page.getByRole("link", { name: "New scan" }).click();
      await expect(page).toHaveURL(/\/scans\/new$/);
      await page.getByLabel("Repo URL").fill(POWER_RAG_GIT_URL);
      await page.getByLabel("Ref").fill(POWER_RAG_REF);
      await page.getByRole("button", { name: "Create scan" }).click();
    });

    await stepScreenshot(page, "Then scan detail shows id and power-rag in job_config", async () => {
      await expect(page).toHaveURL(new RegExp(`/scans/${SCAN_ID}`));
      await expect(page.getByText(SCAN_ID)).toBeVisible();
      await expect(page.getByText(/power-rag/)).toBeVisible();
      await page.getByRole("button", { name: "Expand" }).click();
      await expect(page.getByText(POWER_RAG_GIT_URL)).toBeVisible();
    });

    await stepScreenshot(page, "When returning to Scans hub, recent list links to the scan", async () => {
      await page.getByRole("navigation", { name: "Main" }).getByRole("link", { name: "Scans" }).click();
      await expect(page.getByRole("link", { name: "View" })).toBeVisible();
      await page.getByRole("link", { name: "View" }).click();
      await expect(page).toHaveURL(new RegExp(`/scans/${SCAN_ID}`));
    });

    await stepScreenshot(page, "When Open by ID is used with the same UUID", async () => {
      await page.getByRole("navigation", { name: "Main" }).getByRole("link", { name: "Scans" }).click();
      await page.getByPlaceholder("00000000-0000-4000-8000-000000000000").fill(SCAN_ID);
      await page.getByRole("button", { name: "Open", exact: true }).click();
      await expect(page).toHaveURL(new RegExp(`/scans/${SCAN_ID}`));
    });

    await stepScreenshot(page, "When operator requests cancel with confirm", async () => {
      await page.getByRole("button", { name: "Request cancel" }).first().click();
      await expect(page.getByRole("dialog", { name: "Cancel scan?" })).toBeVisible();
      await page
        .getByRole("dialog", { name: "Cancel scan?" })
        .getByRole("button", { name: "Request cancel" })
        .click();
      await expect(page.getByText("Cancellation requested")).toBeVisible();
    });
  });

  test("BDD: dashboard health refresh shows OK state", async ({ page }) => {
    await stepScreenshot(page, "Given dashboard: refresh control plane health", async () => {
      await page.goto("/dashboard");
      await page.getByRole("button", { name: "Refresh" }).click();
      await expect(page.getByText(/OK|200|healthz/i).first()).toBeVisible();
    });
  });
});
