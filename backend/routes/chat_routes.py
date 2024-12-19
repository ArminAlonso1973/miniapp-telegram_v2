from quart import Blueprint, request, jsonify, send_file
from services.chat_service import buscar_chats, obtener_chat_por_id, descargar_chat
import logging
import os

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chats')

@chat_bp.route('/', methods=['GET'])
async def buscar_chats_endpoint():
    """Buscar chats con filtros."""
    try:
        query = request.args.get('query', '')
        user_id = request.args.get('user_id', None)
        chats = await buscar_chats(query, user_id)
        return jsonify(chats), 200
    except Exception as e:
        logger.error(f"Error al buscar chats: {e}")
        return jsonify({"error": "Error al buscar chats"}), 500

@chat_bp.route('/<int:chat_id>', methods=['GET'])
async def obtener_chat(chat_id):
    """Obtener contenido de un chat por ID."""
    try:
        chat = await obtener_chat_por_id(chat_id)
        if chat:
            return jsonify(chat), 200
        return jsonify({"error": "Chat no encontrado"}), 404
    except Exception as e:
        logger.error(f"Error al obtener chat: {e}")
        return jsonify({"error": "Error al obtener chat"}), 500

@chat_bp.route('/<int:chat_id>/download', methods=['GET'])
async def descargar_chat_endpoint(chat_id):
    """Descargar chat como archivo de texto."""
    try:
        file_path = await descargar_chat(chat_id)
        return await send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "Archivo no encontrado"}), 404
    except Exception as e:
        logger.error(f"Error al descargar chat: {e}")
        return jsonify({"error": "Error al descargar chat"}), 500
