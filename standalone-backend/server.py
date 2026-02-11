"""
Standalone Demo Server for Evangelism CRM
Complete FastAPI application with all features for demo purposes.
"""

from fastapi import FastAPI, APIRouter, HTTPException, status, Depends, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, date, timezone
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
import os
import sys
import uuid
import bcrypt
import logging
import random
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================================
# DATABASE SETUP (In-Memory for Demo)
# =============================================================================

class DemoDatabase:
    """In-memory database for demo purposes."""
    
    def __init__(self):
        self.clients = {}
        self.users = {}
        self.converts = {}
        self.services = {}
        self.health_scores = {}
        self.alerts = {}
        self.voice_calls = {}
        self.voice_agents = {}
        self.call_scripts = {}
        self.conversations = {}
        self.followup_records = {}
        self.workflows = {}
        self.sequences = {}
        self.playbooks = {}
        self.analytics = {}
        self.membership_classes = {}
        self.house_fellowships = {}
        self.initialized = False
        
    def reset(self):
        """Reset all data."""
        self.__init__()
        
db = DemoDatabase()

# =============================================================================
# MODELS
# =============================================================================

class UserRole(str, Enum):
    MAIN_ADMIN = "main_admin"
    CLIENT_ADMIN = "client_admin"
    DATA_ENTRY = "data_entry"
    FOLLOWUP_LEADER = "followup_leader"
    FOLLOWUP_WORKER = "followup_worker"
    PARTNER = "partner"
    PARTNER_CHURCH_USER = "partner_church_user"
    MENTOR = "mentor"
    COUNSELLING_LEADER = "counselling_leader"
    WELFARE_OFFICER = "welfare_officer"
    READONLY = "readonly"
    VOICE_AGENT = "voice_agent"

class ConvertStage(str, Enum):
    NEW = "new"
    IN_FOLLOWUP = "in_followup"
    IN_CLASSES = "in_classes"
    IN_HOUSE_FELLOWSHIP = "in_house_fellowship"
    ESTABLISHED = "established"
    HANDED_OVER = "handed_over"
    INACTIVE = "inactive"

