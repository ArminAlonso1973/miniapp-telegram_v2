import logging
import json
from services.openai_service import openai_client
from services.postgres_service import buscar_respuestas_postgres
from services.redis_service import obtener_cache, guardar_cache

logger = logging.getLogger(__name__)

class AssistantService:
    def __init__(self, client):
        self.client = client

    async def iniciar_flujo_asistente(self, thread_id: str, assistant_id: str, pregunta: str) -> str:
        """Inicia el flujo con OpenAI para manejar la consulta."""
        try:
            logger.info("⏳ Iniciando flujo del asistente...")
            logger.info(f"🔹 Pregunta del usuario: {pregunta}")
            logger.info(f"🔹 Thread ID: {thread_id}, Assistant ID: {assistant_id}")

            # Enviar la pregunta inicial al asistente
            await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=pregunta
            )
            logger.info("✅ Mensaje enviado al asistente.")

            # Crear el run del asistente
            run = await self.client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            logger.info(f"🔹 Run Status: {run.status}")

            # Manejar el estado requires_action
            if run.status == "requires_action":
                logger.info("⚙️ Run requiere acción adicional. Procesando tool calls...")
                return await self.manejar_requires_action(run, thread_id, pregunta)
            elif run.status == "completed":
                logger.info("✅ Run completado. Procesando mensajes...")
                return await self.procesar_mensajes(thread_id)

            logger.warning(f"⚠️ Run finalizado en estado inesperado: {run.status}")
            return "El asistente no pudo procesar la consulta."

        except Exception as e:
            logger.error(f"❌ Error en iniciar_flujo_asistente: {str(e)}")
            return "Error al procesar la consulta."

    async def manejar_requires_action(self, run, thread_id: str, pregunta: str) -> str:
        """Maneja el estado 'requires_action' y completa la operación con Redis."""
        try:
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            logger.info("🔍 Analizando tool calls del asistente...")

            for tool_call in tool_calls:
                if tool_call.function.name == "get_related_keys":
                    argumentos = json.loads(tool_call.function.arguments)
                    related_keys = argumentos.get("related_keys", [])
                    logger.info(f"🔹 Related keys recibidas: {related_keys}")

                    # Buscar respuestas en Redis y PostgreSQL
                    respuestas = await self.buscar_respuestas_con_cache(related_keys)

                    # Cerrar la tool_call enviando las respuestas
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps({"respuestas": respuestas})
                    })
                    logger.info(f"✅ Respuestas encontradas: {respuestas}")

            # Enviar las respuestas al asistente
            run = await self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            logger.info(f"🔹 Run Status después de enviar tool outputs: {run.status}")

            # Procesar el resultado final
            if run.status == "completed":
                return await self.procesar_mensajes(thread_id)
            else:
                return "No se pudo completar el procesamiento con la herramienta."

        except Exception as e:
            logger.error(f"❌ Error manejando requires_action: {str(e)}")
            return "Ocurrió un error al procesar la acción requerida."

    async def buscar_respuestas_con_cache(self, keys: list) -> list:
        """Busca respuestas usando Redis como caché antes de consultar PostgreSQL."""
        respuestas = []
        try:
            logger.info("🔍 Buscando respuestas con caché en Redis y PostgreSQL...")
            for key in keys:
                cache_key = f"respuesta:{key}"
                cached_response = await obtener_cache(cache_key)

                if cached_response:
                    logger.info(f"✅ Respuesta encontrada en Redis para clave: {key}")
                    respuestas.append(json.loads(cached_response))
                else:
                    logger.info(f"🔎 Respuesta no encontrada en Redis. Consultando PostgreSQL para clave: {key}")
                    resultados = await buscar_respuestas_postgres([key])
                    if resultados:
                        respuesta = resultados[0]
                        await guardar_cache(cache_key, json.dumps(respuesta), expiracion=3600)
                        logger.info(f"✅ Respuesta guardada en Redis para clave: {key}")
                        respuestas.append(respuesta)

            logger.info(f"✅ Respuestas finales: {respuestas}")
            return respuestas
        except Exception as e:
            logger.error(f"❌ Error buscando respuestas con caché: {str(e)}")
            return []

    async def procesar_mensajes(self, thread_id: str) -> str:
        """Procesa los mensajes del asistente y devuelve la respuesta final."""
        try:
            logger.info(f"🔍 Procesando mensajes del asistente para thread_id: {thread_id}")
            mensajes = await self.client.beta.threads.messages.alist(thread_id=thread_id)
            for mensaje in mensajes:
                if mensaje.role == "assistant":
                    logger.info("✅ Respuesta final encontrada.")
                    return mensaje.content[0].get('text', "No se pudo extraer la respuesta del asistente.")
            return "No se encontró una respuesta adecuada en los mensajes del asistente."
        except Exception as e:
            logger.error(f"❌ Error procesando mensajes del thread: {str(e)}")
            return "Error al procesar los mensajes del asistente."

            
