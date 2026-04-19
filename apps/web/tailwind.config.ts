import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        dg: {
          page: "var(--dg-surface-page)",
          card: "var(--dg-surface-card)",
          subtle: "var(--dg-surface-subtle)",
          border: "var(--dg-border-default)",
          "border-strong": "var(--dg-border-strong)",
          "text-primary": "var(--dg-text-primary)",
          "text-muted": "var(--dg-text-muted)",
          "text-disabled": "var(--dg-text-disabled)",
          inverse: "var(--dg-text-inverse)",
          brand: "var(--dg-brand-primary)",
          "brand-hover": "var(--dg-brand-primary-hover)",
          "brand-muted": "var(--dg-brand-primary-muted)",
          success: "var(--dg-status-success)",
          "success-bg": "var(--dg-status-success-bg)",
          error: "var(--dg-status-error)",
          "error-bg": "var(--dg-status-error-bg)",
          warning: "var(--dg-status-warning)",
          "warning-bg": "var(--dg-status-warning-bg)",
          info: "var(--dg-status-info)",
          "info-bg": "var(--dg-status-info-bg)",
        },
      },
      borderRadius: {
        "dg-sm": "6px",
        "dg-md": "8px",
        "dg-lg": "12px",
      },
      boxShadow: {
        "dg-sm": "var(--dg-shadow-sm)",
        "dg-md": "var(--dg-shadow-md)",
        "dg-lg": "var(--dg-shadow-lg)",
      },
      maxWidth: {
        content: "1440px",
        form: "560px",
      },
      spacing: {
        sidebar: "240px",
      },
      zIndex: {
        drawer: "50",
        draweroverlay: "40",
        modal: "60",
      },
    },
  },
  plugins: [],
};
export default config;
