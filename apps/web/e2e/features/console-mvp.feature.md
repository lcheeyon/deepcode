# BDD scenarios — DeepGuard console MVP (EPIC-DG-14)

Human-readable mirror of `e2e/console.spec.ts`. Automation uses **Playwright**; exploratory checks may use **agent-browser** (`scripts/agent-browser-smoke.sh`).

**HTML report:** each automated step calls `stepScreenshot()` so the Playwright HTML report includes a **full-page screenshot** per BDD step (`npx playwright show-report playwright-report`).

## Feature: API connectivity

**Scenario: Health succeeds**  
Given saved API base URL and (optional) key  
When the operator runs **Test connection**  
Then `GET /v1/healthz` returns 200 and a success toast is shown.

## Feature: Create and inspect scan

**Scenario: Git scan happy path**  
Given a valid `CreateScanRequest` for Git + code layer  
When the operator submits **Create scan**  
Then the UI navigates to scan detail and shows the `scan_id`.

**Scenario: Cancel scan**  
Given an existing scan id  
When the operator confirms **Request cancel**  
Then `POST /v1/scans/{id}/cancel` returns 202 and a success toast appears.
