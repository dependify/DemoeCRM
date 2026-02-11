"""
Vercel Serverless Function Entry Point
Monolithic deployment of Evangelism CRM Demo
"""
import sys
import os

# Add standalone-backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'standalone-backend')
sys.path.insert(0, backend_path)

# Import and export the FastAPI app
from server import app

# Vercel expects 'app' to be available at module level
# The app is already defined in server.py
