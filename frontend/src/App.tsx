import { useState, FormEvent, ChangeEvent } from 'react'
import './App.css'

const App = () => {
  const [message, setMessage] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)  // Cambiado el tipo

  // URL del backend usando variable de entorno de Vite
  const TELEGRAM_BOT_URL = "http://localhost:5001/telegram-bot"
  const CHAT_ID = import.meta.env.VITE_TELEGRAM_CHAT_ID || "TU_CHAT_ID_AQUI"

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(TELEGRAM_BOT_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          chat_id: CHAT_ID
        })
      })

      const data = await response.json()

      if (response.ok) {
        alert('Mensaje enviado con éxito!')
        setMessage('')
      } else {
        setError(data.message || 'Error al enviar mensaje')
      }
    } catch (err) {
      setError('Error de conexión con el servidor')  // Ahora es válido porque error puede ser string
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleMessageChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value)
  }

  return (
    <div className="container">
      <h1>Telegram Bot Messenger</h1>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="message-form">
        <textarea
          value={message}
          onChange={handleMessageChange}
          placeholder="Escribe tu mensaje aquí"
          rows={4}  // Cambiado a número
          required
        />

        <button 
          type="submit" 
          disabled={loading || !message.trim()}
        >
          {loading ? 'Enviando...' : 'Enviar Mensaje'}
        </button>
      </form>
    </div>
  )
}

export default App