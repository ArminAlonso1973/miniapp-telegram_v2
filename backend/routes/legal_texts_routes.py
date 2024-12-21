from quart import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os
from services.legal_texts_service import LegalTextsService
import logging

logger = logging.getLogger(__name__)
legal_texts_bp = Blueprint('legal_texts', __name__)

service = LegalTextsService()

# Endpoint para cargar un texto legal
@legal_texts_bp.route('/upload', methods=['POST'])
async def upload_legal_text():
    try:
        logger.info("Solicitud recibida para cargar un texto legal.")
        files = await request.files
        uploaded_file = files.get('file')

        if not uploaded_file:
            logger.warning("No se proporcionó un archivo.")
            return jsonify({"error": "No se proporcionó un archivo"}), 400

        # Guardar archivo temporalmente
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join('/tmp', filename)
        await uploaded_file.save(file_path)
        logger.info(f"Archivo guardado temporalmente en: {file_path}")

        # Procesar el texto legal
        text_id = await service.process_legal_text(file_path)
        logger.info(f"Texto legal procesado con ID: {text_id}")
        return jsonify({"status": "success", "text_id": text_id}), 200

    except Exception as e:
        logger.exception("Error al cargar el texto legal:")
        return jsonify({"error": str(e)}), 500

# Endpoint para listar textos legales
@legal_texts_bp.route('/', methods=['GET'])
async def list_legal_texts():
    try:
        texts = await service.list_legal_texts()
        return jsonify(texts), 200
    except Exception as e:
        logger.exception("Error al listar textos legales:")
        return jsonify({"error": str(e)}), 500

# Endpoint para listar artículos de un texto legal
@legal_texts_bp.route('/<int:text_id>/articles', methods=['GET'])
async def list_articles(text_id):
    try:
        articles = await service.list_articles(text_id)
        return jsonify(articles), 200
    except Exception as e:
        logger.exception("Error al listar artículos:")
        return jsonify({"error": str(e)}), 500
