"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, type ReactNode } from "react";
import { useTheme } from "./theme-context";
import { Button } from "./ui/button";

const nav = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/scans", label: "Scans" },
];

const disabledNav = [
  { label: "Findings" },
  { label: "Policies" },
  { label: "Reports" },
];

function NavLink({
  href,
  label,
  active,
  onNavigate,
}: {
  href: string;
  label: string;
  active: boolean;
  onNavigate?: () => void;
}) {
  return (
    <Link
      href={href}
      onClick={onNavigate}
      className={`relative block rounded-dg-md px-3 py-2 text-sm font-medium ${
        active
          ? "bg-dg-subtle text-dg-text-primary before:absolute before:left-0 before:top-1 before:h-[calc(100%-8px)] before:w-[3px] before:rounded-full before:bg-dg-brand"
          : "text-dg-text-primary hover:bg-dg-subtle/80"
      }`}
    >
      {label}
    </Link>
  );
}

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const [drawer, setDrawer] = useState(false);
  const { mode, setMode, resolved } = useTheme();

  const closeDrawer = () => setDrawer(false);

  const sidebar = (
    <aside className="flex h-full w-sidebar shrink-0 flex-col border-r border-dg-border bg-dg-card">
      <div className="px-4 py-4">
        <p className="text-[22px] font-semibold leading-tight tracking-tight">
          DeepGuard
        </p>
        <p className="text-xs text-dg-text-muted">Console</p>
      </div>
      <div className="px-4 pb-2">
        <label className="text-xs text-dg-text-muted" htmlFor="tenant-sel">
          Tenant
        </label>
        <select
          id="tenant-sel"
          disabled
          className="mt-1 w-full rounded-dg-sm border border-dg-border bg-dg-subtle px-2 py-1.5 text-sm text-dg-text-muted"
          aria-label="Tenant (read-only in MVP)"
        >
          <option>ACME staging</option>
        </select>
      </div>
      <nav className="flex flex-1 flex-col gap-1 px-2" aria-label="Main">
        {nav.map((n) => (
          <NavLink
            key={n.href}
            href={n.href}
            label={n.label}
            active={pathname === n.href || pathname.startsWith(`${n.href}/`)}
            onNavigate={closeDrawer}
          />
        ))}
        {disabledNav.map((n) => (
          <span
            key={n.label}
            title="Not available in API yet"
            className="cursor-not-allowed rounded-dg-md px-3 py-2 text-sm text-dg-text-disabled"
            aria-disabled
          >
            {n.label}
          </span>
        ))}
        <div className="mt-auto">
          <NavLink
            href="/settings"
            label="Settings"
            active={pathname.startsWith("/settings")}
            onNavigate={closeDrawer}
          />
        </div>
      </nav>
      <div className="mt-4 flex flex-wrap items-center gap-2 border-t border-dg-border px-4 py-3 text-xs text-dg-text-muted">
        <span>{process.env.NEXT_PUBLIC_APP_VERSION ?? "0.1.0"}</span>
        <span className="rounded-full bg-dg-subtle px-2 py-0.5 text-dg-text-muted">
          {process.env.NEXT_PUBLIC_DEEPGUARD_ENV ?? "local"}
        </span>
      </div>
    </aside>
  );

  return (
    <div className="flex min-h-screen bg-dg-page">
      {/* Desktop sidebar */}
      <div className="hidden lg:flex">{sidebar}</div>

      {/* Mobile drawer */}
      {drawer ? (
        <>
          <button
            type="button"
            className="fixed inset-0 z-draweroverlay bg-black/40 lg:hidden"
            aria-label="Close menu"
            onClick={closeDrawer}
          />
          <div className="fixed inset-y-0 left-0 z-drawer flex w-sidebar lg:hidden">
            {sidebar}
          </div>
        </>
      ) : null}

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-14 shrink-0 items-center justify-between border-b border-dg-border bg-dg-card px-4 lg:px-6">
          <div className="flex items-center gap-3">
            <button
              type="button"
              className="min-h-10 min-w-10 rounded-dg-md border border-dg-border lg:hidden"
              aria-label="Open navigation menu"
              onClick={() => setDrawer(true)}
            >
              ☰
            </button>
            <span className="text-sm text-dg-text-muted">
              {pathname === "/dashboard"
                ? "Dashboard"
                : pathname.startsWith("/scans/new")
                  ? "Scans › New scan"
                  : pathname.match(/^\/scans\/[^/]+$/)
                    ? "Scans › Detail"
                    : pathname.startsWith("/scans")
                      ? "Scans"
                      : pathname.startsWith("/settings")
                        ? "Settings"
                        : "DeepGuard"}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              className="min-h-10 min-w-10 px-0"
              aria-label="Help (placeholder)"
              type="button"
            >
              ?
            </Button>
            <Button
              variant="ghost"
              size="sm"
              className="min-h-10 min-w-10 px-0"
              aria-label="Notifications (placeholder)"
              type="button"
            >
              🔔
            </Button>
            <Button
              variant="ghost"
              size="sm"
              className="min-h-10 min-w-10 px-0"
              aria-label="Account menu (placeholder)"
              type="button"
            >
              ◉
            </Button>
            <label className="ml-2 flex items-center gap-2 text-xs text-dg-text-muted">
              <span className="hidden sm:inline">Theme</span>
              <select
                value={mode}
                onChange={(e) =>
                  setMode(e.target.value as "light" | "dark" | "system")
                }
                className="rounded-dg-sm border border-dg-border bg-dg-card px-2 py-1 text-xs"
                aria-label="Color theme"
              >
                <option value="system">System ({resolved})</option>
                <option value="light">Light</option>
                <option value="dark">Dark</option>
              </select>
            </label>
          </div>
        </header>
        <main className="mx-auto w-full max-w-content flex-1 px-4 py-6 lg:px-6">
          {children}
        </main>
      </div>
    </div>
  );
}
