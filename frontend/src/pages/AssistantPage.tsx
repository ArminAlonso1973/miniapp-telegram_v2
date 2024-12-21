// Página del Asistente Tributario
import { useState } from 'react';
import { ArrowLeft, Search, Bookmark, BookmarkCheck } from 'lucide-react';
import QuestionInput from '@/components/QuestionInput';
import SearchPanel from '@/components/SearchPanel';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

// Define la estructura de un chat en el historial
interface Chat {
  question: string;
  answer: {
    content: string; // Respuesta del asistente
    references: string[]; // Referencias legales asociadas
  };
  isSaved: boolean; // Indica si el chat está guardado
  categories: string[]; // Categorías asociadas al chat
}

interface AssistantPageProps {
  onBack: () => void; // Función para volver a la página anterior
}

const AssistantPage: React.FC<AssistantPageProps> = ({ onBack }) => {
  // Estado del historial de chats
  const [chatHistory, setChatHistory] = useState<Chat[]>([
    {
      question: '¿Cuál es el plazo para declarar el IVA?',
      answer: {
        content: 'El plazo es el día 12 del mes siguiente para no electrónicos y el 20 para electrónicos.',
        references: ['Art. 64 Código Tributario', 'Circular SII N°45'],
      },
      isSaved: false,
      categories: ['IVA'],
    },
  ]);

  const [savedChats, setSavedChats] = useState<Chat[]>([]); // Estado de chats guardados
  const [availableCategories, setAvailableCategories] = useState<string[]>(['IVA', 'Renta', 'Depreciación']);
  const [showSearchPanel, setShowSearchPanel] = useState(false); // Estado del panel de búsqueda

  // Agrega una nueva pregunta simulada al historial
  const handleSendQuestion = (question: string) => {
    const response = {
      content: `Respuesta simulada para: "${question}"`,
      references: ['Art. 123 Código Tributario'],
    };
    setChatHistory((prev) => [...prev, { question, answer: response, isSaved: false, categories: [] }]);
  };

  // Alterna el estado de guardado de un chat y actualiza la lista de guardados
  const toggleSaveChat = (index: number) => {
    setChatHistory((prev) =>
      prev.map((chat, idx) => (idx === index ? { ...chat, isSaved: !chat.isSaved } : chat))
    );

    const chat = chatHistory[index];
    setSavedChats((prev) =>
      chat.isSaved ? prev.filter((savedChat) => savedChat.question !== chat.question) : [...prev, chat]
    );
  };

  // Agrega una categoría a un chat
  const addCategoryToChat = (index: number, category: string) => {
    setChatHistory((prev) =>
      prev.map((chat, idx) =>
        idx === index && !chat.categories.includes(category)
          ? { ...chat, categories: [...chat.categories, category] }
          : chat
      )
    );
  };

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Encabezado con botón para regresar */}
      <div className="border-b border-gray-700 bg-gray-800 p-4 flex items-center">
        <button onClick={onBack} className="flex items-center text-gray-400 hover:text-yellow-500">
          <ArrowLeft className="mr-2" /> Volver al inicio
        </button>
        <h2 className="text-xl font-semibold text-gray-200 ml-4">Asistente Tributario</h2>
      </div>

      {/* Historial de chats */}
      <div className="max-w-4xl mx-auto p-4">
        <QuestionInput onSend={handleSendQuestion} />
        <div className="space-y-4 mt-4">
          {chatHistory.map((chat, index) => (
            <div key={index} className="space-y-2">
              <div className="bg-gray-800 p-3 rounded-lg flex justify-between items-center">
                <p className="text-gray-200">{chat.question}</p>
                <button onClick={() => toggleSaveChat(index)} className={chat.isSaved ? 'text-yellow-500' : 'text-gray-400'}>
                  {chat.isSaved ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
                </button>
              </div>
              <Card className="bg-gray-700 border-gray-600">
                <CardHeader>
                  <CardTitle>Respuesta del Asistente</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>{chat.answer.content}</p>
                  <ul>{chat.answer.references.map((ref, idx) => <li key={idx}>{ref}</li>)}</ul>
                </CardContent>
              </Card>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AssistantPage;
