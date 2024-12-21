import os
import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class LegalTextsService:
    def __init__(self):
        self.legal_texts = {}  # Simula una base de datos para textos legales
        self.articles = {}  # Simula una base de datos para artículos
        self.text_id_counter = 1
        self.article_id_counter = 1

    async def process_legal_text(self, file_path: str) -> int:
        """Procesa un archivo de texto legal y extrae los artículos."""
        try:
            logger.info(f"Procesando texto legal desde: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Extraer artículos usando una expresión regular
            articles = re.split(r'\bArt\. \d+\b', content)
            logger.info(f"Se encontraron {len(articles) - 1} artículos.")

            # Guardar el texto legal y sus artículos
            text_id = self.text_id_counter
            self.text_id_counter += 1
            self.legal_texts[text_id] = {"id": text_id, "title": os.path.basename(file_path)}

            for index, article in enumerate(articles[1:], start=1):
                self.articles[self.article_id_counter] = {
                    "id": self.article_id_counter,
                    "text_id": text_id,
                    "article_number": index,
                    "content": article.strip()
                }
                self.article_id_counter += 1

            os.remove(file_path)  # Limpiar archivo temporal
            return text_id
        except Exception as e:
            logger.error(f"Error al procesar texto legal: {e}")
            raise

    async def list_legal_texts(self) -> List[Dict]:
        """Devuelve la lista de textos legales."""
        return list(self.legal_texts.values())

    async def list_articles(self, text_id: int) -> List[Dict]:
        """Devuelve los artículos de un texto legal."""
        return [article for article in self.articles.values() if article["text_id"] == text_id]
