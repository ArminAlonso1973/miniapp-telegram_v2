import os
import requests
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

def send_message(chat_id: str, message: str) -> dict:
    """Envía un mensaje a través de la API de Telegram."""
    try:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            logger.error("El token de Telegram no está configurado en las variables de entorno.")
            raise ValueError("El token de Telegram no está configurado")

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }

        logger.info(f"Enviando solicitud a Telegram: {url} con payload {payload}")
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP

        result = response.json()
        logger.info(f"Respuesta de Telegram: {result}")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Error al enviar mensaje a Telegram: {e}")
        return {"ok": False, "error": str(e)}
