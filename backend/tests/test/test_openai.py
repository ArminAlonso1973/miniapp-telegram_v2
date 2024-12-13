import asyncio
from services.openai_service import openai_client

async def test_openai():
    assistant_id = 'test_assistant'
    message = 'Hola, ¿qué deducciones puedo aplicar?'

    try:
        # Crear un nuevo thread
        thread = await openai_client.beta.threads.create(
            assistant_id=assistant_id,
            messages=[{"role": "user", "content": message}]
        )

        thread_id = thread.id
        print(f"Thread creado con ID: {thread_id}")

        # Continuar con el flujo normal
        run = await openai_client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

        print(f'Run status: {run.status}')
        if run.status == 'completed':
            print('OpenAI respondió correctamente.')
        else:
            print('Estado inesperado del Run:', run.status)
    except Exception as e:
        print(f'Error al probar OpenAI: {e}')

if __name__ == '__main__':
    asyncio.run(test_openai())
