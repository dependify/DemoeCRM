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
except Exception as e:
    import traceback
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    app = FastAPI()
    
    @app.get("/")
    async def error_root():
        return {
            "error": "Failed to load application", 
            "details": str(e),
            "traceback": traceback.format_exc()
        }
    
    @app.get("/api/health")
    async def health():
        return {"status": "error", "error": str(e)}
