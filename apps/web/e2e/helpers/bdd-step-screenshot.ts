import { test, type Page } from "@playwright/test";

function attachmentName(stepTitle: string): string {
  const base = stepTitle
    .replace(/[^\w.-]+/g, "-")
    .replace(/^-+/g, "")
    .replace(/-+$/g, "");
  return `${base || "step"}.png`;
}

/**
 * BDD-style `test.step` with a **full-page PNG** attached to the Playwright HTML report
 * (visible under each step when you open a test in the report UI).
 */
export async function stepScreenshot(
  page: Page,
  stepTitle: string,
  action: () => Promise<void>
): Promise<void> {
  await test.step(stepTitle, async () => {
    await action();
    await test.info().attach(attachmentName(stepTitle), {
      body: await page.screenshot({
        fullPage: true,
        animations: "disabled",
      }),
      contentType: "image/png",
    });
  });
}
