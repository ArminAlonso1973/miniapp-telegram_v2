from quart import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import asyncio
import os
from services.claude_summarizer_service import ClaudeSummarizer
import logging

logger = logging.getLogger(__name__)

pdf_bp = Blueprint('pdf', __name__)

@pdf_bp.route('/upload-pdf', methods=['POST'])
async def upload_pdf():
    logger.info("Entrando a la ruta /upload-pdf")
    try:
        files = await request.files
        if 'file' not in files:
            logger.warning("No se proporcionó un archivo.")
            return jsonify({"error": "No se proporcionó un archivo"}), 400

        uploaded_file = files.get('file')
        if not uploaded_file:
            logger.warning("Archivo no encontrado en la solicitud.")
            return jsonify({"error": "Archivo no encontrado"}), 400

        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join('/tmp', filename)

        logger.info(f"Guardando archivo en {file_path}.")
        content = await asyncio.to_thread(uploaded_file.read)
        with open(file_path, 'wb') as f:
            f.write(content)

        summarizer = ClaudeSummarizer()
        summary_result = await summarizer.summarize_document(file_path)
        logger.info("Resumen generado exitosamente.")
        return jsonify({
            "status": "success",
            "summary": summary_result["summary"],
            "original_length": summary_result["original_length"],
            "summary_length": summary_result["summary_length"],
        })
    except Exception as e:
        logger.exception("Error al procesar el archivo:")
        return jsonify({"error": str(e)}), 500

