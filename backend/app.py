from quart import Quart, jsonify
from quart_cors import cors
from dotenv import load_dotenv
from services.redis_service import init_redis
from services.postgres_service import connect_postgres
from services.chat_service import ensure_storage_directory
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación Quart
app = Quart(__name__)
app = cors(app, allow_origin="*")

# Verificar y crear carpeta de almacenamiento
ensure_storage_directory()

# Ruta raíz para verificación de estado
@app.route('/')
async def home():
    return jsonify({
        "status": "ok",
        "message": "Backend service is running",
        "environment": {
            "POSTGRES_HOST": os.environ.get('POSTGRES_HOST', 'Not set'),
            "POSTGRES_DB": os.environ.get('POSTGRES_DB', 'Not set'),
            "Redis": "Ready"
        }
    }), 200

# Inicializar servicios antes de iniciar el servidor
@app.before_serving
async def startup():
    try:
        await init_redis()
        logger.info("✅ Redis inicializado correctamente.")
    except Exception as e:
        logger.error(f"❌ Error inicializando Redis: {e}")
        raise

    try:
        postgres_connection = await connect_postgres()
        app.config["postgres_connection"] = postgres_connection
        logger.info("✅ PostgreSQL conectado y configurado.")
    except Exception as e:
        logger.error(f"❌ Error conectando PostgreSQL: {e}")
        raise

# Finalizar servicios al detener el servidor
@app.after_serving
async def shutdown():
    logger.info("Cerrando servicios...")
    postgres_connection = app.config.get("postgres_connection")
    if postgres_connection:
        await postgres_connection.close()
        logger.info("✅ Conexión con PostgreSQL cerrada.")

# Registrar las rutas
from routes.consulta_routes import consulta_bp
from routes.telegram_routes import telegram_bp
from routes.pdf_routes import pdf_bp
from routes.asistente_routes import asistente_bp
from routes.pdft_routes import pdft_bp
from routes.assistant_routes import assistant_bp
from routes.redis_routes import redis_bp
from routes.flujo_routes import flujo_bp
from routes.postgres_routes import postgres_bp
from routes.chat_routes import chat_bp
from routes.informe_routes import informe_bp
from routes.summarize_routes import summarize_bp

logger.info("Registrando blueprints...")
app.register_blueprint(consulta_bp, url_prefix="/api")
app.register_blueprint(telegram_bp, url_prefix="/api/telegram")
app.register_blueprint(pdf_bp, url_prefix="/api/pdf")
app.register_blueprint(asistente_bp, url_prefix="/api/asistente")
app.register_blueprint(pdft_bp, url_prefix="/api/pdft")
app.register_blueprint(assistant_bp, url_prefix="/api/assistant")
app.register_blueprint(redis_bp, url_prefix="/api/redis")
app.register_blueprint(flujo_bp, url_prefix="/api/flujo")
app.register_blueprint(postgres_bp, url_prefix="/api/postgres")
app.register_blueprint(chat_bp, url_prefix="/api/chats")
app.register_blueprint(informe_bp, url_prefix="/api/informe")
app.register_blueprint(summarize_bp, url_prefix="/api/summarize")
logger.info("✅ Todos los blueprints han sido registrados.")

# Ejecutar la aplicación
if __name__ == '__main__':
    logger.info("🚀 Iniciando servidor en http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
