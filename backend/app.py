from flask import Flask, request, jsonify
from flask_cors import CORS

from database import Database

app = Flask(__name__)
CORS(app)

db = Database()


@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'online',
        'message_count': db.get_message_count()
    })


@app.route('/api/messages', methods=['GET'])
def get_messages():
    limit = request.args.get('limit', 100, type=int)
    hours = request.args.get('hours', type=int)
    
    messages = db.get_messages(limit=limit, hours=hours)
    return jsonify({
        'messages': [msg.to_dict() for msg in messages]
    })


@app.route('/api/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    
    if not data or 'username' not in data or 'content' not in data:
        return jsonify({'error': 'username and content are required'}), 400
    
    username = data['username'].strip()
    content = data['content'].strip()
    
    if not username or not content:
        return jsonify({'error': 'username and content cannot be empty'}), 400
    
    message = db.add_message(username, content)
    return jsonify(message.to_dict()), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
