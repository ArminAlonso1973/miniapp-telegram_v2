import { useState } from 'react';
import { ArrowLeft, Search, Bookmark, BookmarkCheck } from 'lucide-react';
import QuestionInput from '@/components/QuestionInput';
import SearchPanel from '@/components/SearchPanel';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

interface Chat {
  question: string;
  answer: {
    content: string;
    references: string[];
  };
  isSaved: boolean;
  categories: string[];
}

interface AssistantPageProps {
  onBack: () => void;
}

const AssistantPage: React.FC<AssistantPageProps> = ({ onBack }) => {
  const [chatHistory, setChatHistory] = useState<Chat[]>([
    {
      question: '¿Cuál es el plazo para declarar el IVA?',
      answer: {
        content:
          'El plazo para declarar el IVA es el día 12 del mes siguiente para contribuyentes no electrónicos y el día 20 para electrónicos.',
        references: ['Art. 64 Código Tributario', 'Circular SII N°45'],
      },
      isSaved: false,
      categories: ['IVA'],
    },
    {
      question: '¿Cómo se calcula la depreciación acelerada?',
      answer: {
        content:
          'La depreciación acelerada reduce a un tercio la vida útil normal del bien. Por ejemplo, si la vida útil es 6 años, se puede depreciar en 2 años.',
        references: ['Art. 31 N°5 Ley de Impuesto a la Renta', 'Circular N°12'],
      },
      isSaved: false,
      categories: ['Depreciación'],
    },
  ]); // Preguntas simuladas como estado inicial

  const [savedChats, setSavedChats] = useState<Chat[]>([]); // Chats guardados
  const [availableCategories, setAvailableCategories] = useState<string[]>([
    'IVA',
    'Renta',
    'Depreciación',
  ]); // Categorías disponibles
  const [showSearchPanel, setShowSearchPanel] = useState(false);

  const handleSendQuestion = (question: string) => {
    const response = {
      content: `Esta es una respuesta simulada para: "${question}"`,
      references: ["Art. 123 Código Tributario", "Circular SII N°45"],
    };

    setChatHistory((prev) => [
      ...prev,
      { question, answer: response, isSaved: false, categories: [] },
    ]);
  };

  const toggleSaveChat = (index: number) => {
    setChatHistory((prev) =>
      prev.map((chat, idx) =>
        idx === index ? { ...chat, isSaved: !chat.isSaved } : chat
      )
    );

    const chat = chatHistory[index];
    setSavedChats((prev) => {
      if (chat.isSaved) {
        // Si estaba guardado, lo quitamos
        return prev.filter((savedChat) => savedChat.question !== chat.question);
      } else {
        // Si no estaba guardado, lo agregamos
        return [...prev, chat];
      }
    });
  };

  const addCategoryToChat = (index: number, category: string) => {
    setChatHistory((prev) =>
      prev.map((chat, idx) =>
        idx === index && !chat.categories.includes(category)
          ? { ...chat, categories: [...chat.categories, category] }
          : chat
      )
    );
  };

  const removeCategoryFromChat = (index: number, category: string) => {
    setChatHistory((prev) =>
      prev.map((chat, idx) =>
        idx === index
          ? {
              ...chat,
              categories: chat.categories.filter((cat) => cat !== category),
            }
          : chat
      )
    );
  };

  const handleAddNewCategory = (newCategory: string) => {
    if (!availableCategories.includes(newCategory)) {
      setAvailableCategories((prev) => [...prev, newCategory]);
    }
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
        <h2 className="text-xl font-semibold text-gray-200 ml-4">
          Asistente Tributario
        </h2>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto p-4">
        {/* Formulario para preguntas */}
        <QuestionInput onSend={handleSendQuestion} />

        {/* Historial de chats */}
        <div className="space-y-4 mt-4">
          {chatHistory.map((chat, index) => (
            <div key={index} className="space-y-2">
              {/* Pregunta */}
              <div className="bg-gray-800 p-3 rounded-lg flex justify-between items-center">
                <p className="text-gray-200">{chat.question}</p>
                <div className="flex gap-2">
                  <button
                    onClick={() => toggleSaveChat(index)}
                    className={`${
                      chat.isSaved
                        ? 'text-yellow-500'
                        : 'text-gray-400 hover:text-yellow-500'
                    }`}
                  >
                    {chat.isSaved ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Respuesta */}
              <div className="ml-4">
                <Card className="bg-gray-700 border-gray-600">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm text-gray-300">
                      Respuesta del Asistente
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-200 mb-4">{chat.answer.content}</p>
                    <div className="border-t border-gray-600 pt-2">
                      <p className="text-sm text-gray-400">Referencias:</p>
                      <ul className="text-sm text-yellow-500">
                        {chat.answer.references.map((ref, idx) => (
                          <li key={idx}>{ref}</li>
                        ))}
                      </ul>
                    </div>

                    {/* Categorías */}
                    <div className="mt-4">
                      <p className="text-sm text-gray-400">Categorías:</p>
                      <div className="flex flex-wrap gap-2">
                        {chat.categories.map((cat) => (
                          <span
                            key={cat}
                            className="text-xs bg-yellow-500 text-gray-900 px-2 py-1 rounded-lg cursor-pointer hover:bg-yellow-600"
                            onClick={() => removeCategoryFromChat(index, cat)}
                          >
                            {cat} &times;
                          </span>
                        ))}
                      </div>
                      <select
                        className="mt-2 p-2 bg-gray-800 border border-gray-600 rounded-lg text-gray-200"
                        onChange={(e) => addCategoryToChat(index, e.target.value)}
                        defaultValue=""
                      >
                        <option value="" disabled>
                          Agregar categoría
                        </option>
                        {availableCategories.map((cat) => (
                          <option key={cat} value={cat}>
                            {cat}
                          </option>
                        ))}
                      </select>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Botón flotante para abrir la búsqueda */}
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
          onSelectChat={(chat) => console.log('Chat seleccionado:', chat)}
          chatHistory={savedChats} // Filtra solo los guardados
        />
      )}
    </div>
  );
};

export default AssistantPage;
