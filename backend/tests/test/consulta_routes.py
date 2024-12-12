# backend/routes/consulta_routes.py

from quart import Blueprint, jsonify
import logging

logger = logging.getLogger(__name__)

consulta_bp = Blueprint('consulta', __name__)

@consulta_bp.route('/test', methods=['GET'])
async def test():
    """Endpoint de prueba para verificar que el backend está funcionando."""
    return jsonify({"status": "success", "message": "API funcionando correctamente"})
