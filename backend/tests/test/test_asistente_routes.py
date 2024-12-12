import pytest
from quart import Quart
from quart.testing import QuartClient
from routes.asistente_routes import asistente_bp

@pytest.fixture
def app():
    """Configura la aplicación de pruebas para Quart."""
    app = Quart(__name__)
    app.register_blueprint(asistente_bp, url_prefix="/api/asistente")
    return app

@pytest.mark.asyncio
async def test_preguntar(client: QuartClient, mocker):
    """Prueba para el endpoint /api/asistente/preguntar."""
    # Simular servicios dependientes
    mocker.patch("services.vector_service.buscar_claves_vectoriales", return_value=["key1", "key2"])
    mocker.patch("services.arango_service.buscar_respuestas_arango", return_value=[
        {"question": "Pregunta 1", "answer": "Respuesta 1", "legal_reference": "Ref 1"}
    ])
    mocker.patch("services.llm_service.consultar_llm_respuesta_final", return_value="Respuesta generada por OpenAI")

    # Realizar petición al endpoint
    response = await client.post("/api/asistente/preguntar", json={"pregunta": "¿Qué es el IVA?"})
    data = await response.get_json()
    assert response.status_code == 200
    assert "respuesta" in data
    assert data["respuesta"] == "Respuesta generada por OpenAI"
