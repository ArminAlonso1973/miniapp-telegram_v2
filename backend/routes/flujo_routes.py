from quart import Blueprint, request, jsonify
from services.flujo_service import iniciar_flujo_asistente, client

flujo_bp = Blueprint("flujo", __name__, url_prefix="/flujo")

@flujo_bp.route('/test-procesar', methods=['GET'])
async def test_procesar():
    thread = await client.beta.threads.create()
    pregunta = "¿Qué es la renta efectiva en Chile?"
    assistant_id = "asst_axido2ljUwFjuqWNmNtMHPsu"  # Ajustar si es necesario

    respuesta = await iniciar_flujo_asistente(
        thread_id=thread.id,
        assistant_id=assistant_id,
        pregunta=pregunta,
        client=client
    )
    return jsonify({"respuesta": respuesta})
