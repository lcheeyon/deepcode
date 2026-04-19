# DeepGuard console (MVP) — wireframes & mockup specification

**Status:** Pre-implementation design artefact  
**Authoring rules:** `.cursor/skills/deepguard-ui-style-guide/SKILL.md` + `reference.md`  
**Product backlog:** `docs/user-stories/EPIC-14-console-frontend-backend-mvp.md`  
**API scope (v0):** `GET /v1/healthz`, `POST|GET /v1/scans`, `POST /v1/scans/{id}/cancel`, `POST /v1/repo-uploads`

This document is the **visual source of truth** until a Figma file exists. Engineers map tokens to **CSS variables** (`--dg-*` from `reference.md` §2) or Tailwind `theme.extend`.

---

## 1. Global layout mockup (desktop ≥1280px)

### 1.1 High-fidelity description

| Region | Spec |
|--------|------|
| **Page background** | `surface.page` `#fafafa` (light) / `#09090b` (dark). |
| **Sidebar** | Fixed **240px** width, `surface.card` with **1px** `border.default` right edge; internal padding **16px** vertical between nav groups. |
| **Logo row** | Product wordmark **DeepGuard** — `Page title` typography (600, 22px); subtitle “Console” `Caption` 12px `text.muted`. |
| **Nav items** | `Body` 14px; active item: **3px left bar** `brand.primary` + `surface.subtle` pill behind label; inactive `text.primary`. |
| **Main column** | Left margin from sidebar **0** (flush); inner padding **24px**; max width **1440px** centred. |
| **Top bar** | Height **56px**, `surface.card` bottom border `border.default`; right cluster: icon buttons **40×40** with `aria-label`. |

### 1.2 ASCII wireframe (desktop)

```text
LIGHT MODE (example)
======================
┌────────────────┬──────────────────────────────────────────────────────────────┐
│ surface.card   │ surface.page                                                  │
│ #ffffff        │ #fafafa                                                       │
│                │ ┌────────────────────────────────────────────────────────────┐ │
│ DeepGuard      │ │ top bar: h-56, border-b, flex justify-end gap-8           │ │
│ Console        │ │                                    (?) (bell) (avatar)   │ │
│                │ └────────────────────────────────────────────────────────────┘ │
│ Tenant ▾       │  Breadcrumb: Scans / New scan                                 │
│ ───────────    │  ┌──────────────────────────────────────────────────────────┐│
│ ■ Dashboard    │  │ Page title (22px semibold)          [Primary: Create …] ││
│ ■ Scans        │  └──────────────────────────────────────────────────────────┘│
│ ○ Findings     │  ┌─ surface.card #fff, radius-md, shadow-sm ────────────────┐│
│   (disabled)   │  │ Form column max-w-[560px]                                 ││
│ ○ Policies     │  │ … fields …                                                ││
│                │  └───────────────────────────────────────────────────────────┘│
│ Settings       │                                                               │
│                │                                                               │
│ v0.1.0  Staging│                                                               │
└────────────────┴──────────────────────────────────────────────────────────────┘
```

---

## 2. Screen: Settings — API connection

### 2.1 Mockup

- **Card:** `surface.card`, `radius-md`, `shadow-sm`, padding **24px**.
- **Fields:** Labels **sentence case**, **12px** gap to input (`§8`).
- **Base URL input:** full width, `radius-sm`, border `border.default`, font **mono 13px** for URL.
- **API key:** `type=password` with secondary **Show** toggle (ghost button `sm`).
- **Primary:** “Test connection” `md` height **40px**, fill `brand.primary` `#4f46e5`, text `text.inverse`.
- **Danger zone** (optional footer in card): `text.muted` 12px — “Keys are stored in browser local storage (MVP).”

### 2.2 Wireframe

