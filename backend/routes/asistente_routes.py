from quart import Blueprint, request, jsonify
from services.vector_service import buscar_claves_vectoriales
from services.arango_service import buscar_respuestas_arango
from services.llm_service import generar_prompt_completo, consultar_llm_respuesta_final

asistente_bp = Blueprint("asistente", __name__)

@asistente_bp.route("/preguntar", methods=["POST"])
async def preguntar():
    """Endpoint para responder preguntas tributarias."""
    try:
        data = await request.get_json()
        pregunta = data.get("pregunta")

        if not pregunta:
            return jsonify({"error": "Debe proporcionar una pregunta."}), 400

        # Paso 1: Buscar claves vectoriales relacionadas
        claves_relacionadas = await buscar_claves_vectoriales(pregunta)

        if not claves_relacionadas:
            return jsonify({"respuesta": "No se encontraron claves relacionadas para tu consulta."}), 404

        # Paso 2: Consultar ArangoDB
        documentos = await buscar_respuestas_arango(claves_relacionadas)

        if not documentos:
            return jsonify({"respuesta": "No se encontraron documentos relevantes en la base de datos."}), 404

        # Paso 3: Generar prompt y consultar OpenAI
        prompt = generar_prompt_completo(pregunta, documentos)
        respuesta = await consultar_llm_respuesta_final(prompt)

        return jsonify({"respuesta": respuesta}), 200

    except Exception as e:
        return jsonify({"error": f"Error procesando la solicitud: {str(e)}"}), 500
