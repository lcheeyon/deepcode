import { test, expect, type Page } from "@playwright/test";
import { stepScreenshot } from "./helpers/bdd-step-screenshot";

const BASE = "http://bdd-epic14-comprehensive.local";
const PING_ID = "00000000-0000-4000-8000-000000000099";
const KNOWN_SCAN = "b2c3d4e5-f6a7-48b9-9d0e-1f2a3b4c5d6e";
const TENANT_ID = "00000000-0000-4000-8000-000000000001";

type StoredConnection = { baseUrl: string; apiKey: string; authKind: "api-key" | "bearer" };

/** Playwright only passes init script args when using the two-argument form (closures are not serialized). */
async function seedConnection(page: Page, conn: StoredConnection) {
  await page.addInitScript((c: StoredConnection) => {
    localStorage.setItem("deepguard:connection:v1", JSON.stringify(c));
  }, conn);
}

async function seedConnectionAndRecent(
  page: Page,
  conn: StoredConnection,
  recent: Array<{ scan_id: string; updated_at: string; status?: string }>
) {
  await page.addInitScript(
    (payload: {
      conn: StoredConnection;
      recent: Array<{ scan_id: string; updated_at: string; status?: string }>;
    }) => {
      localStorage.setItem("deepguard:connection:v1", JSON.stringify(payload.conn));
      localStorage.setItem("deepguard:recent-scans:v1", JSON.stringify(payload.recent));
    },
    { conn, recent }
  );
}

function scanDetailJson(over: Partial<Record<string, unknown>> = {}) {
  return JSON.stringify({
    scan_id: KNOWN_SCAN,
    tenant_id: TENANT_ID,
    status: "RUNNING",
    current_stage: "ANALYZING",
    percent_complete: 42,
    job_config: {
      policy_ids: ["ISO-27001-2022"],
      scan_layers: { code: true, iac: false, cloud: false },
      repo: {
        source: "git",
        url: "https://github.com/octocat/Hello-World",
        ref: "main",
      },
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    idempotency_key: null,
    repo_commit_sha: "cafebabe",
    cancellation_requested: false,
    ...over,
  });
}

async function mockHealthOk(page: import("@playwright/test").Page) {
  await page.route("**/v1/healthz", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ status: "ok" }),
    });
  });
}

test.describe("EPIC-DG-14 BDD — shell, theme, and responsive nav", () => {
  test.beforeEach(async ({ page }) => {
    await mockHealthOk(page);
    await seedConnection(page, { baseUrl: BASE, apiKey: "bdd-key", authKind: "api-key" });
  });

  test("Given the console When user switches theme Then html.dark reflects choice", async ({ page }) => {
    await stepScreenshot(page, "Given: open Dashboard with default shell", async () => {
      await page.goto("/dashboard");
      await expect(page.getByRole("heading", { name: "Dashboard", exact: true })).toBeVisible();
      await expect(page.getByRole("navigation", { name: "Main" })).toBeVisible();
    });

    await stepScreenshot(page, "When: set Color theme to Dark", async () => {
      await page.getByLabel("Color theme").selectOption("dark");
    });

    await stepScreenshot(page, "Then: document root has dark class and footer shows version pill", async () => {
      await expect(page.locator("html")).toHaveClass(/dark/);
      await expect(page.getByText(process.env.NEXT_PUBLIC_APP_VERSION ?? "0.1.0")).toBeVisible();
    });

    await stepScreenshot(page, "When: user switches theme back to Light", async () => {
      await page.getByLabel("Color theme").selectOption("light");
    });

    await stepScreenshot(page, "Then: dark class is removed from document root", async () => {
      await expect(page.locator("html")).not.toHaveClass(/dark/);
    });
  });

  test("Given a narrow viewport When opening the menu Then drawer shows main navigation", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await mockHealthOk(page);
    await seedConnection(page, { baseUrl: BASE, apiKey: "bdd-key", authKind: "api-key" });

    await stepScreenshot(page, "Given: mobile viewport on Dashboard", async () => {
      await page.goto("/dashboard");
      await expect(page.getByRole("heading", { name: "Dashboard", exact: true })).toBeVisible();
    });

    await stepScreenshot(page, "When: open navigation drawer from header", async () => {
      await page.getByRole("button", { name: "Open navigation menu" }).click();
    });

    await stepScreenshot(page, "Then: sidebar links Scans and Settings are reachable", async () => {
      await expect(
        page.getByRole("navigation", { name: "Main" }).getByRole("link", { name: "Scans" })
      ).toBeVisible();
      await page.getByRole("navigation", { name: "Main" }).getByRole("link", { name: "Scans" }).click();
      await expect(page).toHaveURL(/\/scans$/);
    });
  });
});

