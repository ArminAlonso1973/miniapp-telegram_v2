import React from 'react';

// Interfaz que define las propiedades aceptadas por el componente
interface HomePageProps {
  onNavigate: (page: 'assistant' | 'legal-library') => void; // Función para cambiar de página
}

// Componente principal de la página de inicio
const HomePage: React.FC<HomePageProps> = ({ onNavigate }) => (
  <div className="min-h-screen bg-gray-900 p-6">
    {/* Encabezado de bienvenida */}
    <header className="text-center mb-8">
      <h1 className="text-3xl font-bold text-yellow-500">Bienvenido a Tax Assistant Pro</h1>
    </header>

    {/* Contenido principal: menú con opciones */}
    <main className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
      {[
        { title: 'Asistente Tributario', page: 'assistant' }, // Opción 1
        { title: 'Biblioteca Legal', page: 'legal-library' }, // Opción 2
      ].map((item, index) => (
        <section
          key={index}
          // Cambia de página al hacer clic en una opción
          onClick={() => onNavigate(item.page as 'assistant' | 'legal-library')}
          className="p-6 bg-gray-800 rounded-lg shadow-md border border-gray-700 hover:border-yellow-500 cursor-pointer"
        >
          <h2 className="text-xl font-bold text-yellow-500 mb-4">{item.title}</h2>
        </section>
      ))}
    </main>
  </div>
);

export default HomePage;
