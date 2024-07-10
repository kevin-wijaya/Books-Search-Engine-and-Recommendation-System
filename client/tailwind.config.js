/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js}", 
    "*.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          '50': "#f4f4f4",
          '100': "#f0f0f0",
          '200': "#e2e2e2",
          '300': "#909090",
          '400': "#707070",
          '500': "#505050",
          '600': "#404040",
          '650': "#343434",
          '700': "#262626",
          '800': "#101010",
          '900': "#0a0a0a",
          '950': "#010101"
        },
      }
    },
  },
  plugins: [],
}

