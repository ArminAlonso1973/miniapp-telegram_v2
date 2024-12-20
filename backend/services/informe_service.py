# services/informe_service.py
from services.chat_service import obtener_chat_por_id
from services.openai_service import consultar_openai
import logging

logger = logging.getLogger(__name__)

async def generar_informe(query, chat_ids):
    """
    Genera un informe tributario basado en los chats seleccionados y una consulta específica.
    """
    try:
        # Obtener el contenido de los chats seleccionados
        chats = []
        for chat_id in chat_ids:
            chat = await obtener_chat_por_id(chat_id)
            if chat:
                chats.append(chat['content'])

        if not chats:
            raise ValueError("No se encontraron chats para generar el informe.")

        # Crear el prompt para OpenAI
        prompt_lines = [f"- {chat}" for chat in chats]
        prompt = (
            f"Genera un informe tributario basado en la consulta: '{query}'.\n"
            "Los siguientes son los mensajes relevantes:\n"
            f"{chr(10).join(prompt_lines)}\n\n"
            "El informe debe estar estructurado en Markdown e incluir:\n"
            "- Una introducción clara.\n"
            "- Resumen de los puntos clave.\n"
            "- Detalles adicionales relevantes.\n"
        )

        # Consultar a OpenAI y esperar la respuesta
        try:
            respuesta = await consultar_openai(prompt)
            if not respuesta:
                raise ValueError("No se recibió respuesta de OpenAI")
            return respuesta
        except Exception as e:
            logger.error(f"Error en la consulta a OpenAI: {e}")
            raise RuntimeError(f"Error al consultar OpenAI: {str(e)}")

    except Exception as e:
        logger.error(f"Error en generar_informe: {e}")
        raise RuntimeError(f"Error al generar el informe: {str(e)}")