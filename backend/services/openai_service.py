# services/openai_service.py
from openai import AsyncOpenAI
import asyncio
from typing import Optional
import os

# Inicializar el cliente asíncrono
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def consultar_openai(prompt: str, retry_count: int = 3) -> Optional[str]:
    """
    Consulta OpenAI de forma asíncrona con reintentos.
    """
    async def single_attempt():
        completion = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # o "gpt-4" según tu configuración
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        return completion.choices[0].message.content

    for attempt in range(retry_count):
        try:
            return await single_attempt()
        except Exception as e:
            if attempt == retry_count - 1:
                raise RuntimeError(f"Error al consultar OpenAI después de {retry_count} intentos: {str(e)}")
            await asyncio.sleep(1)