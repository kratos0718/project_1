import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17211f",
        field: "#f4f7f2",
        civic: "#256d63",
        warning: "#b45309",
        danger: "#b42318"
      },
      boxShadow: {
        panel: "0 12px 30px rgba(23, 33, 31, 0.08)"
      }
    }
  },
  plugins: []
};

export default config;

