from quart import Blueprint, request, jsonify
from services.flujo_service import iniciar_flujo_asistente, client
from services.postgres_service import buscar_respuestas_postgres
from services.llm_service import normalizar_consulta, generar_prompt_completo, consultar_llm_respuesta_final
import os
import json

assistant_bp = Blueprint('assistant', __name__)

@assistant_bp.route('/assistant', methods=['POST'])
async def consultar_asistente():
    data = await request.get_json()
    pregunta = data.get("question")
    if not pregunta:
        return jsonify({"error": "No se recibió la pregunta"}), 400

    pregunta_normalizada = await normalizar_consulta(pregunta)

    # Este es un ejemplo simplificado.
    # Aquí podrías replicar la lógica de obtener keys de OpenAI, consultar Postgres, etc.
    assistant_id = os.getenv("ASSISTANT_ID", "asst_axido2ljUwFjuqWNmNtMHPsu")
    thread = await client.beta.threads.create()
    respuesta_asistente = await iniciar_flujo_asistente(
        thread_id=thread.id,
        assistant_id=assistant_id,
        pregunta=pregunta_normalizada,
        client=client
    )

    # Extraer keys (ejemplo de función que ya tienes)
    def extraer_keys_de_respuesta(texto: str):
        try:
            data = json.loads(texto)
            keys = data.get("related_keys", [])
            if isinstance(keys, list):
                return keys
        except:
            pass
        return []

    keys = extraer_keys_de_respuesta(respuesta_asistente)
    if not keys:
        # Sin keys, devolver respuesta directa o mensaje genérico
        return jsonify({"respuesta": "No se encontraron claves. Tal vez el asistente no tiene info."}), 200

    respuestas_postgres = await buscar_respuestas_postgres(keys)
    if not respuestas_postgres:
        return jsonify({"respuesta": "No se encontraron datos relacionados en la BD."}), 200

    prompt_final = await generar_prompt_completo(pregunta, respuestas_postgres)
    respuesta_final = await consultar_llm_respuesta_final(prompt_final)

    return jsonify({"respuesta": respuesta_final}), 200
