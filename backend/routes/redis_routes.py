# Archivo: routes/redis_routes.py
from quart import Blueprint, request, jsonify
from services.redis_service import obtener_cache, guardar_cache
import logging

logger = logging.getLogger(__name__)

redis_bp = Blueprint('redis', __name__)

@redis_bp.route('/cache', methods=['GET'])
async def get_cache():
    """Endpoint para obtener datos del caché de Redis."""
    try:
        clave = request.args.get('clave')
        if not clave:
            return jsonify({"status": "error", "message": "Falta el parámetro 'clave'"}), 400

        valor = await obtener_cache(clave)
        if valor:
            return jsonify({"status": "success", "value": valor.decode()}), 200
        return jsonify({"status": "error", "message": "Clave no encontrada"}), 404
    except Exception as e:
        logger.error(f"Error al obtener datos del caché Redis: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@redis_bp.route('/cache', methods=['POST'])
async def set_cache():
    """Endpoint para guardar datos en el caché de Redis."""
    try:
        data = await request.get_json()
        clave = data.get("clave")
        valor = data.get("valor")
        expiracion = data.get("expiracion", 3600)

        if not clave or not valor:
            return jsonify({"status": "error", "message": "Faltan parámetros 'clave' o 'valor'"}), 400

        await guardar_cache(clave, valor, expiracion)
        return jsonify({"status": "success", "message": "Valor almacenado correctamente"}), 200
    except Exception as e:
        logger.error(f"Error al guardar datos en el caché Redis: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
