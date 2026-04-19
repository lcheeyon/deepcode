# EPIC-DG-14 — BDD scenario catalog (console MVP)

Normative BDD text for **EPIC-DG-14**. Each `##` heading matches an **AC-DG-14-*** id from `docs/user-stories/EPIC-14-console-frontend-backend-mvp.md` (GitHub anchor: slug of the heading, e.g. `#ac-dg-14-001-01`).

**Traceability:** `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv` links each AC to Playwright specs, CI job `web-console-e2e`, artifact `playwright-report-console`, workflow URL template, and `reports/playwright-bdd-report.pdf`.

---

## AC-DG-14-001-01

**Acceptance criterion (epic):** CSS variables / Tailwind map to semantic tokens in reference.md section 1; no raw hex in components except token definitions.

```gherkin
Scenario: Surfaces use semantic tokens
  Given the console shell and cards are rendered in the default theme
  When a reviewer inspects component styles against reference.md section 1
  Then surfaces use semantic tokens such as surface.page, surface.card, text.primary, and brand.primary
    And raw hex literals do not appear in component code outside token definition files

Scenario: Brand primary matches light and dark reference
  Given the app is in light theme
  Then brand primary resolves to the documented light value for primary actions
  When the user switches to dark theme
  Then brand primary resolves to the documented dark value for primary actions
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-001-02

**Acceptance criterion (epic):** One primary button per viewport; destructive actions use destructive variant + confirm modal.

```gherkin
Scenario: Single primary action per viewport
  Given the user is on a screen with a form and a page-level primary CTA
  When the viewport is fully visible
  Then only one control is styled as the primary button at that level of hierarchy

Scenario: Destructive cancel requires confirmation
  Given the user initiates a cooperative cancel or other destructive flow
  When the destructive control is activated
  Then a confirm modal opens using the destructive button variant
    And the scan is not cancelled until the user confirms in the modal
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-001-03

**Acceptance criterion (epic):** Sidebar order: logo, tenant, Scans, then disabled placeholders (Findings, Policies, Reports) with tooltip until EPIC-12.

```gherkin
Scenario: Navigation order and placeholders
  Given the app shell sidebar is visible
  When the user reads the sidebar from top to bottom
  Then the order is logo, tenant selector, Scans, then Findings, Policies, and Reports
    And Findings, Policies, and Reports are visibly disabled or placeholder
    And hovering or focusing those entries explains they are not available in the API yet
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-001-04

**Acceptance criterion (epic):** Footer shows app version + environment pill using surface.subtle and text.muted.

```gherkin
Scenario: Footer shows version and environment
  Given the user scrolls to the app shell footer
  Then the application version string is visible
    And an environment pill uses surface.subtle and text.muted styling
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-002-01

**Acceptance criterion (epic):** Test connection calls GET /v1/healthz without auth; success shows toast per reference.md section 3.1.

```gherkin
Scenario: Test connection probes healthz
  Given the user has entered a base URL on Settings
  When they choose Test connection
  Then the client issues GET /v1/healthz without authentication headers
    And a success path shows a toast consistent with reference.md section 3.1 (Saved / Connected)
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-002-02

**Acceptance criterion (epic):** Authenticated requests send X-API-Key; optional toggle for Authorization Bearer instead (mutually exclusive).

```gherkin
Scenario: API key mode sends X-API-Key
  Given API key authentication mode is selected in settings
  When the SPA issues an authenticated request such as POST /v1/scans
  Then the request includes X-API-Key and does not send a Bearer token for the same request

Scenario: Bearer mode sends Authorization only
  Given Bearer token mode is selected instead of API key mode
  When the SPA issues an authenticated request
  Then the request includes Authorization Bearer and not X-API-Key
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-002-03

**Acceptance criterion (epic):** On 401, show inline alert with status.error.bg and role=alert; copy reflects access denial where applicable.

```gherkin
Scenario: Unauthorized responses surface inline
  Given stored credentials are invalid or expired for the configured base URL
  When an authenticated API call returns 401
  Then an inline alert is shown with role="alert" and status.error.bg styling
    And the copy reflects that the user does not have access where applicable
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-003-01

**Acceptance criterion (epic):** Dashboard Refresh triggers GET /v1/healthz; loading uses skeleton or spinner on the card only (no global success toast on poll).

```gherkin
Scenario: Refresh loads health on the dashboard card
  Given the user is on the Dashboard
  When they activate Refresh on the control plane card
  Then the client calls GET /v1/healthz
    And loading feedback is confined to skeleton or spinner on that card
    And there is no global success toast for routine polling or refresh
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-003-02

**Acceptance criterion (epic):** If health fails, show sticky error toast until dismissed (reference.md section 3.2).

