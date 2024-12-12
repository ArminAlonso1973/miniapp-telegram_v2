import openai

def generar_prompt_completo(message: str, respuestas: list) -> str:
    """Genera el prompt para OpenAI."""
    prompt = f"Pregunta: {message}\nContexto:\n"
    for idx, respuesta in enumerate(respuestas, 1):
        prompt += (
            f"{idx}. Pregunta: {respuesta['question']}\n"
            f"   Respuesta: {respuesta['answer']}\n"
            f"   Referencia legal: {respuesta['legal_reference']}\n"
        )
    return prompt

def consultar_llm_respuesta_final(prompt: str) -> str:
    """Consulta OpenAI para generar la respuesta final."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
