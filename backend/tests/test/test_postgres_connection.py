import os
import asyncio
from dotenv import load_dotenv
import asyncpg

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener credenciales desde las variables de entorno
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


async def test_connection():
    """Prueba de conexión a PostgreSQL."""
    try:
        connection = await asyncpg.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        print("✅ Conexión exitosa a PostgreSQL.")
        
        # Consultar versión de PostgreSQL como prueba
        version = await connection.fetchval("SELECT version();")
        print(f"Versión de PostgreSQL: {version}")
        
        await connection.close()
    except Exception as e:
        print(f"❌ Error al conectar a PostgreSQL: {e}")


if __name__ == "__main__":
    asyncio.run(test_connection())
