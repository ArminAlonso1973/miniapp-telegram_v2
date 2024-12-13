import logging
import json
from services.openai_service import openai_client
from services.arango_service import buscar_respuestas_arango
from services.llm_service import generar_prompt_completo, consultar_llm_respuesta_final

logger = logging.getLogger(__name__)

class AssistantService:
    def __init__(self, client):
        self.client = client

    async def iniciar_flujo_asistente(self, thread_id: str, assistant_id: str, message: str) -> dict:
        """Inicia el flujo de interacción con el asistente."""
        try:
            # Enviar mensaje del usuario al asistente
            await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=[{"type": "text", "text": message}]
            )

            # Crear y esperar el resultado del Run
            run = await self.client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id,
            )

            return {"status": run.status, "run": run}
        except Exception as e:
            logger.error(f"Error en iniciar_flujo_asistente: {e}")
            raise


    async def procesar_mensajes(self, thread_id: str) -> str:
        """Procesa los mensajes de un thread para obtener la respuesta del asistente."""
        try:
            mensajes = await self.client.beta.threads.messages.alist(thread_id=thread_id)
            for mensaje in mensajes:
                if mensaje.role == "assistant":
                    return mensaje.content[0].get('text', "No se pudo extraer la respuesta del asistente.")
            return "No se encontró una respuesta adecuada en los mensajes del asistente."
        except Exception as e:
            logger.error(f"Error procesando mensajes del thread: {e}")
            raise

    async def manejar_requires_action(self, run, thread_id: str) -> str:
        """Maneja el estado 'requires_action' del asistente."""
        try:
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for tool_call in tool_calls:
                if tool_call.function.name == "get_related_keys":
                    argumentos = json.loads(tool_call.function.arguments)
                    related_keys = argumentos.get("related_keys", [])
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps({"related_keys": related_keys})
                    })

            run = await self.client.beta.threads.runs.asubmit_tool_outputs_and_poll(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

            all_related_keys = []
            for tool_output in tool_outputs:
                output_data = json.loads(tool_output["output"])
                all_related_keys.extend(output_data.get("related_keys", []))

            if all_related_keys:
                respuestas = await buscar_respuestas_arango(all_related_keys)
                if respuestas:
                    prompt = generar_prompt_completo("", respuestas)
                    return await consultar_llm_respuesta_final(prompt)
                return "No se encontraron datos relevantes en la base de datos."

            return "No se encontraron claves relevantes para tu consulta."
        except Exception as e:
            logger.error(f"Error manejando requires_action: {e}")
            raise
