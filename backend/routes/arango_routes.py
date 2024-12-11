from quart import Blueprint, request, jsonify
from services.database import db, insert_document
import logging

logger = logging.getLogger(__name__)

arango_bp = Blueprint('arango', __name__)

@arango_bp.route('/test', methods=['GET'])
async def test_arango_connection():
    """Endpoint para verificar la conexión con ArangoDB."""
    try:
        # Verificar la lista de colecciones como prueba de conexión
        collections = db.collections()
        return jsonify({"status": "success", "collections": [col["name"] for col in collections]})
    except Exception as e:
        logger.error(f"Error al verificar la conexión con ArangoDB: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@arango_bp.route('/document', methods=['POST'])
async def insert_document_route():
    """Endpoint para insertar un documento en ArangoDB."""
    try:
        data = await request.get_json()
        collection_name = data.get("collection")
        document = data.get("document")

        if not collection_name or not document:
            return jsonify({"status": "error", "message": "Faltan parámetros 'collection' o 'document'"}), 400

        result = insert_document(collection_name, document)
        return jsonify({"status": "success", "message": "Documento insertado correctamente", "result": result})
    except Exception as e:
        logger.error(f"Error al insertar documento en ArangoDB: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@arango_bp.route('/query', methods=['POST'])
async def execute_query():
    try:
        data = await request.get_json()
        query = data.get("query")

        if not query:
            return jsonify({"status": "error", "message": "Falta el parámetro 'query'"}), 400

        cursor = db.aql.execute(query)
        results = [doc for doc in cursor]
        return jsonify({"status": "success", "results": results}), 200
    except Exception as e:
        logger.error(f"Error al ejecutar la consulta AQL: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
