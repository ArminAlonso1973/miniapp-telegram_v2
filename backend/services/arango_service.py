from arango import ArangoClient

arango_client = ArangoClient()
db = arango_client.db("renta_2024", username="root", password="mysecretpassword")

async def buscar_respuestas_arango(keys: list) -> list:
    """Busca respuestas en ArangoDB usando claves."""
    respuestas = []
    try:
        for key in keys:
            doc = db.collection("documentos_renta").get(key)
            if doc:
                respuestas.append({
                    "question": doc.get("question", "Pregunta no disponible"),
                    "answer": doc.get("answer", "Respuesta no disponible"),
                    "legal_reference": doc.get("legal_reference", "Referencia legal no disponible"),
                })
        return respuestas
    except Exception as e:
        print(f"Error buscando en ArangoDB: {str(e)}")
        return []