```gherkin
Scenario: Health failure shows sticky error toast
  Given GET /v1/healthz fails or returns an error state
  When the dashboard surfaces the failure
  Then a sticky error toast appears per reference.md section 3.2
    And the toast remains until the user dismisses it
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-004-01

**Acceptance criterion (epic):** Client validation mirrors Pydantic: layers, repo/archive rules, policy_ids min 1, archive needs s3 storage_uri without url (RepoSpec).

```gherkin
Scenario: Layers and policies validated before submit
  Given the user is on New scan
  When they attempt to submit without selecting at least one layer or without at least one policy
  Then client-side validation blocks submit with clear field-level messaging

Scenario: Archive source requires S3 URI not Git URL
  Given archive source is selected
  When storage_uri is missing, not s3://, or a Git url field is incorrectly filled for archive mode
  Then validation explains the RepoSpec / Pydantic-aligned rules before POST /v1/scans

Scenario: Cloud layer requires repo and/or profiles
  Given Cloud layer is enabled
  When required repo or cloud profile inputs are missing
  Then the form shows validation consistent with server-side Pydantic rules
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-004-02

**Acceptance criterion (epic):** Successful 201 shows toast Scan queued, navigates to scan detail, appends scan_id to recent scans.

```gherkin
Scenario: Create scan success flow
  Given a valid CreateScanRequest can be built from the form
  When POST /v1/scans returns 201 Created
  Then a toast Scan queued appears per reference.md section 3.1
    And the app navigates to the scan detail route for the new scan_id
    And the new scan appears in the recent scans registry for this browser
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-004-03

**Acceptance criterion (epic):** 422 maps field errors to inline role=alert per field (style guide section 8).

```gherkin
Scenario: Validation errors map to fields
  Given the server responds 422 with structured field errors
  When the create-scan response is handled
  Then each affected field shows an inline message with role="alert"
    And messaging follows style guide section 8
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-005-01

**Acceptance criterion (epic):** 503 REPO_UPLOAD_S3_UNCONFIGURED shows inline alert + link to docs / .env.example; no crash.

```gherkin
Scenario: Unconfigured S3 upload is handled gracefully
  Given POST /v1/repo-uploads returns 503 with REPO_UPLOAD_S3_UNCONFIGURED
  When the upload preparation UI receives that response
  Then an inline alert explains S3 is not configured
    And guidance points to documentation or .env.example variables
    And the SPA does not crash
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-005-02

**Acceptance criterion (epic):** On presign success, auto-fill storage_uri on create-scan form with sentence-case labels.

```gherkin
Scenario: Presign result fills archive URI
  Given repo upload presign succeeds
  When the user applies the result to the create flow
  Then storage_uri on the New scan form is auto-filled from the API response
    And visible labels use sentence case
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-005-03

**Acceptance criterion (epic):** Browser PUT uses upload_headers from API; CORS failures show generic error deck with optional request id if present.

```gherkin
Scenario: Upload PUT honors API headers
  Given the client has upload_url and upload_headers from POST /v1/repo-uploads
  When the browser performs the PUT of the archive file
  Then request headers match upload_headers including Content-Type as specified

Scenario: CORS or network failure on PUT
  Given the PUT fails due to CORS or network
  When the error is surfaced to the user
  Then copy uses the Something went wrong pattern
    And a request id is shown only when middleware exposes it
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-006-01

**Acceptance criterion (epic):** Poll GET /v1/scans/{id} every 5s with backoff when tab hidden; no toast on each successful poll.

```gherkin
Scenario: Detail polling while tab visible
  Given the user is viewing a scan detail page
  When the tab stays visible
  Then the client polls GET /v1/scans/{id} approximately every five seconds
    And successful polls do not emit a toast each time

Scenario: Hidden tab reduces polling aggressiveness
  Given the scan detail page is open
  When the browser tab becomes hidden
  Then polling backs off according to the EPIC-12 style pattern
    And resumes a normal interval when the tab is visible again
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-006-02

**Acceptance criterion (epic):** 404 shows dedicated empty state Scan not found with link back to Scans hub.

```gherkin
Scenario: Unknown scan id
  Given GET /v1/scans/{id} returns 404
  When the detail page loads or refreshes
  Then an empty state explains the scan was not found
    And a link returns the user to the Scans hub
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-006-03

**Acceptance criterion (epic):** job_config viewer is read-only; expand/collapse uses accessible control with aria-expanded.

```gherkin
Scenario: Job config inspection
  Given scan detail includes job_config JSON
  When the user toggles expand or collapse
  Then the control exposes aria-expanded appropriately
    And the JSON content cannot be edited in the UI
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-007-01

**Acceptance criterion (epic):** POST cancel 202 shows success toast + refresh; 404 shows error toast + message body.

```gherkin
Scenario: Cancel accepted
  Given the user confirms cancel on an active scan
  When POST /v1/scans/{id}/cancel returns 202
  Then a success toast is shown and detail state refreshes

Scenario: Cancel on missing scan
  Given cancel is requested for a non-existent id
  When the API returns 404
  Then an error toast appears including the response message where available
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-007-02

**Acceptance criterion (epic):** Cancel modal obeys focus trap and Escape per style guide section 12.

```gherkin
Scenario: Modal accessibility for cancel
  Given the cancel confirmation modal is open
  When the user presses Tab and Shift+Tab
  Then focus remains trapped within the modal
  When the user presses Escape
  Then the modal closes per style guide section 12 behaviour for this flow
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-008-01

