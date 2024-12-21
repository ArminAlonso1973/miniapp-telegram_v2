import React from 'react';
import { Chat } from '@/types';

const ChatHistory: React.FC<{ history: Chat[] }> = ({ history }) => (
  <div className="space-y-4">
    {history.map((chat, index) => (
      <div key={index} className="space-y-2">
        {/* Pregunta */}
        <div className="bg-gray-800 p-3 rounded-lg">
          <p className="text-gray-200">{chat.question}</p>
        </div>

        {/* Respuesta */}
        <div className="ml-4">
          <p className="text-gray-200">{chat.answer.content}</p>

          {/* Verificación robusta para references */}
          {Array.isArray(chat.answer.references) && chat.answer.references.length > 0 && (
            <ul className="text-sm text-yellow-500">
              {chat.answer.references.map((ref, idx) => (
                <li key={idx}>{ref}</li>
              ))}
            </ul>
          )}
        </div>
      </div>
    ))}
  </div>
);

export default ChatHistory;
