def clasificar_pregunta(pregunta: str) -> bool:
    """Clasifica si la pregunta es tributaria o no."""
    palabras_clave = [
        "impuesto", "deducción", "renta líquida imponible", "IVA",
        "ISR", "empresa", "gastos", "ley", "comercial",
        "contabilidad", "tributaria", "renta"
    ]
    return any(palabra.lower() in pregunta.lower() for palabra in palabras_clave)
