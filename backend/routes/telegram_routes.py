from quart import Blueprint, request, jsonify
from services.telegram_service import send_message, answer_callback_query, edit_message_text
from services.llm_service import normalizar_consulta, generar_prompt_completo, consultar_llm_respuesta_final
from services.redis_service import obtener_cache, guardar_cache
from services.flujo_service import iniciar_flujo_asistente, client
from services.postgres_service import buscar_respuestas_postgres, almacenar_valoracion_en_postgres
import logging
import os
import json
import uuid

logger = logging.getLogger(__name__)

telegram_bp = Blueprint('telegram', __name__)

def extraer_keys_de_respuesta(texto: str) -> list:
    """Extrae las keys del JSON devuelto por iniciar_flujo_asistente."""
    try:
        data = json.loads(texto)
        keys = data.get("related_keys", [])
        if isinstance(keys, list):
            return keys
    except json.JSONDecodeError:
        pass
    return []

@telegram_bp.route('/telegram-bot', methods=['POST'])
async def telegram_bot():
    """Endpoint principal que recibe el mensaje del usuario vía Telegram."""
    logger.info("Entrando a la ruta /telegram-bot")
    try:
        data = await request.get_json()
        message = data.get('message', {})
        chat = message.get('chat', {})
        chat_id = chat.get('id')
        user_question = message.get('text')

        if not chat_id or not user_question:
            logger.error("No se pudo extraer chat_id o texto del mensaje de Telegram")
            return jsonify({"error": "Datos del mensaje inválidos"}), 400

        # Paso 1: Normalizar la pregunta
        pregunta_normalizada = await normalizar_consulta(user_question)
        logger.info(f"Pregunta normalizada: {pregunta_normalizada}")

        # Enviar mensaje preliminar (antes de cualquier procesamiento pesado)
        preliminar_resp = send_message(str(chat_id),
            "Estoy analizando tu pregunta tributaria...\nPor favor espera unos instantes mientras consulto la información. ⏳")
        preliminar_message_id = preliminar_resp["result"]["message_id"]

        # Paso 2: Consultar cache en Redis
        respuesta_cache = await obtener_cache(pregunta_normalizada)
        if respuesta_cache:
            # Editamos el mensaje preliminar con la respuesta final
            await edit_message_text(chat_id, preliminar_message_id, respuesta_cache)
            return jsonify({"origen": "cache", "respuesta": respuesta_cache}), 200

        # Paso 3: Llamar al asistente de OpenAI para obtener los _key
        assistant_id = os.getenv("ASSISTANT_ID", "asst_axido2ljUwFjuqWNmNtMHPsu")
        thread = await client.beta.threads.create()

        respuesta_asistente = await iniciar_flujo_asistente(
            thread_id=thread.id,
            assistant_id=assistant_id,
            pregunta=pregunta_normalizada,
            client=client
        )

        keys = extraer_keys_de_respuesta(respuesta_asistente)
        if not keys:
            # Sin keys, editamos el mensaje preliminar para informar
            await edit_message_text(chat_id, preliminar_message_id,
                "No se encontraron claves relacionadas en la respuesta del asistente.")
            return jsonify({"origen": "openai", "mensaje": "Sin claves encontradas"}), 200

        # Paso 4: Consultar PostgreSQL con las keys
        respuestas_postgres = await buscar_respuestas_postgres(keys)
        if not respuestas_postgres:
            # Sin datos en BD, editamos el mensaje preliminar
            await edit_message_text(chat_id, preliminar_message_id,
                "No se encontraron datos relacionados en la base de datos.")
            return jsonify({"origen": "postgres", "mensaje": "Sin datos en BD"}), 200

        prompt_final = await generar_prompt_completo(user_question, respuestas_postgres)
        respuesta_final = await consultar_llm_respuesta_final(prompt_final)

        # Paso 5: Preparar interacción para valoración del usuario
        interaction_id = str(uuid.uuid4())

        # Guardar en Redis la pregunta y la respuesta final para el feedback
        await guardar_cache(interaction_id, json.dumps({
            "pregunta": pregunta_normalizada,
            "respuesta": respuesta_final
        }), expiracion=3600)

        # Crear inline keyboard con callback_data simple
        callback_data_like = '{"action":"like","id":"%s"}' % interaction_id
        callback_data_dislike = '{"action":"dislike","id":"%s"}' % interaction_id
        botones = [
            [{"text": "👍", "callback_data": callback_data_like},
             {"text": "👎", "callback_data": callback_data_dislike}]
        ]

        # Ahora editamos el mensaje preliminar reemplazándolo con la respuesta final y los botones
        await edit_message_text(chat_id, preliminar_message_id, respuesta_final, reply_markup=botones)

        return jsonify({"origen": "final", "respuesta_final": respuesta_final}), 200

    except Exception as e:
        logger.exception("Error en /telegram-bot:")
        return jsonify({"error": str(e)}), 500


@telegram_bp.route('/telegram-feedback', methods=['POST'])
async def telegram_feedback():
    """Maneja el feedback del usuario desde los botones inline (callback_query)."""
    data = await request.get_json()
    callback_query = data.get("callback_query", {})
    if not callback_query:
        return jsonify({"error": "No callback_query found"}), 400

    callback_query_id = callback_query.get("id")
    message = callback_query.get("message", {})
    data_callback = callback_query.get("data")

    try:
        callback_data_parsed = json.loads(data_callback)
        action = callback_data_parsed["action"]
        interaction_id = callback_data_parsed["id"]
    except:
        action = "unknown"
        interaction_id = None

    pregunta_normalizada = None
    respuesta_final = None
    if interaction_id:
        datos = await obtener_cache(interaction_id)
        if datos:
            info = json.loads(datos)
            pregunta_normalizada = info["pregunta"]
            respuesta_final = info["respuesta"]

    if pregunta_normalizada and respuesta_final and action in ["like", "dislike"]:
        await almacenar_valoracion_en_postgres(pregunta_normalizada, respuesta_final, action)

        if action == "like":
            await guardar_cache(pregunta_normalizada, respuesta_final, expiracion=86400)
            await answer_callback_query(callback_query_id, text="¡Gracias por tu valoración!")
        else:
            await answer_callback_query(callback_query_id, text="Entendido, intentaré mejorar la respuesta.")
    else:
        await answer_callback_query(callback_query_id, text="No se encontró información para esta interacción.")

    return jsonify({"status": "ok"}), 200
