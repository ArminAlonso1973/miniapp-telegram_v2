# backend/tests/test/test_simple.py

import pytest
from quart.testing import QuartClient

@pytest.mark.asyncio
async def test_api_test(test_client: QuartClient):
    """Prueba simple para verificar el endpoint /api/test."""
    response = await test_client.get("/api/test")
    data = await response.get_json()
    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["message"] == "API funcionando correctamente"
