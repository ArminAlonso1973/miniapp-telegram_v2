import pytest
from quart import Quart
from routes.telegram_routes import telegram_bp

@pytest.fixture
def app():
    app = Quart(__name__)
    app.register_blueprint(telegram_bp, url_prefix="/api/telegram")

    class MockPostgresConnection:
        async def fetchval(self, query):
            return "2024-12-16 00:00:00"

        async def close(self):
            pass

    # Mockear la conexión PostgreSQL
    app.config["postgres_connection"] = MockPostgresConnection()
    return app

@pytest.mark.asyncio
async def test_telegram_bot(app):
    test_client = app.test_client()

    # Simular una solicitud POST
    response = await test_client.post(
        "/api/telegram/telegram-bot",
        json={"chat_id": "123456789", "message": "¿Cuáles son los impuestos en Chile?"}
    )

    # Validar respuesta
    assert response.status_code == 200
    response_json = await response.get_json()
    assert "Tiempo en PostgreSQL" in response_json["respuesta"]