test.describe("EPIC-DG-14 BDD — settings, healthz, and auth headers", () => {
  test.beforeEach(async ({ page }) => {
    await mockHealthOk(page);
    await seedConnection(page, { baseUrl: BASE, apiKey: "probe-secret", authKind: "api-key" });
  });

  test("Given API key mode When Test connection Then X-API-Key is sent on authenticated probe", async ({
    page,
  }) => {
    await page.route(`**/v1/scans/${PING_ID}`, async (route) => {
      if (route.request().method() !== "GET") {
        await route.continue();
        return;
      }
      await route.fulfill({ status: 404, contentType: "application/json", body: "{}" });
    });

    await stepScreenshot(page, "Given: Settings with X-API-Key auth selected", async () => {
      await page.goto("/settings");
      await expect(page.getByRole("heading", { name: "API connection", exact: true })).toBeVisible();
      await page.getByRole("radio", { name: /X-API-Key/i }).check();
    });

    await stepScreenshot(page, "When: Test connection succeeds", async () => {
      const probe = page.waitForRequest(
        (req) => req.method() === "GET" && req.url().includes(`/v1/scans/${PING_ID}`)
      );
      await page.getByRole("button", { name: "Test connection" }).click();
      await expect(page.getByText("Connected")).toBeVisible();
      const req = await probe;
      const h = req.headers();
      const xk = h["x-api-key"] ?? h["X-API-Key"];
      expect(xk, "authenticated probe should send X-API-Key").toBe("probe-secret");
    });

    await stepScreenshot(page, "Then: settings still show last OK metadata", async () => {
      await expect(page.getByText(/Last OK:/)).toBeVisible();
    });
  });

  test("Given Bearer mode When Test connection Then Authorization Bearer is sent on probe", async ({
    page,
  }) => {
    await page.route(`**/v1/scans/${PING_ID}`, async (route) => {
      if (route.request().method() !== "GET") {
        await route.continue();
        return;
      }
      await route.fulfill({ status: 404, contentType: "application/json", body: "{}" });
    });

    await stepScreenshot(page, "Given: switch to Authorization Bearer", async () => {
      await page.goto("/settings");
      await page.getByRole("radio", { name: /Bearer/i }).check();
    });

    await stepScreenshot(page, "When: run Test connection", async () => {
      const probe = page.waitForRequest(
        (req) => req.method() === "GET" && req.url().includes(`/v1/scans/${PING_ID}`)
      );
      await page.getByRole("button", { name: "Test connection" }).click();
      await expect(page.getByText("Connected")).toBeVisible();
      const req = await probe;
      const auth = req.headers()["authorization"] ?? req.headers()["Authorization"];
      expect(auth, "authenticated probe should use Bearer").toMatch(/^Bearer\s+probe-secret$/i);
    });

    await stepScreenshot(page, "Then: no inline auth error on successful 404 probe", async () => {
      await expect(page.getByRole("alert").filter({ hasText: /don’t have access|don't have access/i })).toHaveCount(
        0
      );
    });
  });

  test("Given authenticated probe returns 401 When testing connection Then inline access alert", async ({
    page,
  }) => {
    await page.route(`**/v1/scans/${PING_ID}`, async (route) => {
      if (route.request().method() !== "GET") {
        await route.continue();
        return;
      }
      await route.fulfill({
        status: 401,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Unauthorized" }),
      });
    });

    await stepScreenshot(page, "Given: Settings page", async () => {
      await page.goto("/settings");
    });

    await stepScreenshot(page, "When: health succeeds then authenticated ping returns 401", async () => {
      await page.getByRole("button", { name: "Test connection" }).click();
      await expect(page.getByText("Connected")).toBeVisible();
    });

    await stepScreenshot(page, "Then: role=alert shows access guidance copy", async () => {
      const alert = page.getByRole("alert").filter({ hasText: /don’t have access|don't have access/i });
      await expect(alert).toBeVisible();
    });
  });
});

test.describe("EPIC-DG-14 BDD — dashboard control plane", () => {
  test.beforeEach(async ({ page }) => {
    await seedConnection(page, { baseUrl: BASE, apiKey: "bdd-key", authKind: "api-key" });
  });

  test("Given healthz returns error When Refresh Then sticky error toast with dismiss", async ({ page }) => {
    await page.route("**/v1/healthz", async (route) => {
      await route.fulfill({ status: 503, body: "unavailable" });
    });

    await stepScreenshot(page, "Given: Dashboard with failing health backend", async () => {
      await page.goto("/dashboard");
    });

    await stepScreenshot(page, "When: user clicks Refresh on Control plane card", async () => {
      await page.getByRole("button", { name: "Refresh" }).click();
    });

    await stepScreenshot(page, "Then: sticky error toast shows control plane unreachable", async () => {
      await expect(page.getByText("Control plane unreachable")).toBeVisible();
    });

    await stepScreenshot(page, "When: operator dismisses the toast", async () => {
      await page.getByRole("button", { name: "Dismiss notification" }).click();
    });

    await stepScreenshot(page, "Then: error toast is removed", async () => {
      await expect(page.getByText("Control plane unreachable")).toHaveCount(0);
    });
  });

  test("Given healthy API When Refresh Then OK badge and latency line without success spam", async ({
    page,
  }) => {
    await mockHealthOk(page);

    await stepScreenshot(page, "Given: Dashboard", async () => {
      await page.goto("/dashboard");
    });

    await stepScreenshot(page, "When: Refresh control plane", async () => {
      await page.getByRole("button", { name: "Refresh" }).click();
    });

    await stepScreenshot(page, "Then: OK badge and GET /v1/healthz line visible", async () => {
      await expect(page.getByText("OK").first()).toBeVisible();
      await expect(page.getByText(/GET \/v1\/healthz/i)).toBeVisible();
    });
  });
});

test.describe("EPIC-DG-14 BDD — New scan client validation", () => {
  test.beforeEach(async ({ page }) => {
    await mockHealthOk(page);
    await seedConnection(page, { baseUrl: BASE, apiKey: "bdd-key", authKind: "api-key" });
  });

  test("Given New scan When policies empty Then client blocks with policy error", async ({ page }) => {
    await stepScreenshot(page, "Given: New scan form with defaults", async () => {
      await page.goto("/scans/new");
      await expect(page.getByRole("heading", { name: /New scan/i })).toBeVisible();
    });

    await stepScreenshot(page, "When: clear Policy IDs and submit", async () => {
      await page.getByLabel(/Policy IDs/i).fill("");
      await page.getByRole("button", { name: "Create scan" }).click();
    });

    await stepScreenshot(page, "Then: at least one policy id validation is shown", async () => {
      await expect(page.getByText("Enter at least one policy id.")).toBeVisible();
    });
  });

  test("Given New scan When no layers selected Then scan_layers validation", async ({ page }) => {
    await stepScreenshot(page, "Given: New scan Layers card with all checkboxes off", async () => {
      await page.goto("/scans/new");
      const layerBox = page
        .getByRole("heading", { name: "Layers" })
        .locator("xpath=following-sibling::div[1]");
      await layerBox.getByRole("checkbox").nth(0).uncheck();
      await layerBox.getByRole("checkbox").nth(1).uncheck();
      await layerBox.getByRole("checkbox").nth(2).uncheck();
    });

    await stepScreenshot(page, "Then: Create scan shows layer selection error", async () => {
      await page.getByRole("button", { name: "Create scan" }).click();
      await expect(page.getByText("Select at least one scan layer.")).toBeVisible();
    });
  });

  test("Given Cloud layer only When no repo nor profiles Then cloud validation", async ({ page }) => {
    await stepScreenshot(page, "Given: enable Cloud only and clear Git fields", async () => {
      await page.goto("/scans/new");
      const layers = page.locator("div").filter({ has: page.getByRole("heading", { name: "Layers" }) });
      await layers.getByRole("checkbox").nth(0).uncheck();
      await layers.getByRole("checkbox").nth(1).uncheck();
      await layers.getByRole("checkbox").nth(2).check();
      await page.getByLabel("Repo URL").fill("");
      await page.getByLabel("Ref").fill("");
    });

    await stepScreenshot(page, "When: submit Create scan", async () => {
      await page.getByRole("button", { name: "Create scan" }).click();
    });

    await stepScreenshot(page, "Then: cloud requires repo or profiles message", async () => {
      await expect(page.getByText(/Cloud layer requires/i)).toBeVisible();
    });
  });

  test("Given Archive source When storage URI invalid Then archive validation", async ({ page }) => {
    await stepScreenshot(page, "Given: Archive selected with non-s3 URI", async () => {
      await page.goto("/scans/new");
      await page.getByRole("radio", { name: "Archive", exact: true }).check();
      await page.getByLabel(/Storage URI/i).fill("https://wrong.example/key");
    });

    await stepScreenshot(page, "When: Create scan", async () => {
      await page.getByRole("button", { name: "Create scan" }).click();
    });

    await stepScreenshot(page, "Then: archive storage_uri must start with s3://", async () => {
      await expect(
        page.getByRole("alert").filter({ hasText: /Archive requires storage_uri starting with s3/i })
      ).toBeVisible();
    });
  });
});

test.describe("EPIC-DG-14 BDD — presign prepare-only happy path", () => {
  test.beforeEach(async ({ page }) => {
    await mockHealthOk(page);
    await seedConnection(page, { baseUrl: BASE, apiKey: "bdd-key", authKind: "api-key" });
    await page.route("**/v1/repo-uploads", async (route) => {
      if (route.request().method() !== "POST") {
        await route.continue();
        return;
      }
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          upload_id: "up-1",
          upload_url: `${BASE}/mock-put`,
          upload_headers: { "Content-Type": "application/gzip" },
          storage_uri: "s3://deepguard-bdd/archives/test.tgz",
          expires_in_seconds: 3600,
        }),
      });
    });
  });

  test("Given archive flow When Prepare only Then storage URI auto-filled", async ({ page }) => {
    await stepScreenshot(page, "Given: New scan Archive and open upload modal", async () => {
      await page.goto("/scans/new");
      await page.getByRole("radio", { name: "Archive", exact: true }).check();
      await page.getByRole("button", { name: "Prepare upload" }).click();
      await expect(page.getByRole("dialog", { name: "Upload repo archive" })).toBeVisible();
    });

    await stepScreenshot(page, "When: Prepare only (no file) succeeds", async () => {
      await page.getByRole("dialog", { name: "Upload repo archive" }).getByRole("button", { name: "Prepare only" }).click();
    });

    await stepScreenshot(page, "Then: Storage URI field contains returned s3 URI", async () => {
      await expect(page.getByLabel(/Storage URI/i)).toHaveValue(/s3:\/\/deepguard-bdd\/archives\/test\.tgz/);
      await expect(page.getByText("Prepared")).toBeVisible();
    });
  });
});

