/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#050505",
          900: "#0d0d0d",
          800: "#111111",
          700: "#1a1a1a",
          600: "#222222",
        },
        accent: {
          DEFAULT: "#ff2d78",
          hover: "#e0185e",
          light: "#ff6ea6",
          muted: "#c0005a",
        },
        status: {
          new: "#ff2d78",
          active: "#10b981",
          qualified: "#bf5af2",
          booked: "#ffd60a",
          closed: "#6b7280",
        }
      },
      borderRadius: {
        "2xl": "1.25rem",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "fade-in": "fadeIn 0.3s ease-in-out",
        "slide-in": "slideIn 0.3s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideIn: {
          "0%": { transform: "translateX(-10px)", opacity: "0" },
          "100%": { transform: "translateX(0)", opacity: "1" },
        },
      },
    },
  },
  plugins: [],
};
