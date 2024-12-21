from quart import Blueprint, request, jsonify
import os
import logging
from services.claude_summarizer_service import ClaudeSummarizer
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

summarize_bp = Blueprint('summarize', __name__)

@summarize_bp.route('/summarize', methods=['POST'])
async def summarize():
    logger.info("Solicitud recibida en /summarize.")
    try:
        files = await request.files
        pdf_file = files.get('pdf')
        if not pdf_file:
            logger.warning("No se proporcionó archivo PDF")
            return jsonify({"error": "No se proporcionó archivo PDF"}), 400
        
        filename = secure_filename(pdf_file.filename)
        pdf_path = os.path.join('/tmp', filename)
        logger.info(f"Guardando archivo temporalmente en {pdf_path}.")
        await pdf_file.save(pdf_path)
        
        try:
            summarizer = ClaudeSummarizer()
            resultado = await summarizer.summarize_document(pdf_path)
            logger.info("Resumen generado exitosamente.")
            return jsonify({
                "status": "success",
                "original_length": resultado["original_length"],
                "summary_length": resultado["summary_length"],
                "summary": resultado["summary"],
                "num_chunks": resultado["num_chunks"]
            })
        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                logger.info(f"Archivo temporal eliminado: {pdf_path}")
    except Exception as e:
        logger.exception("Error al procesar el archivo:")
        return jsonify({"error": str(e)}), 500
