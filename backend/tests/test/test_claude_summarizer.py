# backend/tests/test/test_claude_summarizer.py

import pytest
from unittest.mock import patch, AsyncMock
from quart.testing import QuartClient
from quart import Response

@pytest.mark.asyncio
async def test_summarize_endpoint_con_archivo(test_client: QuartClient):
    """Test para el endpoint /summarize con un archivo PDF."""
    mock_pdf_content = b"%PDF-1.4 mock pdf content"
    mock_summary = {
        "original_length": 1000,
        "summary_length": 200,
        "summary": "Este es un resumen simulado del documento."
    }

    # Patch de ClaudeSummarizer.summarize_document correctamente
    with patch('services.ClaudeSummarizer.ClaudeSummarizer.summarize_document', new=AsyncMock(return_value=mock_summary)):
        # Mock de read de aiofiles
        with patch('aiofiles.open', new_callable=AsyncMock) as mock_aiofiles_open:
            mock_file = AsyncMock()
            mock_file.__aenter__.return_value.read.return_value = mock_pdf_content
            mock_aiofiles_open.return_value = mock_file

            # Enviar solicitud POST con archivo
            data = {
                'file': (mock_pdf_content, 'test.pdf')
            }
            headers = {'Content-Type': 'multipart/form-data'}

            response = await test_client.post(
                "/summarize",
                data=data,
                headers=headers
            )
            assert response.status_code == 200
            data = await response.get_json()
            assert data['summary'] == mock_summary['summary']

@pytest.mark.asyncio
async def test_summarize_endpoint_sin_archivo(test_client: QuartClient):
    """Test para el endpoint /summarize sin proporcionar un archivo PDF."""
    data = {}
    headers = {'Content-Type': 'multipart/form-data'}

    response = await test_client.post(
        "/summarize",
        data=data,
        headers=headers
    )
    assert response.status_code == 400  # Asegurarse de que el endpoint retorna 400 para solicitudes inválidas
    data = await response.get_json()
    assert data['error'] == "No se proporcionó ningún archivo PDF."

@pytest.mark.asyncio
async def test_summarize_endpoint_con_error(test_client: QuartClient):
    """Test para el endpoint /summarize manejando errores internos."""
    with patch('services.ClaudeSummarizer.ClaudeSummarizer.summarize_document', new=AsyncMock(side_effect=Exception("Error Interno"))):
        # Enviar solicitud POST con archivo
        data = {
            'file': (b"%PDF-1.4 mock pdf content", 'test.pdf')
        }
        headers = {'Content-Type': 'multipart/form-data'}

        response = await test_client.post(
            "/summarize",
            data=data,
            headers=headers
        )
        assert response.status_code == 500
        data = await response.get_json()
        assert data['error'] == "Error Interno"
