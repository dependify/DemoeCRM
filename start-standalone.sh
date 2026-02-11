#!/bin/bash
# Evangelism CRM Standalone Demo - Quick Start
# =============================================

set -e

echo ""
echo "==========================================="
echo "   EVANGELISM CRM - STANDALONE DEMO"
echo "==========================================="
echo ""

BACKEND_DIR="standalone-backend"
FRONTEND_DIR="standalone-frontend"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

# Setup Backend
echo "[1/3] Setting up backend..."
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$BACKEND_DIR/venv"
fi

source "$BACKEND_DIR/venv/bin/activate"
pip install -q -r "$BACKEND_DIR/requirements.txt"
deactivate

echo ""
echo "==========================================="
echo "   STARTING DEMO APPLICATIONS"
echo "==========================================="
echo ""

# Start Backend
echo "[2/3] Starting Backend Server..."
cd "$BACKEND_DIR"
source venv/bin/activate
python server.py &
BACKEND_PID=$!
deactivate
cd ..

echo "Backend starting on http://localhost:8000"

# Wait for backend to start
sleep 3

# Start Frontend
echo ""
echo "[3/3] Starting Frontend Server..."
cd "$FRONTEND_DIR"

if ! command -v npx &> /dev/null; then
    echo "Installing Node.js dependencies..."
    npm install
fi

npx http-server -p 3005 -c-1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "==========================================="
echo "   DEMO STARTED SUCCESSFULLY!"
echo "==========================================="
echo ""
echo "Frontend: http://localhost:3005"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Login Credentials:"
echo "   Email: admin@graceevangelical.demo"
echo "   Password: Demo@2025"
echo ""
echo "Features:"
echo "   - Convert Management with Kanban Board"
echo "   - Health Scoring System"
echo "   - Alert Management"
echo "   - VOICE AGENT with AI Calling"
echo "   - Call Scripts"
echo "   - Analytics Dashboard"
echo ""
echo "Press Ctrl+C to stop..."
echo ""

# Trap Ctrl+C to clean up
trap 'echo ""; echo "Stopping servers..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo "Done!"; exit 0' INT

# Wait
wait
