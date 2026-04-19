---
name: deepguard-ui-style-guide
description: >-
  DeepGuard (玄武) product UI: semantic color tokens, typography, spacing,
  buttons, form patterns, navigation shell, notifications, tables, modals,
  motion, and accessibility. Use when building or reviewing any frontend
  (console, marketing pages, Storybook, Next.js, Playwright-visible UI), when
  the user asks for layout, styling, design system, toast, menu, or visual
  consistency, or when implementing EPIC-DG-12 (console) UI slices.
---

# DeepGuard — UI design style guide (agent instructions)

**Scope:** All user-visible web UI for DeepGuard. **Default language of UI strings:** English; structure copy so **i18n** can swap strings later (no hard-coded concatenation with variables in the middle of a sentence—use ICU-style placeholders in comments or message keys).

**Companion docs:** Token tables, spacing matrix, and notification copy deck: [reference.md](reference.md).

**Using the same rules in Claude:** Copy this folder’s `SKILL.md` and `reference.md` into a Claude Project’s **Instructions** or **Knowledge**, or paste the sections you need. The rules are tool-agnostic markdown.

---

## 1. Principles (non-negotiable)

1. **Clarity over decoration** — Dense compliance workflows; reduce chrome, maximize legibility and scanability.
2. **Predictable hierarchy** — One primary action per surface; destructive actions never share equal weight with primary.
3. **Honest status** — Show real system state (loading, partial failure, stale data); never fake success.
4. **Accessible by default** — WCAG **2.2 AA** minimum for text contrast, focus, targets, and announcements (see §15).
5. **Calm motion** — Respect `prefers-reduced-motion`; no gratuitous animation on data tables or forms.

---

## 2. Semantic color tokens (light / dark)

Use **semantic names** in code (CSS variables or design tokens), not raw hex in components.

| Token role | Light usage | Dark usage |
|------------|-------------|------------|
| `surface.page` | App background | Same role, darker base |
| `surface.card` | Panels, cards | Elevated layer (+1 step) |
| `surface.subtle` | Table stripes, sidebars | Slightly lifted from page |
| `border.default` | Dividers, inputs | Visible but not harsh |
| `text.primary` | Body, headings | High contrast |
| `text.muted` | Secondary labels, meta | Still ≥ 4.5:1 on surface where feasible |
| `text.disabled` | Inactive only | Do not rely on color alone |
| `brand.primary` | Primary buttons, key links, focus ring | Same hue, adjusted luminance |
| `status.success` | Passed checks, saved | |
| `status.warning` | Attention, quota | |
| `status.error` | Failed scan, validation | |
| `status.info` | Neutral system messages | |

**Rules**