class ConvertSource(str, Enum):
    SERVICE = "service"
    OUTREACH = "outreach"
    PROGRAMME = "programme"
    PARTNER = "partner"
    REFERRAL = "referral"
    WALK_IN = "walk_in"
    PHONE_INQUIRY = "phone_inquiry"
    OTHER = "other"

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class AlertStatus(str, Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

class VoiceCallStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NO_ANSWER = "no_answer"
    VOICEMAIL = "voicemail"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.FOLLOWUP_WORKER
    phone: Optional[str] = None
    location: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

class ConvertBase(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    occupation: Optional[str] = None
    source: ConvertSource = ConvertSource.SERVICE
    source_date: Optional[date] = None
    stage: ConvertStage = ConvertStage.NEW
    notes: Optional[str] = None
    assigned_worker_id: Optional[str] = None
    health_score: Optional[int] = None

class ConvertCreate(ConvertBase):
    pass

class Convert(ConvertBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[str] = None
    
    class Config:
        from_attributes = True

class HealthScore(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    convert_id: str
    score: int = Field(..., ge=0, le=100)
    factors: Dict[str, int] = Field(default_factory=dict)
    calculated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Alert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    convert_id: str
    type: str
    title: str
    description: str
    severity: AlertSeverity
    status: AlertStatus = AlertStatus.OPEN
    assigned_to: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class VoiceAgentConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Grace Voice Agent"
    language: str = "en-NG"
    voice_type: str = "female"
    greeting_template: str = "Hello, this is {church_name}. Am I speaking with {convert_name}?"
    script_template: str = ""
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class VoiceCall(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    convert_id: str
    agent_id: Optional[str] = None
    status: VoiceCallStatus = VoiceCallStatus.SCHEDULED
    scheduled_time: Optional[datetime] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    recording_url: Optional[str] = None
    transcript: Optional[str] = None
    notes: Optional[str] = None
    outcome: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ConversationMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    call_id: str
    speaker: str  # 'agent' or 'convert'
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sentiment: Optional[str] = None

class ServiceInstance(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    type: str
    date: date
    time: str
    venue: str
    preacher: Optional[str] = None
    theme: Optional[str] = None
    attendance: int = 0
    converts_count: int = 0
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DashboardStats(BaseModel):
    total_converts: int
    new_this_month: int
    at_risk: int
    awaiting_followup: int
    average_health_score: float
    active_workers: int
    upcoming_services: int
    open_alerts: int

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

# =============================================================================
# AUTH UTILITIES
# =============================================================================

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def get_user_by_email(email: str) -> Optional[UserInDB]:
    for user in db.users.values():
        if user["email"] == email:
            return UserInDB(**user)
    return None

def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    user = get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(user_id: str) -> str:
    # Simple token for demo - in production use JWT
    import base64
    import json
    payload = {
        "user_id": user_id,
        "exp": (datetime.now(timezone.utc) + timedelta(days=7)).timestamp()
    }
    return base64.b64encode(json.dumps(payload).encode()).decode()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    import base64
    import json
    try:
        token = credentials.credentials
        payload = json.loads(base64.b64decode(token))
        user_id = payload.get("user_id")
        if user_id and user_id in db.users:
            user_data = db.users[user_id].copy()
            user_data.pop("hashed_password", None)
            return User(**user_data)
    except Exception as e:
        logger.error(f"Token validation error: {e}")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials"
    )

# =============================================================================
# DEMO DATA GENERATORS
# =============================================================================

NIGERIAN_FIRST_NAMES_MALE = [
    "Emmanuel", "Daniel", "Samuel", "David", "John", "Joseph", "Michael", "James",
    "Peter", "Paul", "Stephen", "Matthew", "Andrew", "Chinedu", "Chukwuemeka",
    "Obinna", "Ifeanyi", "Uchenna", "Uzoma", "Kelechi", "Olumide", "Olusegun",
    "Adeola", "Adebayo", "Ademola", "Yakubu", "Yusuf", "Ibrahim", "Bamidele",
    "Ayodele", "Kunle", "Segun", "Gbenga"
]

NIGERIAN_FIRST_NAMES_FEMALE = [
    "Mary", "Sarah", "Elizabeth", "Grace", "Joy", "Peace", "Patience", "Faith",
    "Hope", "Blessing", "Favour", "Chioma", "Chidinma", "Chiamaka", "Ngozi",
    "Nkechi", "Ifeoma", "Oluchi", "Adebimpe", "Adenike", "Aisha", "Fatima",
    "Ayomide", "Kemi", "Funmi", "Bimpe"
]

NIGERIAN_LAST_NAMES = [
    "Adeyemi", "Adeleke", "Adekunle", "Adesanya", "Adewale", "Ogunlesi",
    "Balogun", "Bankole", "Ojo", "Okonkwo", "Okorie", "Okoro", "Nnamdi",
    "Obi", "Eze", "Ezeani", "Ude", "Ugochukwu", "Okeke", "Chukwu",
    "Abdullahi", "Abubakar", "Adamu", "Ahmad", "Aliyu", "Bala",
    "Peters", "Johnson", "Williams"
]

NIGERIAN_STATES = ["Lagos", "Oyo", "Ogun", "Ondo", "Osun", "Ekiti", "Kwara",
                   "Kano", "Kaduna", "Katsina", "Rivers", "Delta", "Edo", "Enugu",
                   "Anambra", "Imo", "Abia", "Akwa Ibom", "Cross River"]

OCCUPATIONS = ["Teacher", "Doctor", "Nurse", "Lawyer", "Engineer", "Banker",
               "Business Owner", "Trader", "Software Developer", "Student",
               "Civil Servant", "Entrepreneur", "Fashion Designer", "Driver"]

def generate_phone() -> str:
    networks = ["0803", "0805", "0806", "0810", "0813", "0814", "0903", "0708"]
    return random.choice(networks) + ''.join([str(random.randint(0, 9)) for _ in range(7)])

def generate_nigerian_person(gender: str = None) -> Dict[str, Any]:
    gender = gender or random.choice(["male", "female"])
    
    if gender == "male":
        first_name = random.choice(NIGERIAN_FIRST_NAMES_MALE)
    else:
        first_name = random.choice(NIGERIAN_FIRST_NAMES_FEMALE)
    
    last_name = random.choice(NIGERIAN_LAST_NAMES)
    state = random.choice(NIGERIAN_STATES)
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "full_name": f"{first_name} {last_name}",
        "gender": gender,
        "phone": generate_phone(),
        "email": f"{first_name.lower()}.{last_name.lower()}{random.randint(1,99)}@gmail.com",
        "state": state,
        "city": f"{state} City",
        "occupation": random.choice(OCCUPATIONS),
    }

def populate_demo_data():
    """Populate the demo database with sample data."""
    if db.initialized:
        return
    
    logger.info("Populating demo data...")
    
    # Create admin user
    admin_password = get_password_hash("Demo@2025")
    admin_id = str(uuid.uuid4())
    db.users[admin_id] = {
        "id": admin_id,
        "name": "Pastor Emmanuel Adeyemi",
        "email": "admin@graceevangelical.demo",
        "username": "admin",
        "role": UserRole.CLIENT_ADMIN.value,
        "phone": generate_phone(),
        "location": "Lagos",
        "is_active": True,
        "hashed_password": admin_password,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    
    # Create additional users
    roles = [UserRole.FOLLOWUP_LEADER, UserRole.FOLLOWUP_WORKER, UserRole.DATA_ENTRY,
             UserRole.MENTOR, UserRole.COUNSELLING_LEADER, UserRole.WELFARE_OFFICER,
             UserRole.VOICE_AGENT]
    
    for i, role in enumerate(roles):
        person = generate_nigerian_person()
        user_id = str(uuid.uuid4())
        db.users[user_id] = {
            "id": user_id,
            "name": person["full_name"],
            "email": f"{role.value}{i+1}@graceevangelical.demo",
            "username": f"{role.value}{i+1}",
            "role": role.value,
            "phone": person["phone"],
            "location": person["city"],
            "is_active": True,
            "hashed_password": get_password_hash("Demo@2025"),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    
    worker_ids = [u["id"] for u in db.users.values() if u["role"] in [
        UserRole.FOLLOWUP_WORKER.value, UserRole.FOLLOWUP_LEADER.value, UserRole.MENTOR.value
    ]]
    
    # Create converts
    stages = list(ConvertStage)
    stage_weights = [0.15, 0.30, 0.20, 0.15, 0.10, 0.05, 0.05]
    
    for i in range(100):  # 100 converts for demo
        person = generate_nigerian_person()
        stage = random.choices(stages, weights=stage_weights)[0]
        days_ago = random.randint(1, 180)
        created_at = datetime.now(timezone.utc) - timedelta(days=days_ago)
        
        convert_id = str(uuid.uuid4())
        health_score = random.randint(20, 95)
        
        db.converts[convert_id] = {
            "id": convert_id,
            "first_name": person["first_name"],
            "last_name": person["last_name"],
            "phone": person["phone"],
            "email": person["email"],
            "gender": person["gender"],
            "city": person["city"],
            "state": person["state"],
            "occupation": person["occupation"],
            "source": random.choice(list(ConvertSource)).value,
            "source_date": (date.today() - timedelta(days=days_ago)).isoformat(),
            "stage": stage.value,
            "assigned_worker_id": random.choice(worker_ids) if worker_ids else None,
            "health_score": health_score,
            "notes": random.choice([
                "Very interested in joining the church",
                "Has questions about baptism",
                "Family challenges, needs prayer support",
                "Enthusiastic about youth programs",
                "Wants to join house fellowship",
                None, None, None  # 50% chance of no notes
            ]),
            "created_at": created_at.isoformat(),
            "updated_at": created_at.isoformat(),
            "created_by": admin_id,
        }
        
        # Create health score record
        db.health_scores[convert_id] = {
            "id": str(uuid.uuid4()),
            "convert_id": convert_id,
            "score": health_score,
            "factors": {
                "attendance_rate": random.randint(0, 100),
                "engagement_level": random.randint(0, 100),
                "response_time": random.randint(0, 100),
                "spiritual_growth": random.randint(0, 100),
                "social_connection": random.randint(0, 100),
            },
            "calculated_at": datetime.now(timezone.utc).isoformat(),
        }
        
        # Create alerts for low health scores
        if health_score < 40:
            alert_id = str(uuid.uuid4())
            db.alerts[alert_id] = {
                "id": alert_id,
                "convert_id": convert_id,
                "type": "low_engagement",
                "title": "Low Engagement Alert",
                "description": f"{person['full_name']} has a low health score of {health_score}",
                "severity": AlertSeverity.HIGH.value if health_score < 25 else AlertSeverity.MEDIUM.value,
                "status": AlertStatus.OPEN.value,
                "assigned_to": random.choice(worker_ids) if worker_ids else None,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
    
    # Create services
    for i in range(20):
        service_date = date.today() - timedelta(days=random.randint(1, 120))
        service_id = str(uuid.uuid4())
        db.services[service_id] = {
            "id": service_id,
            "title": f"Sunday Worship Service - {service_date.strftime('%B %d, %Y')}",
            "type": random.choice(["Sunday Service", "Midweek Service", "Prayer Meeting", "Special Program"]),
            "date": service_date.isoformat(),
            "time": random.choice(["08:00", "09:00", "10:00", "18:00"]),
            "venue": random.choice(["Main Sanctuary", "Youth Hall", "Fellowship Hall"]),
            "preacher": random.choice([u["name"] for u in db.users.values()]),
            "theme": random.choice([
                "Faith That Moves Mountains",
                "Walking in Divine Health",
                "The Power of Thanksgiving",
                "Breaking Generational Curses"
            ]),
            "attendance": random.randint(150, 500),
            "converts_count": random.randint(5, 25),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    
    # Create voice agent config
    agent_id = str(uuid.uuid4())
    db.voice_agents[agent_id] = {
        "id": agent_id,
        "name": "Grace Voice Agent",
        "language": "en-NG",
        "voice_type": "female",
        "greeting_template": "Hello, this is Grace Evangelical Ministries. Am I speaking with {convert_name}?",
        "script_template": """I'm calling to follow up on your recent visit to our church. 
We wanted to know how you're doing and if you have any prayer requests. 
We also wanted to invite you to our upcoming service this Sunday at 10 AM.""",
        "is_active": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    
    # Create sample call scripts
    scripts = [
        {
            "name": "Welcome Call",
            "content": "Hello {name}, welcome to Grace Evangelical! We're thrilled you joined us. How can we support your spiritual journey?",
            "purpose": "welcome"
        },
        {
            "name": "Follow-up Call",
            "content": "Hi {name}, this is {caller_name} from Grace Evangelical. Just checking in on you. Do you have any prayer requests?",
            "purpose": "followup"
        },
        {
            "name": "Service Invitation",
            "content": "Hello {name}, we'd love to invite you to our special service this Sunday. Pastor will be teaching on faith and miracles.",
            "purpose": "invitation"
        },
        {
            "name": "Welfare Check",
            "content": "Hi {name}, we noticed you haven't been around for a while. Is everything okay? We're here to support you.",
            "purpose": "welfare"
        }
    ]
    
    for script in scripts:
        script_id = str(uuid.uuid4())
        db.call_scripts[script_id] = {
            "id": script_id,
            "name": script["name"],
            "content": script["content"],
            "purpose": script["purpose"],
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    
    # Create some sample voice calls
    for i in range(15):
        convert = random.choice(list(db.converts.values()))
        call_id = str(uuid.uuid4())
        scheduled_time = datetime.now(timezone.utc) + timedelta(hours=random.randint(-48, 48))
        
        status = random.choice(list(VoiceCallStatus))
        started_at = None
        ended_at = None
        duration = None
        transcript = None
        
        if status in [VoiceCallStatus.COMPLETED, VoiceCallStatus.VOICEMAIL]:
            started_at = scheduled_time
            ended_at = started_at + timedelta(minutes=random.randint(2, 15))
            duration = int((ended_at - started_at).total_seconds())
            transcript = f"[AI Generated] Call with {convert['first_name']}. They expressed interest in attending next Sunday service."
        
        db.voice_calls[call_id] = {
            "id": call_id,
            "convert_id": convert["id"],
            "agent_id": agent_id,
            "status": status.value,
            "scheduled_time": scheduled_time.isoformat(),
            "started_at": started_at.isoformat() if started_at else None,
            "ended_at": ended_at.isoformat() if ended_at else None,
            "duration_seconds": duration,
            "transcript": transcript,
            "notes": random.choice(["Great conversation", "Left voicemail", "No answer", "Will call back", None]),
            "outcome": random.choice(["interested", "callback_requested", "not_interested", "voicemail", None]),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        
        # Add conversation messages for completed calls
        if status == VoiceCallStatus.COMPLETED:
            messages = [
                {"speaker": "agent", "message": f"Hello, may I speak with {convert['first_name']}?"},
                {"speaker": "convert", "message": "Yes, this is me."},
                {"speaker": "agent", "message": "This is Grace Evangelical calling. How are you doing today?"},
                {"speaker": "convert", "message": "I'm fine, thank you for calling."},
                {"speaker": "agent", "message": "We'd love to see you at our service this Sunday."},
                {"speaker": "convert", "message": "I'll try to make it. Thank you!"},
            ]
            for msg in messages:
                msg_id = str(uuid.uuid4())
                db.conversations[msg_id] = {
                    "id": msg_id,
                    "call_id": call_id,
                    "speaker": msg["speaker"],
                    "message": msg["message"],
                    "timestamp": (started_at + timedelta(seconds=random.randint(10, 300))).isoformat(),
                    "sentiment": random.choice(["positive", "neutral", "positive"]),
                }
    
    db.initialized = True
    logger.info(f"Demo data populated: {len(db.users)} users, {len(db.converts)} converts, {len(db.voice_calls)} voice calls")

# =============================================================================
# LIFESPAN
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Evangelism CRM Standalone Demo Server...")
    populate_demo_data()
    yield
    logger.info("Shutting down...")

# =============================================================================
# CREATE APP
# =============================================================================

app = FastAPI(
    title="Evangelism CRM - Standalone Demo",
    description="Complete standalone demo with Voice Agent feature",
    version="2.0.0-demo-standalone",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# ROUTERS
# =============================================================================

api_router = APIRouter(prefix="/api")

# -----------------------------------------------------------------------------
# AUTH ROUTES
# -----------------------------------------------------------------------------

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    user = authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    token = create_access_token(user.id)
    user_dict = user.model_dump()
    user_dict.pop("hashed_password", None)
    
    return TokenResponse(
        access_token=token,
        user=user_dict
    )

@api_router.get("/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# -----------------------------------------------------------------------------
# USER ROUTES
# -----------------------------------------------------------------------------

@api_router.get("/users", response_model=List[User])
async def list_users(current_user: User = Depends(get_current_user)):
    users = []
    for user_data in db.users.values():
        user_copy = user_data.copy()
        user_copy.pop("hashed_password", None)
        users.append(User(**user_copy))
    return users

@api_router.get("/users/{user_id}")
async def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    if user_id not in db.users:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = db.users[user_id].copy()
    user_data.pop("hashed_password", None)
    return user_data

# -----------------------------------------------------------------------------
# CONVERT ROUTES
# -----------------------------------------------------------------------------

@api_router.get("/converts")
async def list_converts(
    stage: Optional[str] = None,
    search: Optional[str] = None,
    assigned_to: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    converts = list(db.converts.values())
    
    if stage:
        converts = [c for c in converts if c["stage"] == stage]
    
    if assigned_to:
        converts = [c for c in converts if c["assigned_worker_id"] == assigned_to]
    
    if search:
        search_lower = search.lower()
        converts = [
            c for c in converts 
            if search_lower in c["first_name"].lower() 
            or search_lower in c["last_name"].lower()
            or (c.get("phone") and search_lower in c["phone"])
        ]
    
    return converts

@api_router.get("/converts/{convert_id}")
async def get_convert(convert_id: str, current_user: User = Depends(get_current_user)):
    if convert_id not in db.converts:
        raise HTTPException(status_code=404, detail="Convert not found")
    return db.converts[convert_id]

@api_router.post("/converts", status_code=201)
async def create_convert(
    data: ConvertCreate,
    current_user: User = Depends(get_current_user)
):
    convert_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    convert_data = data.model_dump()
    convert_data["id"] = convert_id
    convert_data["created_at"] = now
    convert_data["updated_at"] = now
    convert_data["created_by"] = current_user.id
    
    # Calculate initial health score
    health_score = random.randint(30, 50)
    convert_data["health_score"] = health_score
    
    db.converts[convert_id] = convert_data
    
    # Create health score record
    db.health_scores[convert_id] = {
        "id": str(uuid.uuid4()),
        "convert_id": convert_id,
        "score": health_score,
        "factors": {
            "attendance_rate": random.randint(20, 40),
            "engagement_level": random.randint(30, 50),
            "response_time": random.randint(40, 60),
            "spiritual_growth": random.randint(20, 40),
            "social_connection": random.randint(10, 30),
        },
        "calculated_at": now,
    }
    
    return convert_data

@api_router.patch("/converts/{convert_id}")
async def update_convert(
    convert_id: str,
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    if convert_id not in db.converts:
        raise HTTPException(status_code=404, detail="Convert not found")
    
    db.converts[convert_id].update(data)
    db.converts[convert_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
    return db.converts[convert_id]

@api_router.delete("/converts/{convert_id}", status_code=204)
async def delete_convert(convert_id: str, current_user: User = Depends(get_current_user)):
    if convert_id in db.converts:
        del db.converts[convert_id]
    return None

# -----------------------------------------------------------------------------
# DASHBOARD ROUTES
# -----------------------------------------------------------------------------

@api_router.get("/dashboard/stats")
async def get_dashboard_stats(current_user: User = Depends(get_current_user)):
    total_converts = len(db.converts)
    
    # New this month
    month_ago = datetime.now(timezone.utc) - timedelta(days=30)
    new_this_month = len([
        c for c in db.converts.values()
        if datetime.fromisoformat(c["created_at"]) > month_ago
    ])
    
    # At risk (health score < 40)
    at_risk = len([c for c in db.converts.values() if c.get("health_score", 100) < 40])
    
    # Awaiting followup (in NEW stage)
    awaiting_followup = len([c for c in db.converts.values() if c["stage"] == "new"])
    
    # Average health score
    health_scores = [c.get("health_score", 0) for c in db.converts.values()]
    avg_health = sum(health_scores) / len(health_scores) if health_scores else 0
    
    # Active workers
    active_workers = len([u for u in db.users.values() if u["is_active"]])
    
    # Upcoming services
    upcoming_services = len([
        s for s in db.services.values()
        if datetime.fromisoformat(s["created_at"]) > month_ago
    ])
    
    # Open alerts
    open_alerts = len([
        a for a in db.alerts.values()
        if a["status"] in ["open", "acknowledged"]
    ])
    
    return {
        "total_converts": total_converts,
        "new_this_month": new_this_month,
        "at_risk": at_risk,
        "awaiting_followup": awaiting_followup,
        "average_health_score": round(avg_health, 1),
        "active_workers": active_workers,
        "upcoming_services": upcoming_services,
        "open_alerts": open_alerts,
    }

@api_router.get("/dashboard/stage-distribution")
async def get_stage_distribution(current_user: User = Depends(get_current_user)):
    distribution = {}
    for stage in ConvertStage:
        count = len([c for c in db.converts.values() if c["stage"] == stage.value])
        distribution[stage.value] = count
    return distribution

@api_router.get("/dashboard/recent-activity")
async def get_recent_activity(current_user: User = Depends(get_current_user)):
    # Combine recent converts, calls, and alerts
    activities = []
    
    # Recent converts
    for c in list(db.converts.values())[:5]:
        activities.append({
            "type": "convert_created",
            "message": f"New convert: {c['first_name']} {c['last_name']}",
            "timestamp": c["created_at"],
        })
    
    # Recent calls
    for call in sorted(db.voice_calls.values(), key=lambda x: x["created_at"], reverse=True)[:5]:
        convert = db.converts.get(call["convert_id"], {})
        activities.append({
            "type": "voice_call",
            "message": f"Voice call with {convert.get('first_name', 'Unknown')} - {call['status']}",
            "timestamp": call["created_at"],
        })
    
    # Sort by timestamp
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    return activities[:10]

# -----------------------------------------------------------------------------
# HEALTH SCORE ROUTES
# -----------------------------------------------------------------------------

@api_router.get("/health-scores")
async def list_health_scores(current_user: User = Depends(get_current_user)):
    return list(db.health_scores.values())

@api_router.get("/health-scores/{convert_id}")
async def get_convert_health_score(
    convert_id: str,
    current_user: User = Depends(get_current_user)
):
    if convert_id not in db.health_scores:
        raise HTTPException(status_code=404, detail="Health score not found")
    return db.health_scores[convert_id]

@api_router.post("/health-scores/{convert_id}/recalculate")
async def recalculate_health_score(
    convert_id: str,
    current_user: User = Depends(get_current_user)
):
    if convert_id not in db.converts:
        raise HTTPException(status_code=404, detail="Convert not found")
    
    # Simulate recalculation
    new_score = random.randint(30, 95)
    db.health_scores[convert_id] = {
        "id": str(uuid.uuid4()),
        "convert_id": convert_id,
        "score": new_score,
        "factors": {
            "attendance_rate": random.randint(0, 100),
            "engagement_level": random.randint(0, 100),
            "response_time": random.randint(0, 100),
            "spiritual_growth": random.randint(0, 100),
            "social_connection": random.randint(0, 100),
        },
        "calculated_at": datetime.now(timezone.utc).isoformat(),
    }
    
    # Update convert
    db.converts[convert_id]["health_score"] = new_score
    db.converts[convert_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    return db.health_scores[convert_id]

# -----------------------------------------------------------------------------
# ALERT ROUTES
# -----------------------------------------------------------------------------

@api_router.get("/alerts")
async def list_alerts(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    alerts = list(db.alerts.values())
    
    if status:
        alerts = [a for a in alerts if a["status"] == status]
    
    if severity:
        alerts = [a for a in alerts if a["severity"] == severity]
    
    # Add convert info
    for alert in alerts:
        convert = db.converts.get(alert["convert_id"], {})
        alert["convert_name"] = f"{convert.get('first_name', '')} {convert.get('last_name', '')}"
        alert["convert_phone"] = convert.get("phone")
    
    return alerts

@api_router.get("/alerts/{alert_id}")
async def get_alert(alert_id: str, current_user: User = Depends(get_current_user)):
    if alert_id not in db.alerts:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert = db.alerts[alert_id].copy()
    convert = db.converts.get(alert["convert_id"], {})
    alert["convert"] = convert
    return alert

@api_router.patch("/alerts/{alert_id}")
async def update_alert(
    alert_id: str,
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    if alert_id not in db.alerts:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db.alerts[alert_id].update(data)
    db.alerts[alert_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
    return db.alerts[alert_id]

# -----------------------------------------------------------------------------
# VOICE AGENT ROUTES
# -----------------------------------------------------------------------------

@api_router.get("/voice-agent/config")
async def get_voice_agent_config(current_user: User = Depends(get_current_user)):
    """Get the voice agent configuration."""
    if not db.voice_agents:
        return {
            "id": str(uuid.uuid4()),
            "name": "Grace Voice Agent",
            "language": "en-NG",
            "voice_type": "female",
            "greeting_template": "Hello, this is Grace Evangelical Ministries. Am I speaking with {convert_name}?",
            "is_active": True,
        }
    return list(db.voice_agents.values())[0]

@api_router.put("/voice-agent/config")
async def update_voice_agent_config(
    config: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Update voice agent configuration."""
    if db.voice_agents:
        agent_id = list(db.voice_agents.keys())[0]
        db.voice_agents[agent_id].update(config)
        db.voice_agents[agent_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
        return db.voice_agents[agent_id]
    else:
        agent_id = str(uuid.uuid4())
        config["id"] = agent_id
        config["created_at"] = datetime.now(timezone.utc).isoformat()
        db.voice_agents[agent_id] = config
        return config

@api_router.get("/voice-agent/scripts")
async def list_call_scripts(current_user: User = Depends(get_current_user)):
    """List all call scripts."""
    return list(db.call_scripts.values())

@api_router.post("/voice-agent/scripts", status_code=201)
async def create_call_script(
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Create a new call script."""
    script_id = str(uuid.uuid4())
    script = {
        "id": script_id,
        "name": data.get("name"),
        "content": data.get("content"),
        "purpose": data.get("purpose", "general"),
        "is_active": data.get("is_active", True),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    db.call_scripts[script_id] = script
    return script

@api_router.put("/voice-agent/scripts/{script_id}")
async def update_call_script(
    script_id: str,
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Update a call script."""
    if script_id not in db.call_scripts:
        raise HTTPException(status_code=404, detail="Script not found")
    
    db.call_scripts[script_id].update(data)
    db.call_scripts[script_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
    return db.call_scripts[script_id]

@api_router.delete("/voice-agent/scripts/{script_id}", status_code=204)
async def delete_call_script(
    script_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a call script."""
    if script_id in db.call_scripts:
        del db.call_scripts[script_id]
    return None

@api_router.get("/voice-agent/calls")
async def list_voice_calls(
    status: Optional[str] = None,
    convert_id: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """List all voice calls with optional filtering."""
    calls = list(db.voice_calls.values())
    
    if status:
        calls = [c for c in calls if c["status"] == status]
    
    if convert_id:
        calls = [c for c in calls if c["convert_id"] == convert_id]
    
    # Add convert info
    for call in calls:
        convert = db.converts.get(call["convert_id"], {})
        call["convert_name"] = f"{convert.get('first_name', '')} {convert.get('last_name', '')}"
        call["convert_phone"] = convert.get("phone")
    
    return calls

@api_router.get("/voice-agent/calls/{call_id}")
async def get_voice_call(
    call_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get details of a specific voice call."""
    if call_id not in db.voice_calls:
        raise HTTPException(status_code=404, detail="Call not found")
    
    call = db.voice_calls[call_id].copy()
    convert = db.converts.get(call["convert_id"], {})
    call["convert"] = convert
    
    # Get conversation
    conversation = [
        msg for msg in db.conversations.values() if msg["call_id"] == call_id
    ]
    conversation.sort(key=lambda x: x["timestamp"])
    call["conversation"] = conversation
    
    return call

@api_router.post("/voice-agent/calls", status_code=201)
async def schedule_voice_call(
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Schedule a new voice call."""
    call_id = str(uuid.uuid4())
    
    # Get agent
    agent_id = list(db.voice_agents.keys())[0] if db.voice_agents else None
    
    call = {
        "id": call_id,
        "convert_id": data.get("convert_id"),
        "agent_id": agent_id,
        "status": VoiceCallStatus.SCHEDULED.value,
        "scheduled_time": data.get("scheduled_time"),
        "script_id": data.get("script_id"),
        "notes": data.get("notes"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    
    db.voice_calls[call_id] = call
    
    # Add convert info to response
    convert = db.converts.get(call["convert_id"], {})
    call["convert_name"] = f"{convert.get('first_name', '')} {convert.get('last_name', '')}"
    call["convert_phone"] = convert.get("phone")
    
    return call

@api_router.post("/voice-agent/calls/{call_id}/start")
async def start_voice_call(
    call_id: str,
    current_user: User = Depends(get_current_user)
):
    """Mark a voice call as started."""
    if call_id not in db.voice_calls:
        raise HTTPException(status_code=404, detail="Call not found")
    
    db.voice_calls[call_id]["status"] = VoiceCallStatus.IN_PROGRESS.value
    db.voice_calls[call_id]["started_at"] = datetime.now(timezone.utc).isoformat()
    db.voice_calls[call_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    return db.voice_calls[call_id]

@api_router.post("/voice-agent/calls/{call_id}/complete")
async def complete_voice_call(
    call_id: str,
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Mark a voice call as completed."""
    if call_id not in db.voice_calls:
        raise HTTPException(status_code=404, detail="Call not found")
    
    started_at = datetime.fromisoformat(db.voice_calls[call_id]["started_at"])
    ended_at = datetime.now(timezone.utc)
    duration = int((ended_at - started_at).total_seconds())
    
    db.voice_calls[call_id].update({
        "status": VoiceCallStatus.COMPLETED.value,
        "ended_at": ended_at.isoformat(),
        "duration_seconds": duration,
        "transcript": data.get("transcript"),
        "notes": data.get("notes"),
        "outcome": data.get("outcome"),
        "updated_at": ended_at.isoformat(),
    })
    
    # Update convert stage if interested
    if data.get("outcome") == "interested":
        convert_id = db.voice_calls[call_id]["convert_id"]
        if convert_id in db.converts:
            db.converts[convert_id]["stage"] = ConvertStage.IN_FOLLOWUP.value
            db.converts[convert_id]["updated_at"] = ended_at.isoformat()
    
    return db.voice_calls[call_id]

@api_router.post("/voice-agent/calls/{call_id}/simulate")
async def simulate_voice_call(
    call_id: str,
    current_user: User = Depends(get_current_user)
):
    """Simulate a complete voice call (for demo purposes)."""
    if call_id not in db.voice_calls:
        raise HTTPException(status_code=404, detail="Call not found")
    
    call = db.voice_calls[call_id]
    convert = db.converts.get(call["convert_id"], {})
    
    # Simulate call duration (2-10 minutes)
    duration = random.randint(120, 600)
    now = datetime.now(timezone.utc)
    started_at = now - timedelta(seconds=duration)
    
    # Simulate conversation
    conversation = [
        {"speaker": "agent", "message": f"Hello, may I speak with {convert.get('first_name', 'there')}?", "delay": 2},
        {"speaker": "convert", "message": "Yes, speaking. Who is this?", "delay": 3},
        {"speaker": "agent", "message": "This is Grace Evangelical Ministries. We wanted to check on you and invite you to our service this Sunday.", "delay": 8},
        {"speaker": "convert", "message": "Oh, thank you for calling! I've been meaning to come back.", "delay": 5},
        {"speaker": "agent", "message": "That's wonderful! We have a special program this Sunday at 10 AM. Would you be able to make it?", "delay": 7},
        {"speaker": "convert", "message": "Yes, I'll definitely be there. Thank you for the reminder!", "delay": 4},
        {"speaker": "agent", "message": "Great! We look forward to seeing you. Have a blessed day!", "delay": 4},
        {"speaker": "convert", "message": "You too. Bye!", "delay": 2},
    ]
    
    # Save conversation
    current_time = started_at
    for msg in conversation:
        current_time += timedelta(seconds=msg["delay"])
        msg_id = str(uuid.uuid4())
        db.conversations[msg_id] = {
            "id": msg_id,
            "call_id": call_id,
            "speaker": msg["speaker"],
            "message": msg["message"],
            "timestamp": current_time.isoformat(),
            "sentiment": "positive" if msg["speaker"] == "convert" else None,
        }
    
    # Update call
    transcript = " ".join([msg["message"] for msg in conversation])
    db.voice_calls[call_id].update({
        "status": VoiceCallStatus.COMPLETED.value,
        "started_at": started_at.isoformat(),
        "ended_at": now.isoformat(),
        "duration_seconds": duration,
        "transcript": transcript,
        "outcome": "interested",
        "notes": "Convert expressed interest in attending Sunday service",
        "updated_at": now.isoformat(),
    })
    
    # Update convert stage
    if call["convert_id"] in db.converts:
        db.converts[call["convert_id"]]["stage"] = ConvertStage.IN_FOLLOWUP.value
        db.converts[call["convert_id"]]["updated_at"] = now.isoformat()
    
    return {
        "call": db.voice_calls[call_id],
        "conversation": conversation,
        "summary": {
            "duration_minutes": round(duration / 60, 1),
            "outcome": "interested",
            "sentiment": "positive",
        }
    }

@api_router.post("/voice-agent/make-call")
async def make_voice_call(
    data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Initiate an immediate voice call to a convert."""
    convert_id = data.get("convert_id")
    if convert_id not in db.converts:
        raise HTTPException(status_code=404, detail="Convert not found")
    
    convert = db.converts[convert_id]
    
    # Create call record
    call_id = str(uuid.uuid4())
    agent_id = list(db.voice_agents.keys())[0] if db.voice_agents else None
    
    now = datetime.now(timezone.utc)
    
    call = {
        "id": call_id,
        "convert_id": convert_id,
        "agent_id": agent_id,
        "status": VoiceCallStatus.SCHEDULED.value,
        "scheduled_time": now.isoformat(),
        "script_id": data.get("script_id"),
        "notes": data.get("notes"),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
    }
    
    db.voice_calls[call_id] = call
    
    # Simulate the call in background
    background_tasks.add_task(simulate_call_async, call_id)
    
    return {
        "message": "Voice call initiated",
        "call_id": call_id,
        "convert_name": f"{convert['first_name']} {convert['last_name']}",
        "phone": convert["phone"],
        "status": "scheduled",
    }

async def simulate_call_async(call_id: str):
    """Simulate a call asynchronously."""
    import asyncio
    
    # Wait a moment then mark as completed
    await asyncio.sleep(5)
    
    if call_id in db.voice_calls:
        call = db.voice_calls[call_id]
        convert = db.converts.get(call["convert_id"], {})
        
        now = datetime.now(timezone.utc)
        duration = random.randint(120, 600)
        
        db.voice_calls[call_id].update({
            "status": VoiceCallStatus.COMPLETED.value,
            "started_at": (now - timedelta(seconds=duration)).isoformat(),
            "ended_at": now.isoformat(),
            "duration_seconds": duration,
            "transcript": f"Simulated call with {convert.get('first_name', 'convert')}. Positive response received.",
            "outcome": "interested",
            "updated_at": now.isoformat(),
        })
        
        logger.info(f"Voice call {call_id} completed")

# -----------------------------------------------------------------------------
# ANALYTICS ROUTES
# -----------------------------------------------------------------------------

@api_router.get("/analytics/converts")
async def get_convert_analytics(current_user: User = Depends(get_current_user)):
    """Get convert analytics."""
    converts = list(db.converts.values())
    
    # Stage distribution
    stage_dist = {}
    for stage in ConvertStage:
        stage_dist[stage.value] = len([c for c in converts if c["stage"] == stage.value])
    
    # Source distribution
    source_dist = {}
    for source in ConvertSource:
        source_dist[source.value] = len([c for c in converts if c["source"] == source.value])
    
    # Monthly trend (simulate)
    monthly = {}
    for i in range(6):
        month_key = (datetime.now(timezone.utc) - timedelta(days=30*i)).strftime("%Y-%m")
        monthly[month_key] = random.randint(10, 50)
    
    # Health score distribution
    health_dist = {"excellent": 0, "good": 0, "fair": 0, "poor": 0}
    for c in converts:
        score = c.get("health_score", 50)
        if score >= 80:
            health_dist["excellent"] += 1
        elif score >= 60:
            health_dist["good"] += 1
        elif score >= 40:
            health_dist["fair"] += 1
        else:
            health_dist["poor"] += 1
    
    return {
        "total": len(converts),
        "by_stage": stage_dist,
        "by_source": source_dist,
        "monthly_trend": monthly,
        "health_distribution": health_dist,
    }

@api_router.get("/analytics/voice-calls")
async def get_voice_call_analytics(current_user: User = Depends(get_current_user)):
    """Get voice call analytics."""
    calls = list(db.voice_calls.values())
    
    total_calls = len(calls)
    completed = len([c for c in calls if c["status"] == "completed"])
    failed = len([c for c in calls if c["status"] == "failed"])
    no_answer = len([c for c in calls if c["status"] == "no_answer"])
    
    avg_duration = 0
    durations = [c.get("duration_seconds", 0) for c in calls if c.get("duration_seconds")]
    if durations:
        avg_duration = sum(durations) / len(durations)
    
    outcomes = {}
    for call in calls:
        outcome = call.get("outcome", "unknown")
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
    
    return {
        "total_calls": total_calls,
        "completed": completed,
        "failed": failed,
        "no_answer": no_answer,
        "average_duration_seconds": round(avg_duration, 1),
        "outcomes": outcomes,
        "success_rate": round((completed / total_calls * 100), 1) if total_calls > 0 else 0,
    }

# -----------------------------------------------------------------------------
# DEMO INFO ROUTES
# -----------------------------------------------------------------------------

@api_router.get("/demo/info")
async def demo_info():
    """Get demo information."""
    return {
        "name": "Evangelism CRM - Standalone Demo",
        "version": "2.0.0",
        "church": "Grace Evangelical Ministries",
        "location": "Lagos, Nigeria",
        "description": "Complete standalone demo with Voice Agent feature",
        "features": [
            "Convert Management",
            "Health Scoring",
            "Alert System",
            "Voice Agent with AI Calling",
            "Call Scripts",
            "Dashboard & Analytics",
            "Follow-up Tracking",
            "Workflow Automation"
        ],
        "credentials": {
            "admin_email": "admin@graceevangelical.demo",
            "admin_password": "Demo@2025"
        }
    }

@api_router.get("/demo/stats")
async def demo_stats():
    """Get demo database statistics."""
    return {
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "users": len(db.users),
            "converts": len(db.converts),
            "services": len(db.services),
            "health_scores": len(db.health_scores),
            "alerts": len(db.alerts),
            "voice_calls": len(db.voice_calls),
            "voice_agents": len(db.voice_agents),
            "call_scripts": len(db.call_scripts),
        }
    }

@api_router.post("/demo/reset")
async def reset_demo():
    """Reset demo data."""
    db.reset()
    populate_demo_data()
    return {
        "status": "success",
        "message": "Demo data reset successfully",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# -----------------------------------------------------------------------------
# HEALTH CHECK
# -----------------------------------------------------------------------------

@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mode": "standalone-demo",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@api_router.get("/")
async def root():
    return {
        "message": "Evangelism CRM - Standalone Demo API",
        "version": "2.0.0",
        "docs": "/docs",
        "demo_info": "/api/demo/info"
    }

# Include router
app.include_router(api_router)

# Static files - serve frontend for non-API routes (monolithic deployment)
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import pathlib

# Try to serve static index.html for root and non-API paths
@app.get("/", response_class=HTMLResponse)
async def serve_root():
    """Serve the frontend index.html for root path."""
    # Look for index.html in various locations
    possible_paths = [
        pathlib.Path(__file__).parent.parent / "standalone-frontend" / "index.html",
        pathlib.Path(__file__).parent / "standalone-frontend" / "index.html",
        pathlib.Path("standalone-frontend") / "index.html",
        pathlib.Path("index.html"),
    ]
    
    for path in possible_paths:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
    
    # Fallback: return simple message if index.html not found
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Evangelism CRM Demo</title>
        <style>
            body { font-family: system-ui; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #f5f5f5; }
            .card { background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; max-width: 400px; }
            h1 { color: #d97706; margin-bottom: 1rem; }
            p { color: #666; margin-bottom: 1.5rem; }
            .btn { background: #d97706; color: white; padding: 0.75rem 1.5rem; border-radius: 0.5rem; text-decoration: none; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Evangelism CRM Demo</h1>
            <p>Frontend not found. API is running correctly.</p>
            <a href="/api/demo/info" class="btn">View API Info</a>
        </div>
    </body>
    </html>
    """)

# Catch-all for other non-API routes (SPA support)
@app.get("/{path:path}", response_class=HTMLResponse)
async def serve_spa(path: str):
    """Serve the frontend for any non-API, non-static path (SPA routing)."""
    # Skip API routes and static files
    if path.startswith("api/") or "." in path:
        raise HTTPException(status_code=404, detail="Not found")
    
    # Serve index.html for all other routes
    return await serve_root()

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    
    print("\n" + "="*60)
    print("EVANGELISM CRM - STANDALONE DEMO SERVER")
    print("="*60)
    print(f"\nAPI Server: http://localhost:{port}")
    print(f"API Docs:   http://localhost:{port}/docs")
    print(f"Demo Info: http://localhost:{port}/api/demo/info")
    print("\nLogin Credentials:")
    print("   Email: admin@graceevangelical.demo")
    print("   Password: Demo@2025")
    print("\nVoice Agent feature enabled!")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
