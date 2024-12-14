from arango import ArangoClient
import logging

# Configuración del cliente ArangoDB
logger = logging.getLogger(__name__)

async def connect_arango():
    """Establece la conexión a la base de datos ArangoDB."""
    try:
        client = ArangoClient()
        db = client.db(  # Nota: No necesitas `await` aquí porque `arango` no es asíncrono.
            "renta_2024",
            username="root",
            password="mysecretpassword",
        )
        logger.info("Conexión exitosa a la base de datos 'renta_2024'")
        return db
    except Exception as e:
        logger.error(f"Error conectando a ArangoDB: {e}")
        raise

async def buscar_respuestas_arango(keys: list) -> list:
    """
    Busca respuestas en ArangoDB usando claves.
    Args:
        keys (list): Lista de claves a buscar.
    Returns:
        list: Respuestas encontradas en la base de datos.
    """
    if not keys:
        logger.warning("La lista de claves está vacía.")
        return []

    respuestas = []
    try:
        db = await connect_arango()
        collection = db.collection("documentos_renta")

        for key in keys:
            doc = collection.get(key)  # Nota: `collection.get` no es asíncrono.
            if doc:
                respuestas.append({
                    "question": doc.get("question", "Pregunta no disponible"),
                    "answer": doc.get("answer", "Respuesta no disponible"),
                    "legal_reference": doc.get("legal_reference", "Referencia legal no disponible"),
                })

        logger.info(f"Se encontraron {len(respuestas)} respuestas para las claves proporcionadas.")
        return respuestas

    except Exception as e:
        logger.error(f"Error buscando en ArangoDB: {e}")
        return []
