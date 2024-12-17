# backend/services/llm_service.py

import logging
from services.openai_service import openai_client  # Importa el cliente OpenAI actualizado
import re

logger = logging.getLogger(__name__)

async def generar_prompt_completo(message: str, respuestas: list) -> str:
    """Genera el prompt para OpenAI."""
    try:
        prompt = (
            "Eres un experto en tributación chilena y legislación fiscal. "
            "Responde la siguiente pregunta del usuario usando el contexto proporcionado.\n\n"
            f"Pregunta: {message}\n\n"
            "Contexto:\n"
        )
        for idx, respuesta in enumerate(respuestas, 1):
            prompt += (
                f"{idx}. Pregunta: {respuesta['question']}\n"
                f"   Respuesta: {respuesta['answer']}\n"
                f"   Referencia legal: {respuesta['legal_reference']}\n"
            )
        return prompt
    except Exception as e:
        logger.error(f"Error generando el prompt: {e}")
        return "Error al generar el prompt."

async def consultar_llm_respuesta_final(prompt: str) -> str:
    """Consulta OpenAI para generar la respuesta final."""
    try:
        # Usa el cliente OpenAI asincrónico directamente
        respuesta = await openai_client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",  # Ajusta el modelo según configuración
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        # Extraer la respuesta del modelo
        return respuesta.choices[0].message.content
    except Exception as e:
        logger.error(f"Error consultando LLM para respuesta final: {e}")
        return "Error al consultar el modelo LLM."

async def normalizar_consulta(consulta: str) -> str:
    """
    Limpia y estructura una consulta del usuario.
    """
    try:
        consulta = consulta.strip().lower()
        consulta = re.sub(r"[^a-zA-Z0-9áéíóúñü\s]", "", consulta)
        consulta = re.sub(r"\s+", " ", consulta)
        return consulta
    except Exception as e:
        raise ValueError(f"Error al normalizar consulta: {str(e)}")




