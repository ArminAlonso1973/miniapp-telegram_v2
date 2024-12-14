import os
import logging
from redis.asyncio import Redis
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Configuración de variables de entorno
REDIS_HOST = os.getenv("REDIS_HOST", "redis_service")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

redis_client = None  # Variable global para la instancia de Redis

async def init_redis():
    """Inicializa la conexión a Redis y la asigna a una variable global."""
    global redis_client
    try:
        redis_client = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD
        )
        await redis_client.ping()  # Verificar conexión
        logger.info(f"Conexión exitosa a Redis en {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        logger.error(f"Error al conectar a Redis: {e}")
        raise

async def guardar_cache(clave, valor, expiracion):
    """Guarda un valor en el cache."""
    try:
        if not redis_client:
            await init_redis()
        await redis_client.set(clave, valor, ex=expiracion)
        logger.info(f"Clave '{clave}' guardada en Redis con expiración de {expiracion} segundos.")
    except Exception as e:
        logger.error(f"Error al guardar en Redis: {e}")
        raise

async def obtener_cache(clave):
    """Obtiene un valor del cache y lo decodifica."""
    try:
        if not redis_client:
            await init_redis()
        valor = await redis_client.get(clave)
        valor_decodificado = valor.decode("utf-8") if valor else None
        logger.info(f"Clave '{clave}' obtenida de Redis con valor: {valor_decodificado}.")
        return valor_decodificado
    except Exception as e:
        logger.error(f"Error al obtener la clave '{clave}' de Redis: {e}")
        raise

__all__ = ["init_redis", "guardar_cache", "obtener_cache"]
