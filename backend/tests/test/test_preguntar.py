import pytest
from quart.testing import QuartClient
from unittest.mock import AsyncMock
from services.assistant_service import AssistantService

@pytest.mark.asyncio
async def test_preguntar(test_client: QuartClient, mocker):
    """Prueba para el endpoint /api/asistente/preguntar."""

    # Mockear la función iniciar_flujo_asistente del servicio AssistantService
    mock_iniciar_flujo = AsyncMock(return_value="Respuesta generada por el asistente.")
    mocker.patch("services.assistant_service.AssistantService.iniciar_flujo_asistente", new=mock_iniciar_flujo)

    # Simular solicitud POST
    response = await test_client.post(
        "/api/asistente/preguntar",
        json={"pregunta": "¿Qué es el IVA?"}
    )

    # Validar respuesta
    assert response.status_code == 200
    json_data = await response.get_json()
    assert json_data["respuesta"] == "Respuesta generada por el asistente."
