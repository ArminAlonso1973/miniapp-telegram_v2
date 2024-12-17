# backend/tests/conftest.py

import pytest_asyncio
import tracemalloc
import logging
import os
from unittest.mock import patch, AsyncMock
from unittest.mock import Mock
from quart import Quart
from quart_cors import cors
from routes.consulta_routes import consulta_bp
from routes.telegram_routes import telegram_bp
from routes.pdf_routes import pdf_bp
from routes.asistente_routes import asistente_bp
from routes.pdft_routes import pdft_bp
from dotenv import load_dotenv  # IMPORTANTE: Agregar esta línea
from routes.assistant_routes import assistant_bp

# Configurar logging para rastrear el flujo de las pruebas
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pytest_configure(config):
    """Iniciar tracemalloc para rastrear asignaciones de memoria durante las pruebas."""
    tracemalloc.start()
    logger.info("tracemalloc iniciado.")

def pytest_unconfigure(config):
    """Detener tracemalloc después de que finalicen las pruebas."""
    tracemalloc.stop()
    logger.info("tracemalloc detenido.")

@pytest_asyncio.fixture
async def app():
    """Crear la aplicación Quart con todos los blueprints registrados."""
    logger.info("Creando la fixture 'app'...")
    app = Quart(__name__)
    app = cors(app, allow_origin="*")

      # Cargar variables de entorno
    load_dotenv()

    # Registrar blueprints para las rutas
    app.register_blueprint(consulta_bp, url_prefix="/api")
    app.register_blueprint(telegram_bp, url_prefix="/api")
    app.register_blueprint(pdf_bp, url_prefix="/api")
    app.register_blueprint(asistente_bp, url_prefix="/api/asistente")
    app.register_blueprint(pdft_bp, url_prefix="/api/pdft")
    app.register_blueprint(assistant_bp, url_prefix="/api/assistant")
    logger.info("Fixture 'app' creada correctamente.")
    return app

@pytest_asyncio.fixture
async def test_client(app):
    """Crear un cliente de pruebas asíncrono para realizar solicitudes HTTP simuladas."""
    logger.info("Creando la fixture 'test_client'...")
    async with app.test_client() as client_instance:
        logger.info("Fixture 'test_client' creada correctamente.")
        yield client_instance

@pytest_asyncio.fixture(autouse=True)
async def mock_env():
    """Mockear variables de entorno necesarias para las pruebas."""
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "mocked_api_key",
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
    }):
        yield

@pytest_asyncio.fixture
async def mock_openai(mocker):
    """Mockear el cliente de OpenAI."""
    mocker.patch("services.assistant_service.openai_client", new_callable=AsyncMock)
    return mocker







