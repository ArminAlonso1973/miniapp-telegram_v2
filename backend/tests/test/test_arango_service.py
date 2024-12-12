import pytest
from services.arango_service import buscar_respuestas_arango

@pytest.mark.asyncio
async def test_buscar_respuestas_arango(mocker):
    """Prueba para buscar respuestas en ArangoDB."""
    # Simular conexión a la base de datos y colección
    mock_collection = mocker.MagicMock()
    mock_collection.get.side_effect = lambda key: {
        "_key": key,
        "question": f"Pregunta para {key}",
        "answer": f"Respuesta para {key}",
        "legal_reference": f"Referencia para {key}"
    } if key in ["key1", "key2"] else None
    mocker.patch("services.arango_service.db.collection", return_value=mock_collection)

    # Claves de prueba
    keys = ["key1", "key2", "key3"]

    # Llamar a la función y validar resultados
    respuestas = await buscar_respuestas_arango(keys)
    assert len(respuestas) == 2
    assert respuestas[0]["question"] == "Pregunta para key1"
    assert respuestas[1]["answer"] == "Respuesta para key2"
