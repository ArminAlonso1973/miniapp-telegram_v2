# backend/tests/test/test_assistant_service.py

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from services.assistant_service import AssistantService

@pytest.mark.asyncio
@patch("services.assistant_service.AsyncOpenAI")
async def test_iniciar_flujo_asistente(mock_openai):
    """
    Prueba el método iniciar_flujo_asistente con mocks para OpenAI.
    """
    # Configurar mocks
    mock_client = mock_openai.return_value
    mock_client.beta.threads.messages.acreate = AsyncMock()
    mock_run = MagicMock()
    mock_run.status = "completed"
    mock_client.beta.threads.runs.acreate_and_poll = AsyncMock(return_value=mock_run)

    # Crear instancia del servicio
    service = AssistantService(mock_client)

    # Ejecutar función
    thread_id = "test_thread"
    assistant_id = "test_assistant"
    message = "Hola, ¿qué deducciones puedo aplicar?"
    response = await service.iniciar_flujo_asistente(thread_id, assistant_id, message)

    # Verificar resultados
    assert response["status"] == "completed"
    mock_client.beta.threads.messages.acreate.assert_called_once()
    mock_client.beta.threads.runs.acreate_and_poll.assert_called_once()
