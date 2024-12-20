# backend/tests/test/test_llm_service.py

import pytest
from unittest.mock import AsyncMock
from services.llm_service import consultar_llm_respuesta_final

@pytest.mark.asyncio
async def test_consultar_llm_respuesta_final(mocker):
    """Prueba para consultar la respuesta final al modelo LLM."""
    # Simular el comportamiento de `consultar_openai` con una respuesta que incluye 'consumo'
    mocker.patch(
        "services.openai_service.consultar_openai",
        return_value={
            "respuesta": "El IVA, o Impuesto sobre el Valor Añadido, es un impuesto indirecto que se aplica al consumo de bienes y servicios."
        }
    )

    prompt = "¿Qué es el IVA?"
    respuesta = await consultar_llm_respuesta_final(prompt)

    # Validar que la respuesta contiene las palabras clave
    assert "IVA" in respuesta
    assert "impuesto" in respuesta
    assert "consumo" in respuesta  # La palabra 'consumo' ahora está presente

@pytest.mark.asyncio
async def test_normalizar_consulta():
    """Prueba para la función normalizar_consulta."""
    from services.llm_service import normalizar_consulta
    consulta = "¿Cuál es la tasa del IVA?"
    consulta_normalizada = await normalizar_consulta(consulta)
    assert consulta_normalizada == "¿Cuál es la tasa del IVA?"
