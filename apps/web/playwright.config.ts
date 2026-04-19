import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 1 : undefined,
  /* HTML report: `npx playwright show-report playwright-report` (default UI often http://127.0.0.1:9324 ).
   * Each BDD step uses `stepScreenshot()` to attach a full-page PNG under that step. */
  reporter: [
    ["list"],
    ["html", { open: "never", outputFolder: "playwright-report" }],
    /* Used by scripts/playwright_bdd_report_to_pdf.py to build one PDF with step screenshots. */
    ["json", { outputFile: "playwright-report/results.json" }],
  ],
  use: {
    baseURL: "http://127.0.0.1:3000",
    trace: process.env.PW_TRACE === "1" ? "on" : "on-first-retry",
    /* Extra end-of-test capture (step-level screenshots are primary). */
    screenshot: "only-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: "npm run dev",
    url: "http://127.0.0.1:3000",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
