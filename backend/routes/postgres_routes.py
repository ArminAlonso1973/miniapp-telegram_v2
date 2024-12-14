from quart import Quart, jsonify
import os

app = Quart(__name__)

@app.route('/')
async def home():
    return jsonify({
        "status": "ok",
        "message": "Backend service is running",
        "database": "ArangoDB",
        "environment": {
            "POSTGRES_HOST": os.environ.get('POSTGRES_HOST', 'Not set'),
            "POSTGRES_DB": os.environ.get('POSTGRES_DB', 'Not set')
        }
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)