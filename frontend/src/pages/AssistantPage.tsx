import { useState } from 'react';
import { ArrowLeft, Search, Star } from 'lucide-react';
import QuestionInput from '@/components/QuestionInput';
import ChatHistory from '@/components/ChatHistory';
import SearchPanel from '@/components/SearchPanel';

interface Chat {
  question: string;
  answer: {
    content: string;
    references: string[];
  };
  isImportant: boolean;
  categories: string[];
}

interface AssistantPageProps {
  onBack: () => void;
}

const AssistantPage: React.FC<AssistantPageProps> = ({ onBack }) => {
  const [chatHistory, setChatHistory] = useState<Chat[]>([]);
  const [showSearchPanel, setShowSearchPanel] = useState(false);

  const handleSendQuestion = (question: string) => {
    console.log("Pregunta enviada:", question); // Log para verificar el evento
    const response = {
      content: `Respuesta generada para: ${question}`,
      references: ["Artículo 123", "Ley Tributaria 2024"],
    };
    setChatHistory((prev) => [
      ...prev,
      { question, answer: response, isImportant: false, categories: [] },
    ]);
  };

  const toggleImportant = (index: number) => {
    console.log("Marcando como importante el chat:", index);
    setChatHistory((prev) =>
      prev.map((chat, idx) =>
        idx === index ? { ...chat, isImportant: !chat.isImportant } : chat
      )
    );
  };

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <div className="border-b border-gray-700 bg-gray-800 p-4 flex items-center">
        <button
          onClick={onBack}
          className="flex items-center text-gray-400 hover:text-yellow-500"
        >
          <ArrowLeft className="mr-2" />
          Volver al inicio
        </button>
        <h2 className="text-xl font-semibold text-gray-200 ml-4">Asistente Tributario</h2>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto p-4">
        <QuestionInput onSend={handleSendQuestion} />

        <ChatHistory history={chatHistory} />
      </div>

      {/* Botón flotante para búsqueda */}
      <button
        onClick={() => setShowSearchPanel(true)}
        className="fixed bottom-6 right-6 bg-yellow-500 p-3 rounded-full text-gray-900 hover:bg-yellow-600 shadow-lg"
      >
        <Search className="w-5 h-5" />
      </button>

      {/* Panel de búsqueda */}
      {showSearchPanel && (
        <SearchPanel
          onClose={() => setShowSearchPanel(false)}
          onSelectChat={(chat) => console.log("Chat seleccionado:", chat)}
          chatHistory={chatHistory.filter((chat) => chat.isImportant)}
        />
      )}
    </div>
  );
};

export default AssistantPage;
