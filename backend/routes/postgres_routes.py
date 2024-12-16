from quart import Blueprint, request, jsonify
from services.postgres_service import buscar_respuestas_postgres
import logging

logger = logging.getLogger(__name__)

postgres_bp = Blueprint('postgres', __name__)


@postgres_bp.route('/query', methods=['POST'])
async def execute_query_postgres():
    data = await request.get_json()
    keys = data.get("keys")
    results = await buscar_respuestas_postgres(keys)
    return jsonify({"status": "success", "results": results})



