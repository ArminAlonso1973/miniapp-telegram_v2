# Archivo: services/buscar_respuestas_service.py
from services.postgres_service import ejecutar_consulta
from services.redis_service import obtener_cache, guardar_cache
import logging

logger = logging.getLogger(__name__)

async def buscar_respuestas(keys: list) -> list:
    """
    Busca respuestas en PostgreSQL usando claves con soporte de Redis como caché.
    Args:
        keys (list): Lista de claves a buscar.
    Returns:
        list: Respuestas encontradas.
    """
    if not keys:
        logger.warning("La lista de claves está vacía.")
        return []

    respuestas = []
    try:
        for key in keys:
            # Intentar obtener la respuesta desde Redis
            cache_key = f"respuesta:{key}"
            cached_response = await obtener_cache(cache_key)

            if cached_response:
                logger.info(f"Respuesta obtenida del caché para la clave {key}.")
                respuestas.append(eval(cached_response))
            else:
                # Si no está en el caché, consultar en PostgreSQL
                query = """
                SELECT question, answer, legal_reference 
                FROM documentos_renta 
                WHERE id = $1
                """
                result = await ejecutar_consulta(query.replace("$1", f"'{key}'"))

                if result:
                    response = result[0]
                    respuestas.append(response)

                    # Almacenar en Redis
                    await guardar_cache(cache_key, str(response))

        logger.info(f"Se encontraron {len(respuestas)} respuestas para las claves proporcionadas.")
        return respuestas

    except Exception as e:
        logger.error(f"Error buscando respuestas en PostgreSQL: {e}")
        return []
