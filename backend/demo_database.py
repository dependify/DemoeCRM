"""
Demo Database Utilities for Evangelism CRM
Connects to a separate demo database with 'demo_' prefix.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global database connections
_main_client: Optional[AsyncIOMotorClient] = None
_demo_client: Optional[AsyncIOMotorClient] = None
_main_db: Optional[AsyncIOMotorDatabase] = None
_demo_db: Optional[AsyncIOMotorDatabase] = None

# Demo database suffix
DEMO_DB_SUFFIX = "_demo"


def get_main_database() -> AsyncIOMotorDatabase:
    """Get the main production database instance."""
    global _main_client, _main_db
    
    if _main_db is None:
        mongo_url = os.environ.get("MONGO_URL")
        db_name = os.environ.get("DB_NAME", "evangelism_crm")
        
        if not mongo_url:
            raise ValueError("MONGO_URL must be set")
        
        _main_client = AsyncIOMotorClient(mongo_url)
        _main_db = _main_client[db_name]
    
    return _main_db


def get_demo_database() -> AsyncIOMotorDatabase:
    """Get the demo database instance (with _demo suffix)."""
    global _demo_client, _demo_db
    
    if _demo_db is None:
        mongo_url = os.environ.get("MONGO_URL")
        base_db_name = os.environ.get("DB_NAME", "evangelism_crm")
        demo_db_name = f"{base_db_name}{DEMO_DB_SUFFIX}"
        
        if not mongo_url:
            raise ValueError("MONGO_URL must be set")
        
        _demo_client = AsyncIOMotorClient(mongo_url)
        _demo_db = _demo_client[demo_db_name]
    
    return _demo_db


async def close_demo_database():
    """Close the demo database connection."""
    global _demo_client, _demo_db
    if _demo_client:
        _demo_client.close()
        _demo_client = None
        _demo_db = None


async def close_main_database():
    """Close the main database connection."""
    global _main_client, _main_db
    if _main_client:
        _main_client.close()
        _main_client = None
        _main_db = None


async def close_all_databases():
    """Close all database connections."""
    await close_demo_database()
    await close_main_database()


# Collection names - V2 Multi-Tenant Architecture
# Same as main app but for demo database
DEMO_COLLECTIONS = {
    # Core Multi-Tenant
    "clients": "clients",
    "users": "users",
    "partner_churches": "partner_churches",
    
    # Converts
    "converts": "converts",
    "convert_lists": "convert_lists",
    
    # Events & Services
    "service_templates": "service_templates",
    "service_instances": "service_instances",
    "programmes": "programmes",
    "outreaches": "outreaches",
    
    # Classes & Growth
    "membership_classes": "membership_classes",
    "class_sessions": "class_sessions",
    "class_enrollments": "class_enrollments",
    "house_fellowships": "house_fellowships",
    
    # Follow-up
    "followup_records": "followup_records",
    "mentorship_reports": "mentorship_reports",
    
    # Workflows
    "workflow_definitions": "workflow_definitions",
    "workflow_executions": "workflow_executions",
    "followup_tasks": "followup_tasks",
    
    # Sequences & Playbooks
    "sequence_definitions": "sequence_definitions",
    "sequence_executions": "sequence_executions",
    "playbooks": "playbooks",
    "playbook_executions": "playbook_executions",
    
    # Health Score and Alerts
    "health_scores": "health_scores",
    "alerts": "alerts",
    "alert_rules": "alert_rules",
    
    # Communications
    "sms_logs": "sms_logs",
    "sms_settings": "sms_settings",
    "sms_campaigns": "sms_campaigns",
    "voice_calls": "voice_calls",
    "call_scripts": "call_scripts",
    
    # Analytics
    "analytics_events": "analytics_events",
    "reports": "reports",
    "dashboards": "dashboards",
    
    # RBAC
    "roles": "roles",
    "user_roles": "user_roles",
    "role_templates": "role_templates",
    "permission_audit": "permission_audit",
    "permission_usage": "permission_usage",
    
    # Legacy
    "contacts": "contacts",
    "workflows": "workflows",
    "stages": "stages",
    "interactions": "interactions",
    "outings": "outings",
    "activities": "activities",
    "enrollments": "enrollments",
    "service_areas": "service_areas",
    "lead_scores": "lead_scores",
    "workflow_rules": "workflow_rules",
    "contact_spirituals": "contact_spirituals",
    "comments": "comments",
    "audit_logs": "audit_logs",
    "consent_logs": "consent_logs",
    "webhooks": "webhooks",
    "custom_fields": "custom_fields",
    "voice_recordings": "voice_recordings",
    
    # Demo-specific
    "demo_metadata": "demo_metadata",
    "demo_reset_log": "demo_reset_log",
}


async def create_demo_indexes(db: AsyncIOMotorDatabase):
    """Create all necessary indexes for the demo database."""
    
    # Clients indexes
    await db.clients.create_index("name", unique=True)
    await db.clients.create_index("status")
    await db.clients.create_index("type")
    
    # Users indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("role")
    await db.users.create_index("client_id")
    await db.users.create_index([("client_id", 1), ("role", 1)])
    
    # Converts indexes
    await db.converts.create_index("id", unique=True)
    await db.converts.create_index("client_id")
    await db.converts.create_index("email")
    await db.converts.create_index("phone")
    await db.converts.create_index("assigned_worker_id")
    await db.converts.create_index("stage")
    await db.converts.create_index("created_at")
    await db.converts.create_index([("client_id", 1), ("stage", 1)])
    await db.converts.create_index([("first_name", "text"), ("last_name", "text")])
    
    # Service indexes
    await db.service_templates.create_index("id", unique=True)
    await db.service_instances.create_index("id", unique=True)
    await db.service_instances.create_index("date")
    await db.programmes.create_index("id", unique=True)
    
    # Follow-up indexes
    await db.followup_records.create_index("convert_id")
    await db.followup_records.create_index("worker_id")
    await db.mentorship_reports.create_index("mentor_id")
    await db.mentorship_reports.create_index("mentee_id")
    
    # Workflow indexes
    await db.workflow_definitions.create_index("id", unique=True)
    await db.workflow_executions.create_index("workflow_id")
    await db.workflow_executions.create_index("convert_id")
    await db.followup_tasks.create_index("assignee_id")
    await db.followup_tasks.create_index("convert_id")
    await db.followup_tasks.create_index("due_date")
    
    # Sequences and Playbooks
    await db.sequence_definitions.create_index("id", unique=True)
    await db.sequence_executions.create_index("convert_id")
    await db.playbooks.create_index("id", unique=True)
    await db.playbook_executions.create_index("convert_id")
    
    # Health Score and Alerts
    await db.health_scores.create_index("convert_id")
    await db.health_scores.create_index([("client_id", 1), ("score", 1)])
    await db.alerts.create_index("convert_id")
    await db.alerts.create_index("assigned_to")
    await db.alerts.create_index("status")
    
    # Communications
    await db.sms_logs.create_index("convert_id")
    await db.sms_logs.create_index("created_at")
    await db.voice_calls.create_index("convert_id")
    
    # Analytics and Audit
    await db.audit_logs.create_index("user_id")
    await db.audit_logs.create_index("timestamp")
    
    # RBAC indexes
    await db.roles.create_index("id", unique=True)
    await db.user_roles.create_index([("user_id", 1), ("role_id", 1)])


async def reset_demo_database():
    """Reset the demo database by dropping all collections."""
    db = get_demo_database()
    
    # Get all collections
    collections = await db.list_collection_names()
    
    # Drop each collection
    for collection_name in collections:
        await db.drop_collection(collection_name)
    
    # Recreate indexes
    await create_demo_indexes(db)
    
    return {"status": "success", "message": f"Dropped {len(collections)} collections"}


async def get_demo_stats() -> Dict[str, Any]:
    """Get statistics about the demo database."""
    db = get_demo_database()
    
    stats = {}
    for key, collection_name in DEMO_COLLECTIONS.items():
        try:
            count = await db[collection_name].count_documents({})
            stats[key] = count
        except Exception:
            stats[key] = 0
    
    return stats
