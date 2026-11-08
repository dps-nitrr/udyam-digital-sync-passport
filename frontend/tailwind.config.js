/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "var(--brand)",
          dark: "var(--brand-dark)",
          light: "var(--brand-light)",
        },
        graphite: {
          DEFAULT: "var(--graphite)",
          light: "var(--graphite-light)",
          dark: "var(--graphite-dark)",
        },
        surface: {
          DEFAULT: "var(--surface)",
          card: "var(--surface-card)",
          muted: "var(--surface-muted)",
        },
        success: {
          DEFAULT: "var(--success)",
          light: "var(--success-light)",
        },
        warn: {
          DEFAULT: "var(--warn)",
          light: "var(--warn-light)",
        },
        danger: {
          DEFAULT: "var(--danger)",
          light: "var(--danger-light)",
        },
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
      },
      maxWidth: {
        mobile: "430px",
      }
    },
  },
  plugins: [],
}