test.describe("EPIC-DG-14 BDD — Scans hub registry and Open by ID", () => {
  test.beforeEach(async ({ page }) => {
    await mockHealthOk(page);
    const now = new Date().toISOString();
    await seedConnectionAndRecent(
      page,
      { baseUrl: BASE, apiKey: "k", authKind: "api-key" },
      [
        { scan_id: KNOWN_SCAN, updated_at: now, status: "QUEUED" },
        { scan_id: "c3d4e5f6-a7b8-49c0-9d1e-2f3a4b5c6d7e", updated_at: now, status: "FAILED" },
      ]
    );
    await page.route(`**/v1/scans/${KNOWN_SCAN}`, async (route) => {
      if (route.request().method() !== "GET") {
        await route.continue();
        return;
      }
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: scanDetailJson(),
      });
    });
  });

  test("Given recent scans When Clear list confirmed Then empty state", async ({ page }) => {
    await stepScreenshot(page, "Given: Scans hub shows recent rows", async () => {
      await page.goto("/scans");
      await expect(page.getByRole("heading", { name: "Scans", exact: true })).toBeVisible();
      await expect(page.getByText(new RegExp(`${KNOWN_SCAN.slice(0, 8)}`))).toBeVisible();
    });

    await stepScreenshot(page, "When: Clear list opens confirm modal", async () => {
      await page.getByRole("button", { name: "Clear list" }).filter({ hasText: "Clear list" }).first().click();
      await expect(page.getByRole("dialog", { name: "Clear recent scans?" })).toBeVisible();
    });

    await stepScreenshot(page, "When: confirm destructive clear", async () => {
      await page
        .getByRole("dialog", { name: "Clear recent scans?" })
        .getByRole("button", { name: "Clear list" })
        .filter({ hasText: "Clear list" })
        .last()
        .click();
    });

    await stepScreenshot(page, "Then: empty state with Create scan CTA", async () => {
      await expect(page.getByText("No scans yet.")).toBeVisible();
      await expect(page.getByRole("link", { name: "Create scan" })).toBeVisible();
    });
  });

  test("Given invalid UUID When Open by ID Then alert and button stays disabled", async ({ page }) => {
    await stepScreenshot(page, "Given: Scans hub Open by ID", async () => {
      await page.goto("/scans");
      await page.getByPlaceholder("00000000-0000-4000-8000-000000000000").fill("not-a-uuid");
    });

    await stepScreenshot(page, "Then: validation alert and Open disabled", async () => {
      await expect(page.getByText("Enter a valid UUID.")).toBeVisible();
      await expect(page.getByRole("button", { name: "Open", exact: true })).toBeDisabled();
    });
  });
});

