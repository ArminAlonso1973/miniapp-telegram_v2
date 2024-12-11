import { useState, FormEvent, ChangeEvent } from 'react';
import UploadPDF from './components/UploadPDF';

const App = () => {
  const [message, setMessage] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const CHAT_ID = import.meta.env.VITE_TELEGRAM_CHAT_ID;
  const TELEGRAM_BOT_URL = `${import.meta.env.VITE_BACKEND_URL}/telegram-bot`;

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(TELEGRAM_BOT_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          chat_id: CHAT_ID,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert('Mensaje enviado con éxito!');
        setMessage('');
      } else {
        setError(data.message || 'Error al enviar mensaje');
      }
    } catch (err) {
      setError('Error de conexión con el servidor');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleMessageChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
  };

    return (
      <div className="min-h-screen flex flex-col bg-gray-light text-gray-dark">
        <header className="bg-gray-dark text-gold-light py-4 text-center">
          <h1 className="text-2xl font-bold">Mini App Administrativa</h1>
        </header>
    
        <main className="flex-1 container mx-auto p-4">
          <section className="mb-6 p-6 bg-white rounded-lg shadow-md border border-gray-dark">
            <h2 className="text-xl font-bold text-gold-dark mb-4">Enviar mensaje al bot de Telegram</h2>
            {error && <div className="text-red-500">{error}</div>}
            <form onSubmit={handleSubmit} className="space-y-4">
              <textarea
                className="w-full p-3 border border-gray-dark rounded-md text-gray-dark focus:ring-2 focus:ring-gold"
                placeholder="Escribe tu mensaje aquí"
                rows={4}
                value={message}
                onChange={handleMessageChange}
                required
              />
              <button
                type="submit"
                className="w-full py-2 bg-gold text-white font-bold rounded-md shadow hover:bg-gold-dark transition"
                disabled={loading || !message.trim()}
              >
                {loading ? 'Enviando...' : 'Enviar Mensaje'}
              </button>
            </form>
          </section>
    
          <section className="p-6 bg-white rounded-lg shadow-md border border-gray-dark">
            <h2 className="text-xl font-bold text-gold-dark mb-4">Cargar y Resumir PDF</h2>
            <UploadPDF />
          </section>
        </main>
    
        <footer className="bg-gray-dark text-gold-light py-2 text-center">
          <p>&copy; 2024 Mini App Administrativa - Todos los derechos reservados</p>
        </footer>
      </div>
    );
    
};

export default App;
