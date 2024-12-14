import pytest
from services.redis_service import init_redis, guardar_cache, obtener_cache

@pytest.mark.asyncio
async def test_guardar_y_obtener_cache():
    """Prueba guardar y recuperar un valor de Redis."""
    await init_redis()  # Inicializa Redis

    clave = "test_key"
    valor = "test_value"
    expiracion = 60

    # Guardar en cache
    await guardar_cache(clave, valor, expiracion)

    # Obtener valor del cache
    resultado = await obtener_cache(clave)

    # Verificar el resultado
    assert resultado == valor
