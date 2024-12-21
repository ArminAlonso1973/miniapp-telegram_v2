import React, { useState } from "react";
import { ArrowLeft, Book, Tag, Home } from "lucide-react";
import SaveButton from "@/components/ui/SaveButton"; // Importa el botón genérico

// Estructura de un artículo legal
interface Article {
  id: number;
  number: string;
  content: string;
  isSaved: boolean; // Indica si está guardado
  tags: string[]; // Etiquetas asociadas al artículo
}

// Estructura de un texto legal
interface LegalText {
  id: number;
  title: string;
  articles: Article[];
}

// Props del componente
interface LegalTextsSystemProps {
  onBack: () => void; // Función para volver a la página anterior
  onHome: () => void; // Función para volver al menú principal
}

// Datos de ejemplo para textos legales
const demoLegalTexts: LegalText[] = [
  {
    id: 1,
    title: "Código Tributario",
    articles: [
      { id: 1, number: "Art. 1", content: "La presente ley regula las relaciones jurídicas originadas por los tributos...", isSaved: false, tags: [] },
      { id: 2, number: "Art. 2", content: "Para los fines de esta ley, se entiende por tributos los impuestos, las tasas...", isSaved: false, tags: [] },
      { id: 3, number: "Art. 3", content: "Las normas tributarias regirán desde la fecha en que entren en vigencia...", isSaved: false, tags: [] }
    ]
  },
  {
    id: 2,
    title: "Ley de Impuesto a la Renta",
    articles: [
      { id: 4, number: "Art. 1", content: "Establécese, de conformidad a la presente ley, un impuesto sobre la renta...", isSaved: false, tags: [] },
      { id: 5, number: "Art. 2", content: "Para los efectos de la presente ley se entenderá por renta...", isSaved: false, tags: [] },
      { id: 6, number: "Art. 3", content: "Salvo disposición en contrario de la presente ley, toda persona domiciliada...", isSaved: false, tags: [] }
    ]
  }
];

const LegalTextsSystem: React.FC<LegalTextsSystemProps> = ({ onBack, onHome }) => {
  const [currentView, setCurrentView] = useState<"list" | "detail">("list");
  const [selectedText, setSelectedText] = useState<LegalText | null>(null);

  // Función para alternar el estado de guardado de un artículo
  const toggleSaveArticle = (articleId: number) => {
    if (selectedText) {
      setSelectedText({
        ...selectedText,
        articles: selectedText.articles.map((article) =>
          article.id === articleId ? { ...article, isSaved: !article.isSaved } : article
        ),
      });
    }
  };

  // Función para agregar etiquetas a un artículo
  const addTagToArticle = (articleId: number, tag: string) => {
    if (selectedText) {
      setSelectedText({
        ...selectedText,
        articles: selectedText.articles.map((article) =>
          article.id === articleId && !article.tags.includes(tag)
            ? { ...article, tags: [...article.tags, tag] }
            : article
        ),
      });
    }
  };

  const LegalTextsList = () => (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {demoLegalTexts.map((text) => (
        <div
          key={text.id}
          className="bg-gray-800 border border-gray-700 cursor-pointer hover:border-yellow-500 transition-colors p-4 rounded"
          onClick={() => {
            setSelectedText(text);
            setCurrentView("detail");
          }}
        >
          <div className="flex items-center mb-3">
            <Book className="w-5 h-5 text-yellow-500 mr-2" />
            <h3 className="text-gray-200 font-medium">{text.title}</h3>
          </div>
          <p className="text-sm text-gray-400">{text.articles.length} artículos</p>
        </div>
      ))}
    </div>
  );

  const LegalTextDetail = () => (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-6">
        <button
          className="flex items-center text-gray-400 hover:text-yellow-500"
          onClick={() => setCurrentView("list")}
        >
          <ArrowLeft className="mr-2 w-5 h-5" />
          Volver atrás
        </button>
        <span className="text-gray-200 font-medium">{selectedText?.title}</span>
      </div>

      <div className="grid gap-4">
        {selectedText?.articles.map((article) => (
          <div key={article.id} className="bg-gray-800 border border-gray-700 p-4 rounded">
            <div className="flex items-center justify-between mb-2">
              <h4 className="text-yellow-500 font-medium">{article.number}</h4>
              <div className="flex gap-2">
                {/* Botón de guardar con comportamiento genérico */}
                <SaveButton
                  isSaved={article.isSaved}
                  onToggle={() => toggleSaveArticle(article.id)}
                />
                <button
                  className="text-gray-400 hover:text-yellow-500"
                  onClick={() => {
                    const tag = prompt("Ingrese una etiqueta para este artículo:");
                    if (tag) addTagToArticle(article.id, tag);
                  }}
                >
                  <Tag className="w-5 h-5" />
                </button>
              </div>
            </div>
            <p className="text-gray-200 text-sm">{article.content}</p>
            {article.tags.length > 0 && (
              <div className="mt-2">
                <p className="text-sm text-gray-400">Etiquetas:</p>
                <div className="flex flex-wrap gap-2">
                  {article.tags.map((tag, idx) => (
                    <span
                      key={idx}
                      className="bg-yellow-500 text-gray-900 px-2 py-1 rounded text-xs"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <div className="border-b border-gray-700 bg-gray-800 p-4 flex justify-between items-center">
        <button
          onClick={onHome}
          className="flex items-center text-gray-400 hover:text-yellow-500"
        >
          <Home className="mr-2 w-5 h-5" />
          Menú Principal
        </button>
        <h2 className="text-xl font-semibold text-gray-200 text-center flex-1">
          Textos Legales
        </h2>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto p-6">
        {currentView === "list" && <LegalTextsList />}
        {currentView === "detail" && selectedText && <LegalTextDetail />}
      </div>
    </div>
  );
};

export default LegalTextsSystem;
