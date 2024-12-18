from quart import Blueprint, request, jsonify
from services.assistant_service import AssistantService
from services.postgres_service import buscar_respuestas_postgres
import os
import logging

logger = logging.getLogger(__name__)

# Instancia de AssistantService
from services.openai_service import openai_client
assistant_service = AssistantService(openai_client)

asistente_bp = Blueprint("asistente", __name__)

@asistente_bp.route("/preguntar", methods=["POST"])
async def preguntar():
    """Endpoint para responder preguntas tributarias."""
    try:
        data = await request.get_json()
        logger.info(f"Datos recibidos: {data}")  # Log de entrada

        pregunta = data.get("pregunta")

        if not pregunta:
            logger.warning("No se proporcionó ninguna pregunta.")
            return jsonify({"error": "Debe proporcionar una pregunta."}), 400

        logger.info(f"Procesando pregunta: {pregunta}")
        
        respuesta = await assistant_service.iniciar_flujo_asistente(
            thread_id="123", assistant_id=os.getenv("ASSISTANT_ID"), pregunta=pregunta
        )
        logger.info(f"Respuesta obtenida del servicio: {respuesta}")  # Log de salida

        return jsonify({"status": "success", "respuesta": respuesta}), 200

    except Exception as e:
        logger.error(f"Error en /preguntar: {str(e)}", exc_info=True)  # Log detallado con traceback
        return jsonify({"status": "error", "error": str(e)}), 500



@asistente_bp.route("/test-postgres", methods=["POST"])
async def test_postgres():
    """Prueba de conexión y consulta en PostgreSQL."""
    try:
        data = await request.get_json()
        keys = data.get("keys", [])

        if not keys:
            return jsonify({"error": "No se proporcionaron claves."}), 400

        resultados = await buscar_respuestas_postgres(keys)
        return jsonify({"status": "success", "resultados": resultados}), 200

    except Exception as e:
        logger.error(f"Error en test-postgres: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@asistente_bp.route("/test-vector", methods=["POST"])
async def test_vector_service():
    """Endpoint para probar búsqueda de claves."""
    try:
        data = await request.get_json()
        pregunta = data.get("pregunta")

        if not pregunta:
            return jsonify({"error": "Debe proporcionar una pregunta."}), 400

        respuesta = await assistant_service.iniciar_flujo_asistente(
            thread_id="123", assistant_id=os.getenv("ASSISTANT_ID"), pregunta=pregunta
        )
        return jsonify({"status": "success", "respuesta": respuesta}), 200

    except Exception as e:
        logger.error(f"Error en test-vector: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500
