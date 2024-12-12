# backend/tests/test/test_asistente_routes.py

import pytest
from quart.testing import QuartClient
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_preguntar(test_client: QuartClient, mocker):
    """Prueba para el endpoint /api/asistente/preguntar."""
    
    # Mockear funciones asíncronas correctamente
    mocker.patch("routes.asistente_routes.buscar_claves_vectoriales", new=AsyncMock(return_value=["key1", "key2"]))
    mocker.patch("routes.asistente_routes.buscar_respuestas_arango", new=AsyncMock(return_value=[
        {"question": "Pregunta simulada", "answer": "Respuesta simulada", "legal_reference": "Referencia simulada"}
    ]))
    mocker.patch("routes.asistente_routes.generar_prompt_completo", new=AsyncMock(return_value="prompt generado"))
    mocker.patch("routes.asistente_routes.consultar_llm_respuesta_final", new=AsyncMock(return_value="Respuesta generada por OpenAI"))

    # Realizar la petición al endpoint
    response = await test_client.post("/api/asistente/preguntar", json={"pregunta": "¿Qué es el IVA?"})
    data = await response.get_json()

    # Validar la respuesta
    assert response.status_code == 200
    assert "respuesta" in data
    assert data["respuesta"] == "Respuesta generada por OpenAI"
