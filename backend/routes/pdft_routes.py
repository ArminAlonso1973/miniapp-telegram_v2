from quart import Blueprint, request, jsonify

pdft_bp = Blueprint("pdft", __name__)

@pdft_bp.route("/upload", methods=["POST"])
async def upload_pdf():
    """Endpoint para subir y procesar un PDF."""
    try:
        files = await request.files  # Espera la coroutine
        if "file" not in files:
            return jsonify({"error": "No se ha proporcionado ningún archivo."}), 400

        pdf_file = files["file"]  # Accede al archivo
        if pdf_file.filename == "":
            return jsonify({"error": "El archivo no tiene nombre."}), 400

        # Procesar el archivo (aquí iría la lógica de resumen o análisis)
        resumen = f"Resumen del documento {pdf_file.filename} (simulado)"
        
        return jsonify({"status": "success", "summary": resumen}), 200
    except Exception as e:
        return jsonify({"error": f"Error al procesar el archivo: {str(e)}"}), 500
