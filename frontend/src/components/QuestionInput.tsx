import React, { useState } from 'react';

interface QuestionInputProps {
  onSend: (question: string) => void;
}

const QuestionInput: React.FC<QuestionInputProps> = ({ onSend }) => {
  const [question, setQuestion] = useState('');

  return (
    <div className="flex gap-2">
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Escribe tu consulta aquí"
        className="flex-1 p-3 bg-gray-200 border border-gray-300 rounded-lg"
      />
      <button
        onClick={() => {
          if (question.trim()) {
            onSend(question);
            setQuestion('');
          }
        }}
        className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
      >
        Enviar
      </button>
    </div>
  );
};

export default QuestionInput;
