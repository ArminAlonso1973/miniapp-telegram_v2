# backend/tests/test/test_openai.py

import pytest
from unittest.mock import patch, AsyncMock
from quart.testing import QuartClient
from quart import Response

@pytest.mark.asyncio
async def test_consultar_openai(test_client: QuartClient):
    """Test para la función consultar_openai."""
    prompt = "¿Qué es la renta efectiva?"
    mock_response = {
        'choices': [
            {'message': {'content': 'La renta efectiva es...'}}
        ]
    }

    # Patch correcto del cliente de OpenAI
    with patch('services.openai_service.client.chat.Completion.create', new=AsyncMock(return_value=mock_response)):
        response = await test_client.post(
            "/api/openai",
            json={"prompt": prompt}
        )
        assert response.status_code == 200
        data = await response.get_json()
        assert data['response'] == mock_response['choices'][0]['message']['content']
