# routes/assistant_routes.py

from quart import Blueprint, request, jsonify
from services.assistant_service import AssistantService
from services.openai_service import openai_client

# Crear el blueprint
assistant_bp = Blueprint("assistant", __name__)

# Crear instancia del servicio con openai_client
assistant_service = AssistantService(openai_client)

@assistant_bp.route("/start", methods=["POST"])
async def start_assistant():
    """
    Inicia el flujo del asistente.
    """
    data = await request.get_json()
    thread_id = data.get("thread_id")
    assistant_id = data.get("assistant_id")
    message = data.get("message")

    if not assistant_id or not message:
        return jsonify({"error": "Faltan datos necesarios"}), 400

    try:
        # Crear thread si no existe
        if not thread_id:
            thread = await openai_client.beta.threads.create(
                assistant_id=assistant_id,
                messages=[{"role": "user", "content": message}]
            )
            thread_id = thread.id

        # Iniciar flujo con thread_id
        result = await assistant_service.iniciar_flujo_asistente(thread_id, assistant_id, message)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Error procesando la solicitud: {e}"}), 500


