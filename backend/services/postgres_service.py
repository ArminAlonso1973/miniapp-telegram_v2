import asyncpg
import logging

logger = logging.getLogger(__name__)

async def connect_postgres():
    """Establece la conexión con PostgreSQL."""
    try:
        connection = await asyncpg.connect(
            user="asistente_tributario_db_user",
            password="3fBc0D7Chp5bll8m9m7G6L5cvPNYPCOU",
            database="asistente_tributario_db",
            host="postgres_service",
            port=5432,
        )
        logger.info("✅ Conexión a PostgreSQL establecida.")
        return connection
    except Exception as e:
        logger.error(f"❌ Error al conectar con PostgreSQL: {e}")
        raise


async def buscar_respuestas_postgres(keys: list):
    """
    Busca respuestas en PostgreSQL usando claves.
    Args:
        keys (list): Lista de claves a buscar.
    Returns:
        list: Respuestas encontradas en la base de datos.
    """
    if not keys:
        logger.warning("La lista de claves está vacía.")
        return []

    try:
        conn = await asyncpg.connect(
            user="asistente_tributario_db_user",
            password="3fBc0D7Chp5bll8m9m7G6L5cvPNYPCOU",
            database="asistente_tributario_db",
            host="localhost",
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