**Acceptance criterion (epic):** Persist last 50 scan entries in localStorage; clear list with destructive confirm.

```gherkin
Scenario: Recent scans cap and persistence
  Given the user has created or opened many scans in one browser
  When entries are stored in localStorage
  Then at most fifty recent items are retained with updated_at metadata

Scenario: Clear recent scans
  Given recent scans exist
  When the user chooses clear list
  Then a destructive confirmation is required before localStorage entries are removed
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-008-02

**Acceptance criterion (epic):** Open by ID validates UUID before issuing GET.

```gherkin
Scenario: Invalid UUID blocked client-side
  Given the user enters a non-UUID string in Open by ID
  When they submit open
  Then the client does not call GET /v1/scans/{id}
    And validation explains the expected UUID format
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-009-01

**Acceptance criterion (epic):** Status badges use status.* tokens; dot + label, not colour alone.

```gherkin
Scenario: Status chip semantics
  Given a scan is in a known API status such as QUEUED or INGESTING
  When the UI renders the status badge
  Then colours map through status.* design tokens
    And each badge pairs a dot with a text label for non-colour-only cues
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-009-02

**Acceptance criterion (epic):** percent_complete uses tabular numerals; right-align in tables.

```gherkin
Scenario: Progress numbers are tabular
  Given percent_complete is shown in the UI or a table column
  When values update during polling
  Then numbers use tabular lining figures
    And table layouts right-align the percentage column where applicable
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-010-01

**Acceptance criterion (epic):** Below lg, sidebar becomes drawer with overlay z-index per reference.md section 6; desktop keeps critical actions out of hamburger-only traps.

```gherkin
Scenario: Mobile drawer navigation
  Given the viewport width is below the lg breakpoint
  When the user opens navigation
  Then the sidebar appears as a drawer with an overlay using the documented z-index stacking

Scenario: Desktop critical actions
  Given the viewport is at or above lg
  When primary navigation and scans actions are used
  Then critical actions are not only reachable through a hamburger icon per style guide section 16
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-010-02

**Acceptance criterion (epic):** Page padding 16px on small breakpoints (style guide section 4).

```gherkin
Scenario: Compact viewport padding
  Given the viewport matches small breakpoints
  When main page content is laid out
  Then horizontal page padding is sixteen pixels per style guide section 4
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-011-01

**Acceptance criterion (epic):** WCAG baseline: contrast, focus ring on brand.primary, targets, aria on tables/modals/forms (skill section 15).

```gherkin
Scenario: Keyboard and screen reader baseline
  Given focus moves through shell, forms, tables, and modals
  Then visible focus rings use brand.primary with two pixel ring and offset as specified
    And interactive targets meet minimum touch and pointer sizes
    And tables, modals, and form controls expose appropriate aria attributes
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-011-02

**Acceptance criterion (epic):** prefers-reduced-motion removes non-essential motion (skill section 14).

```gherkin
Scenario: Reduced motion respected
  Given the OS requests prefers-reduced-motion: reduce
  When the user navigates the console
  Then non-essential animations are suppressed while essential feedback remains clear
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-012-01

**Acceptance criterion (epic):** Dark mode toggle persists; all screens use dark column from reference.md section 1.

```gherkin
Scenario: Theme persistence
  Given the user enables dark mode
  When they reload the application or navigate between routes
  Then dark mode remains selected
    And surfaces resolve using the dark column tokens from reference.md section 1
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-012-02

**Acceptance criterion (epic):** Avoid pure #000 on #fff large fields in dark mode (skill section 2).

```gherkin
Scenario: Dark mode field contrast
  Given dark mode is active
  When large text fields and surfaces are rendered
  Then colour pairs avoid pure black on pure white for extended reading areas
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-013-01

**Acceptance criterion (epic):** Playwright smoke: health, create scan (git stub), GET detail, assert visible scan_id in CI.

```gherkin
Scenario: Automated MVP path in CI
  Given a mocked or dockerised API is available to the Playwright suite
  When the web-console-e2e job runs
  Then tests exercise GET /v1/healthz or equivalent connection check
    And a scan is created with a git-style stub payload
    And GET /v1/scans/{id} is exercised
    And the HTML report shows the scan_id assertion as evidence
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

## AC-DG-14-014-01

**Acceptance criterion (epic):** apps/web README documents NEXT_PUBLIC_* env vars, API base URL, and wireframes doc link.

```gherkin
Scenario: Contributor onboarding
  Given a new developer opens apps/web README
  Then NEXT_PUBLIC_* variables are documented with purpose
    And API base URL configuration is explained
    And docs/design/frontend-console-mvp-wireframes-and-mockups.md is linked as the visual reference
```

*Automation coverage and spec file hints:* see the matching row in `docs/user-stories/traceability-epic-dg-14-bdd-evidence.csv`.

