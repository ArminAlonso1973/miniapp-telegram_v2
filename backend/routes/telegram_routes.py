from quart import Blueprint, request, jsonify
from services.telegram_service import send_message
import logging

logger = logging.getLogger(__name__)

telegram_bp = Blueprint('telegram', __name__)

@telegram_bp.route('/telegram-bot', methods=['POST'])
async def telegram_bot():
    """Endpoint para enviar mensajes al bot de Telegram."""
    logger.info("Entrando a la ruta /telegram-bot")
    try:
        data = await request.get_json()
        chat_id = data.get('chat_id')
        message_text = data.get('message')

        if not chat_id or not message_text:
            logger.error("Faltan parámetros en la solicitud")
            return jsonify({"error": "Faltan parámetros"}), 400

        response = send_message(chat_id, message_text)
        return jsonify(response)

    except Exception as e:
        logger.exception("Error en /telegram-bot:")
        return jsonify({"error": str(e)}), 500
