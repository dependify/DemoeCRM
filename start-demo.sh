#!/bin/bash
# Evangelism CRM Demo - Unix/Linux/macOS Quick Start
# ===================================================

set -e

echo ""
echo "==========================================="
echo "   EVANGELISM CRM DEMO - QUICK START"
echo "==========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "==========================================="
echo "   POPULATING DEMO DATA"
echo "==========================================="
echo ""
python scripts/populate_demo.py

echo ""
echo "==========================================="
echo "   STARTING DEMO SERVER"
echo "==========================================="
echo ""
echo "The demo server will start on http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Trap Ctrl+C to clean up
trap 'echo ""; echo "Demo server stopped."; deactivate; exit 0' INT

python backend/demo_server.py
