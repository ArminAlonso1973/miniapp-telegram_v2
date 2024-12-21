import os
import re
import asyncio
import numpy as np
from typing import List, Dict
from dotenv import load_dotenv
import anthropic
import pypdf
import logging

logger = logging.getLogger(__name__)

class AdaptiveChunker:
    def __init__(self, base_chunk_size: int = 1024):
        self.base_chunk_size = base_chunk_size
    
    def calculate_complexity(self, text: str) -> float:
        """Calcula la complejidad del texto basada en múltiples factores"""
        try:
            words = text.split()
            avg_word_length = np.mean([len(word) for word in words]) if words else 0
            punctuation_density = len(re.findall(r'[.,;:!?]', text)) / len(text) if text else 0
            technical_terms = r'\b(pursuant|hereinafter|notwithstanding|thereof|whereby|herein)\b'
            technical_density = len(re.findall(technical_terms, text, re.I)) / len(words) if words else 0
            complexity = (avg_word_length / 15 + punctuation_density + technical_density) / 3
            return min(max(complexity, 0), 1)
        except Exception as e:
            logger.error(f"Error calculando complejidad: {e}")
            return 0.5

    def create_adaptive_chunks(self, text: str) -> List[Dict[str, any]]:
        """Crea chunks con tamaño adaptativo basado en la complejidad del texto"""
        try:
            sentences = re.split(r'(?<=[.!?])\s+', text)
            chunks = []
            current_chunk = []
            current_length = 0
            
            for sentence in sentences:
                complexity = self.calculate_complexity(sentence)
                adjusted_size = int(self.base_chunk_size * (1.2 - complexity))
                sentence_length = len(sentence)
                
                if current_length + sentence_length > adjusted_size and current_chunk:
                    chunk_text = ' '.join(current_chunk)
                    chunks.append({'text': chunk_text, 'length': len(chunk_text)})
                    current_chunk = [sentence]
                    current_length = sentence_length
                else:
                    current_chunk.append(sentence)
                    current_length += sentence_length
            
            if current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append({'text': chunk_text, 'length': len(chunk_text)})
            
            return chunks
        except Exception as e:
            logger.error(f"Error creando chunks adaptativos: {e}")
            raise

class ClaudeSummarizer:
    def __init__(self, chunk_size: int = 1024, batch_size: int = 4):
        load_dotenv()
        self.client = anthropic.Anthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        self.chunk_size = chunk_size
        self.batch_size = batch_size
        self.adaptive_chunker = AdaptiveChunker(base_chunk_size=chunk_size)

    async def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extracción asincrónica de texto de PDF"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
            logger.info(f"Texto extraído con éxito. Longitud: {len(text)} caracteres.")
            return text
        except Exception as e:
            logger.error(f"Error al extraer texto del PDF: {e}")
            raise

    def preprocess_text(self, text: str) -> str:
        """Preprocesamiento de texto mejorado"""
        try:
            logger.info("Iniciando preprocesamiento de texto.")
            text = re.sub(r'\n+', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'[^\w\s.,!?;:\(\)\[\]"\'/-]', '', text)
            preprocessed_text = text.strip()
            logger.info("Preprocesamiento completado.")
            return preprocessed_text
        except Exception as e:
            logger.error(f"Error durante el preprocesamiento del texto: {e}")
            raise

    def create_chunks(self, text: str) -> List[str]:
        """División de texto en chunks usando estrategia adaptativa"""
        try:
            logger.info("Iniciando división adaptativa del texto en chunks.")
            chunks = self.adaptive_chunker.create_adaptive_chunks(text)
            return [chunk['text'] for chunk in chunks]
        except Exception as e:
            logger.error(f"Error al dividir texto en chunks: {e}")
            raise

    async def summarize_chunk(self, chunk: str) -> str:
        """Resumen asincrónico de un chunk"""
        try:
            response = await asyncio.to_thread(
                self.client.messages.create,
                model="claude-3-haiku-20240307",
                max_tokens=300,
                messages=[
                    {"role": "user", "content": f"Resume el siguiente texto: {chunk}"}
                ]
            )
            if hasattr(response, 'content'):
                logger.info("Chunk resumido exitosamente.")
                return response.content
            else:
                logger.error("La respuesta de la API no contiene el atributo 'content'.")
                return ""
        except Exception as e:
            logger.error(f"Error al resumir chunk: {e}")
            return ""

    async def summarize_document(self, pdf_path: str) -> Dict[str, str]:
        """Resumen asincrónico de documento completo"""
        try:
            text = await self.extract_text_from_pdf(pdf_path)
            clean_text = self.preprocess_text(text)
            chunks = self.create_chunks(clean_text)

            summaries = await asyncio.gather(*[self.summarize_chunk(chunk) for chunk in chunks])
            final_summary = " ".join(summaries)
            
            result = {
                "original_length": len(clean_text),
                "summary_length": len(final_summary),
                "summary": final_summary,
                "num_chunks": len(chunks)
            }
            logger.info("Documento resumido exitosamente.")
            return result
        except Exception as e:
            logger.error(f"Error en el proceso de resumen: {e}")
            raise
