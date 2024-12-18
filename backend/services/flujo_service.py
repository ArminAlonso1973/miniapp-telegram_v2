import asyncio
import os
import logging
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

logger = logging.getLogger(__name__)

# Configuración del cliente OpenAI usando variable de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def poll_run_status(thread_id, run_id, client, max_retries=30, delay=1):
    for _ in range(max_retries):
        run = await client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        logger.info(f"🔄 Estado del Run: {run.status}")
        if run.status in ["completed", "requires_action"]:
            return run
        await asyncio.sleep(delay)
    raise TimeoutError("El run no se completó en el tiempo esperado.")

async def procesar_mensajes(thread_id, client):
    try:
        logger.info("📥 Obteniendo mensajes del asistente...")
        mensajes = await client.beta.threads.messages.list(thread_id=thread_id)
        respuestas = [m.content[0].text.value for m in mensajes.data if m.role == "assistant"]
        return "\n".join(respuestas) if respuestas else "No hay respuestas disponibles."
    except Exception as e:
        logger.error(f"❌ Error al procesar los mensajes: {str(e)}", exc_info=True)
        return "Error al procesar las respuestas del asistente."

async def iniciar_flujo_asistente(thread_id: str, assistant_id: str, pregunta: str, client: AsyncOpenAI) -> str:
    """Inicia el flujo de interacción con el asistente."""
    try:
        logger.debug("⏳ Iniciando flujo del asistente...")
        logger.debug(f"🔹 Pregunta del usuario: {pregunta}")

        # Enviar mensaje del usuario
        response = await client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=pregunta
        )
        logger.info("✅ Mensaje enviado al asistente.")
        logger.debug(f"🔄 Respuesta del servidor: {response}")

        # Crear el run
        run = await client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        logger.info(f"✅ Run creado: ID={run.id}, Estado={run.status}")

        # Polling optimizado
        run = await poll_run_status(thread_id, run.id, client)

        # Procesar resultados
        logger.info(f"🔍 Estado final del Run: {run.status}")
        if run.status == "requires_action":
            # Retornará JSON con assistant_message y related_keys
            return await manejar_requires_action(run, thread_id, client)
        elif run.status == "completed":
            # Run completado sin acciones adicionales: retornar mensaje final
            return await procesar_mensajes(thread_id, client)
        else:
            logger.warning(f"⚠️ Estado inesperado del Run: {run.status}")
            return "El asistente no pudo procesar la consulta."

    except Exception as e:
        logger.error(f"❌ Error en iniciar_flujo_asistente: {str(e)}", exc_info=True)
        return "Error al procesar la consulta."

async def manejar_requires_action(run, thread_id: str, client: AsyncOpenAI) -> str:
    """Maneja tool calls de forma asíncrona y devuelve JSON con mensaje final y keys."""
    try:
        logger.info("⚙️ Procesando acciones requeridas...")
        logger.info(f"🧵 Estado actual del run: {run.status}")

        if not run.required_action:
            logger.error("❌ 'required_action' está vacío o no definido.")
            return json.dumps({"assistant_message": "No hay acción requerida", "related_keys": []})

        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        if not tool_calls:
            logger.warning("⚠️ No se encontraron tool calls en 'required_action'.")
            return json.dumps({"assistant_message": "No se encontraron tool calls", "related_keys": []})

        # Procesar tool calls
        tasks = [procesar_tool_call(tool_call) for tool_call in tool_calls]
        tool_outputs = await asyncio.gather(*tasks, return_exceptions=True)

        # Extraer keys de los tool_outputs
        all_keys = []
        for out in tool_outputs:
            if isinstance(out, str):
                try:
                    data = json.loads(out)
                    if "related_keys" in data:
                        all_keys.extend(data["related_keys"])
                except json.JSONDecodeError:
                    pass

        outputs = [{"tool_call_id": t.id, "output": o} for t, o in zip(tool_calls, tool_outputs)]

        # Enviar los resultados al asistente
        run = await client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=outputs
        )

        logger.info(f"🔄 Nuevo estado del Run: {run.status}")
        if run.status == "completed":
            # Obtener el mensaje final del asistente
            mensajes = await procesar_mensajes(thread_id, client)
            # Retornar JSON con mensaje final y keys
            return json.dumps({"assistant_message": mensajes, "related_keys": all_keys})
        else:
            return json.dumps({"assistant_message": "Error al completar la acción", "related_keys": []})

    except Exception as e:
        logger.error(f"❌ Error manejando tool calls: {str(e)}", exc_info=True)
        return json.dumps({"assistant_message": "Error procesando tool calls", "related_keys": []})

async def procesar_tool_call(tool_call):
    """Procesa una tool_call y devuelve el resultado."""
    try:
        logger.info(f"🛠 Procesando tool_call ID: {tool_call.id}, función: {tool_call.function.name}")
        argumentos = json.loads(tool_call.function.arguments)
        related_keys = argumentos.get("related_keys", [])
        resultado = json.dumps({"related_keys": related_keys})
        logger.info(f"✅ Resultado generado para la tool_call: {resultado}")
        return resultado
    except Exception as e:
        logger.error(f"❌ Error procesando tool_call {tool_call.id}: {str(e)}")
        return json.dumps({"error": "Error al procesar tool_call", "related_keys": []})
