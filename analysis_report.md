### Estructura del Proyecto

- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/.pytest_cache
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/.pytest_cache/v
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/.pytest_cache/v/cache
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/__pycache__
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/feature
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/routes
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/routes/__pycache__
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/scripts
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/services
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/services/__pycache__
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/tests
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/tests/__pycache__
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/tests/test
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/tests/test/__pycache__
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/backend/utils
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend
- file: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/eslint.config.js
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/public
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src
- file: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src/App.tsx
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src/assets
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src/components
- file: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src/components/ChatWithAssistant.tsx
- file: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src/components/TypewriterEffect.tsx
- file: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src/components/UploadPDF.tsx
- file: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src/main.tsx
- file: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/tailwind.config.js
- file: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/vite-env.d.ts
- file: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/vite.config.d.ts
- file: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/vite.config.js
- file: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/vite.config.ts
- directory: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/secrets

### Archivos Analizados


#### Archivo: eslint.config.js
- Ubicación: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/eslint.config.js

**Contenido:**
```javascript
import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  { ignores: ['dist'] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
    },
  },
)

```

**Problemas Detectados:**
  - Línea undefined: File ignored because outside of base path. (null)

#### Archivo: App.tsx
- Ubicación: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src/App.tsx

**Contenido:**
```javascript
import { useState, FormEvent, ChangeEvent } from 'react';
import UploadPDF from './components/UploadPDF';
import ChatWithAssistant from './components/ChatWithAssistant';

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

        <section className="p-6 bg-white rounded-lg shadow-md border border-gray-dark mb-6">
          <h2 className="text-xl font-bold text-gold-dark mb-4">Cargar y Resumir PDF</h2>
          <UploadPDF />
        </section>

        <section className="p-6 bg-white rounded-lg shadow-md border border-gray-dark">
          <h2 className="text-xl font-bold text-gold-dark mb-4">Asistente Tributario</h2>
          <ChatWithAssistant />
        </section>
      </main>

      <footer className="bg-gray-dark text-gold-light py-2 text-center">
        <p>&copy; 2024 Mini App Administrativa - Todos los derechos reservados</p>
      </footer>
    </div>
  );
};

export default App;

```

**Problemas Detectados:**
  - Línea undefined: File ignored because outside of base path. (null)

#### Archivo: ChatWithAssistant.tsx
- Ubicación: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src/components/ChatWithAssistant.tsx

**Contenido:**
```javascript
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

```

**Problemas Detectados:**
  - Línea undefined: File ignored because outside of base path. (null)

#### Archivo: TypewriterEffect.tsx
- Ubicación: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src/components/TypewriterEffect.tsx

**Contenido:**
```javascript
import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

interface TypewriterEffectProps {
  text: string;
  speed?: number; // Velocidad en milisegundos por carácter
}

const TypewriterEffect: React.FC<TypewriterEffectProps> = ({ text, speed = 180 }) => {
  const [displayedText, setDisplayedText] = useState('');

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      setDisplayedText((prev) => prev + text[index]);
      index++;
      if (index === text.length) {
        clearInterval(interval); // Detener el intervalo cuando termine el texto
      }
    }, speed);

    return () => clearInterval(interval); // Limpiar el intervalo si el componente se desmonta
  }, [text, speed]);

  return (
    <div>
      <ReactMarkdown>{displayedText}</ReactMarkdown>
    </div>
  );
};

export default TypewriterEffect;

```

**Problemas Detectados:**
  - Línea undefined: File ignored because outside of base path. (null)

#### Archivo: UploadPDF.tsx
- Ubicación: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src/components/UploadPDF.tsx

**Contenido:**
```javascript
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

```

**Problemas Detectados:**
  - Línea undefined: File ignored because outside of base path. (null)

#### Archivo: main.tsx
- Ubicación: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/src/main.tsx

**Contenido:**
```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // Archivo para Tailwind y estilos globales.
import App from './App'; // Componente principal.

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);


```

**Problemas Detectados:**
  - Línea undefined: File ignored because outside of base path. (null)

#### Archivo: tailwind.config.js
- Ubicación: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/tailwind.config.js

**Contenido:**
```javascript
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          DEFAULT: '#D4AF37',
          light: '#F3D897',
          dark: '#B18D2C',
        },
        gray: {
          light: '#F5F5F5',
          DEFAULT: '#B0B0B0',
          dark: '#333333',
        },
      },
    },
  },
  plugins: [],
};

```

**Problemas Detectados:**
  - Línea undefined: File ignored because outside of base path. (null)

#### Archivo: vite-env.d.ts
- Ubicación: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/vite-env.d.ts

**Contenido:**
```javascript
/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_BACKEND_URL: string;
    readonly VITE_TELEGRAM_CHAT_ID: string;
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
  
```

