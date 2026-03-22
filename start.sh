#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing backend dependencies..."
cd "$SCRIPT_DIR/backend"
pip install -r requirements.txt -q

echo "Starting backend server on http://0.0.0.0:5000..."
python app.py &
BACKEND_PID=$!

cd "$SCRIPT_DIR/frontend"
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install -q
fi

echo "Starting frontend server on http://localhost:3000..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "Servers started:"
echo "  Backend:  http://localhost:5000"
echo "  Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"

cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

wait
