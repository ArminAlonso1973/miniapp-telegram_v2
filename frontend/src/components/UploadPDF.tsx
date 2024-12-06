import React, { useState } from 'react';

const UploadPDF = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

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
        setMessage("Archivo procesado exitosamente.");
        setSummary(data.summary); // Mostrar el resumen
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
      <h2>Subir y Resumir PDF</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          disabled={loading}
        />
        <button type="submit" disabled={!file || loading}>
          {loading ? 'Procesando...' : 'Subir'}
        </button>
      </form>
      {message && <p>{message}</p>}
      {summary && (
        <div>
          <h3>Resumen del Documento:</h3>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
};

export default UploadPDF;
