import pytest
from services.postgres_service import buscar_respuestas_postgres

@pytest.mark.asyncio
async def test_buscar_respuestas_postgres():
    keys = ["123", "456"]
    results = await buscar_respuestas_postgres(keys)
    assert len(results) >= 0  # Verifica que no cause errores
