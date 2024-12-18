from quart import Blueprint, request, jsonify
from services.postgres_service import buscar_respuestas_postgres
from services.postgres_service import connect_postgres

import logging

logger = logging.getLogger(__name__)

postgres_bp = Blueprint('postgres', __name__)


@postgres_bp.route('/query', methods=['POST'])
async def execute_query_postgres():
    data = await request.get_json()
    keys = data.get("keys")
    results = await buscar_respuestas_postgres(keys)
    return jsonify({"status": "success", "results": results})


@postgres_bp.route("/test-postgres-select", methods=["GET"])
async def test_postgres_select():
    """Endpoint para obtener registros de la tabla preguntas."""
    try:
        conn = await connect_postgres()
        query = "SELECT * FROM preguntas LIMIT 10;"  # Consulta para obtener los primeros 10 registros
        registros = await conn.fetch(query)
        await conn.close()

        # Convertir registros a una lista de diccionarios
        resultados = [dict(registro) for registro in registros]

        return jsonify({"status": "success", "registros": resultados}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

