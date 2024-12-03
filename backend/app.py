from flask import Flask, request, jsonify
from flask_cors import CORS
import telegram
import os

app = Flask(__name__)
CORS(app)

# Configuración del bot de Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'TU_TOKEN_AQUI')
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "success", "message": "API funcionando correctamente"})

@app.route('/telegram-bot', methods=['POST'])
async def send_message():
    try:
        data = request.get_json()
        message = data.get('message')
        chat_id = data.get('chat_id')

        if message and chat_id:
            await bot.send_message(chat_id=chat_id, text=message)
            return jsonify({"status": "success", "message": "Mensaje enviado correctamente"})
        else:
            return jsonify({"status": "error", "message": "Faltan datos requeridos"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)