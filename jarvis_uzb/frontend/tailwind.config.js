/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    // Next.js 13+ da `pages` papkasi odatda ishlatilmaydi
  ],
  theme: {
    extend: {
      colors: {
        'dark-blue': '#0a192f',
        'light-blue': '#1f93ff',
        'slate': '#8892b0',
        'light-slate': '#a8b2d1',
        'white': '#e6f1ff',
      },
      fontFamily: {
        'sans': ['"Inter"', 'sans-serif'],
        'mono': ['"Fira Code"', 'monospace'],
      },
    },
  },
  plugins: [],
}
