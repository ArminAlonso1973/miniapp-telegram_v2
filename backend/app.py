from quart import Quart
from quart_cors import cors
from routes.consulta_routes import consulta_bp
from routes.telegram_routes import telegram_bp
from routes.pdf_routes import pdf_bp
from dotenv import load_dotenv
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación Quart
app = Quart(__name__)
app = cors(app, allow_origin="*")

# Registrar las rutas
app.register_blueprint(consulta_bp, url_prefix="/api")
app.register_blueprint(telegram_bp, url_prefix="/api")
app.register_blueprint(pdf_bp, url_prefix="/api")

if __name__ == '__main__':
    logger.info("Iniciando servidor en http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
