import { Chat } from '@/types';
import { X } from 'lucide-react';

interface SearchPanelProps {
  onClose: () => void;
  onSelectChat: (chat: Chat) => void;
  chatHistory: Chat[];
}

const SearchPanel: React.FC<SearchPanelProps> = ({ onClose, onSelectChat, chatHistory }) => (
  <div className="fixed right-0 top-0 h-full w-80 bg-gray-800 border-l border-gray-700 p-4 transform transition-transform">
    <div className="flex justify-between items-center mb-4">
      <h3 className="text-lg font-semibold text-gray-200">Búsqueda de Chats</h3>
      <button onClick={onClose} className="text-gray-400 hover:text-gray-200">
        <X size={20} />
      </button>
    </div>
    <input
      type="text"
      placeholder="Buscar..."
      className="w-full p-2 bg-gray-700 border border-gray-600 rounded-lg text-gray-200 mb-4"
    />
    <div className="space-y-2">
      {chatHistory.map((chat, idx) => (
        <div 
          key={idx}
          className="p-2 bg-gray-700 rounded-lg cursor-pointer hover:bg-gray-600"
          onClick={() => onSelectChat(chat)}
        >
          <p className="text-sm text-gray-200 truncate">{chat.question}</p>
          <p className="text-xs text-gray-400">Fecha: {new Date().toLocaleDateString()}</p>
        </div>
      ))}
    </div>
  </div>
);

export default SearchPanel;
