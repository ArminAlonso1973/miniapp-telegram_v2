import pytest
from services.llm_service import consultar_llm_respuesta_final

@pytest.mark.asyncio
async def test_generar_prompt_completo():
    """Prueba para generar el prompt completo."""
    from services.llm_service import generar_prompt_completo
    respuestas = [
        {
            "question": "¿Qué es el IVA?",
            "answer": "El IVA es un impuesto al valor agregado.",
            "legal_reference": "Ley de IVA, Artículo 1"
        },
        {
            "question": "¿Cuánto es el IVA en Chile?",
            "answer": "El IVA en Chile es del 19%.",
            "legal_reference": "Ley de IVA, Artículo 2"
        }
    ]
    prompt = await generar_prompt_completo("¿Qué es el IVA?", respuestas)
    assert "Pregunta: ¿Qué es el IVA?" in prompt
    assert "1. Pregunta: ¿Qué es el IVA?" in prompt
    assert "Respuesta: El IVA es un impuesto al valor agregado." in prompt

@pytest.mark.asyncio
async def test_consultar_llm_respuesta_final(mocker):
    """Prueba para consultar la respuesta final al modelo LLM."""
    # Simular el comportamiento de `consultar_openai`
    mocker.patch(
        "services.openai_service.consultar_openai",
        return_value={"respuesta": "El IVA, o Impuesto sobre el Valor Añadido, es un impuesto indirecto que se aplica al consumo de bienes y servicios."}
    )

    prompt = "¿Qué es el IVA?"
    respuesta = await consultar_llm_respuesta_final(prompt)

    # Validar que la respuesta contiene las palabras clave
    assert "IVA" in respuesta
    assert "impuesto" in respuesta
    assert "consumo" in respuesta
