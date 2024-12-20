# backend/tests/test/test_chat_routes.py

import pytest
from unittest.mock import patch, AsyncMock
from quart.testing import QuartClient
from quart import Response
import os

@pytest.mark.asyncio
async def test_buscar_chats_endpoint(test_client: QuartClient):
    """Test para el endpoint /api/chats/ con resultados."""
    query = "renta efectiva"
    user_id = 6359036493
    mock_chats = [
        {"id": 1, "chat_id": user_id, "created_at": "2024-12-19T14:00:00Z", "preview": "¿Qué es la renta efectiva?"},
        {"id": 2, "chat_id": user_id, "created_at": "2024-12-20T10:30:00Z", "preview": "Implicaciones tributarias..."},
    ]

    # Patch en el módulo donde se usa la función
    with patch('routes.chat_routes.buscar_chats', new=AsyncMock(return_value=mock_chats)):
        response = await test_client.get(f"/api/chats/?query={query}&user_id={user_id}")
        assert response.status_code == 200
        data = await response.get_json()
        assert len(data) == 2
        assert data[0]['id'] == 1
        assert data[1]['id'] == 2

@pytest.mark.asyncio
async def test_buscar_chats_endpoint_sin_resultados(test_client: QuartClient):
    """Test para el endpoint /api/chats/ sin resultados."""
    query = "no existente"
    user_id = 6359036493
    mock_chats = []

    # Patch en el módulo donde se usa la función
    with patch('routes.chat_routes.buscar_chats', new=AsyncMock(return_value=mock_chats)):
        response = await test_client.get(f"/api/chats/?query={query}&user_id={user_id}")
        assert response.status_code == 200
        data = await response.get_json()
        assert len(data) == 0

@pytest.mark.asyncio
async def test_obtener_chat_endpoint_existe(test_client: QuartClient):
    """Test para el endpoint /api/chats/<chat_id> cuando el chat existe."""
    chat_id = 1
    mock_chat = {
        "id": 1,
        "chat_id": 6359036493,
        "created_at": "2024-12-19T14:00:00Z",
        "content": "Contenido del chat completo."
    }

    with patch('routes.chat_routes.obtener_chat_por_id', new=AsyncMock(return_value=mock_chat)):
        response = await test_client.get(f"/api/chats/{chat_id}")
        assert response.status_code == 200
        data = await response.get_json()
        assert data['id'] == 1
        assert data['content'] == "Contenido del chat completo."

@pytest.mark.asyncio
async def test_obtener_chat_endpoint_no_existe(test_client: QuartClient):
    """Test para el endpoint /api/chats/<chat_id> cuando el chat no existe."""
    chat_id = 999

    with patch('routes.chat_routes.obtener_chat_por_id', new=AsyncMock(return_value=None)):
        response = await test_client.get(f"/api/chats/{chat_id}")
        assert response.status_code == 404
        data = await response.get_json()
        assert data['error'] == "Chat no encontrado"

@pytest.mark.asyncio
async def test_descargar_chat_endpoint_existe(test_client: QuartClient, tmp_path):
    """Test para el endpoint /api/chats/<chat_id>/download cuando el chat existe."""
    chat_id = 1
    mock_file_path = tmp_path / f"chat_{chat_id}.txt"
    mock_file_content = "Fecha: 2024-12-19T14:00:00Z\n\nContenido del chat completo."

    # Mock de descargar_chat para retornar el path del archivo
    with patch('routes.chat_routes.descargar_chat', new=AsyncMock(return_value=str(mock_file_path))):
        # Mock de os.path.exists para simular que el archivo existe
        with patch('os.path.exists', return_value=True):
            # Crear una respuesta de ejemplo para send_file
            mock_response = Response(status=200)
            mock_response.headers['Content-Disposition'] = f'attachment; filename="chat_{chat_id}.txt"'

            # Mock de send_file para simular el envío del archivo
            with patch('quart.send_file', new=AsyncMock(return_value=mock_response)):
                response = await test_client.get(f"/api/chats/{chat_id}/download")
                assert response.status_code == 200
                # Verificar headers
                assert response.headers['Content-Disposition'] == f'attachment; filename="chat_{chat_id}.txt"'

@pytest.mark.asyncio
async def test_descargar_chat_endpoint_no_existe(test_client: QuartClient):
    """Test para el endpoint /api/chats/<chat_id>/download cuando el chat no existe."""
    chat_id = 999

    # Mock de descargar_chat para lanzar FileNotFoundError
    with patch('routes.chat_routes.descargar_chat', new=AsyncMock(side_effect=FileNotFoundError("Chat no encontrado"))):
        response = await test_client.get(f"/api/chats/{chat_id}/download")
        assert response.status_code == 404
        data = await response.get_json()
        assert data['error'] == "Archivo no encontrado"

@pytest.mark.asyncio
async def test_descargar_chat_endpoint_con_error(test_client: QuartClient):
    """Test para el endpoint /api/chats/<chat_id>/download manejando errores internos."""
    chat_id = 1

    # Mock de descargar_chat para lanzar una excepción
    with patch('routes.chat_routes.descargar_chat', new=AsyncMock(side_effect=Exception("Unexpected Error"))):
        response = await test_client.get(f"/api/chats/{chat_id}/download")
        assert response.status_code == 500
        data = await response.get_json()
        assert data['error'] == "Error al descargar chat"
