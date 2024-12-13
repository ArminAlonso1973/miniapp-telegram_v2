import logging
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

class AssistantService:
    def __init__(self, openai_client: AsyncOpenAI):
        self.openai_client = openai_client

    async def iniciar_flujo_asistente(self, thread_id: str, assistant_id: str, message: str) -> dict:
        """
        Inicia el flujo de interacción con el asistente.
        """
        try:
            # Enviar mensaje al asistente
            await self.openai_client.beta.threads.messages.acreate(
                thread_id=thread_id,
                role="user",
                content=[{"type": "text", "text": message}]
            )

            # Crear y esperar el resultado del Run
            run = await self.openai_client.beta.threads.runs.acreate_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id
            )

            return {"status": run.status, "run": run}
        except Exception as e:
            logger.error(f"Error en iniciar_flujo_asistente: {e}")
            raise ValueError("Error al iniciar el flujo del asistente.")