test.describe("EPIC-DG-14 BDD — Scan detail, 404, and cancel modal", () => {
  test.beforeEach(async ({ page }) => {
    await mockHealthOk(page);
    await seedConnection(page, { baseUrl: BASE, apiKey: "bdd-key", authKind: "api-key" });
    await page.route(`**/v1/scans/${KNOWN_SCAN}`, async (route) => {
      if (route.request().method() !== "GET") {
        await route.continue();
        return;
      }
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: scanDetailJson(),
      });
    });
    await page.route(`**/v1/scans/${KNOWN_SCAN}/cancel`, async (route) => {
      if (route.request().method() !== "POST") {
        await route.continue();
        return;
      }
      await route.fulfill({
        status: 202,
        contentType: "application/json",
        body: JSON.stringify({ scan_id: KNOWN_SCAN, cancellation_requested: true }),
      });
    });
  });

  test("Given unknown scan id When detail loads Then not-found card and back link", async ({ page }) => {
    await page.route("**/v1/scans/deadbeef-dead-dead-dead-deadbeefdead", async (route) => {
      if (route.request().method() !== "GET") {
        await route.continue();
        return;
      }
      await route.fulfill({ status: 404, contentType: "application/json", body: "{}" });
    });

    await stepScreenshot(page, "Given: navigate to non-existent scan UUID", async () => {
      await page.goto("/scans/deadbeef-dead-dead-dead-deadbeefdead");
    });

    await stepScreenshot(page, "Then: Scan not found empty state", async () => {
      await expect(page.getByRole("heading", { name: "Scan not found" })).toBeVisible();
      await expect(page.getByRole("button", { name: "Back to scans" })).toBeVisible();
    });
  });

  test("Given scan detail When expand job_config Then JSON visible and aria-expanded true", async ({ page }) => {
    await stepScreenshot(page, "Given: scan detail loads", async () => {
      await page.goto(`/scans/${KNOWN_SCAN}`);
      await expect(page.getByText(KNOWN_SCAN)).toBeVisible();
    });

    await stepScreenshot(page, "When: Expand job_config", async () => {
      await page.getByRole("button", { name: "Expand" }).click();
    });

    await stepScreenshot(page, "Then: job_config contains policy and repo JSON", async () => {
      await expect(page.getByRole("button", { name: "Collapse" })).toHaveAttribute("aria-expanded", "true");
      await expect(page.getByText(/"policy_ids"/)).toBeVisible();
      await expect(page.getByText(/octocat\/Hello-World/)).toBeVisible();
    });
  });

  test("Given cancel modal When Keep scan Then dialog closes without toast", async ({ page }) => {
    await stepScreenshot(page, "Given: open cancel confirmation", async () => {
      await page.goto(`/scans/${KNOWN_SCAN}`);
      await page.getByRole("button", { name: "Request cancel" }).first().click();
      await expect(page.getByRole("dialog", { name: "Cancel scan?" })).toBeVisible();
    });

    await stepScreenshot(page, "When: operator chooses Keep scan", async () => {
      await page.getByRole("dialog", { name: "Cancel scan?" }).getByRole("button", { name: "Keep scan" }).click();
    });

    await stepScreenshot(page, "Then: dialog closed and no cancellation toast", async () => {
      await expect(page.getByRole("dialog", { name: "Cancel scan?" })).toHaveCount(0);
      await expect(page.getByText("Cancellation requested")).toHaveCount(0);
    });
  });

  test("Given cancel confirmed When API accepts Then success toast", async ({ page }) => {
    await stepScreenshot(page, "Given: cancel dialog confirmed", async () => {
      await page.goto(`/scans/${KNOWN_SCAN}`);
      await page.getByRole("button", { name: "Request cancel" }).first().click();
      await page
        .getByRole("dialog", { name: "Cancel scan?" })
        .getByRole("button", { name: "Request cancel" })
        .click();
    });

    await stepScreenshot(page, "Then: cancellation requested toast", async () => {
      await expect(page.getByText("Cancellation requested")).toBeVisible();
    });
  });
});

