# backend/tests/test/test_fixture.py

import pytest
from quart.testing import QuartClient

@pytest.mark.asyncio
async def test_client_fixture(test_client: QuartClient):
    """Prueba simple para verificar que el fixture 'test_client' funciona correctamente."""
    response = await test_client.get("/api/test")
    data = await response.get_json()
    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["message"] == "API funcionando correctamente"
