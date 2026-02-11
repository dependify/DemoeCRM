"""
Vercel Serverless Function Entry Point
Monolithic deployment of Evangelism CRM Demo
"""
import sys
import os

# Add standalone-backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'standalone-backend')
sys.path.insert(0, backend_path)

# Import the FastAPI app
try:
    from server import app
except ImportError as e:
    # Fallback error app if import fails
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    app = FastAPI()
    
    @app.get("/")
    async def error_root():
        return {"error": "Failed to load application", "details": str(e)}
    
    @app.get("/api/health")
    async def health():
        return {"status": "error", "error": str(e)}

# Vercel Python runtime expects 'app' to be an ASGI application
# The 'app' variable is automatically detected and served
