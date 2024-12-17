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

# Instancia global de Redis
redis_client = None

async def init_redis():
    """Inicializa la conexión a Redis si no está ya inicializada."""
    global redis_client
    if redis_client is None:
        try:
            redis_client = Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD
            )
            await redis_client.ping()  # Verificar conexión
            logger.info(f"✅ Conexión exitosa a Redis en {REDIS_HOST}:{REDIS_PORT}")
        except Exception as e:
            logger.error(f"❌ Error al conectar a Redis: {e}")
            raise

async def guardar_cache(clave, valor, expiracion=3600):
    """Guarda un valor en el caché."""
    try:
        await redis_client.set(clave, valor, ex=expiracion)
        logger.info(f"✅ Clave '{clave}' guardada en Redis con expiración de {expiracion} segundos.")
    except Exception as e:
        logger.error(f"❌ Error al guardar en Redis: {e}")
        raise

async def obtener_cache(clave):
    """Obtiene un valor del caché."""
    try:
        valor = await redis_client.get(clave)
        return valor.decode("utf-8") if valor else None
    except Exception as e:
        logger.error(f"❌ Error al obtener la clave '{clave}' de Redis: {e}")
        return None
