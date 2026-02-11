#!/bin/bash
# Start Evangelism CRM Demo Frontend on Port 3005
# ================================================

echo ""
echo "Starting Frontend Server on Port 3005..."
echo ""

cd standalone-frontend

# Check if npx is available
if ! command -v npx &> /dev/null; then
    echo "ERROR: npx not found. Please install Node.js."
    exit 1
fi

echo ""
echo "==========================================="
echo "   FRONTEND STARTED!"
echo "==========================================="
echo ""
echo "Open your browser to: http://localhost:3005"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npx http-server -p 3005 -c-1 -o

cd ..
