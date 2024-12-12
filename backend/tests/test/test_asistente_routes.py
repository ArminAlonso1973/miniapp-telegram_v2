import pytest
from quart import Quart
from quart.testing import QuartClient
from routes.asistente_routes import asistente_bp

@pytest.fixture
def app() -> Quart:
    """Crea la aplicación para pruebas."""
    app = Quart(__name__)
    app.register_blueprint(asistente_bp, url_prefix="/api/asistente")
    return app

@pytest.fixture
def client(app: Quart) -> QuartClient:
    """Crea el cliente de pruebas para la aplicación."""
    return app.test_client()

@pytest.mark.asyncio
async def test_preguntar(client: QuartClient):
    """Prueba para la ruta /api/asistente/preguntar."""
    response = await client.post("/api/asistente/preguntar", json={"pregunta": "¿Qué es el IVA?"})
    data = await response.get_json()
    assert response.status_code == 200
    assert "respuesta" in data
    assert "IVA" in data["respuesta"]
