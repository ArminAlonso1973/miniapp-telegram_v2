import React, { useState } from 'react';

const LoginPage = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    if (email.trim() && password.trim()) {
      onLogin(); // Simula el cambio de página
    } else {
      alert('Por favor, completa ambos campos.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-gray-800 rounded-lg p-8 border border-gray-700">
        <h1 className="text-2xl font-bold text-yellow-500 text-center mb-6">Tax Assistant Pro</h1>
        <div className="space-y-4">
          <input
            type="email"
            placeholder="Correo electrónico"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-200"
          />
          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-200"
          />
          <button
            onClick={handleLogin}
            className="w-full bg-yellow-500 text-gray-900 font-bold py-3 rounded-lg hover:bg-yellow-600"
          >
            Iniciar Sesión
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
