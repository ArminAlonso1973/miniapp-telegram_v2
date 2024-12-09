from quart import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import asyncio
import os
from services.ClaudeSummarizer import ClaudeSummarizer
import logging

logger = logging.getLogger(__name__)

pdf_bp = Blueprint('pdf', __name__)

@pdf_bp.route('/upload-pdf', methods=['POST'])
async def upload_pdf():
    """Endpoint para subir y resumir un archivo PDF."""
    logger.info("Entrando a la ruta /upload-pdf")
    try:
        files = await request.files
        if 'file' not in files:
            return jsonify({"error": "No se proporcionó un archivo"}), 400

        uploaded_file = files.get('file')
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join('/tmp', filename)

        content = await asyncio.to_thread(uploaded_file.read)
        with open(file_path, 'wb') as f:
            f.write(content)

        summarizer = ClaudeSummarizer()
        summary_result = await summarizer.summarize_document(file_path)
        return jsonify({
            "status": "success",
            "summary": summary_result["summary"],
            "original_length": summary_result["original_length"],
            "summary_length": summary_result["summary_length"],
        })
    except Exception as e:
        logger.exception("Error al procesar el archivo:")
        return jsonify({"error": str(e)}), 500
