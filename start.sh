#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"


cd "$SCRIPT_DIR/backend"
echo "Starting server on http://0.0.0.0:5000..."
python app.py &
BACKEND_PID=$!

echo ""
echo "Server started: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"

cleanup() {
    echo ""
    echo "Stopping server..."
    kill $BACKEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

wait
