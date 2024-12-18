import pytest
from quart.testing import QuartClient

@pytest.mark.asyncio
async def test_telegram_bot(test_client: QuartClient):
    """Prueba para la ruta /api/telegram/telegram-bot."""
    response = await test_client.post(
        "/api/telegram/telegram-bot",
        json={"chat_id": "123456789", "message": "¿Cuáles son los impuestos en Chile?"}
    )

    # Validar respuesta
    assert response.status_code == 200
    json_data = await response.get_json()
    assert "respuesta" in json_data
