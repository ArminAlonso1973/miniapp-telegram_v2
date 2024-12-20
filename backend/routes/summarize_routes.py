from quart import Blueprint, request, jsonify
import os
import logging
from services.claude_summarizer_service import ClaudeSummarizer

# Configurar logging
logger = logging.getLogger(__name__)

# Crear el blueprint
summarize_bp = Blueprint('summarize', __name__)

@summarize_bp.route('/', methods=['POST'])
async def summarize():
    try:
        # Recibir archivo PDF
        files = await request.files
        pdf_file = files.get('pdf')
        
        if not pdf_file:
            logger.warning("No se proporcionó archivo PDF")
            return jsonify({"error": "No se proporcionó archivo PDF"}), 400
        
        # Guardar archivo temporalmente
        pdf_path = f"temp_{pdf_file.filename}"
        await pdf_file.save(pdf_path)
        
        try:
            # Inicializar servicio y generar resumen
            summarizer = ClaudeSummarizer()
            resultado = await summarizer.summarize_document(pdf_path)
            logger.info("Resumen generado exitosamente")
            return jsonify(resultado)
            
        finally:
            # Eliminar archivo temporal
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
    
    except Exception as e:
        logger.exception("Error al procesar el archivo:")
        return jsonify({"error": str(e)}), 500