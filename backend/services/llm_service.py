import logging
from services.openai_service import consultar_openai

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
        respuesta = await consultar_openai(prompt)
        return respuesta.get("respuesta", "No se pudo obtener una respuesta del modelo.")
    except Exception as e:
        logger.error(f"Error consultando LLM para respuesta final: {e}")
        return "Error al consultar el modelo LLM."
