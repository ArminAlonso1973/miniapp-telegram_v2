import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Permite conexiones externas en Docker
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://backend:5001',
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
