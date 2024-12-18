from quart import Blueprint, request, jsonify
from services.telegram_service import send_message, send_message_with_inline_keyboard, answer_callback_query
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

        # Paso 2: Consultar cache en Redis
        respuesta_cache = await obtener_cache(pregunta_normalizada)
        if respuesta_cache:
            # Responder directamente desde cache
            send_message(str(chat_id), respuesta_cache)
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

        # Extraer las keys del JSON retornado
        keys = extraer_keys_de_respuesta(respuesta_asistente)
        if not keys:
            mensaje_sin_keys = "No se encontraron claves relacionadas en la respuesta del asistente."
            send_message(str(chat_id), mensaje_sin_keys)
            return jsonify({"origen": "openai", "mensaje": "Sin claves encontradas"}), 200

        # Paso 4: Consultar PostgreSQL con las keys
        respuestas_postgres = await buscar_respuestas_postgres(keys)
        if not respuestas_postgres:
            mensaje_sin_bd = "No se encontraron datos relacionados en la base de datos."
            send_message(str(chat_id), mensaje_sin_bd)
            return jsonify({"origen": "postgres", "mensaje": "Sin datos en BD"}), 200

        prompt_final = await generar_prompt_completo(user_question, respuestas_postgres)
        respuesta_final = await consultar_llm_respuesta_final(prompt_final)

        # Paso 5: Preparar interacción para valoración del usuario
        # Generar un ID único para esta interacción
        interaction_id = str(uuid.uuid4())

        # Guardar en Redis la pregunta y la respuesta final para recuperar tras la valoración
        await guardar_cache(interaction_id, json.dumps({
            "pregunta": pregunta_normalizada,
            "respuesta": respuesta_final
        }), expiracion=3600)  # 1 hora de expiración

        # Crear inline keyboard con callback_data simple
        callback_data_like = '{"action":"like","id":"%s"}' % interaction_id
        callback_data_dislike = '{"action":"dislike","id":"%s"}' % interaction_id
        botones = [
            [{"text": "👍", "callback_data": callback_data_like},
             {"text": "👎", "callback_data": callback_data_dislike}]
        ]

        send_message_with_inline_keyboard(str(chat_id), respuesta_final, botones)
        return jsonify({"origen": "final", "respuesta_final": respuesta_final}), 200

    except Exception as e:
        logger.exception("Error en /telegram-bot:")
        return jsonify({"error": str(e)}), 500


@telegram_bp.route('/telegram-feedback', methods=['POST'])
async def telegram_feedback():
    data = await request.get_json()
    callback_query = data.get("callback_query", {})
    if not callback_query:
        return jsonify({"error": "No callback_query found"}), 400

    callback_query_id = callback_query.get("id")
    message = callback_query.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    message_id = message.get("message_id")  # Importante para editar el mensaje original
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
            # Guardar en Redis como pregunta frecuente
            await guardar_cache(pregunta_normalizada, respuesta_final, expiracion=86400)
            # Mostrar un alert más visible:
            await answer_callback_query(callback_query_id, text="¡Gracias por tu valoración!", show_alert=True)
            
            # Editar el mensaje para reflejar la valoración
            from services.telegram_service import edit_message_text
            nuevo_texto = f"{respuesta_final}\n\n✅ Valorada positivamente"
            await edit_message_text(chat_id, message_id, nuevo_texto)
        else:
            await answer_callback_query(callback_query_id, text="Entendido, intentaré mejorar la respuesta.")
            # También puedes editar el mensaje para indicar valoración negativa
            from services.telegram_service import edit_message_text
            nuevo_texto = f"{respuesta_final}\n\n❌ Valorada negativamente"
            await edit_message_text(chat_id, message_id, nuevo_texto)
    else:
        await answer_callback_query(callback_query_id, text="No se encontró información para esta interacción.", show_alert=True)

    return jsonify({"status": "ok"}), 200

