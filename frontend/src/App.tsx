import { useState, FormEvent, ChangeEvent } from 'react';
import './App.css';
import UploadPDF from './components/UploadPDF';

const App = () => {
  const [message, setMessage] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Variables de entorno
  const CHAT_ID = import.meta.env.VITE_TELEGRAM_CHAT_ID; // Sin fallback
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
    <div className="container">
      <header className="app-header">
        <h1>Mini App Administrativa</h1>
      </header>

      <main className="app-main">
        {/* Telegram Bot Messenger */}
        <section className="telegram-section">
          <h2>Telegram Bot Messenger</h2>
          {error && <div className="error-message">{error}</div>}
          <form onSubmit={handleSubmit} className="message-form">
            <textarea
              value={message}
              onChange={handleMessageChange}
              placeholder="Escribe tu mensaje aquí"
              rows={4}
              required
            />
            <button type="submit" disabled={loading || !message.trim()}>
              {loading ? 'Enviando...' : 'Enviar Mensaje'}
            </button>
          </form>
        </section>

        {/* Cargar y Resumir PDF */}
        <section className="pdf-section">
          <h2>Cargar y Resumir PDF</h2>
          <UploadPDF />
        </section>
      </main>

      <footer className="app-footer">
        <p>&copy; 2024 Mini App Administrativa - Todos los derechos reservados</p>
      </footer>
    </div>
  );
};

export default App;
