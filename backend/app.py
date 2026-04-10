import os
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from mimetypes import guess_type

from database import Database

BASE_DIR = Path(__file__).parent.resolve()
FRONTEND_DIST = (BASE_DIR.parent / "frontend" / "dist").resolve()

app = Flask(__name__, static_folder=None)
CORS(app)

db = Database()


@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "online", "message_count": db.get_message_count()})


@app.route("/api/messages", methods=["GET"])
def get_messages():
    limit = request.args.get("limit", 100, type=int)
    hours = request.args.get("hours", type=int)

    messages = db.get_messages(limit=limit, hours=hours)
    return jsonify({"messages": [msg.to_dict() for msg in messages]})


@app.route("/api/messages", methods=["POST"])
def post_message():
    data = request.get_json()

    if not data or "username" not in data or "content" not in data:
        return jsonify({"error": "username and content are required"}), 400

    username = data["username"].strip()
    content = data["content"].strip()

    if not username or not content:
        return jsonify({"error": "username and content cannot be empty"}), 400

    message = db.add_message(username, content)
    return jsonify(message.to_dict()), 201


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    file_path = FRONTEND_DIST / path
    if path and file_path.is_file():
        mimetype, _ = guess_type(str(file_path))
        return send_file(file_path, mimetype=mimetype)
    return send_file(FRONTEND_DIST / "index.html", mimetype="text/html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12358, debug=True)
