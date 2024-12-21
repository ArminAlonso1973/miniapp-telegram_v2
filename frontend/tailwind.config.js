module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          DEFAULT: '#D4AF37',
          light: '#F3D897',
          dark: '#B18D2C',
        },
        gray: {
          light: '#F5F5F5',
          100: '#F5F5F5', // Agrega extensiones específicas
          200: '#E5E5E5',
          DEFAULT: '#B0B0B0',
          800: '#333333',
        },
      },
    },
  },
  plugins: [],
};
