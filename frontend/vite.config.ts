import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // Alias para el directorio `src`
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        // Permite importar variables SCSS globalmente (si usas SCSS)
        additionalData: `@import "@/styles/variables.scss";`,
      },
    },
  },
  server: {
    host: '0.0.0.0', // Permite conexiones externas en Docker
    port: 5173, // Puerto del servidor de desarrollo
    proxy: {
      '/api': {
        target: 'http://backend:5001', // URL del backend
        changeOrigin: true, // Cambia el origen del host
        secure: false, // Ignora certificados SSL no válidos
      },
    },
  },
  build: {
    outDir: 'dist', // Directorio de salida para la compilación
    sourcemap: true, // Genera mapas de fuente para depuración
  },
  optimizeDeps: {
    include: ['react', 'react-dom'], // Asegura la optimización de dependencias clave
  },
});
