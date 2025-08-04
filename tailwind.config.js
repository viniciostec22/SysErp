/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // <- necessário para o botão de tema funcionar
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './static/src/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
