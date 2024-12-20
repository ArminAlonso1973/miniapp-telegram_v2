# backend/tests/conftest.py

import pytest_asyncio
import tracemalloc
import logging
import os
from unittest.mock import patch, AsyncMock
from quart import Quart
from quart_cors import cors
from routes.consulta_routes import consulta_bp
from routes.telegram_routes import telegram_bp
from routes.pdf_routes import pdf_bp
from routes.asistente_routes import asistente_bp
from routes.pdft_routes import pdft_bp
from routes.assistant_routes import assistant_bp
from routes.chat_routes import chat_bp
from routes.redis_routes import redis_bp
from dotenv import load_dotenv

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
    app.register_blueprint(telegram_bp, url_prefix="/api/telegram")
    app.register_blueprint(pdf_bp, url_prefix="/api/pdf")
    app.register_blueprint(asistente_bp, url_prefix="/api/asistente")
    app.register_blueprint(pdft_bp, url_prefix="/api/pdft")
    app.register_blueprint(assistant_bp, url_prefix="/api/assistant")
    app.register_blueprint(chat_bp, url_prefix="/api/chats")
    app.register_blueprint(redis_bp, url_prefix="/api/redis")
    # Registrar otros blueprints según sea necesario

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
        "ANTHROPIC_API_KEY": "mocked_anthropic_api_key",
        # Agregar otras variables de entorno según sea necesario
    }):
        yield

@pytest_asyncio.fixture
async def mock_redis():
    """Mockear las funciones de Redis."""
    with patch('services.redis_service.redis_client', new=AsyncMock()) as mock_redis_client:
        mock_redis_client.set = AsyncMock(return_value=True)
        mock_redis_client.get = AsyncMock(return_value=b"mocked_value")  # Retornar bytes
        yield mock_redis_client.set, mock_redis_client.get

@pytest_asyncio.fixture
async def mock_openai(mocker):
    """Mockear el cliente de OpenAI."""
    mocker.patch("services.openai_service.client.chat.Completion.create", new=AsyncMock())
    return mocker

@pytest_asyncio.fixture(autouse=True)
async def mock_redis_init():
    """Mockear la inicialización de Redis para evitar conexiones reales."""
    with patch('services.redis_service.init_redis', new=AsyncMock()):
        yield