**Problemas Detectados:**
  - Línea undefined: File ignored because outside of base path. (null)

#### Archivo: vite.config.d.ts
- Ubicación: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/vite.config.d.ts

**Contenido:**
```javascript
declare const _default: import("vite").UserConfig;
export default _default;

```

**Problemas Detectados:**
  - Línea undefined: File ignored because outside of base path. (null)

#### Archivo: vite.config.js
- Ubicación: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/vite.config.js

**Contenido:**
```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        host: '0.0.0.0',
        port: 5173,
    },
});

```

**Problemas Detectados:**
  - Línea undefined: File ignored because outside of base path. (null)

#### Archivo: vite.config.ts
- Ubicación: /Users/arminpalma/Documents/Documentos - MacBook Pro de Armin (2)/python/miniapp-telegram_v2/frontend/vite.config.ts

**Contenido:**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
})
```

**Problemas Detectados:**
  - Línea undefined: File ignored because outside of base path. (null)

### Análisis de Arquitectura

Para el análisis de la arquitectura del proyecto "miniapp-telegram_v2", observaré la estructura de directorios y los componentes principales, proporcionando una evaluación detallada.

### 1. Patrones de arquitectura identificados

El proyecto parece seguir un enfoque basado en la arquitectura de microservicios, dado que tiene una clara separación entre el `frontend` y el `backend`. Esto puede indicar que se diseñó para escalar y manejar diferentes módulos de funcionalidad de manera independiente. Además, el `frontend` parece construirse con una pila moderna (posiblemente React, dado el uso de archivos .tsx), lo que sugiere un enfoque reactivo hacia la interfaz de usuario.

### 2. Posibles mejoras de diseño

- **Estructura de directorios**: La estructura del backend puede ser mejorada mediante la agrupación de módulos relacionados. Por ejemplo, los servicios pueden estar más claramente organizados en función de sus correspondientes características o funcionalidades.
  
- **Archivos de configuración**: Configuraciones como `eslint.config.js` y otras relacionadas con el frontend (como `tailwind.config.js` y `vite.config.js`) podrían beneficiarse de ser centralizadas en un directorio de configuración para mejorar la legibilidad y el mantenimiento.

### 3. Sugerencias de refactorización

- **Modularización del frontend**: Los componentes de la UI en el frontend (como ChatWithAssistant, TypewriterEffect, UploadPDF) pueden agrupase bajo un directorio `components` que puede ser fácilmente escalable. Asimismo, incrementar el uso de hooks personalizados si se detectan patrones repetidos en el manejo de estado.

- **Servicios en el backend**: Si los servicios están realizando tareas distintas (por ejemplo, manejo de datos, autenticación, acceso a la base de datos), considera dividirlos en módulos separados que permitan pruebas unitarias y mantención más sencilla.

- **Desacoplar lógica de presentación**: La separación entre el manejo de la lógica de negocio y la presentación del frontend puede ser mejorada al utilizar contenedores o patrones de diseño como "Presentational and Container Components".

### 4. Evaluación de separación de responsabilidades

La separación entre `frontend` y `backend` es clara, lo que facilita la escalabilidad y el mantenimiento. Sin embargo:

- **Responsabilidades del frontend**: Si la lógica de negocio del frontend (como peticiones a la API, manipulación de datos) está demasiado acoplada a la UI, puede ser mejor separar estas operaciones usando una arquitectura de estados como Redux o Context API.

- **Tests**: La presencia de un directorio `tests` es positiva, pero es crucial asegurarse de que las pruebas cubran tanto la lógica de negocio como los componentes de la interfaz de usuario en ambas partes (frontend y backend).

### 5. Identificación de posibles code smells

- **Caché y archivos `__pycache__`**: La existencia de estos archivos indica que se están generando archivos de bytecode de Python que pueden ser innecesarios para el control de versiones. Asegúrate de añadir `__pycache__/` y otros temporalidades a tu `.gitignore`.

- **Nombres de Directorios**: El directorio `feature` es un término muy general. Podrías ser más específico en nombrar los directorios de acuerdo a las funcionalidades que implementan (por ejemplo, `userManagement`, `notifications`).

- **Archivos de configuración en directo en root**: Considera usar un directorio `config` para almacenar archivos como `eslint.config.js`, `tailwind.config.js`, etc. Esto mantendría el diseño más limpio y hará más fácil localizar configuraciones.

### Conclusión

En general, el proyecto "miniapp-telegram_v2" demuestra una buena estructura de separación entre frontend y backend, pero hay varias áreas donde se puede mejorar la organización del código, la separación de responsabilidades y la modularización. La implementación de patrones de diseño y principios SOLID puede llevar a un código más mantenible y escalable, así como facilitar el trabajo en equipo y la producción de pruebas más efectivas.