# backend/tests/test/test_telegram_routes.py

import pytest
from unittest.mock import patch, AsyncMock
from quart.testing import QuartClient
from quart import Response

@pytest.mark.asyncio
async def test_telegram_bot_success(test_client: QuartClient):
    """Prueba exitosa para la ruta /api/telegram/telegram-bot."""
    chat_id = "123456789"
    message_text = "¿Cuáles son los impuestos en Chile?"
    mock_response_final = "Los impuestos en Chile incluyen el Impuesto a la Renta, el IVA, entre otros."

    # Mock de obtener_cache para retornar None (no está en cache)
    with patch('services.redis_service.obtener_cache', new=AsyncMock(return_value=None)):
        # Mock de iniciar_flujo_asistente
        with patch('services.flujo_service.iniciar_flujo_asistente', new=AsyncMock(return_value='{"related_keys": ["impuesto_renta", "iva"]}')):
            # Mock de buscar_respuestas_postgres para retornar respuestas
            with patch('services.postgres_service.buscar_respuestas_postgres', new=AsyncMock(return_value=[
                {"question": "¿Qué es el IVA?", "answer": "El IVA es el Impuesto al Valor Agregado...", "legal_reference": "Ley XYZ"},
                {"question": "¿Cómo se calcula el Impuesto a la Renta?", "answer": "Se calcula sobre la renta líquida...", "legal_reference": "Ley ABC"}
            ])):
                # Mock de generar_prompt_completo
                with patch('services.llm_service.generar_prompt_completo', new=AsyncMock(return_value="Prompt generado")):
                    # Mock de consultar_llm_respuesta_final
                    with patch('services.llm_service.consultar_llm_respuesta_final', new=AsyncMock(return_value=mock_response_final)):
                        # Mock de guardar_cache
                        with patch('services.redis_service.guardar_cache', new=AsyncMock()):
                            # Mock de manejar_mensaje_telegram
                            with patch('services.chat_service.manejar_mensaje_telegram', new=AsyncMock(return_value={
                                "origen": "final",
                                "respuesta_final": mock_response_final
                            })):
                                # Enviar solicitud POST al endpoint con estructura JSON correcta
                                response = await test_client.post(
                                    "/api/telegram/telegram-bot",
                                    json={
                                        "chat": {"id": chat_id},
                                        "message": {"text": message_text}  # Asegurarse de que 'message' es un dict
                                    }
                                )
                                assert response.status_code == 200
                                data = await response.get_json()
                                assert data['response'] == mock_response_final

@pytest.mark.asyncio
async def test_telegram_bot_no_message(test_client: QuartClient):
    """Prueba para la ruta /api/telegram/telegram-bot sin proporcionar un mensaje."""
    chat_id = "123456789"
    data = {
        "chat": {"id": chat_id},
        # 'message' está ausente
    }

    response = await test_client.post(
        "/api/telegram/telegram-bot",
        json=data
    )
    assert response.status_code == 400  # Asegurarse de que el endpoint retorna 400 para solicitudes inválidas
    data = await response.get_json()
    assert data['error'] == "No se proporcionó un mensaje."

@pytest.mark.asyncio
async def test_telegram_bot_error(test_client: QuartClient):
    """Test para la ruta /api/telegram/telegram-bot manejando errores internos."""
    chat_id = "123456789"
    message_text = "¿Cuáles son los impuestos en Chile?"

    # Mock de manejar_mensaje_telegram para lanzar una excepción
    with patch('services.chat_service.manejar_mensaje_telegram', new=AsyncMock(side_effect=Exception("Redis Error"))):
        response = await test_client.post(
            "/api/telegram/telegram-bot",
            json={
                "chat": {"id": chat_id},
                "message": {"text": message_text}
            }
        )
        assert response.status_code == 500
        data = await response.get_json()
        assert "Redis Error" in data['error']
