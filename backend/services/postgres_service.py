# Archivo: services/postgres_service.py
import asyncpg
import logging

logger = logging.getLogger(__name__)

POSTGRES_URI = "postgresql://user:password@localhost:5432/renta_2024"
pg_pool = None

async def init_postgres():
    global pg_pool
    if not pg_pool:
        pg_pool = await asyncpg.create_pool(dsn=POSTGRES_URI)
        logger.info("Conexión exitosa a PostgreSQL")

async def insertar_documento(table_name, document):
    """
    Inserta un documento en la tabla especificada en PostgreSQL.
    Args:
        table_name (str): Nombre de la tabla.
        document (dict): Documento a insertar.
    Returns:
        int: ID del documento insertado.
    """
    try:
        columns = ", ".join(document.keys())
        values = ", ".join(f"'{v}'" for v in document.values())

        async with pg_pool.acquire() as connection:
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) RETURNING id"
            result = await connection.fetchval(query)
            return result
    except Exception as e:
        logger.error(f"Error al insertar documento en PostgreSQL: {e}")
        raise

async def ejecutar_consulta(query):
    """
    Ejecuta una consulta en PostgreSQL.
    Args:
        query (str): Consulta SQL.
    Returns:
        list: Resultados de la consulta.
    """
    try:
        async with pg_pool.acquire() as connection:
            results = await connection.fetch(query)
            return [dict(record) for record in results]
    except Exception as e:
        logger.error(f"Error al ejecutar consulta en PostgreSQL: {e}")
        raise
