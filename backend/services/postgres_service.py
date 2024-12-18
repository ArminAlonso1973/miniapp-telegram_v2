import asyncpg
import logging
import os

logger = logging.getLogger(__name__)

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres_service")
POSTGRES_DB = os.getenv("POSTGRES_DB", "asistente_tributario_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "asistente_tributario_db_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "3fBc0D7Chp5bll8m9m7G6L5cvPNYPCOU")


async def connect_postgres():
    """Establece la conexión con PostgreSQL."""
    try:
        connection = await asyncpg.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB,
            host=POSTGRES_HOST,
            port=5432,
        )
        logger.info("✅ Conexión a PostgreSQL establecida.")
        return connection
    except Exception as e:
        logger.error(f"❌ Error al conectar con PostgreSQL: {e}")
        raise


async def buscar_respuestas_postgres(keys: list):
    """Busca respuestas en PostgreSQL usando claves."""
    if not keys:
        logger.warning("La lista de claves está vacía.")
        return []

    try:
        conn = await asyncpg.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB,
            host=POSTGRES_HOST,
            port=5432
        )

        query = """
            SELECT question, answer, legal_reference
            FROM preguntas
            WHERE _key = ANY($1::text[]);
        """
        respuestas = await conn.fetch(query, keys)
        await conn.close()

        logger.info(f"Se encontraron {len(respuestas)} respuestas para las claves proporcionadas.")
        return [dict(respuesta) for respuesta in respuestas]

    except Exception as e:
        logger.error(f"Error buscando en PostgreSQL: {e}")
        return []


async def almacenar_valoracion_en_postgres(pregunta_normalizada: str, respuesta: str, valoracion: str):
    """Almacena la valoración del usuario en la base de datos."""
    try:
        conn = await asyncpg.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB,
            host=POSTGRES_HOST,
            port=5432
        )

        query = """
            INSERT INTO feedback (pregunta_normalizada, respuesta, valoracion, timestamp)
            VALUES ($1, $2, $3, NOW())
        """
        await conn.execute(query, pregunta_normalizada, respuesta, valoracion)
        await conn.close()
        logger.info("✅ Valoración almacenada en PostgreSQL.")
    except Exception as e:
        logger.error(f"❌ Error al almacenar valoración en PostgreSQL: {e}")