test.describe("EPIC-DG-14 BDD — form edge cases and accessibility affordances", () => {
  test.beforeEach(async ({ page }) => {
    await mockHealthOk(page);
    await seedConnection(page, { baseUrl: BASE, apiKey: "bdd-key", authKind: "api-key" });
  });

  test("Given New scan When clone depth out of range Then validation message", async ({ page }) => {
    await stepScreenshot(page, "Given: New scan with invalid clone depth", async () => {
      await page.goto("/scans/new");
      await page.getByLabel("Clone depth (optional)").fill("0");
    });
    await stepScreenshot(page, "When: submit Create scan", async () => {
      await page.getByRole("button", { name: "Create scan" }).click();
    });
    await stepScreenshot(page, "Then: clone depth range error", async () => {
      await expect(page.getByText(/Clone depth must be between 1 and 10000/i)).toBeVisible();
    });
  });

  test("Given New scan When webhook URL invalid Then URL validation", async ({ page }) => {
    await stepScreenshot(page, "Given: webhook URL not HTTP(S)", async () => {
      await page.goto("/scans/new");
      await page.getByPlaceholder("https://example.com/hook").fill("not-a-valid-url");
    });
    await stepScreenshot(page, "When: Create scan", async () => {
      await page.getByRole("button", { name: "Create scan" }).click();
    });
    await stepScreenshot(page, "Then: webhook URL error", async () => {
      await expect(page.getByText(/Enter a valid webhook URL/i)).toBeVisible();
    });
  });

  test("Given New scan When budget LLM not positive Then budget validation", async ({ page }) => {
    await stepScreenshot(page, "Given: negative max LLM USD", async () => {
      await page.goto("/scans/new");
      await page
        .getByText("Max LLM USD", { exact: true })
        .locator("xpath=following-sibling::input")
        .fill("-5");
    });
    await stepScreenshot(page, "When: Create scan", async () => {
      await page.getByRole("button", { name: "Create scan" }).click();
    });
    await stepScreenshot(page, "Then: budget validation", async () => {
      await expect(page.getByText(/Must be a positive number/i)).toBeVisible();
    });
  });

  test("Given Settings When toggling Show Then API key field type changes", async ({ page }) => {
    await stepScreenshot(page, "Given: API key masked by default", async () => {
      await page.goto("/settings");
      await expect(page.locator("#key")).toHaveAttribute("type", "password");
    });
    await stepScreenshot(page, "When: click Show", async () => {
      await page.getByRole("button", { name: "Show" }).click();
    });
    await stepScreenshot(page, "Then: key input is text type", async () => {
      await expect(page.locator("#key")).toHaveAttribute("type", "text");
    });
  });
});

