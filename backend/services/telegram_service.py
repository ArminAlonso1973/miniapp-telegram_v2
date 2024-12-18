# services/telegram_service.py

import os
import requests
import logging
import aiohttp

logger = logging.getLogger(__name__)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_message(chat_id: str, message: str) -> dict:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    logger.info(f"Respuesta de Telegram: {result}")
    return result

async def edit_message_text(chat_id: int, message_id: int, text: str, reply_markup=None):
    """Edita el texto de un mensaje ya enviado y opcionalmente su teclado inline."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text
    }
    if reply_markup is not None:
        # reply_markup es una lista de listas de dict con "text" y "callback_data"
        payload["reply_markup"] = {"inline_keyboard": reply_markup}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            resp_json = await resp.json()
            logger.info(f"Respuesta de editMessageText: {resp_json}")
            return resp_json


def send_message_with_inline_keyboard(chat_id: str, message: str, keyboard: list) -> dict:
    """Envía un mensaje con teclado inline."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "reply_markup": {
            "inline_keyboard": keyboard
        }
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    logger.info(f"Respuesta de Telegram con inline keyboard: {result}")
    return result

async def answer_callback_query(callback_query_id: str, text: str):
    """Responde a una callback_query de Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    payload = {
        "callback_query_id": callback_query_id,
        "text": text,
        "show_alert": False
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            resp_json = await resp.json()
            logger.info(f"Respuesta de answerCallbackQuery: {resp_json}")
            return resp_json

