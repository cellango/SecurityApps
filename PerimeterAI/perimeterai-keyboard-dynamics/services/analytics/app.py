from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import redis
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
redis_client = redis.from_url(os.getenv('REDIS_URL'))

@app.route('/analyze', methods=['POST'])
def analyze_typing_pattern():
    try:
        data = request.get_json()
        # Add your keyboard dynamics analysis logic here
        return jsonify({'status': 'success', 'risk_score': 0.5})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
