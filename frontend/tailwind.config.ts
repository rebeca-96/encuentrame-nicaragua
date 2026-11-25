import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: "#0A192F",
          800: "#0F2A4A",
          700: "#1E3A8A",
          600: "#2563EB",
          50: "#F0F5FA"
        },
        civic: {
          teal: "#0D9488",
          tealLight: "#14B8A6",
          amber: "#D97706",
          red: "#DC2626",
          green: "#059669"
        }
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
