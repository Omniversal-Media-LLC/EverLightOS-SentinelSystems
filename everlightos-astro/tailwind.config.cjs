/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{astro,html,js,jsx,ts,tsx,md,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        everdark: "#050915",
        everlight: "#e5fff7",
        aura: "#91f0ff"
      },
      backgroundImage: {
        iridescent: "linear-gradient(135deg,#91f0ff 0%,#ff91f0 100%)"
      },
      borderRadius: {
        "2xl": "1.5rem"
      }
    }
  },
  plugins: []
};