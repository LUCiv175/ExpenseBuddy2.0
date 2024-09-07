/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Aggiungi i percorsi ai tuoi file React
    "./public/index.html",         // Se hai file HTML nel pubblico
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
