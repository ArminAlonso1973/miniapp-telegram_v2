import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import TypewriterEffect from './TypewriterEffect';

const UploadPDF: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [useTypewriter, setUseTypewriter] = useState<boolean>(true); // Alternar entre efecto y Markdown

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setMessage(null); // Limpiar mensajes anteriores
      setSummary(null); // Limpiar resumen anterior
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) {
      setMessage("Por favor selecciona un archivo.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setMessage(null);

    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/upload-pdf`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        const sanitizedSummary = data.summary ? data.summary.trim() : ''; // Validar y limpiar el texto
        setMessage("Archivo procesado exitosamente.");
        setSummary(sanitizedSummary);
      } else {
        setMessage(`Error: ${data.error || 'Error desconocido'}`);
      }
    } catch (err) {
      console.error("Error al conectar con el servidor:", err);
      setMessage("Error al conectar con el servidor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="text-lg font-bold mb-4">Subir y Resumir PDF</h2>
      <form onSubmit={handleSubmit} className="mb-4">
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          disabled={loading}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-gray-200 file:text-gray-700 hover:file:bg-gray-300"
        />
        <button
          type="submit"
          disabled={!file || loading}
          className="mt-4 bg-gold text-white font-bold py-2 px-4 rounded hover:bg-dark-gold transition"
        >
          {loading ? "Procesando..." : "Subir"}
        </button>
      </form>

      {message && <p className="text-sm text-gray-700 mb-4">{message}</p>}

      {summary && (
        <div className="p-4 border border-gray-300 rounded bg-gray-50">
          <h3 className="text-md font-bold mb-2">Resumen del Documento:</h3>
          <button
            onClick={() => setUseTypewriter(!useTypewriter)}
            className="mb-4 bg-gray-200 text-sm px-2 py-1 rounded hover:bg-gray-300 transition"
          >
            {useTypewriter ? "Ver en Markdown" : "Ver con Efecto Máquina"}
          </button>
          {useTypewriter ? (
            <TypewriterEffect text={summary} speed={50} />
          ) : (
            <ReactMarkdown>{summary}</ReactMarkdown>
          )}
        </div>
      )}
    </div>
  );
};

export default UploadPDF;
