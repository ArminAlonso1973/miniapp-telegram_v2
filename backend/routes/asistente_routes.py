from quart import Blueprint, request, jsonify
from services.openai_service import consultar_openai
from services.utils import clasificar_pregunta

asistente_bp = Blueprint("asistente", __name__)

@asistente_bp.route("/preguntar", methods=["POST"])
async def preguntar():
    """Ruta para realizar preguntas al asistente tributario."""
    try:
        data = await request.json
        pregunta = data.get("pregunta", "")

        if not pregunta:
            return jsonify({"error": "La pregunta es obligatoria"}), 400

        # Validar si es una pregunta tributaria
        if not clasificar_pregunta(pregunta):
            return jsonify({"error": "La pregunta no es de ámbito tributario"}), 400

        # Consultar a OpenAI usando el servicio existente
        respuesta = await consultar_openai(f"Pregunta: {pregunta}")
        return jsonify(respuesta), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
