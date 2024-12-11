import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

interface TypewriterEffectProps {
  text: string;
  speed?: number; // Velocidad en milisegundos por carácter
}

const TypewriterEffect: React.FC<TypewriterEffectProps> = ({ text, speed = 180 }) => {
  const [displayedText, setDisplayedText] = useState('');

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      setDisplayedText((prev) => prev + text[index]);
      index++;
      if (index === text.length) {
        clearInterval(interval); // Detener el intervalo cuando termine el texto
      }
    }, speed);

    return () => clearInterval(interval); // Limpiar el intervalo si el componente se desmonta
  }, [text, speed]);

  return (
    <div>
      <ReactMarkdown>{displayedText}</ReactMarkdown>
    </div>
  );
};

export default TypewriterEffect;
