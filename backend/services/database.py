from arango import ArangoClient
from dotenv import load_dotenv
import os
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Variables de entorno
ARANGO_HOST = os.getenv("ARANGO_HOST", "http://arangodb_clean_service_new:8529")
ARANGO_USERNAME = os.getenv("ARANGO_USERNAME", "root")
ARANGO_PASSWORD = os.getenv("ARANGO_PASSWORD", "mysecretpassword")
ARANGO_DB_NAME = os.getenv("ARANGO_DB_NAME", "renta_2024")

logger.info(f"Conectando a ArangoDB en {ARANGO_HOST} con base de datos {ARANGO_DB_NAME}")



# Conexión al cliente ArangoDB
for _ in range(3):  # Reintentar 3 veces
    try:
        client = ArangoClient(hosts=ARANGO_HOST)
        db = client.db(ARANGO_DB_NAME, username=ARANGO_USERNAME, password=ARANGO_PASSWORD)
        logger.info(f"Conexión exitosa a la base de datos '{ARANGO_DB_NAME}' en {ARANGO_HOST}")
        break
    except Exception as e:
        logger.error(f"Intento fallido de conectar a ArangoDB: {e}")
        db = None



def insert_document(collection_name, data):
    """Inserta un documento en una colección de ArangoDB."""
    if db is None:
        logger.error("No se puede insertar documento: la conexión a ArangoDB no está inicializada.")
        raise ConnectionError("No se pudo conectar a ArangoDB.")

    try:
        if not db.has_collection(collection_name):
            raise ValueError(f"La colección '{collection_name}' no existe.")
        
        collection = db.collection(collection_name)
        result = collection.insert(data)
        logger.info(f"Documento insertado en la colección '{collection_name}': {result}")
        return result
    except Exception as e:
        logger.error(f"Error al insertar documento en la colección '{collection_name}': {e}")
        raise
