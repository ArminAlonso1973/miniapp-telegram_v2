interface SaveButtonProps {
    isSaved: boolean; // Estado de guardado
    onToggle: () => void; // Función que alterna el estado de guardado
  }
  
  const SaveButton: React.FC<SaveButtonProps> = ({ isSaved, onToggle }) => (
    <button
      onClick={onToggle}
      className={`px-4 py-2 rounded ${
        isSaved ? 'bg-yellow-500 text-white' : 'bg-gray-300 text-gray-700'
      }`}
    >
      {isSaved ? 'Guardado' : 'Guardar'}
    </button>
  );
  
  export default SaveButton;
  