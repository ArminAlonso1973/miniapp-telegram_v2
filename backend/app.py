from quart import Quart, jsonify
from quart_cors import cors
from routes.consulta_routes import consulta_bp
from routes.telegram_routes import telegram_bp
from routes.pdf_routes import pdf_bp
from routes.arango_routes import arango_bp
from routes.asistente_routes import asistente_bp
from routes.pdft_routes import pdft_bp
from routes.assistant_routes import assistant_bp
from routes.redis_routes import redis_bp
from services.redis_service import init_redis
from dotenv import load_dotenv
import logging
import os

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación Quart
app = Quart(__name__)
app = cors(app, allow_origin="*")

# Ruta raíz para verificación de estado
@app.route('/')
async def home():
    return jsonify({
        "status": "ok",
        "message": "Backend service is running",
        "environment": {
            "POSTGRES_HOST": os.environ.get('POSTGRES_HOST', 'Not set'),
            "POSTGRES_DB": os.environ.get('POSTGRES_DB', 'Not set'),
            "ArangoDB": "Connected"
        }
    }), 200

# Registrar las rutas
app.register_blueprint(consulta_bp, url_prefix="/api")
app.register_blueprint(telegram_bp, url_prefix="/api")
app.register_blueprint(pdf_bp, url_prefix="/api")
app.register_blueprint(arango_bp, url_prefix="/api/arango")
app.register_blueprint(asistente_bp, url_prefix="/api/asistente")
app.register_blueprint(pdft_bp, url_prefix="/api/pdft")
app.register_blueprint(assistant_bp, url_prefix="/api/assistant")
app.register_blueprint(redis_bp, url_prefix='/')

# Inicializar servicios antes de iniciar el servidor
@app.before_serving
async def startup():
    await init_redis()

if __name__ == '__main__':
    logger.info("Iniciando servidor en http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
