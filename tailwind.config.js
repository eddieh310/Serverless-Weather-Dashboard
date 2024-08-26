/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Include all HTML files in the templates directory
  ],
  theme: {
    extend: {
      fontFamily: {
        'jersey10': ['Jersey 10', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
