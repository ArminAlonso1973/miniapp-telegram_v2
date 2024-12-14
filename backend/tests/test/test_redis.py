import pytest
from services.redis_service import init_redis, guardar_cache, obtener_cache

@pytest.mark.asyncio
async def test_redis_connection():
    """Prueba la conexión inicial a Redis."""
    await init_redis()  # Verifica que la conexión inicializa sin errores
    assert True  # Si no hay excepciones, la conexión fue exitosa


