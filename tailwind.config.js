/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.{js,css}"
  ],
  theme: {
    container: {
      center: true,
      padding: '16px',
    },
    extend: {
      colors: {
        primary: '#14b8a6',
        dark: '#0f172a',
        customBlue1: '#A3EAF1',
        customBlue2: '#22d3ee',
      
      
        backgroundImage: {
          'islamic-pattern': "url('/home/istami/web-chatbot/src/images/Untitled_design__1_-removebg-preview.png')",
      }
        
      },
      screens: {
        '2xl': '1320px'
      }
    },
  },
  plugins: [],
}
