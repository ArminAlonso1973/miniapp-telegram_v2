from quart import Quart, request, jsonify
from quart_cors import cors
import os
from dotenv import load_dotenv
from services.ClaudeSummarizer import ClaudeSummarizer
import asyncio
from werkzeug.utils import secure_filename
import logging
import requests
import unicodedata
from typing import List, Dict 
from openai import OpenAI


# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Inicializar el cliente OpenAI
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Crear la aplicación Quart
app = Quart(__name__)
app = cors(app, allow_origin="*")

# Palabras clave para clasificar preguntas tributarias
PALABRAS_CLAVE = [
    "impuesto", "deducción", "renta líquida imponible", "iva", "isr",
    "empresa", "gastos", "ley", "comercial", "contabilidad", "tributaria", "renta"
]


def clasificar_pregunta(pregunta: str) -> bool:
    """Clasifica si la pregunta está relacionada con temas tributarios."""
    return any(palabra.lower() in pregunta.lower() for palabra in PALABRAS_CLAVE)

async def consultar_openai(prompt: str) -> Dict:
    try:
        # Ejecutar la llamada a OpenAI en un hilo separado
        response = await asyncio.to_thread(
            openai_client.chat.completions.create,
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        # Extract the content using the new method
        respuesta = response.choices[0].message.content
        return {"respuesta": respuesta}

    except Exception as e:
        logger.exception(f"Error al consultar OpenAI: {e}")
        return {"error": "Error al consultar OpenAI"}


@app.route('/consulta-tributaria', methods=['POST'])
async def consulta_tributaria():
    """Endpoint principal para procesar preguntas tributarias."""
    try:
        data = await request.get_json()
        pregunta = data.get("pregunta")

        if not pregunta:
            logger.warning("Solicitud sin el campo 'pregunta'")
            return jsonify({"error": "Falta el campo 'pregunta'"}), 400

        # Clasificar la pregunta
        if not clasificar_pregunta(pregunta):
            logger.info("Pregunta no clasificada como tributaria")
            return jsonify({"error": "La pregunta no parece ser tributaria. Por favor, formula una pregunta relacionada con impuestos."}), 400

        # Consultar a OpenAI
        respuesta = await consultar_openai(pregunta)
        return jsonify(respuesta), 200

    except Exception as e:
        logger.exception("Error en /consulta-tributaria:")
        return jsonify({"error": "Error interno del servidor."}), 500

@app.route('/test', methods=['GET'])
async def test():
    """Endpoint de prueba para verificar que el backend está funcionando."""
    logger.info("Endpoint de prueba /test accedido")
    return jsonify({"status": "success", "message": "API funcionando correctamente"}), 200


@app.route('/telegram-bot', methods=['POST'])
async def telegram_bot():
    logger.info("Entrando a la ruta /telegram-bot")
    try:
        data = await request.get_json()

        # Ahora esperamos que el frontend envíe directamente chat_id y message
        chat_id = data.get('chat_id')
        message_text = data.get('message')

        if not chat_id:
            logger.error("No se encontró chat_id en la petición a /telegram-bot.")
            return jsonify({"error": "Falta 'chat_id'"}), 400

        if not message_text:
            logger.error("No se encontró message en la petición a /telegram-bot.")
            return jsonify({"error": "Falta 'message'"}), 400

        # Obtener el TOKEN del bot desde .env
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            logger.error("No se encontró el TOKEN del bot.")
            return jsonify({"error": "No se encontró el TOKEN del bot"}), 500

        send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message_text
        }

        logger.info(f"Enviando mensaje a Telegram: {payload}")

        # Llamada sincrónica a la API de Telegram
        import requests
        resp = requests.post(send_message_url, json=payload)
        logger.info(f"Respuesta de Telegram: status_code={resp.status_code}, respuesta={resp.text}")

        if resp.status_code == 200:
            logger.info("Mensaje enviado con éxito a Telegram.")
            return jsonify({"status": "success"})
        else:
            logger.error(f"Error al enviar el mensaje a Telegram. Status Code: {resp.status_code}, Respuesta: {resp.text}")
            return jsonify({"error": "Error al enviar el mensaje"}), 500

    except Exception as e:
        logger.exception("Error en /telegram-bot:")
        return jsonify({"error": str(e)}), 500



@app.route('/upload-pdf', methods=['POST'])
async def upload_pdf():
    logger.info("Entrando a la ruta /upload-pdf")
    try:
        # Aqui está el cambio, se usa await para obtener los archivos
        files = await request.files
        logger.info(f"Archivos recibidos: {list(files.keys())}")

        if 'file' not in files:
            logger.error("No se proporcionó el archivo en la petición.")
            return jsonify({"error": "No se proporcionó un archivo"}), 400

        uploaded_file = files.get('file')
        if not uploaded_file:
            logger.error("El archivo recibido es inválido o None.")
            return jsonify({"error": "No se proporcionó un archivo válido"}), 400

        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join('/tmp', filename)
        logger.info(f"Guardando el archivo temporalmente en: {file_path}")

        # El método read() de FileStorage es síncrono, lo envolvemos con asyncio.to_thread
        content = await asyncio.to_thread(uploaded_file.read)

        with open(file_path, 'wb') as f:
            f.write(content)
        logger.info(f"Archivo guardado exitosamente en {file_path}")

        summarizer = ClaudeSummarizer()
        logger.info("Iniciando el proceso de resumen...")
        summary_result = await summarizer.summarize_document(file_path)
        logger.info("Proceso de resumen completado con éxito.")

        return jsonify({
            "status": "success",
            "summary": summary_result["summary"],
            "original_length": summary_result["original_length"],
            "summary_length": summary_result["summary_length"],
        })

    except Exception as e:
        logger.exception("Error al procesar el archivo:")
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    print("Rutas disponibles:")
    print(app.url_map)
    app.run(host='0.0.0.0', port=5001, debug=True)
