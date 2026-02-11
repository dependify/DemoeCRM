"""
Demo Server for Evangelism CRM
A lightweight FastAPI server configured specifically for demo mode.
"""

from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import os
import sys
from pathlib import Path
import logging

# Add parent directories to path
SCRIPT_DIR = Path(__file__).parent.resolve()
DEMO_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = DEMO_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(DEMO_DIR))

# Import from backend
from routes.auth import router as auth_router
from routes.users_v2 import router as users_router
from routes.converts import router as converts_router
from routes.services_v2 import router as services_router
from routes.followup import router as followup_router
from routes.dashboard_v2 import router as dashboard_router
from routes.workflows_v2 import router as workflows_router
from routes.health_score import router as health_score_router
from routes.alerts import router as alerts_router
from routes.analytics import router as analytics_router
from routes.sequences import router as sequences_router
from routes.playbooks import router as playbooks_router

# Import demo database
from backend.demo_database import get_demo_database, create_demo_indexes, close_demo_database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown."""
    # Startup
    logger.info("🚀 Starting Evangelism CRM Demo Server...")
    
    try:
        db = get_demo_database()
        await create_demo_indexes(db)
        logger.info("✅ Demo database connected and indexes created")
    except Exception as e:
        logger.error(f"❌ Failed to connect to demo database: {e}")
        yield
        return
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Demo Server...")
    await close_demo_database()


# Create the demo app
app = FastAPI(
    title="Evangelism CRM - Demo",
    description="Demo version of Evangelism CRM with Nigerian church data",
    version="2.0.0-demo",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # More permissive for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API router
api_router = APIRouter(prefix="/api")


# Demo-specific endpoints
@api_router.get("/demo/info")
async def demo_info():
    """Get demo information."""
    return {
        "name": "Evangelism CRM Demo",
        "version": "2.0.0-demo",
        "church": "Grace Evangelical Ministries",
        "location": "Lagos, Nigeria",
        "description": "Demo version with realistic Nigerian church data",
        "credentials": {
            "admin_email": "admin@graceevangelical.demo",
            "admin_password": "Demo@2025"
        },
        "features": [
            "Multi-tenant architecture",
            "Convert management with Nigerian data",
            "Health scoring system",
            "Automated alerts",
            "Workflow automation",
            "Sequence messaging",
            "Retention playbooks",
            "Analytics and reporting",
            "Follow-up tracking",
            "House fellowship management"
        ]
    }


@api_router.get("/demo/stats")
async def demo_stats():
    """Get demo database statistics."""
    try:
        db = get_demo_database()
        
        stats = {
            "clients": await db.clients.count_documents({}),
            "users": await db.users.count_documents({}),
            "converts": await db.converts.count_documents({}),
            "services": await db.service_instances.count_documents({}),
            "membership_classes": await db.membership_classes.count_documents({}),
            "house_fellowships": await db.house_fellowships.count_documents({}),
            "followup_records": await db.followup_records.count_documents({}),
            "health_scores": await db.health_scores.count_documents({}),
            "alerts": await db.alerts.count_documents({}),
            "workflows": await db.workflow_definitions.count_documents({}),
            "sequences": await db.sequence_definitions.count_documents({}),
            "playbooks": await db.playbooks.count_documents({}),
        }
        
        # Calculate some demo metrics
        total_converts = stats["converts"]
        if total_converts > 0:
            # Get stage distribution
            pipeline = [
                {"$group": {"_id": "$stage", "count": {"$sum": 1}}}
            ]
            stage_distribution = await db.converts.aggregate(pipeline).to_list(None)
            
            # Get health score average
            health_pipeline = [
                {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}
            ]
            health_result = await db.health_scores.aggregate(health_pipeline).to_list(None)
            avg_health = health_result[0]["avg_score"] if health_result else 0
            
            stats["metrics"] = {
                "stage_distribution": {item["_id"]: item["count"] for item in stage_distribution},
                "average_health_score": round(avg_health, 2),
                "open_alerts": await db.alerts.count_documents({"status": {"$in": ["open", "acknowledged"]}})
            }
        
        return {
            "status": "success",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Error getting demo stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/demo/reset")
async def reset_demo():
    """Reset demo data to initial state."""
    try:
        # Import the populator
        import subprocess
        import sys
        
        script_path = DEMO_DIR / "scripts" / "populate_demo.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(DEMO_DIR)
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "message": "Demo data reset successfully",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to reset demo: {result.stderr}"
            )
    except Exception as e:
        logger.error(f"Error resetting demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Include standard routers (they'll use demo database)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(converts_router)
api_router.include_router(services_router)
api_router.include_router(followup_router)
api_router.include_router(dashboard_router)
api_router.include_router(workflows_router)
api_router.include_router(health_score_router)
api_router.include_router(alerts_router)
api_router.include_router(analytics_router)
api_router.include_router(sequences_router)
api_router.include_router(playbooks_router)


# Health check
@api_router.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        db = get_demo_database()
        await db.command("ping")
        return {
            "status": "healthy",
            "database": "connected",
            "mode": "demo",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


# Root endpoint
@api_router.get("/")
async def root():
    return {
        "message": "Evangelism CRM API - Demo Mode",
        "version": "2.0.0-demo",
        "church": "Grace Evangelical Ministries",
        "location": "Lagos, Nigeria",
        "docs": "/docs"
    }


# Include the API router
app.include_router(api_router)


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("DEMO_PORT", 8001))
    
    print("\n" + "="*60)
    print("🚀 EVANGELISM CRM DEMO SERVER")
    print("="*60)
    print(f"\n📍 Server running at: http://localhost:{port}")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    print(f"🔍 Demo Info: http://localhost:{port}/api/demo/info")
    print(f"📊 Demo Stats: http://localhost:{port}/api/demo/stats")
    print("\n" + "="*60)
    
    uvicorn.run(app, host="0.0.0.0", port=port)
