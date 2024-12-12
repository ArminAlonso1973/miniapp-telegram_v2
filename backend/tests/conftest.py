# backend/tests/conftest.py

import pytest_asyncio
import tracemalloc
from quart import Quart
from quart_cors import cors
from routes.consulta_routes import consulta_bp
from routes.telegram_routes import telegram_bp
from routes.pdf_routes import pdf_bp
from routes.arango_routes import arango_bp
from routes.asistente_routes import asistente_bp
from routes.pdft_routes import pdft_bp

def pytest_configure(config):
    """Iniciar tracemalloc para rastrear asignaciones de memoria."""
    tracemalloc.start()

@pytest_asyncio.fixture
async def app():
    """Fixture para crear la aplicación Quart con todos los blueprints registrados."""
    app = Quart(__name__)
    app = cors(app, allow_origin="*")
    
    # Registrar todos los blueprints necesarios
    app.register_blueprint(consulta_bp, url_prefix="/api")
    app.register_blueprint(telegram_bp, url_prefix="/api")
    app.register_blueprint(pdf_bp, url_prefix="/api")
    app.register_blueprint(arango_bp, url_prefix="/api/arango")
    app.register_blueprint(asistente_bp, url_prefix="/api/asistente")
    app.register_blueprint(pdft_bp, url_prefix="/api/pdft")
    
    print("Fixture 'app' creada correctamente.")
    return app

@pytest_asyncio.fixture
async def test_client(app):
    """Fixture para crear un cliente de pruebas asíncrono."""
    async with app.test_client() as client_instance:
        print("Fixture 'test_client' creada correctamente.")
        yield client_instance