```text
┌──────────────── API connection ──────────────────────────────┐
│  surface.card / padding 24 / shadow-sm                       │
│                                                              │
│  Base URL                                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ https://api.staging.example.com                        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  API key                                                     │
│  ┌──────────────────────────────────────┐  [ Show ] ghost │
│  │ ••••••••••••••••••••                   │                  │
│  └──────────────────────────────────────┘                  │
│                                                              │
│  [ Test connection ]  primary                                │
│                                                              │
│  Last result: ● OK  GET /v1/healthz  42ms   caption muted     │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Screen: Dashboard

### 3.1 Mockup

- Two **cards** in a **2-column grid** (`gap-24`, stack to 1 column `<md`).
- **Health card:** title “Control plane” `Section title` 16px 600; badge **OK** = `status.success` text on `status.success.bg` pill `radius-full` px-3 py-1.
- **Refresh:** secondary outline button right side of card header row.
- **Second card:** informational `status.info` icon + “Redis” copy; muted body explaining queue behaviour (no false success if unknown).

### 3.2 Wireframe

```text
  Dashboard                           (Page title 22px)
  ┌─────────────────────┐ ┌─────────────────────┐
  │ Control plane  [↻]  │ │ Background jobs    │
  │ ● OK   28ms         │ │ ℹ When Redis is    │
  │ GET /v1/healthz     │ │ configured, new    │
  │                     │ │ scans are queued.  │
  └─────────────────────┘ └─────────────────────┘
