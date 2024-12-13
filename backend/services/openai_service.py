import asyncio
from openai import AsyncOpenAI
import os

# Inicializar el cliente asíncrono
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def consultar_openai(prompt: str):
    """Consulta a OpenAI con un prompt y devuelve la respuesta."""
    try:
        response = await asyncio.to_thread(
            openai_client.chat.completions.create,
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return {"respuesta": response.choices[0].message.content}
    except Exception as e:
        raise RuntimeError(f"Error al consultar OpenAI: {e}")
