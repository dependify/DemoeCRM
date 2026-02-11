#!/bin/bash
set -e

echo "Installing Python dependencies..."

# Create a virtual environment to avoid system package conflicts
python3 -m venv .venv || python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate || . .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "Python dependencies installed successfully!"