```

---

## 4. Screen: New scan (create)

### 4.1 Mockup

- **Layout:** single column **max 560px** (skill §4); on wide screens align column **start** (not centred) to match data-console bias, or centre if marketing prefers — **default: start** under breadcrumb.
- **Source control:** **segmented control** or two **radio cards** (`surface.subtle` selected, `border.strong`); selected state not by colour alone — **inner ring + label weight 600**.
- **Git branch:** `Repo URL` + `Ref` side by side on `md+` (grid 2 cols gap-16); stack on mobile.
- **Archive branch:** “Prepare upload” opens **modal** (`shadow.lg`, `radius-lg`, §12).
- **Policy chips:** removable chips `radius-full`, `surface.subtle`, X hit target **32px**.
- **Layer toggles:** three **Switch** components with sentence labels to the right.
- **Cloud profile repeater:** each row in nested `surface.subtle` card `radius-md` padding 16.
- **Footer actions:** sticky optional; **Cancel** secondary, **Create scan** primary; **loading** state disables duplicate submit + spinner in button.

### 4.2 Wireframe

```text
  New scan
  ┌──────────────────────────────────────── max 560px ────────────────────────┐
  │ Source                                                                     │
  │  ( • ) Git repository    (   ) Pre-uploaded archive (S3)                  │
  │                                                                            │
  │  Repo URL                                              Ref                 │
  │  [https://github.com/org/repo.git____________]         [main_______]       │
  │                                                                            │
  │  Clone depth [ 50 ]    Sub-path (optional) [ services/api______ ]          │
  │                                                                            │
  │  Policy IDs   [ ISO-27001 × ] [ SOC2 × ]  [ + Add ]                         │
  │                                                                            │
  │  Scan layers   Code [on]  IaC [on]  Cloud [off]                           │
  │                                                                            │
  │  ── Budget (optional) ──                                                 │
  │  Max LLM USD [____]   Max wall (sec) [____]                               │
  │                                                                            │
  │  ── Webhook (optional) ──                                                │
  │  URL [https://hooks.example/____________]                                  │
  │  Events [completed ▼] [failed ▼]                                          │
  │                                                                            │
  │  Idempotency-Key (optional) [________________________]                     │
  │                                                                            │
  │                         [ Cancel ]  [ Create scan ]  ← single primary     │
  └──────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Modal: Repo archive upload

### 5.1 Mockup

- **Scrim:** `surface.page` @ **60% opacity**, `z-index` 200 (`reference.md` §6).
- **Panel:** `surface.elevated` light `#ffffff`, width **560px**, `radius-lg`, padding **24px**, `z-index` 210.
- **Steps:** numbered **Caption** steps 1–2; **progress bar** for PUT uses `brand.primary` fill on `surface.subtle` track.
- **Actions:** “Use this URI in form” **primary** only after PUT **200**; **Cancel** secondary closes modal (confirm if upload in flight).

### 5.2 Wireframe

```text
         SCRIM (dark 60%)
    ┌──────── Upload archive ────────┐
    │ 1. Request presigned URL ✓      │
    │ 2. Upload file …                │
    │ ┌────────────────────────────┐ │
    │ │ file: repo.tar.gz  8 MB    │ │
    │ │ ████████░░  80%            │ │
    │ └────────────────────────────┘ │
    │  [ Cancel ]  [ Use URI in form ]│
    └────────────────────────────────┘
```

---

## 6. Screen: Scans hub (recent + open by ID)

### 6.1 Mockup

- **Table:** dense row height, **8px** vertical cell padding (`§9`); header row `text.muted` **600** 12–13px (not forced ALL CAPS).
- **Columns:** Started (left), Scan ID (mono), Status (badge), Stage % (right tabular), Actions (right, ghost **View**).
- **Empty state:** illustration optional; **primary** “Create scan” + `text.muted` helper line.

### 6.2 Wireframe

```text
  Scans
  ┌────────────────────────────────────────────────────────────────────────────┐
  │ [ + New scan ] primary                                                      │
  │                                                                             │
  │ Open by ID  [ uuid paste field ──────────────────────── ] [ Open ] secondary│
  │                                                                             │
  │ Recent on this device                                                     │
  │ ┌───────────┬────────────────────┬──────────┬─────┬────────┐               │
  │ │ Started   │ Scan ID            │ Status   │ %   │ Actions│               │
  │ ├───────────┼────────────────────┼──────────┼─────┼────────┤               │
  │ │ 10:02     │ 3fa2…c91 (mono)      │ Queued ● │ 0   │ View   │               │
  │ └───────────┴────────────────────┴──────────┴─────┴────────┘               │
  └────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Screen: Scan detail

### 7.1 Mockup

- **Header row:** `Page title` = short UUID ellipsis middle; right: **Refresh** secondary, **Request cancel** outline **destructive** border `status.error` text `status.error` (not fill until confirm).
- **Status row:** horizontal flex: **Badge** (`QUEUED`), **pipe** `text.muted`, stage text, **pipe**, `percent_complete` **tabular** with `%`.
- **JSON panel:** `surface.subtle`, `radius-md`, padding **16px**, `mono` 13px; syntax colours optional (theme-aware); collapse control is **tertiary** chevron with `aria-expanded`.

### 7.2 Wireframe

```text
  Scan  …c91f
  ┌──────────────────────────────────────────────────────────────────────────┐
  │ [Queued]  INGESTING  ·  15%                    [ Refresh ] [ Cancel… ]   │
  │                                                                           │
  │ Repo commit sha (mono)                                                    │
  │ a1b2c3d4e5f6…                         (or “—” if null)                   │
  │                                                                           │
  │ job_config                                                                │
  │ ┌ surface.subtle mono 13px ────────────────────────────────────────────┐ │
  │ │ {                                                                      │ │
  │ │   "repo": { "source": "git", "url": "https://…", "ref": "main" },      │ │
  │ │   "policy_ids": [ "ISO-27001-2022" ],                                   │ │
  │ │   …                                                                    │ │
  │ │ }                                                                      │ │
  │ └────────────────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Toast & error stack (global)

### 8.1 Mockup

- **Position:** bottom-right desktop (`§11`), top on `<md`.
- **Success:** `status.success.bg` left border 4px solid `status.success`, auto-dismiss **4s**.
- **Error (API):** sticky until dismissed; title + body from `reference.md` §3.2; include **`error_code`** from JSON body when present (`REPO_UPLOAD_S3_UNCONFIGURED`, etc.).

### 8.2 Wireframe

```text
                                    ┌ Toast (shadow-lg) ──────┐
                                    │ ✓ Scan queued           │
                                    │ You will see status…    │
                                    └─────────────────────────┘
```

---

## 9. Component inventory (implementation checklist)

| Component | Token / rule |
|-----------|----------------|
| Button primary | `brand.primary`, hover `brand.primary.hover`, focus ring `focus.ring` |
| Button secondary | Ghost/outline on `surface.card` |
| Input | `radius-sm`, h-40, border `border.default`, focus border `brand.primary` |
| Badge status | `status.*` + dot icon |
| Modal | `radius-lg`, `shadow.lg`, focus trap |
| Table | zebra optional `surface.subtle`, sticky header `z-10` |

---

## 10. Out of scope (placeholder nav)

Sidebar items **Findings**, **Policies**, **Reports** render **disabled** with `cursor-not-allowed`, `text.disabled`, tooltip: “Not in API yet — see EPIC-DG-12.” Do **not** navigate to broken routes.

---

## 11. Sign-off gate (before coding)

- [ ] Product owner accepts **EPIC-DG-14** story list.  
- [ ] Design review accepts **this document** + token compliance with **UI skill**.  
- [ ] Engineering spikes: **CORS** for `PUT` to presigned S3/MinIO from browser origin; document dev proxy if needed.
