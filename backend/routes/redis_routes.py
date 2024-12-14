from quart import Blueprint, request, jsonify
from services.redis_service import guardar_cache, obtener_cache

redis_bp = Blueprint('redis', __name__)

@redis_bp.route('/cache', methods=['GET'])
async def get_cache():
    """Obtener datos del caché de Redis."""
    clave = request.args.get('clave')
    if not clave:
        return jsonify({"status": "error", "message": "Falta el parámetro 'clave'"}), 400

    valor = await obtener_cache(clave)
    if valor:
        return jsonify({"status": "success", "value": valor.decode()}), 200
    return jsonify({"status": "error", "message": "Clave no encontrada"}), 404

@redis_bp.route('/cache', methods=['POST'])
async def set_cache():
    """Guardar datos en el caché de Redis."""
    data = await request.get_json()
    clave = data.get("clave")
    valor = data.get("valor")
    expiracion = data.get("expiracion", 3600)

    if not clave or not valor:
        return jsonify({"status": "error", "message": "Faltan parámetros 'clave' o 'valor'"}), 400

    await guardar_cache(clave, valor, expiracion)
    return jsonify({"status": "success", "message": "Valor almacenado correctamente"}), 200
