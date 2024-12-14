import pytest
from services.arango_service import buscar_respuestas_arango

@pytest.mark.asyncio
async def test_buscar_respuestas_arango_claves_validas(mock_arango):
    """Prueba con claves válidas."""
    keys = ["key1", "key2"]
    respuestas = await buscar_respuestas_arango(keys)

    assert len(respuestas) == len(keys)
    assert respuestas[0]["question"] == "Pregunta simulada para key1"
    assert respuestas[1]["question"] == "Pregunta simulada para key2"

@pytest.mark.asyncio
async def test_buscar_respuestas_arango_clave_invalida(mock_arango):
    """Prueba con clave inválida."""
    keys = ["key_invalido"]
    respuestas = await buscar_respuestas_arango(keys)

    assert respuestas == []

@pytest.mark.asyncio
async def test_buscar_respuestas_arango_lista_vacia(mock_arango):
    """Prueba con lista vacía."""
    keys = []
    respuestas = await buscar_respuestas_arango(keys)

    assert respuestas == []

@pytest.mark.asyncio
async def test_buscar_respuestas_arango_error(mock_arango, mocker):
    """Prueba simulando un error en la conexión."""
    mocker.patch("services.arango_service.connect_arango", side_effect=Exception("Error de conexión"))

    keys = ["key1"]
    respuestas = await buscar_respuestas_arango(keys)
    assert respuestas == []
