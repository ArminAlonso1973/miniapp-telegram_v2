# backend/services/chat_service.py

import os
import json
from datetime import datetime
from services.postgres_service import ejecutar_query
import aiofiles
import logging

# Logger para depuración
logger = logging.getLogger(__name__)

# Ruta base donde se almacenarán los archivos de chat
BASE_DIR = os.getenv("CHAT_STORAGE_PATH", os.path.expanduser("~/miniapp_chats"))

def ensure_storage_directory():
    """Verificar o crear la carpeta de almacenamiento."""
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

async def buscar_chats(query, user_id=None):
    """Buscar chats que coincidan con un query."""
    sql = """
    SELECT id, chat_id, created_at, LEFT(content, 100) AS preview
    FROM chats
    WHERE content ILIKE $1
    """
    params = [f"%{query}%"]
    if user_id:
        sql += " AND user_id = $2"
        params.append(user_id)
    
    logger.info(f"Ejecutando query de búsqueda con parámetros: query={query}, user_id={user_id}")
    try:
        result = await ejecutar_query(sql, params)
        
        # Convertir los resultados a una lista de diccionarios
        result_dicts = [dict(record) for record in result]
        logger.info(f"Resultado de búsqueda: {result_dicts}")
        
        return result_dicts
    except Exception as e:
        logger.error(f"Error al buscar chats: {e}")
        return []

async def obtener_chat_por_id(chat_id):
    """Obtener el contenido completo de un chat por ID."""
    logger.info(f"Buscando chat con ID: {chat_id}")
    try:
        sql = "SELECT * FROM chats WHERE id = $1"
        result = await ejecutar_query(sql, [chat_id])
        if result:
            logger.info(f"Chat encontrado: {result[0]}")
            return dict(result[0])  # Convertir Record a dict
        logger.warning(f"No se encontró chat con ID: {chat_id}")
        return None
    except Exception as e:
        logger.error(f"Error al obtener chat por ID {chat_id}: {e}")
        raise

async def descargar_chat(chat_id):
    """Generar archivo de texto para descargar un chat."""
    chat = await obtener_chat_por_id(chat_id)
    if not chat:
        raise FileNotFoundError("Chat no encontrado")
    
    # Generar el archivo en la carpeta designada
    file_path = os.path.join(BASE_DIR, f"chat_{chat_id}.txt")
    async with aiofiles.open(file_path, mode='w') as file:
        await file.write(f"Fecha: {chat['created_at']}\n\n")
        await file.write(chat['content'])
    return file_path

async def manejar_mensaje_telegram(chat_id: str, message: str) -> dict:
    """Procesa el mensaje recibido y retorna una respuesta."""
    # Implementación de la lógica
    return {
        "origen": "final",
        "respuesta_final": "Respuesta procesada."
    }
