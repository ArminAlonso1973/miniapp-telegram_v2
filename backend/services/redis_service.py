# Archivo: services/redis_service.py
import aioredis
import logging

logger = logging.getLogger(__name__)

REDIS_URI = "redis://localhost:6379"
redis = None

async def init_redis():
    global redis
    if not redis:
        redis = await aioredis.from_url(REDIS_URI)
        logger.info("Conexión exitosa a Redis")

async def obtener_cache(clave):
    """
    Obtiene un valor del caché Redis.
    Args:
        clave (str): Clave del caché.
    Returns:
        str: Valor almacenado.
    """
    return await redis.get(clave)

async def guardar_cache(clave, valor, expiracion=3600):
    """
    Guarda un valor en el caché Redis.
    Args:
        clave (str): Clave del caché.
        valor (str): Valor a almacenar.
        expiracion (int): Tiempo de expiración en segundos.
    """
    await redis.set(clave, valor, ex=expiracion)
