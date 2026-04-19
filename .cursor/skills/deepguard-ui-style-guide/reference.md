# DeepGuard UI style guide — reference

Companion to `SKILL.md`. Use for concrete hex values, copy patterns, and IA skeletons.

---

## 1. Color palette

Map these to CSS variables (example names). **Light** and **dark** pairs preserve hue relationships.

### 1.1 Surfaces & borders (Zinc-based neutrals)

| Token | Light (hex) | Dark (hex) |
|-------|---------------|------------|
| `surface.page` | `#fafafa` | `#09090b` |
| `surface.subtle` | `#f4f4f5` | `#18181b` |
| `surface.card` | `#ffffff` | `#18181b` |
| `surface.elevated` | `#ffffff` | `#27272a` |
| `border.default` | `#e4e4e7` | `#3f3f46` |
| `border.strong` | `#d4d4d8` | `#52525b` |

### 1.2 Text

| Token | Light | Dark |
|-------|-------|------|
| `text.primary` | `#18181b` | `#fafafa` |
| `text.muted` | `#52525b` | `#a1a1aa` |
| `text.disabled` | `#a1a1aa` | `#52525b` |
| `text.inverse` | `#fafafa` | `#18181b` |

### 1.3 Brand & focus

| Token | Light | Dark |
|-------|-------|------|
| `brand.primary` | `#4f46e5` (indigo-600) | `#818cf8` (indigo-400) |
| `brand.primary.hover` | `#4338ca` | `#6366f1` |
| `brand.primary.muted` | `#eef2ff` | `#312e81` |
| `focus.ring` | same as `brand.primary` | same |

### 1.4 Status

| Token | Light | Dark |
|-------|-------|------|
| `status.success` | `#059669` | `#34d399` |
| `status.success.bg` | `#ecfdf5` | `#064e3b` |
| `status.warning` | `#d97706` | `#fbbf24` |
| `status.warning.bg` | `#fffbeb` | `#78350f` |
| `status.error` | `#e11d48` | `#fb7185` |
| `status.error.bg` | `#fff1f2` | `#881337` |
| `status.info` | `#0284c7` | `#38bdf8` |
| `status.info.bg` | `#f0f9ff` | `#0c4a6e` |

**Destructive button fill:** `status.error` background with `text.inverse`; hover one step darker on the same hue scale.

---

## 2. CSS variable naming (suggested)

```text
--dg-surface-page
--dg-surface-card
--dg-surface-subtle
--dg-border-default
--dg-text-primary
--dg-text-muted
--dg-brand-primary
--dg-status-success
--dg-status-warning
--dg-status-error
--dg-status-info
--dg-radius-sm / md / lg
--dg-shadow-sm / md / lg
```

---

## 3. Notification copy deck

Use **sentence case**. Include **error ID** when logs exist.

### 3.1 Success

| Context | Title | Body (optional) |
|---------|-------|-----------------|
| Generic save | Saved | Your changes were saved. |
| Scan queued | Scan queued | You will see status updates as the scan runs. |
| Policy uploaded | Policy uploaded | Validation runs in the background. |
| Webhook test | Test delivery sent | Check your endpoint logs for the payload. |

### 3.2 Error

| Context | Title | Body |
|---------|-------|------|
| Network | Something went wrong | Check your connection and try again. If this continues, contact support with request ID **{id}**. |
| Permission | You don’t have access | Ask an admin for the **{role}** role or switch tenant. |
| Validation | Fix the highlighted fields | Review the form and correct the errors. |
| Server 5xx | DeepGuard is having trouble | Try again in a few minutes. Reference: **{id}**. |

### 3.3 Warning

| Context | Title | Body |
|---------|-------|------|
| Quota | Approaching usage limit | **{percent}%** of your monthly scan quota is used. |
| Unsaved | Leave without saving? | You have unsaved changes. |

### 3.4 Info

| Context | Title | Body |
|---------|-------|------|
| Read-only | View only | You can browse this scan but cannot change settings. |
| Stale data | Data may be outdated | Last refreshed **{time}**. |

---

## 4. Application shell wireframe

**Sidebar order (top → bottom):**

1. Logo + product name “DeepGuard”
2. Tenant selector (combo)
3. **Primary nav**
   - Dashboard (optional)
   - Scans
   - Findings
   - Policies
   - Reports
   - **Separator**
   - Settings
   - Admin (role-gated)
4. Footer: version string `v{semver}`, environment pill (`Production` / `Staging`)

**Top bar (left → right):**

1. Mobile menu trigger (hidden on `lg+`)
2. Breadcrumb slot
3. Spacer
4. Global search (optional, cmd-k hint)
5. Notifications
6. Help (docs link)
7. User avatar → menu: Profile, API keys, Organization, Sign out

**Content area:** breadcrumb (if any) + page title row (title left, primary actions right) + page body.

---

## 5. Iconography

- **Stroke width:** prefer **1.5px** at 20px box for consistency (Heroicons / Lucide defaults).
- **Meaning:** icon + text label for nav; icon-only only in toolbars with `aria-label`.
- **Status:** pair color with shape (checkmark, triangle, circle-x) not color alone.

---

## 6. Z-index scale (suggested)

| Layer | z-index |
|-------|---------|
| Base content | 0 |
| Sticky table header | 10 |
| Dropdown / popover | 50 |
| Sidebar overlay (mobile) | 100 |
| Modal scrim | 200 |
| Modal | 210 |
| Toast | 300 |

---

## 7. Breakpoints (suggested)

| Name | Min width |
|------|-----------|
| `sm` | 640px |
| `md` | 768px |
| `lg` | 1024px |
| `xl` | 1280px |
| `2xl` | 1536px |

Collapse sidebar to rail + tooltip at `lg` if product requires denser data views.
