# tests/test/test_assistant_routes.py

import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
@patch("routes.assistant_routes.assistant_service")
@patch("services.openai_service.openai_client", autospec=True)
async def test_start_assistant(mock_openai_client, mock_service, test_client):
    """
    Prueba la ruta '/assistant/start' para iniciar el flujo del asistente.
    """
    # Configurar mock del cliente OpenAI
    mock_openai_client.chat.completions.create = AsyncMock(
        return_value={
            "choices": [{"message": {"content": "Respuesta simulada"}}]
        }
    )

    # Configurar mock del servicio
    mock_service.iniciar_flujo_asistente = AsyncMock(return_value={"status": "completed"})

    # Simular datos de la solicitud
    data = {
        "thread_id": "test_thread",
        "assistant_id": "test_assistant",
        "message": "Hola, ¿qué deducciones puedo aplicar?"
    }

    # Realizar la solicitud al endpoint
    response = await test_client.post("/api/assistant/start", json=data)

    # Verificar resultados
    assert response.status_code == 200
    response_json = await response.get_json()  # Obtener el JSON correctamente
    assert response_json["status"] == "completed"  # Validar el estado

    # Corregir el orden esperado en la prueba
    mock_service.iniciar_flujo_asistente.assert_called_once_with(
        "test_thread", "test_assistant", "Hola, ¿qué deducciones puedo aplicar?"
    )