test.describe("EPIC-DG-14 BDD — scan detail interactions", () => {
  test.beforeEach(async ({ page }) => {
    await mockHealthOk(page);
    await seedConnection(page, { baseUrl: BASE, apiKey: "bdd-key", authKind: "api-key" });
    let hits = 0;
    await page.route(`**/v1/scans/${KNOWN_SCAN}`, async (route) => {
      if (route.request().method() !== "GET") {
        await route.continue();
        return;
      }
      hits += 1;
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: scanDetailJson({ percent_complete: Math.min(99, 10 + hits) }),
      });
    });
  });

  test("Given scan detail When Refresh clicked Then manual reload succeeds", async ({ page }) => {
    await stepScreenshot(page, "Given: detail page loaded", async () => {
      await page.goto(`/scans/${KNOWN_SCAN}`);
      await expect(page.getByText(KNOWN_SCAN)).toBeVisible();
    });
    await stepScreenshot(page, "When: operator clicks Refresh", async () => {
      await page.getByRole("button", { name: "Refresh" }).click();
    });
    await stepScreenshot(page, "Then: percent still visible", async () => {
      await expect(page.getByText(/%/)).toBeVisible();
    });
  });

  test("Given cancel modal When Escape Then dialog closes", async ({ page }) => {
    await page.route(`**/v1/scans/${KNOWN_SCAN}/cancel`, async (route) => {
      if (route.request().method() !== "POST") {
        await route.continue();
        return;
      }
      await route.fulfill({
        status: 202,
        contentType: "application/json",
        body: JSON.stringify({ scan_id: KNOWN_SCAN, cancellation_requested: true }),
      });
    });
    await stepScreenshot(page, "Given: cancel dialog open", async () => {
      await page.goto(`/scans/${KNOWN_SCAN}`);
      await page.getByRole("button", { name: "Request cancel" }).first().click();
      await expect(page.getByRole("dialog", { name: "Cancel scan?" })).toBeVisible();
    });
    await stepScreenshot(page, "When: press Escape", async () => {
      await page.keyboard.press("Escape");
    });
    await stepScreenshot(page, "Then: dialog is closed", async () => {
      await expect(page.getByRole("dialog", { name: "Cancel scan?" })).toHaveCount(0);
    });
  });
});
