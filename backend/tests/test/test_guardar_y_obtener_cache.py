# backend/tests/test/test_guardar_y_obtener_cache.py

import pytest
from unittest.mock import AsyncMock
from services.redis_service import guardar_cache, obtener_cache

@pytest.mark.asyncio
async def test_guardar_y_obtener_cache(mock_redis):
    """Prueba guardar y recuperar un valor en Redis."""
    mock_set, mock_get = mock_redis
    clave = "test_key"
    valor = "test_value"

    # Guardar en Redis
    await guardar_cache(clave, valor, expiracion=10)
    mock_set.assert_called_once_with(clave, valor, ex=10)

    # Obtener de Redis
    mock_get.return_value = b"mocked_value"  # Asegurar que retorna bytes
    resultado = await obtener_cache(clave)
    mock_get.assert_called_once_with(clave)
    assert resultado == "mocked_value"