- **Never** use pure `#000` text on pure `#fff` for large areas; use `text.primary` / `surface.page` pairs from the reference scale.
- **Charts:** distinct hues from status colors where possible; provide pattern or label redundancy for color-blind users.
- Full hex tables: [reference.md](reference.md#1-color-palette).

---

## 3. Typography

| Role | Weight | Size (desktop) | Line height | Letter-spacing |
|------|--------|----------------|-------------|----------------|
| Display (rare) | 600 | 28–32px | 1.2 | -0.02em |
| Page title | 600 | 22–24px | 1.25 | -0.01em |
| Section title | 600 | 16–18px | 1.3 | normal |
| Body | 400 | 14–15px | 1.5 | normal |
| Body strong | 600 | 14–15px | 1.5 | normal |
| Caption / meta | 400 | 12–13px | 1.45 | normal |
| Mono (IDs, paths, JSON) | 400 | 13px | 1.45 | normal |

**Font stack:** `ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji"`. **Mono:** `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace`.

**Rules:** Title Case for **navigation** and **page titles**; **Sentence case** for buttons, labels, and body. Avoid ALL CAPS except **≤3 letter** abbreviations and legal acronyms. Truncate long file paths with middle-ellipsis in tables.

---

## 4. Spacing & layout

- **Base unit:** **4px**. Use multiples only: 4, 8, 12, 16, 24, 32, 40, 48, 64.
- **Page padding:** 24px desktop, 16px mobile; max content width **1440px** with fluid side padding for console pages.
- **Card padding:** 16–24px; **dense tables** 8px vertical / 12px horizontal cell padding.
- **Grid:** 12-column mental model for dashboards; single-column forms max **560px** width for readability.

---

## 5. Radius, stroke, elevation

- **Radius:** `sm` 6px (inputs, small buttons), `md` 8px (cards, buttons), `lg` 12px (modals), `full` for pills only.
- **Border:** 1px `border.default`; **no** double borders between stacked cards—use gap or shadow.
- **Elevation:** `shadow.sm` for cards at rest; `shadow.md` for popovers/dropdowns; `shadow.lg` for modals. Dark mode: prefer lighter border + subtle shadow over heavy glow.

---

## 6. Buttons

| Variant | When to use |
|---------|-------------|
| **Primary** | Single main action (Save, Create scan, Submit). **Max one** primary per view (excluding sticky footers for the same action). |
| **Secondary** | Alternative safe actions (Cancel route change, Back). Outline or ghost on `surface.card`. |
| **Tertiary / ghost** | Inline actions in tables (View, Expand), low emphasis. |
| **Destructive** | Irreversible or dangerous (Delete tenant, Purge data). Always confirm (modal). Red label; not used for “Remove filter”. |
| **Icon-only** | Toolbar only; **must** have `aria-label` and optional tooltip with matching text. Min hit target **40×40px** (extend tap area if icon is smaller). |

**Sizes:** `sm` height 32px, `md` **40px** (default), `lg` 48px (marketing / rare empty states).

**States:** `hover`, `active`, `focus-visible` (ring 2px `brand.primary` offset 2px), `disabled` (reduced opacity + `cursor: not-allowed` + no pointer events), `loading` (spinner replaces label or trailing spinner; keep button width stable).

**Loading:** Disable duplicate submit; show spinner + “Saving…” text for long operations (>400ms).

---

## 7. Links

- Default: `brand.primary` + underline on **hover** (not always on by default if inline in dense text—then underline on hover only).
- Visited: same as unvisited in app chrome (avoid confusion); optional distinction in long-form docs only.
- External: append “opens in new tab” in `aria-label` and optional icon.

---

## 8. Forms

- **Label** above control; **12px** gap to input. Required: asterisk in label + `aria-required="true"`.
- **Help text** below field, `text.muted`, 12px. **Error text** replaces help text in error state; `role="alert"` on live region.
- **Placeholders:** examples only, never the sole label. **Do not** use placeholder as substitute for help text.
- **Select / combobox:** show **empty** state explicitly (“Select tenant…”).
- **Toggles:** sentence to the right (“Enable webhook retries”); state change announces via live region when outcome is non-obvious.

---

## 9. Tables (data-heavy console)

- **Header:** sticky on vertical scroll; `text.muted` uppercase **not** required—use **600** weight + smaller caption size for contrast.
- **Zebra:** optional `surface.subtle` alternating rows; **hover** full-row highlight.
- **Numeric columns:** right-align; use tabular nums (`font-variant-numeric: tabular-nums`).
- **Actions column:** right-align; icon buttons with labels in menu if >2 actions.
- **Empty table:** illustration optional; primary CTA to create first entity + link to docs.

---

## 10. Navigation & information architecture

**App shell (desktop):**

- **Left sidebar (240px)** — product mark + tenant switcher at top; **primary nav** grouped: *Scans*, *Findings*, *Policies*, *Reports*, *Settings* (adjust to roadmap). Collapse to icons **≥1280px** optional; persist user preference.
- **Top bar** — global search (optional), **notifications** bell, **help/docs**, **user menu** (profile, API keys, sign out).
- **Breadcrumbs** below top bar on nested routes: `Tenant / Scans / Scan abc123`.

**Mobile:** bottom nav **or** hamburger with same IA order as desktop; **no** hidden-only critical actions.

**Active state:** `surface.subtle` pill or **3px** left border `brand.primary` on active item; do not rely on color alone.

Full skeleton: [reference.md](reference.md#4-application-shell-wireframe).

---

## 11. Notifications

| Channel | Use for | Duration / dismissal |
|---------|---------|----------------------|
| **Toast (stack bottom-right desktop, top mobile)** | Fast feedback after user action | Success 4s auto; error **sticky** until dismissed |
| **Inline alert** | Page-level errors, read-only banners | Dismiss or persist until condition clears |
| **Banner (below top bar)** | Maintenance, trial expiry | Sticky; one banner max; severity color + icon |
| **Modal** | Destructive confirm, legal consent | Explicit buttons only |

**Copy rules:** Lead with **outcome** (“Scan queued”) not subsystem (“POST succeeded”). Errors: **what failed** + **what to do next** + optional error ID. See copy deck: [reference.md](reference.md#3-notification-copy-deck).

**Do not** toast on **every** background poll success; batch or silent refresh.

---

## 12. Modals & drawers

- **Modal:** max width **560px** (forms) / **720px** (read-only detail); **16px** padding mobile full-bleed safe area.
- **Focus trap** + return focus on close; **Escape** closes only if no dirty unsaved form (otherwise confirm).
- **Drawer:** filters, scan timeline, secondary detail; width **400px** default; **overlay** scrim `surface.page` @ 60% opacity.

---

## 13. Tags, badges, chips

- **Status badge:** noun + state (“Queued”, “Running”, “Failed”); color + **dot** or icon.
- **Count chips:** neutral background; **≤99** show as number; **100+** show `99+`.
- **Removable filter chips:** X with 32px min target; announce removal to screen readers.

---

## 14. Motion

- **Duration:** 150–200ms for color/size; **250–300ms** for panel slide max.
- **Easing:** `cubic-bezier(0.4, 0, 0.2, 1)` standard; **no** bounce on enterprise chrome.
- **`prefers-reduced-motion: reduce`:** replace transitions with instant state change; keep opacity fade ≤100ms or none.

---

## 15. Accessibility checklist (agents must verify)

- [ ] Text contrast **≥ 4.5:1** body; **≥ 3:1** large text / UI icons on surfaces.
- [ ] Focus visible on all interactive elements; no `outline: none` without replacement ring.
- [ ] Hit target **≥ 24×24px** minimum; **40×40** for icon-only in toolbars.
- [ ] Form errors associated with fields (`aria-describedby`); alerts use `role="alert"` or `aria-live="polite"` appropriately.
- [ ] Tables: `<th scope="col|row">`; captions or `aria-label` on complex tables.
- [ ] Modals: `aria-modal="true"`, labelled `aria-labelledby` or `aria-label`.
- [ ] Images: `alt` text; decorative images `alt=""`.

---

## 16. Anti-patterns (reject in review)

- Multiple competing primary buttons on one screen.
- Success toasts for **no-op** or background-only operations user did not trigger.
- **Red** text for non-error emphasis.
- Disabled primary with **no** explanation why (use tooltip or inline hint).
- **Hamburger-only** primary nav on desktop for core product.
- Custom scrollbars that hide scroll position or break trackpad behavior.

---

## 17. Implementation note (stack-agnostic)

Map tokens to **CSS variables** (e.g. `--dg-surface-page`) or your design tool; in **Tailwind**, extend `theme.colors` once and use semantic aliases. In **Next.js / React**, prefer a single `ThemeProvider` and typed token object so Playwright and Storybook stay aligned.

When unsure, **read** [reference.md](reference.md) for hex values and example strings—do not invent one-off colors outside the scale.
