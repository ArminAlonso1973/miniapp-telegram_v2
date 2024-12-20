# services/openai_service.py
import os
from dotenv import load_dotenv
from openai import OpenAI
import asyncio
import logging
from services.openai_service import openai_client  # Importa el cliente OpenAI actualizado
import re

# Cargar variables de entorno
load_dotenv()

# Inicializar el cliente de OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def consultar_openai(prompt: str):
    """
    Función base para consultar OpenAI de forma asíncrona.
    """
    try:
        response = await asyncio.to_thread(
            lambda: openai_client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Error al consultar OpenAI: {e}")

# backend/services/llm_service.py



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
    try:
        # Asegurarse de usar await aquí
        respuesta = await consultar_openai(prompt)
        return respuesta
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




