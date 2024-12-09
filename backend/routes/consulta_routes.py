from quart import Blueprint, request, jsonify
from services.openai_service import consultar_openai
import logging

logger = logging.getLogger(__name__)

consulta_bp = Blueprint('consulta', __name__)

# Palabras clave para clasificar preguntas tributarias
PALABRAS_CLAVE = [
    "impuesto", "deducción", "renta líquida imponible", "iva", "isr",
    "empresa", "gastos", "ley", "comercial", "contabilidad", "tributaria", "renta"
]

def clasificar_pregunta(pregunta: str) -> bool:
    """Clasifica si la pregunta está relacionada con temas tributarios."""
    return any(palabra.lower() in pregunta.lower() for palabra in PALABRAS_CLAVE)

@consulta_bp.route('/test', methods=['GET'])
async def test():
    """Endpoint de prueba para verificar que el backend está funcionando."""
    return jsonify({"status": "success", "message": "API funcionando correctamente"})


@consulta_bp.route('/consulta-tributaria', methods=['POST'])
async def consulta_tributaria():
    """Endpoint principal para procesar preguntas tributarias."""
    try:
        data = await request.get_json()
        pregunta = data.get("pregunta")

        if not pregunta:
            logger.warning("Solicitud sin el campo 'pregunta'")
            return jsonify({"error": "Falta el campo 'pregunta'"}), 400

        if not clasificar_pregunta(pregunta):
            logger.info("Pregunta no clasificada como tributaria")
            return jsonify({"error": "La pregunta no parece ser tributaria. Por favor, formula una pregunta relacionada con impuestos."}), 400

        respuesta = await consultar_openai(pregunta)
        return jsonify(respuesta), 200

    except Exception as e:
        logger.exception("Error en /consulta-tributaria:")
        return jsonify({"error": "Error interno del servidor."}), 500



