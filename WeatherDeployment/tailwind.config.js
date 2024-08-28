/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html', // Adjusted to include the root directory HTML file
    './css/**/*.css', // Optional: Include CSS files if you use Tailwind CSS classes within CSS
  ],
  theme: {
    extend: {
      fontFamily: {
        'jersey10': ['Jersey 10', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
