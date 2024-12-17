import pytest
from services.redis_service import init_redis, guardar_cache, obtener_cache

@pytest.mark.asyncio
async def test_redis_connection():
    """Prueba la conexión inicial a Redis."""
    await init_redis()
    assert True

@pytest.mark.asyncio
async def test_guardar_y_obtener_cache():
    """Prueba guardar y recuperar un valor en Redis."""
    await init_redis()
    clave = "test_key"
    valor = "test_value"

    # Guardar en Redis
    await guardar_cache(clave, valor, expiracion=10)
    resultado = await obtener_cache(clave)

    assert resultado == valor
