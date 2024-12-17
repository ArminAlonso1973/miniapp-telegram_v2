from quart import Blueprint, request, jsonify
from services.vector_service import buscar_claves_vectoriales
from services.postgres_service import buscar_respuestas_postgres


asistente_bp = Blueprint("asistente", __name__)

from services.llm_service import normalizar_consulta



@asistente_bp.route("/preguntar", methods=["POST"])
async def preguntar():
    """Endpoint para responder preguntas tributarias."""
    try:
        # Paso 1: Extraer la pregunta del usuario
        data = await request.get_json()
        pregunta = data.get("pregunta")

        if not pregunta:
            return jsonify({"error": "Debe proporcionar una pregunta."}), 400

        # Paso 2: Buscar claves vectoriales relacionadas usando OpenAI
        claves_relacionadas = await buscar_claves_vectoriales(pregunta)

        if not claves_relacionadas:
            return jsonify({"respuesta": "No se encontraron claves relacionadas para tu consulta."}), 404

        # Filtrar claves para asegurar un máximo de 6
        claves_relacionadas = claves_relacionadas[:6]

        # Paso 3: Consultar PostgreSQL usando las claves encontradas
        documentos = await buscar_respuestas_postgres(claves_relacionadas)

        if not documentos:
            return jsonify({"respuesta": "No se encontraron documentos relevantes en la base de datos."}), 404

        # Paso 4: Generar el prompt con OpenAI para obtener una respuesta
        prompt = await generar_prompt_completo(pregunta, documentos)
        respuesta = await consultar_llm_respuesta_final(prompt)

        # Respuesta final al usuario
        return jsonify({"respuesta": respuesta}), 200

    except Exception as e:
        return jsonify({"error": f"Error procesando la solicitud: {str(e)}"}), 500



@asistente_bp.route("/test-vector", methods=["POST"])
async def test_vector_service():
    """Endpoint para probar la función buscar_claves_vectoriales."""
    try:
        data = await request.get_json()
        pregunta = data.get("pregunta")

        if not pregunta:
            return jsonify({"error": "Debe proporcionar una pregunta."}), 400

        # Llamar a la función buscar_claves_vectoriales
        claves_vectoriales = await buscar_claves_vectoriales(pregunta)

        return jsonify({"claves_vectoriales": claves_vectoriales}), 200

    except Exception as e:
        return jsonify({"error": f"Error durante la prueba: {str(e)}"}), 500




from services.llm_service import normalizar_consulta

@asistente_bp.route("/test-normalizar", methods=["POST"])
async def test_normalizar_consulta():
    """Prueba de normalización de consulta."""
    try:
        data = await request.get_json()
        consulta = data.get("consulta")

        if not consulta:
            return jsonify({"error": "Debe proporcionar una consulta válida."}), 400

        consulta_normalizada = await normalizar_consulta(consulta)
        return jsonify({"consulta_normalizada": consulta_normalizada}), 200

    except Exception as e:
        return jsonify({"error": f"Error al normalizar la consulta: {str(e)}"}), 500

@asistente_bp.route("/test-generar-prompt", methods=["POST"])
async def test_generar_prompt():
    """Prueba para generar el prompt completo."""
    try:
        data = await request.get_json()
        pregunta = data.get("pregunta")
        respuestas = data.get("respuestas", [])

        if not pregunta or not respuestas:
            return jsonify({"error": "Se requieren 'pregunta' y 'respuestas'"}), 400

        prompt = await generar_prompt_completo(pregunta, respuestas)
        return jsonify({"prompt": prompt}), 200

    except Exception as e:
        return jsonify({"error": f"Error generando el prompt: {str(e)}"}), 500



@asistente_bp.route("/test-buscar-claves", methods=["POST"])
async def test_buscar_claves():
    """Prueba para buscar claves vectoriales usando OpenAI."""
    try:
        data = await request.get_json()
        pregunta = data.get("pregunta")

        if not pregunta:
            return jsonify({"error": "Se requiere el campo 'pregunta'"}), 400

        claves = await buscar_claves_vectoriales(pregunta)
        return jsonify({"claves_vectoriales": claves}), 200

    except Exception as e:
        return jsonify({"error": f"Error buscando claves vectoriales: {str(e)}"}), 500
