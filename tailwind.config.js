/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        arholdings: {
          primary: "#5f3ea8",
          secondary: "#e39424",
          accent: "#f9b616",
          neutral: "#3d4451",
          success: "#00b97b",
          warning: "#ffb000",
          error: "#d30000",
          "base-100": "#ffffff",
        },
      },
    ],
  },
};
