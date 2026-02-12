#!/usr/bin/env python3
"""
Demo Data Population Script for Evangelism CRM
Creates realistic Nigerian church data for demonstration purposes.
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta, date, timezone
from typing import List, Dict, Any, Optional
import uuid
import random
import bcrypt
import argparse

# Add parent directories to path for imports
SCRIPT_DIR = Path(__file__).parent.resolve()
DEMO_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = DEMO_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(DEMO_DIR))

# Import from demo data generators
from data.nigerian_data import (
    generate_nigerian_person, generate_nigerian_phone, generate_nigerian_address,
    generate_nigerian_email, NIGERIAN_STATES_LGAS, NIGERIAN_CHURCHES,
    SERVICE_TYPES, EVENT_NAMES, OCCUPATIONS, DEMO_CONFIG, get_random_state,
    get_church_branches, NIGERIAN_FIRST_NAMES_MALE, NIGERIAN_FIRST_NAMES_FEMALE,
    NIGERIAN_LAST_NAMES
)

# Import from backend models
from models.user import UserRole, User, UserInDB
from models.convert import Convert, ConvertStage, ConvertSource, ConvertList

# Import database utilities
from backend.demo_database import get_demo_database, create_demo_indexes, DEMO_COLLECTIONS


class DemoDataPopulator:
    """Populates the demo database with realistic Nigerian church data."""
    
    def __init__(self):
        self.db = None
        self.client_id = DEMO_CONFIG["demo_client_id"]
        self.church_name = DEMO_CONFIG["church_name"]
        self.users: List[Dict] = []
        self.converts: List[Dict] = []
        self.services: List[Dict] = []
        self.converts_count = DEMO_CONFIG["default_converts_count"]
        self.workers_count = DEMO_CONFIG["default_workers_count"]
        self.services_count = DEMO_CONFIG["default_services_count"]
        self.outreaches_count = DEMO_CONFIG["default_outreaches_count"]
        
    async def initialize(self):
        """Initialize database connection."""
        self.db = get_demo_database()
        await create_demo_indexes(self.db)
        print(f"✓ Connected to demo database")
        
    async def clear_existing_data(self):
        """Clear all existing demo data."""
        print("\n🗑️  Clearing existing demo data...")
        collections = [
            "clients", "users", "converts", "convert_lists",
            "service_templates", "service_instances", "programmes", "outreaches",
            "membership_classes", "class_sessions", "class_enrollments",
            "house_fellowships", "followup_records", "mentorship_reports",
            "workflow_definitions", "workflow_executions", "followup_tasks",
            "sequence_definitions", "sequence_executions", "playbooks", "playbook_executions",
            "health_scores", "alerts", "alert_rules",
            "sms_logs", "voice_calls", "audit_logs", "demo_metadata"
        ]
        
        for collection in collections:
            try:
                await self.db[collection].delete_many({})
            except Exception as e:
                print(f"  Warning: Could not clear {collection}: {e}")
        
        print("✓ Existing data cleared")
        
    async def create_client(self):
        """Create the demo church client."""
        print(f"\n🏢 Creating demo client: {self.church_name}")
        
        client_data = {
            "id": self.client_id,
            "name": self.church_name,
            "type": "church",
            "status": "active",
            "address": "15 Church Street, Ikeja, Lagos",
            "city": "Ikeja",
            "state": "Lagos",
            "country": "Nigeria",
            "phone": generate_nigerian_phone(),
            "email": "info@dependifygospel.ng",
            "website": "https://dependifygospel.ng",
            "pastor_in_charge": "Rev. Dr. Emmanuel Adeyemi",
            "founded_year": 2005,
            "member_count": 2500,
            "description": "A vibrant Pentecostal church committed to evangelism and disciple-making",
            "doctrine": "Pentecostal",
            "service_times": {
                "sunday": "8:00 AM, 10:00 AM, 12:00 PM",
                "wednesday": "6:00 PM",
                "friday": "6:30 PM"
            },
            "logo_url": "",
            "settings": {
                "timezone": "Africa/Lagos",
                "currency": "NGN",
                "language": "en",
                "date_format": "DD/MM/YYYY"
            },
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "is_demo": True
        }
        
        await self.db.clients.insert_one(client_data)
        print(f"✓ Client created: {self.church_name}")
        return client_data
        
    async def create_users(self):
        """Create demo users with different roles."""
        print(f"\n👥 Creating {self.workers_count} demo users...")
        
        # Admin user
        admin_person = generate_nigerian_person("male")
        admin_password = bcrypt.hashpw(DEMO_CONFIG["admin_password"].encode(), bcrypt.gensalt())
        
        admin_user = {
            "id": str(uuid.uuid4()),
            "name": admin_person["full_name"],
            "email": DEMO_CONFIG["admin_email"],
            "username": "admin",
            "role": UserRole.CLIENT_ADMIN.value,
            "phone": admin_person["phone"],
            "location": "Lagos",
            "is_active": True,
            "client_id": self.client_id,
            "hashed_password": admin_password.decode(),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "is_demo": True
        }
        
        await self.db.users.insert_one(admin_user)
        self.users.append(admin_user)
        print(f"  ✓ Admin: {admin_user['name']} ({admin_user['email']})")
        
        # Role distribution
        roles = [
            UserRole.FOLLOWUP_LEADER,
            UserRole.FOLLOWUP_WORKER,
            UserRole.FOLLOWUP_WORKER,
            UserRole.DATA_ENTRY,
            UserRole.MENTOR,
            UserRole.COUNSELLING_LEADER,
            UserRole.WELFARE_OFFICER,
            UserRole.PARTNER,
            UserRole.PARTNER,
            UserRole.FOLLOWUP_WORKER,
            UserRole.FOLLOWUP_WORKER,
            UserRole.FOLLOWUP_WORKER,
            UserRole.FOLLOWUP_WORKER,
            UserRole.FOLLOWUP_WORKER,
        ]
        
        # Generate additional users
        for i, role in enumerate(roles):
            person = generate_nigerian_person()
            password = bcrypt.hashpw("Demo@2025".encode(), bcrypt.gensalt())
            
            user = {
                "id": str(uuid.uuid4()),
                "name": person["full_name"],
                "email": f"{role.value}{i+1}@dependifygospel.demo",
                "username": f"{role.value}{i+1}",
                "role": role.value,
                "phone": person["phone"],
                "location": person["city"],
                "is_active": True,
                "client_id": self.client_id,
                "hashed_password": password.decode(),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            }
            
            await self.db.users.insert_one(user)
            self.users.append(user)
            print(f"  ✓ {role.value}: {user['name']}")
        
        print(f"✓ Created {len(self.users)} users")
        return self.users
        
    async def create_converts(self):
        """Create demo converts with realistic data."""
        print(f"\n🙏 Creating {self.converts_count} demo converts...")
        
        worker_ids = [u["id"] for u in self.users if u["role"] in [
            UserRole.FOLLOWUP_WORKER.value, 
            UserRole.FOLLOWUP_LEADER.value,
            UserRole.MENTOR.value
        ]]
        
        stages = list(ConvertStage)
        sources = list(ConvertSource)
        stage_weights = [0.15, 0.25, 0.20, 0.15, 0.10, 0.05, 0.10]  # Distribution
        
        converts_data = []
        
        for i in range(self.converts_count):
            person = generate_nigerian_person()
            
            # Random stage based on weights
            stage = random.choices(stages, weights=stage_weights)[0]
            source = random.choice(sources)
            
            # Generate dates
            today = date.today()
            days_ago = random.randint(1, 365)
            created_at = datetime.now(timezone.utc) - timedelta(days=days_ago)
            
            convert_data = {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "first_name": person["first_name"],
                "last_name": person["last_name"],
                "phone": person["phone"],
                "email": person["email"],
                "gender": person["gender"],
                "date_of_birth": person["date_of_birth"],
                "address": person["address"],
                "city": person["city"],
                "occupation": person["occupation"],
                "source": source.value,
                "source_date": (today - timedelta(days=days_ago)).isoformat(),
                "stage": stage.value,
                "stage_updated_at": created_at.isoformat(),
                "assigned_worker_id": random.choice(worker_ids) if worker_ids else None,
                "notes": f"Convert from {source.value}. Interested in learning more about the church." if random.random() > 0.7 else None,
                "tags": random.sample(["new", "prayer-request", "follow-up-needed", "baptism-candidate"], k=random.randint(0, 2)),
                "salvation_date": (today - timedelta(days=days_ago + random.randint(0, 30))).isoformat() if random.random() > 0.3 else None,
                "created_at": created_at.isoformat(),
                "updated_at": created_at.isoformat(),
                "created_by": random.choice([u["id"] for u in self.users]),
                "is_demo": True
            }
            
            converts_data.append(convert_data)
            
            # Batch insert every 100 records
            if len(converts_data) >= 100:
                await self.db.converts.insert_many(converts_data)
                converts_data = []
                
        # Insert remaining
        if converts_data:
            await self.db.converts.insert_many(converts_data)
            
        self.converts = await self.db.converts.find({"client_id": self.client_id}).to_list(None)
        print(f"✓ Created {len(self.converts)} converts")
        return self.converts
        
    async def create_services(self):
        """Create demo church services."""
        print(f"\n⛪ Creating {self.services_count} demo services...")
        
        services_data = []
        today = date.today()
        
        service_types = ["Sunday Service", "Midweek Service", "Prayer Meeting", "Special Program"]
        
        for i in range(self.services_count):
            service_date = today - timedelta(days=random.randint(1, 180))
            service_type = random.choice(service_types)
            
            # Determine title based on service type
            if service_type == "Sunday Service":
                title = f"Sunday Worship Service - {service_date.strftime('%B %d, %Y')}"
            elif service_type == "Midweek Service":
                title = f"Midweek Bible Study - {service_date.strftime('%B %d, %Y')}"
            elif service_type == "Prayer Meeting":
                title = f"Prayer and Fasting - {service_date.strftime('%B %d, %Y')}"
            else:
                title = f"{random.choice(EVENT_NAMES)}"
            
            # Count converts from this service
            converts_count = random.randint(5, 30) if random.random() > 0.3 else 0
            
            service_data = {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "title": title,
                "type": service_type,
                "date": service_date.isoformat(),
                "time": random.choice(["08:00", "09:00", "10:00", "18:00", "18:30"]),
                "venue": random.choice(["Main Sanctuary", "Youth Hall", "Fellowship Hall", "Outdoor Arena"]),
                "preacher": random.choice([u["name"] for u in self.users]),
                "theme": random.choice([
                    "Faith That Moves Mountains",
                    "Walking in Divine Health",
                    "The Power of Thanksgiving",
                    "Breaking Generational Curses",
                    "Financial Prosperity",
                    "Marriage Success",
                    "Raising Godly Children",
                    "Spiritual Warfare",
                    "The Holy Spirit",
                    "Divine Direction"
                ]),
                "attendance": random.randint(150, 800),
                "converts_count": converts_count,
                "description": f"A blessed {service_type.lower()} with powerful ministration",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "created_by": self.users[0]["id"],
                "is_demo": True
            }
            
            services_data.append(service_data)
        
        await self.db.service_instances.insert_many(services_data)
        self.services = services_data
        print(f"✓ Created {len(services_data)} services")
        return services_data
        
    async def create_convert_lists(self):
        """Create convert lists from services."""
        print("\n📋 Creating convert lists...")
        
        lists_data = []
        
        for service in self.services:
            if service["converts_count"] > 0:
                list_data = {
                    "id": str(uuid.uuid4()),
                    "client_id": self.client_id,
                    "name": f"Converts from {service['title']}",
                    "source": "service",
                    "source_id": service["id"],
                    "source_date": service["date"],
                    "stages": [
                        {"id": "new", "name": "New", "sequence": 0, "color": "#f97316"},
                        {"id": "contacted", "name": "First Contact", "sequence": 1, "color": "#eab308"},
                        {"id": "in_followup", "name": "In Follow-up", "sequence": 2, "color": "#22c55e"},
                        {"id": "in_classes", "name": "In Classes", "sequence": 3, "color": "#3b82f6"},
                        {"id": "in_house_fellowship", "name": "In House Fellowship", "sequence": 4, "color": "#8b5cf6"},
                        {"id": "established", "name": "Established", "sequence": 5, "color": "#0d9488"},
                    ],
                    "total_converts": service["converts_count"],
                    "is_active": True,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                    "created_by": service["created_by"],
                    "is_demo": True
                }
                
                lists_data.append(list_data)
        
        if lists_data:
            await self.db.convert_lists.insert_many(lists_data)
        
        print(f"✓ Created {len(lists_data)} convert lists")
        return lists_data
        
    async def create_membership_classes(self):
        """Create demo membership classes."""
        print("\n📚 Creating membership classes...")
        
        classes_data = [
            {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "name": "Foundation Class",
                "description": "Introduction to the Christian faith and our church doctrine",
                "duration_weeks": 4,
                "topics": [
                    "The New Birth",
                    "Water Baptism",
                    "The Holy Spirit",
                    "Christian Living"
                ],
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            },
            {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "name": "Discipleship Class",
                "description": "Deepening your walk with God",
                "duration_weeks": 8,
                "topics": [
                    "Prayer Life",
                    "Studying the Bible",
                    "Faith",
                    "The Holy Spirit",
                    "Spiritual Gifts",
                    "Evangelism",
                    "Stewardship",
                    "Church Membership"
                ],
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            },
            {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "name": "Leadership Class",
                "description": "Training for church workers and leaders",
                "duration_weeks": 12,
                "topics": [
                    "Leadership Principles",
                    "Servant Leadership",
                    "Team Building",
                    "Communication",
                    "Conflict Resolution",
                    "Mentoring Others"
                ],
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            }
        ]
        
        await self.db.membership_classes.insert_many(classes_data)
        print(f"✓ Created {len(classes_data)} membership classes")
        return classes_data
        
    async def create_house_fellowships(self):
        """Create demo house fellowships."""
        print("\n🏠 Creating house fellowships...")
        
        locations = [
            ("Ikeja", "Lagos"), ("Yaba", "Lagos"), ("Surulere", "Lagos"),
            ("Ikorodu", "Lagos"), ("Lekki", "Lagos"), ("Victoria Island", "Lagos"),
            ("Ibadan", "Oyo"), ("Abeokuta", "Ogun"), ("Osogbo", "Osun"),
            ("Akure", "Ondo")
        ]
        
        fellowships_data = []
        for i, (city, state) in enumerate(locations[:8]):
            leader = generate_nigerian_person()
            
            fellowship_data = {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "name": f"{city} House Fellowship {i+1}",
                "address": generate_nigerian_address(state, city)["full_address"],
                "city": city,
                "state": state,
                "leader_name": leader["full_name"],
                "leader_phone": leader["phone"],
                "leader_email": leader["email"],
                "meeting_day": random.choice(["Tuesday", "Wednesday", "Thursday", "Saturday"]),
                "meeting_time": random.choice(["18:00", "18:30", "19:00"]),
                "member_count": random.randint(8, 35),
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            }
            
            fellowships_data.append(fellowship_data)
        
        await self.db.house_fellowships.insert_many(fellowships_data)
        print(f"✓ Created {len(fellowships_data)} house fellowships")
        return fellowships_data
        
    async def create_followup_records(self):
        """Create demo follow-up records."""
        print("\n📞 Creating follow-up records...")
        
        worker_ids = [u["id"] for u in self.users if u["role"] in [
            UserRole.FOLLOWUP_WORKER.value, UserRole.FOLLOWUP_LEADER.value
        ]]
        
        records_data = []
        
        # Create follow-up records for some converts
        sample_converts = random.sample(self.converts, min(len(self.converts) // 3, 100))
        
        for convert in sample_converts:
            num_records = random.randint(1, 5)
            
            for _ in range(num_records):
                record_date = datetime.fromisoformat(convert["created_at"]) + timedelta(
                    days=random.randint(1, 60)
                )
                
                record_data = {
                    "id": str(uuid.uuid4()),
                    "client_id": self.client_id,
                    "convert_id": convert["id"],
                    "worker_id": random.choice(worker_ids),
                    "type": random.choice(["call", "visit", "sms", "email", "meeting"]),
                    "status": random.choice(["completed", "completed", "completed", "no_response", "scheduled"]),
                    "notes": random.choice([
                        "Convert is progressing well in faith",
                        "Needs prayer for job situation",
                        "Interested in joining house fellowship",
                        "Has questions about water baptism",
                        "Family challenges, needs support",
                        "Very enthusiastic about the church",
                        "Missed last two services, follow up needed"
                    ]),
                    "scheduled_date": record_date.isoformat(),
                    "completed_date": record_date.isoformat() if random.random() > 0.2 else None,
                    "created_at": record_date.isoformat(),
                    "is_demo": True
                }
                
                records_data.append(record_data)
        
        if records_data:
            await self.db.followup_records.insert_many(records_data)
        
        print(f"✓ Created {len(records_data)} follow-up records")
        return records_data
        
    async def create_health_scores(self):
        """Create demo health scores for converts."""
        print("\n💚 Creating health scores...")
        
        scores_data = []
        
        # Create health scores for converts
        for convert in self.converts:
            # Calculate score based on stage and activity
            base_scores = {
                ConvertStage.NEW.value: random.randint(20, 40),
                ConvertStage.IN_FOLLOWUP.value: random.randint(35, 60),
                ConvertStage.IN_CLASSES.value: random.randint(50, 75),
                ConvertStage.IN_HOUSE_FELLOWSHIP.value: random.randint(65, 85),
                ConvertStage.ESTABLISHED.value: random.randint(80, 100),
                ConvertStage.HANDED_OVER.value: random.randint(40, 70),
                ConvertStage.INACTIVE.value: random.randint(5, 25),
            }
            
            score = base_scores.get(convert["stage"], 50)
            
            score_data = {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "convert_id": convert["id"],
                "score": score,
                "factors": {
                    "attendance_rate": random.randint(0, 100),
                    "engagement_level": random.randint(0, 100),
                    "response_time": random.randint(0, 100),
                    "spiritual_growth": random.randint(0, 100),
                    "social_connection": random.randint(0, 100)
                },
                "calculated_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            }
            
            scores_data.append(score_data)
        
        # Batch insert
        batch_size = 100
        for i in range(0, len(scores_data), batch_size):
            batch = scores_data[i:i+batch_size]
            await self.db.health_scores.insert_many(batch)
        
        print(f"✓ Created {len(scores_data)} health scores")
        return scores_data
        
    async def create_alerts(self):
        """Create demo alerts."""
        print("\n🚨 Creating alerts...")
        
        # Get converts with low health scores
        low_score_converts = await self.db.health_scores.find({
            "client_id": self.client_id,
            "score": {"$lt": 40}
        }).to_list(None)
        
        alerts_data = []
        
        alert_types = [
            ("low_engagement", "Low Engagement Alert", "Convert has not attended services for 3 weeks"),
            ("at_risk", "At Risk Alert", "Convert showing signs of disengagement"),
            ("follow_up_overdue", "Follow-up Overdue", "Scheduled follow-up is overdue"),
            ("no_response", "No Response Alert", "Convert not responding to communication"),
        ]
        
        for score in low_score_converts[:20]:  # Create alerts for first 20 low scores
            alert_type, title, description = random.choice(alert_types)
            
            alert_data = {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "convert_id": score["convert_id"],
                "type": alert_type,
                "title": title,
                "description": description,
                "severity": random.choice(["low", "medium", "high"]),
                "status": random.choice(["open", "open", "acknowledged", "in_progress"]),
                "assigned_to": random.choice([u["id"] for u in self.users if u["role"] == UserRole.FOLLOWUP_LEADER.value]),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            }
            
            alerts_data.append(alert_data)
        
        if alerts_data:
            await self.db.alerts.insert_many(alerts_data)
        
        print(f"✓ Created {len(alerts_data)} alerts")
        return alerts_data
        
    async def create_workflows(self):
        """Create demo workflow definitions."""
        print("\n⚙️  Creating workflows...")
        
        workflows_data = [
            {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "name": "New Convert Onboarding",
                "description": "Automated workflow for welcoming and onboarding new converts",
                "trigger": "convert_created",
                "steps": [
                    {"step": 1, "action": "send_welcome_sms", "delay_hours": 0},
                    {"step": 2, "action": "assign_followup_worker", "delay_hours": 2},
                    {"step": 3, "action": "send_followup_email", "delay_hours": 24},
                    {"step": 4, "action": "create_followup_task", "delay_hours": 48},
                    {"step": 5, "action": "schedule_call", "delay_hours": 72},
                ],
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            },
            {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "name": "Absent Member Recovery",
                "description": "Workflow for re-engaging absent members",
                "trigger": "no_attendance_14_days",
                "steps": [
                    {"step": 1, "action": "send_care_sms", "delay_hours": 0},
                    {"step": 2, "action": "create_welfare_task", "delay_hours": 24},
                    {"step": 3, "action": "pastor_call", "delay_hours": 72},
                    {"step": 4, "action": "home_visit", "delay_hours": 168},
                ],
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            },
            {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "name": "Baptism Preparation",
                "description": "Workflow to prepare converts for water baptism",
                "trigger": "baptism_interest",
                "steps": [
                    {"step": 1, "action": "enroll_baptism_class", "delay_hours": 0},
                    {"step": 2, "action": "send_class_reminder", "delay_hours": 48},
                    {"step": 3, "action": "schedule_baptism", "delay_hours": 168},
                    {"step": 4, "action": "send_confirmation", "delay_hours": 336},
                ],
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            }
        ]
        
        await self.db.workflow_definitions.insert_many(workflows_data)
        print(f"✓ Created {len(workflows_data)} workflows")
        return workflows_data
        
    async def create_sequences(self):
        """Create demo sequences (automation)."""
        print("\n📬 Creating sequences...")
        
        sequences_data = [
            {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "name": "New Convert Welcome Series",
                "description": "7-day email/SMS series for new converts",
                "type": "onboarding",
                "messages": [
                    {"day": 1, "channel": "sms", "content": "Welcome to Dependify Gospel! We're excited to have you. Service is Sunday 9am."},
                    {"day": 2, "channel": "email", "content": "Here's a guide to help you get started..."},
                    {"day": 3, "channel": "sms", "content": "Join us for midweek service tomorrow at 6pm!"},
                    {"day": 7, "channel": "email", "content": "How was your first week? We'd love to hear from you."},
                ],
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            },
            {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "name": "Follow-up Reminder Sequence",
                "description": "Reminders for follow-up workers",
                "type": "internal",
                "messages": [
                    {"day": 0, "channel": "sms", "content": "New convert assigned to you. Please contact within 24 hours."},
                    {"day": 3, "channel": "sms", "content": "Reminder: Follow up on your assigned converts."},
                    {"day": 7, "channel": "email", "content": "Weekly follow-up summary..."},
                ],
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            }
        ]
        
        await self.db.sequence_definitions.insert_many(sequences_data)
        print(f"✓ Created {len(sequences_data)} sequences")
        return sequences_data
        
    async def create_playbooks(self):
        """Create demo playbooks (retention strategies)."""
        print("\n📖 Creating playbooks...")
        
        playbooks_data = [
            {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "name": "First Time Visitor Engagement",
                "description": "Strategy for engaging first-time church visitors",
                "category": "retention",
                "steps": [
                    {"order": 1, "title": "Immediate Welcome", "description": "Send welcome SMS within 2 hours", "owner": "automation"},
                    {"order": 2, "title": "Personal Call", "description": "Follow-up worker calls within 24 hours", "owner": "followup_worker"},
                    {"order": 3, "title": "Invite to Fellowship", "description": "Invite to house fellowship meeting", "owner": "followup_worker"},
                    {"order": 4, "title": "Sunday Service Reminder", "description": "Send reminder for next Sunday", "owner": "automation"},
                    {"order": 5, "title": "Personal Greeting", "description": "Greet personally on next visit", "owner": "usher_team"},
                ],
                "target_audience": "first_time_visitors",
                "expected_outcome": "70% return for second visit",
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            },
            {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "name": "At-Risk Member Recovery",
                "description": "Strategy for re-engaging members showing signs of disengagement",
                "category": "recovery",
                "steps": [
                    {"order": 1, "title": "Identify At-Risk", "description": "System identifies members absent for 2+ weeks", "owner": "system"},
                    {"order": 2, "title": "Welfare Check", "description": "Welfare officer makes welfare check call", "owner": "welfare_officer"},
                    {"order": 3, "title": "Personal Visit", "description": "If no response, schedule home visit", "owner": "followup_leader"},
                    {"order": 4, "title": "Pastoral Care", "description": "Pastor reaches out if still no response", "owner": "pastor"},
                    {"order": 5, "title": "Re-engagement Program", "description": "Enroll in special re-engagement program", "owner": "discipleship_team"},
                ],
                "target_audience": "at_risk_members",
                "expected_outcome": "40% re-engagement rate",
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            },
            {
                "id": str(uuid.uuid4()),
                "client_id": self.client_id,
                "name": "New Member Integration",
                "description": "Strategy for integrating new members into the church community",
                "category": "integration",
                "steps": [
                    {"order": 1, "title": "Foundation Class", "description": "Enroll in foundation class", "owner": "discipleship_team"},
                    {"order": 2, "title": "Department Placement", "description": "Assess and place in appropriate department", "owner": "head_of_departments"},
                    {"order": 3, "title": "House Fellowship", "description": "Connect to nearest house fellowship", "owner": "followup_worker"},
                    {"order": 4, "title": "Mentor Assignment", "description": "Assign a mature member as mentor", "owner": "mentorship_coordinator"},
                    {"order": 5, "title": "Follow-up", "description": "Check-in after 3 months", "owner": "followup_worker"},
                ],
                "target_audience": "new_members",
                "expected_outcome": "80% complete integration within 6 months",
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_demo": True
            }
        ]
        
        await self.db.playbooks.insert_many(playbooks_data)
        print(f"✓ Created {len(playbooks_data)} playbooks")
        return playbooks_data
        
    async def create_demo_metadata(self):
        """Create demo metadata record."""
        metadata = {
            "id": "demo-metadata",
            "client_id": self.client_id,
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_reset": datetime.now(timezone.utc).isoformat(),
            "data_summary": {
                "users_count": len(self.users),
                "converts_count": len(self.converts),
                "services_count": self.services_count,
            },
            "is_demo": True
        }
        
        await self.db.demo_metadata.insert_one(metadata)
        print("✓ Demo metadata created")
        return metadata
        
    async def populate_all(self):
        """Run all population tasks."""
        print("\n" + "="*60)
        print("🚀 EVANGELISM CRM DEMO DATA POPULATION")
        print("="*60)
        
        await self.initialize()
        await self.clear_existing_data()
        
        # Create core data
        await self.create_client()
        await self.create_users()
        
        # Create converts and related data
        await self.create_converts()
        await self.create_services()
        await self.create_convert_lists()
        
        # Create supporting structures
        await self.create_membership_classes()
        await self.create_house_fellowships()
        await self.create_followup_records()
        
        # Create intelligence data
        await self.create_health_scores()
        await self.create_alerts()
        
        # Create automation
        await self.create_workflows()
        await self.create_sequences()
        await self.create_playbooks()
        
        # Create metadata
        await self.create_demo_metadata()
        
        # Print summary
        print("\n" + "="*60)
        print("✅ DEMO POPULATION COMPLETE!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"  • Church: {self.church_name}")
        print(f"  • Admin Email: {DEMO_CONFIG['admin_email']}")
        print(f"  • Admin Password: {DEMO_CONFIG['admin_password']}")
        print(f"  • Users: {len(self.users)}")
        print(f"  • Converts: {len(self.converts)}")
        print(f"  • Services: {self.services_count}")
        print(f"\n🌐 Access the demo at: http://localhost:3000")
        print(f"   Login with the admin credentials above")
        print("="*60)


async def main():
    parser = argparse.ArgumentParser(description="Populate Evangelism CRM demo data")
    parser.add_argument("--converts", type=int, default=500, help="Number of converts to create")
    parser.add_argument("--workers", type=int, default=15, help="Number of workers to create")
    parser.add_argument("--services", type=int, default=20, help="Number of services to create")
    parser.add_argument("--reset", action="store_true", help="Reset existing demo data first")
    
    args = parser.parse_args()
    
    populator = DemoDataPopulator()
    populator.converts_count = args.converts
    populator.workers_count = args.workers
    populator.services_count = args.services
    
    await populator.populate_all()


if __name__ == "__main__":
    asyncio.run(main())
