from quart import Blueprint, request, jsonify
from services.telegram_service import send_message
from services.llm_service import normalizar_consulta, generar_prompt_completo, consultar_llm_respuesta_final
from services.redis_service import obtener_cache
from services.flujo_service import iniciar_flujo_asistente, client
from services.postgres_service import buscar_respuestas_postgres
import logging
import os
import json

logger = logging.getLogger(__name__)

telegram_bp = Blueprint('telegram', __name__)

def extraer_keys_de_respuesta(texto: str) -> list:
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

        # Extraer las keys de la respuesta del asistente
        keys = extraer_keys_de_respuesta(respuesta_asistente)
        if not keys:
            mensaje_sin_keys = "No se encontraron claves relacionadas en la respuesta del asistente."
            send_message(str(chat_id), mensaje_sin_keys)
            return jsonify({"origen": "openai", "mensaje": "Sin claves encontradas"}), 200

        # Paso 4: Consultar PostgreSQL con las keys
        respuestas_postgres = await buscar_respuestas_postgres(keys)
        if not respuestas_postgres:
            # Si no se encontraron resultados en la base de datos, informa al usuario
            mensaje_sin_bd = "No se encontraron datos relacionados en la base de datos."
            send_message(str(chat_id), mensaje_sin_bd)
            return jsonify({"origen": "postgres", "mensaje": "Sin datos en BD"}), 200

        # Generar prompt completo con las respuestas de Postgres
        prompt_final = await generar_prompt_completo(user_question, respuestas_postgres)

        # Consultar LLM para la respuesta final
        respuesta_final = await consultar_llm_respuesta_final(prompt_final)

        # Enviar la respuesta final al usuario
        send_message(str(chat_id), respuesta_final)
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

    message = callback_query.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    data_callback = callback_query.get("data")

    # Recuperar la pregunta normalizada y la respuesta final si las guardaste temporalmente
    # Por ejemplo, podrías haber enviado la pregunta normalizada y la respuesta final en el keyboard callback_data
    # o bien almacenarla en Redis temporalmente. Aquí asumiré que el callback_data sólo indica "like" o "dislike".
    # Necesitarás una forma de identificar qué pregunta se está valorando. Una estrategia:
    #  - Al enviar el mensaje final, incluir en callback_data un JSON con la pregunta_normalizada y la respuesta.
    # Por ejemplo: {"action":"like","pregunta":"que es la renta efectiva en chile","respuesta":"..."}
    # Entonces data_callback podría ser un string JSON, lo parseas y obtienes esos datos.

    # Ejemplo si data_callback es un JSON:
    import json
    try:
        callback_data_parsed = json.loads(data_callback)
        action = callback_data_parsed["action"]
        pregunta_normalizada = callback_data_parsed["pregunta"]
        respuesta_final = callback_data_parsed["respuesta"]
    except:
        # Si no es JSON, es sólo "like" o "dislike"
        action = data_callback
        pregunta_normalizada = None
        respuesta_final = None

    if action == "like" and pregunta_normalizada and respuesta_final:
        # Guardar en Redis
        from services.redis_service import guardar_cache
        await guardar_cache(pregunta_normalizada, respuesta_final, expiracion=86400)  # Un día de expiración, por ejemplo
        # Responder al callback_query para que el usuario vea algo en Telegram
        # Nota: Para callbacks, se usa answerCallbackQuery
        await answer_callback_query(callback_query.get("id"), text="Gracias por tu valoración!")
    elif action == "dislike":
        await answer_callback_query(callback_query.get("id"), text="Entendido, mejoraré la respuesta.")

    return jsonify({"status": "ok"}), 200
