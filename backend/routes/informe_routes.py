# routes/informe_routes.py
from quart import Blueprint, jsonify, request
from services.informe_service import generar_informe
import logging

logger = logging.getLogger(__name__)

informe_bp = Blueprint('informe', __name__, url_prefix='/api/informe')

@informe_bp.route('/generar', methods=['POST'])
async def generar_informe_endpoint():
    try:
        data = await request.get_json()
        query = data.get("query", "").strip()
        chat_ids = data.get("chat_ids", [])
        
        if not query or not chat_ids:
            return jsonify({"error": "Faltan parámetros: 'query' y/o 'chat_ids'"}), 400
            
        informe = await generar_informe(query, chat_ids)  # Agregamos await aquí
        return jsonify({"informe": informe}), 200
    except Exception as e:
        logger.error(f"Error al generar el informe: {e}")
        return jsonify({"error": str(e)}), 500