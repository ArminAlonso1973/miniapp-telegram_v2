import React, { useState } from 'react';
import LoginPage from './pages/LoginPage.jsx';
import HomePage from './pages/HomePage.jsx';

const App = () => {
  const [currentPage, setCurrentPage] = useState('login');

  return (
    <div className="min-h-screen bg-gray-900 text-gray-200">
      {currentPage === 'login' && <LoginPage onLogin={() => setCurrentPage('home')} />}
      {currentPage === 'home' && <HomePage />}
    </div>
  );
};

export default App;
