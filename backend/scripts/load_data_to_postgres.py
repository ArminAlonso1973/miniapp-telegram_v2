import asyncio
import asyncpg
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de conexión a PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATA_FILE = "./scripts/data.json"  # Ruta al archivo de datos

async def load_data_to_postgres():
    try:
        # Conectar a la base de datos
        connection = await asyncpg.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
        )
        print("✅ Conexión exitosa a PostgreSQL.")

        # Crear tablas si no existen
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS preguntas (
                _key TEXT PRIMARY KEY,
                tema_principal TEXT,
                fecha DATE,
                question TEXT,
                answer TEXT,
                legal_reference TEXT,
                tema TEXT
            );
        """)

        await connection.execute("""
            CREATE TABLE IF NOT EXISTS etiquetas (
                _key SERIAL PRIMARY KEY,
                pregunta_key TEXT REFERENCES preguntas(_key),
                etiqueta TEXT
            );
        """)

        # Cargar datos desde el archivo JSON
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        for record in data:
            # Insertar en la tabla `preguntas`
            await connection.execute("""
                INSERT INTO preguntas (_key, tema_principal, fecha, question, answer, legal_reference, tema)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (_key) DO NOTHING;
            """, record["_key"], record["tema_principal"], record["fecha"], record["question"],
               record["answer"], record["legal_reference"], record["tema"])

            # Insertar etiquetas relacionadas
            for etiqueta in record["etiquetas"]:
                await connection.execute("""
                    INSERT INTO etiquetas (pregunta_key, etiqueta)
                    VALUES ($1, $2);
                """, record["_key"], etiqueta)

        print("✅ Datos cargados exitosamente.")

        # Cerrar la conexión
        await connection.close()

    except Exception as e:
        print(f"❌ Error al cargar datos: {e}")

if __name__ == "__main__":
    asyncio.run(load_data_to_postgres())
