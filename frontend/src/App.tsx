import { useState } from 'react';
import LoginPage from './pages/LoginPage';
import AssistantPage from './pages/AssistantPage';

const App = () => {
  const [currentPage, setCurrentPage] = useState('login');

  const handleBack = () => {
    console.log("Volviendo al inicio"); // Log para verificar navegación
    setCurrentPage('login');
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-200">
      {currentPage === 'login' && (
        <LoginPage onLogin={() => setCurrentPage('assistant')} />
      )}
      {currentPage === 'assistant' && <AssistantPage onBack={handleBack} />}
    </div>
  );
};

export default App;
