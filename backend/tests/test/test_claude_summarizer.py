import pytest
from unittest.mock import patch, AsyncMock
from quart.testing import QuartClient

@pytest.mark.asyncio
async def test_summarize_endpoint_con_archivo(test_client: QuartClient):
    mock_summary = {
        "original_length": 1000,
        "summary_length": 200,
        "summary": "Este es un resumen simulado del documento."
    }

    with patch('services.claude_summarizer_service.ClaudeSummarizer.summarize_document', new=AsyncMock(return_value=mock_summary)):
        data = {
            'file': (b"%PDF-1.4 mock pdf content", 'test.pdf')
        }
        headers = {'Content-Type': 'multipart/form-data'}

        response = await test_client.post("/api/summarize", data=data, headers=headers)
        assert response.status_code == 200
        assert await response.get_json() == mock_summary

@pytest.mark.asyncio
async def test_summarize_endpoint_sin_archivo(test_client: QuartClient):
    response = await test_client.post("/api/summarize", data={}, headers={'Content-Type': 'multipart/form-data'})
    assert response.status_code == 400
    data = await response.get_json()
    assert data['error'] == "No se proporcionó archivo PDF"

@pytest.mark.asyncio
async def test_summarize_endpoint_con_error(test_client: QuartClient):
    with patch('services.claude_summarizer_service.ClaudeSummarizer.summarize_document', new=AsyncMock(side_effect=Exception("Error Interno"))):
        data = {
            'file': (b"%PDF-1.4 mock pdf content", 'test.pdf')
        }
        headers = {'Content-Type': 'multipart/form-data'}

        response = await test_client.post("/api/summarize", data=data, headers=headers)
        assert response.status_code == 500
        assert await response.get_json() == {"error": "Error Interno"}
