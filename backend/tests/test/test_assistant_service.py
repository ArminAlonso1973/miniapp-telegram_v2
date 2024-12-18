import pytest
from unittest.mock import AsyncMock, patch
from services.assistant_service import AssistantService

@pytest.mark.asyncio
@patch("services.openai_service.openai_client")
async def test_iniciar_flujo_asistente(mock_client):
    """Prueba para iniciar_flujo_asistente."""
    # Configurar mocks
    mock_client.beta.threads.messages.create = AsyncMock()
    mock_run = AsyncMock()
    mock_run.status = "completed"
    mock_client.beta.threads.runs.create_and_poll = AsyncMock(return_value=mock_run)

    # Crear instancia del servicio
    service = AssistantService(mock_client)

    # Ejecutar función
    thread_id = "test_thread"
    assistant_id = "test_assistant"
    pregunta = "¿Qué es el IVA?"

    response = await service.iniciar_flujo_asistente(thread_id, assistant_id, pregunta)

    # Validar resultado
    assert isinstance(response, str)
