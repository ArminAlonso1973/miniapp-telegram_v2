

const HomePage = () => (
  <div className="min-h-screen bg-gray-900 p-6">
    <header className="text-center mb-8">
      <h1 className="text-3xl font-bold text-yellow-500">Bienvenido a Tax Assistant Pro</h1>
    </header>
    <main className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
      {[
        { title: 'Asistente Tributario', page: 'assistant' },
        { title: 'Resumen PDF', page: 'pdf' },
        { title: 'Búsqueda de Chats', page: 'search' },
        { title: 'Convertidor', page: 'converter' },
      ].map((item, index) => (
        <section
          key={index}
          className="p-6 bg-gray-800 rounded-lg shadow-md border border-gray-700 hover:border-yellow-500"
        >
          <h2 className="text-xl font-bold text-yellow-500 mb-4">{item.title}</h2>
          <p className="text-gray-300">Descripción de {item.title}...</p>
        </section>
      ))}
    </main>
  </div>
);

export default HomePage;
