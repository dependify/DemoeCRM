"""
Vercel Serverless Function Entry Point
Monolithic deployment of Evangelism CRM Demo
"""
import sys
import os

# Check if virtual environment exists and use it
venv_path = os.path.join(os.path.dirname(__file__), '..', '.venv')
if os.path.exists(venv_path):
    venv_site_packages = os.path.join(venv_path, 'lib')
    if os.path.exists(venv_site_packages):
        # Find the site-packages directory
        for root, dirs, files in os.walk(venv_site_packages):
            if 'site-packages' in dirs:
                site_packages = os.path.join(root, 'site-packages')
                if site_packages not in sys.path:
                    sys.path.insert(0, site_packages)
                break

# Add standalone-backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'standalone-backend')
sys.path.insert(0, backend_path)

# Import and export the FastAPI app
try:
    from server import app
except ImportError as e:
    # Fallback error app if import fails
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def error_root():
        return {"error": "Failed to load application", "details": str(e)}
    
    @app.get("/api/health")
    async def health():
        return {"status": "error", "error": str(e)}

# Vercel expects 'app' to be available at module level
