import { useState } from 'react';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import AssistantPage from './pages/AssistantPage';
import LegalTextsSystem from './components/LegalTextsSystem';
import ReportGeneratorDemo from './components/ReportGeneratorDemo';

const App = () => {
  // Controla la navegación entre páginas
  const [currentPage, setCurrentPage] = useState<'login' | 'home' | 'assistant' | 'legal-library' | 'report-generator'>('login');

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Página de inicio de sesión */}
      {currentPage === 'login' && (
        <LoginPage onLogin={() => setCurrentPage('home')} />
      )}
      
      {/* Página principal */}
      {currentPage === 'home' && (
        <HomePage onNavigate={(page) => setCurrentPage(page)} />
      )}
      
      {/* Página del Asistente Tributario */}
      {currentPage === 'assistant' && (
        <AssistantPage onBack={() => setCurrentPage('home')} />
      )}
      
      {/* Página del sistema de textos legales */}
      {currentPage === 'legal-library' && (
        <LegalTextsSystem
          onBack={() => setCurrentPage('home')} // Vuelve al menú principal
          onHome={() => setCurrentPage('home')} // Va al inicio
        />
      )}

      {/* Página del generador de informes */}
      {currentPage === 'report-generator' && (
        <ReportGeneratorDemo />
      )}
    </div>
  );
};

export default App;
