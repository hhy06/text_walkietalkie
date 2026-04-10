#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing backend dependencies..."
cd "$SCRIPT_DIR/backend"
pip install -r requirements.txt -q

cd "$SCRIPT_DIR/frontend"
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install -q
fi

echo "Building frontend..."
npm run build

cd "$SCRIPT_DIR/backend"
echo "Starting server on http://0.0.0.0:12358..."
python app.py &
BACKEND_PID=$!

echo ""
echo "Server started: http://localhost:12358"
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
