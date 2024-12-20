# tests/test_chat_service.py

import pytest
from unittest.mock import patch, AsyncMock
from services.chat_service import buscar_chats

@pytest.mark.asyncio
async def test_buscar_chats_con_resultados():
    query = "renta efectiva"
    user_id = 6359036493

    # Mock de ejecutar_query para retornar resultados simulados
    mock_result = [
        {"id": 1, "chat_id": 6359036493, "created_at": "2024-12-19T14:00:00Z", "preview": "¿Qué es la renta efectiva?"},
        {"id": 2, "chat_id": 6359036493, "created_at": "2024-12-20T10:30:00Z", "preview": "Implicaciones tributarias..."},
    ]

    with patch('services.chat_service.ejecutar_query', new=AsyncMock(return_value=mock_result)):
        resultados = await buscar_chats(query, user_id)

        assert len(resultados) == 2
        assert resultados[0]['id'] == 1
        assert resultados[1]['id'] == 2
        assert resultados[0]['preview'] == "¿Qué es la renta efectiva?"

@pytest.mark.asyncio
async def test_buscar_chats_sin_resultados():
    query = "no existente"
    user_id = 6359036493

    # Mock de ejecutar_query para retornar una lista vacía
    mock_result = []

    with patch('services.chat_service.ejecutar_query', new=AsyncMock(return_value=mock_result)):
        resultados = await buscar_chats(query, user_id)

        assert len(resultados) == 0

@pytest.mark.asyncio
async def test_buscar_chats_con_error():
    query = "renta efectiva"
    user_id = 6359036493

    # Mock de ejecutar_query para lanzar una excepción
    with patch('services.chat_service.ejecutar_query', new=AsyncMock(side_effect=Exception("Database Error"))):
        resultados = await buscar_chats(query, user_id)

        assert resultados == []
