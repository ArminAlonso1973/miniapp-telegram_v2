from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/summarize', methods=['POST'])
def summarize():
    # Llamar a claude_summarizer.py (exportación nombrada)
    return jsonify({"summary": "Resumen generado con éxito"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
