import React, { useState } from "react";
import {
  ArrowLeft,
  Download,
  X,
  Eye,
  Plus,
  Home,
} from "lucide-react";
import { Card } from "@/components/ui/card";

const ReportGeneratorDemo = () => {
  const [showPreview, setShowPreview] = useState(true);
  const [selectedChats, setSelectedChats] = useState([
    {
      question: "¿Cuál es el plazo para declarar IVA mensual?",
      answer: {
        content: "El plazo para declarar y pagar el IVA mensual vence el día 12 de cada mes para contribuyentes de papel y el 20 para contribuyentes electrónicos.",
        references: ["Art. 64 Código Tributario"],
      },
      categories: ["IVA"],
    },
  ]);
  const [legalTexts, setLegalTexts] = useState([
    { text: "Según el artículo 31 de la Ley sobre Impuesto a la Renta...", tags: ["Renta"] },
  ]);
  const [savedReports, setSavedReports] = useState<string[]>([
    "Informe Tributario - Diciembre 2024",
    "Informe Legal - IVA y Renta",
  ]);
  const [filterTag, setFilterTag] = useState<string | null>(null);
  const [filterCategory, setFilterCategory] = useState<string | null>(null);

  const handleDownload = (content: string, fileName: string) => {
    const blob = new Blob([content], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    a.click();
    URL.revokeObjectURL(url);
  };

  const generatePreviewContent = () => {
    return `
# Informe Tributario

## Consultas Seleccionadas
${selectedChats
  .map(
    (chat) => `
### ${chat.question}
${chat.answer.content}
Referencias: ${chat.answer.references.join(", ")}
`
  )
  .join("\n")}

## Artículos Seleccionados
${legalTexts.map((text) => `- ${text.text}`).join("\n")}
    `;
  };

  const saveReport = () => {
    const newReportName = `Informe - ${new Date().toLocaleDateString()}`;
    setSavedReports((prev) => [...prev, newReportName]);
    alert(`Informe guardado: ${newReportName}`);
  };

  const filteredLegalTexts = filterTag
    ? legalTexts.filter((text) => text.tags.includes(filterTag))
    : legalTexts;

  const filteredChats = filterCategory
    ? selectedChats.filter((chat) => chat.categories.includes(filterCategory))
    : selectedChats;

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <div className="border-b border-gray-700 bg-gray-800 p-4 flex items-center justify-between">
        <button
          onClick={() => setShowPreview(!showPreview)}
          className="flex items-center text-gray-400 hover:text-yellow-500"
        >
          <ArrowLeft className="mr-2" />
          {showPreview ? "Editar Selecciones" : "Vista Previa"}
        </button>
        <h2 className="text-xl font-semibold text-gray-200">Generador de Informes</h2>
        <button
          onClick={() => alert("Volviendo al Menú Principal")}
          className="flex items-center text-gray-400 hover:text-yellow-500"
        >
          <Home className="mr-2 w-5 h-5" />
          Menú Principal
        </button>
      </div>

      <div className="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sección de Vista Previa o Selecciones */}
        <div className="lg:col-span-1">
          {showPreview ? (
            <Card className="bg-gray-800 border-gray-700">
              <div className="p-6">
                <h3 className="text-lg font-semibold text-gray-200 mb-4">Vista Previa del Informe</h3>
                <div>
                  <h4 className="text-sm font-medium text-gray-400 mb-2">Consultas Seleccionadas:</h4>
                  {filteredChats.map((chat, idx) => (
                    <div key={idx} className="mb-4">
                      <p className="text-gray-200 font-medium">{chat.question}</p>
                      <p className="text-gray-300">{chat.answer.content}</p>
                      <p className="text-sm text-yellow-500">
                        Referencias: {chat.answer.references.join(", ")}
                      </p>
                    </div>
                  ))}
                </div>
                <div className="mt-4">
                  <h4 className="text-sm font-medium text-gray-400 mb-2">Artículos Seleccionados:</h4>
                  {filteredLegalTexts.map((text, idx) => (
                    <p key={idx} className="text-gray-300 mb-2">- {text.text}</p>
                  ))}
                </div>
                <div className="flex justify-between mt-6">
                  <button
                    onClick={saveReport}
                    className="bg-yellow-500 text-gray-900 px-4 py-2 rounded-lg hover:bg-yellow-600"
                  >
                    Guardar Informe
                  </button>
                  <button
                    onClick={() =>
                      handleDownload(generatePreviewContent(), "informe.md")
                    }
                    className="bg-yellow-500 text-gray-900 px-4 py-2 rounded-lg hover:bg-yellow-600"
                  >
                    <Download className="w-4 h-4 mr-2 inline-block" />
                    Descargar Informe
                  </button>
                </div>
              </div>
            </Card>
          ) : (
            <>
              {/* Visualizadores de Consultas y Artículos */}
              <Card className="bg-gray-800 border-gray-700 mb-6">
                <div className="p-4">
                  <h3 className="text-lg font-semibold text-gray-200 mb-4">Consultas Guardadas</h3>
                  <select
                    className="w-full bg-gray-700 p-2 rounded-lg text-gray-200 mb-4"
                    onChange={(e) => setFilterCategory(e.target.value)}
                    value={filterCategory || ""}
                  >
                    <option value="">Todas</option>
                    <option value="IVA">IVA</option>
                    <option value="Renta">Renta</option>
                  </select>
                  {filteredChats.map((chat, idx) => (
                    <div key={idx} className="p-4 bg-gray-700 rounded-lg mb-4">
                      <p className="text-gray-200 font-medium">{chat.question}</p>
                      <p className="text-gray-300">{chat.answer.content}</p>
                    </div>
                  ))}
                </div>
              </Card>

              <Card className="bg-gray-800 border-gray-700">
                <div className="p-4">
                  <h3 className="text-lg font-semibold text-gray-200 mb-4">Artículos Guardados</h3>
                  <select
                    className="w-full bg-gray-700 p-2 rounded-lg text-gray-200 mb-4"
                    onChange={(e) => setFilterTag(e.target.value)}
                    value={filterTag || ""}
                  >
                    <option value="">Todas</option>
                    <option value="Renta">Renta</option>
                  </select>
                  {filteredLegalTexts.map((text, idx) => (
                    <div key={idx} className="p-4 bg-gray-700 rounded-lg mb-4">
                      <p className="text-gray-200">{text.text}</p>
                    </div>
                  ))}
                </div>
              </Card>
            </>
          )}
        </div>

        {/* Informes Anteriores */}
        <Card className="bg-gray-800 border-gray-700 lg:col-span-1">
          <div className="p-4">
            <h3 className="text-lg font-semibold text-gray-200 mb-4">Informes Guardados</h3>
            {savedReports.map((report, idx) => (
              <div
                key={idx}
                className="flex justify-between items-center bg-gray-700 p-3 rounded-lg mb-3"
              >
                <span className="text-gray-200">{report}</span>
                <div className="flex gap-2">
                  <button
                    className="text-gray-400 hover:text-yellow-500"
                    onClick={() => alert(`Visualizando: ${report}`)}
                  >
                    <Eye className="w-5 h-5" />
                  </button>
                  <button
                    className="text-gray-400 hover:text-yellow-500"
                    onClick={() =>
                      handleDownload(`Contenido del informe: ${report}`, `${report}.md`)
                    }
                  >
                    <Download className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default ReportGeneratorDemo;
