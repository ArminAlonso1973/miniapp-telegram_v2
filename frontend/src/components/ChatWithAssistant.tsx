import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import TypewriterEffect from './TypewriterEffect';

const ChatWithAssistant: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [useTypewriter, setUseTypewriter] = useState(true);
  const [message, setMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setMessage("Consultando, por favor espera... ⏳");
    setAnswer(null);

    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/assistant`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ question })
      });
      const data = await response.json();
      if (response.ok) {
        setAnswer(data.respuesta || "No se obtuvo respuesta.");
        setMessage(null); // Quitar el mensaje de estado
      } else {
        setMessage(`Error: ${data.error || 'Error desconocido'}`);
      }
    } catch (err) {
      console.error(err);
      setMessage("Error al conectar con el servidor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 border border-gray-300 rounded bg-white shadow-sm">
      <h3 className="text-lg font-bold mb-4">Asistente Tributario</h3>
      <form onSubmit={handleSubmit} className="mb-4">
        <textarea
          className="w-full p-2 border border-gray-300 rounded mb-2"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Escribe tu pregunta tributaria aquí..."
          rows={4}
          disabled={loading}
        />
        <button
          type="submit"
          disabled={!question.trim() || loading}
          className="bg-gold text-white font-bold py-2 px-4 rounded hover:bg-gold-dark transition w-full"
        >
          {loading ? "Procesando..." : "Consultar"}
        </button>
      </form>

      {message && <p className="mb-4 text-sm text-gray-700">{message}</p>}

      {answer && (
        <div className="p-4 border border-gray-300 rounded bg-gray-50">
          <h4 className="text-md font-bold mb-2">Respuesta:</h4>
          <button
            onClick={() => setUseTypewriter(!useTypewriter)}
            className="mb-4 bg-gray-200 text-sm px-2 py-1 rounded hover:bg-gray-300 transition"
          >
            {useTypewriter ? "Ver en Markdown" : "Ver con Efecto Máquina"}
          </button>
          {useTypewriter ? (
            <TypewriterEffect text={answer} speed={50} />
          ) : (
            <ReactMarkdown>{answer}</ReactMarkdown>
          )}
        </div>
      )}
    </div>
  );
};

export default ChatWithAssistant;