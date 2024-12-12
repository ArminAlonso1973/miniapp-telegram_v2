import pytest
from services.arango_service import buscar_respuestas_arango

@pytest.mark.asyncio
async def test_buscar_respuestas_arango(mocker):
    """Simula búsqueda en ArangoDB."""
    mock_collection = mocker.Mock()
    mock_collection.get.side_effect = lambda key: {"question": f"Pregunta para {key}", "answer": "Respuesta simulada", "legal_reference": "Referencia simulada"}
    mocker.patch("services.arango_service.db.collection", return_value=mock_collection)

    keys = ["key1", "key2"]
    respuestas = await buscar_respuestas_arango(keys)

    assert len(respuestas) == 2
    assert respuestas[0]["question"] == "Pregunta para key1"
    assert respuestas[0]["answer"] == "Respuesta simulada"
