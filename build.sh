#!/bin/bash
# Custom build script for Vercel

# Try different pip install methods
if pip install -r requirements.txt 2>/dev/null; then
    echo "Packages installed successfully"
elif pip install --user -r requirements.txt 2>/dev/null; then
    echo "Packages installed with --user"
elif python -m pip install -r requirements.txt 2>/dev/null; then
    echo "Packages installed with python -m pip"
else
    echo "Warning: Could not install packages, but continuing..."
fi

echo "Build complete"
