import pytest
from quart import Quart
from routes.asistente_routes import asistente_bp

@pytest.fixture
def app():
    app = Quart(__name__)
    app.register_blueprint(asistente_bp, url_prefix="/api/asistente")
    return app

@pytest.mark.asyncio
async def test_preguntar(client):
    """Prueba para la ruta /api/asistente/preguntar."""
    response = await client.post("/api/asistente/preguntar", json={"pregunta": "¿Qué es el IVA?"})
    data = await response.get_json()
    assert response.status_code == 200
    assert "respuesta" in data
