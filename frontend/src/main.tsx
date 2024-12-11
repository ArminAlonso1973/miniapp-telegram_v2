import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // Archivo para Tailwind y estilos globales.
import App from './App'; // Componente principal.

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

