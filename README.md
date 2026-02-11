# Evangelism CRM - Demo Version

A fully functional demo version of the Evangelism CRM system populated with realistic Nigerian church data. This demo showcases all the features and capabilities of the system without affecting production data.

## 🎯 What's Included

### Demo Church
- **Name**: Grace Evangelical Ministries
- **Location**: Lagos, Nigeria
- **Denomination**: Pentecostal
- **Member Count**: 2,500+

### Demo Data
- ✅ **500+ Converts** with realistic Nigerian names and contact information
- ✅ **15+ Church Workers** with various roles (Admin, Follow-up Leaders, Workers, Mentors, etc.)
- ✅ **20+ Church Services** over the past 6 months
- ✅ **Membership Classes** and House Fellowships
- ✅ **Follow-up Records** and Health Scores
- ✅ **Automated Alerts** for at-risk converts
- ✅ **Workflows, Sequences, and Playbooks**
- ✅ **Analytics and Reporting Data**

### Features Demonstrated

#### 1. Convert Management
- Kanban board view of converts by stage
- Detailed convert profiles with Nigerian demographics
- Source tracking (Services, Outreaches, Referrals)
- Stage progression tracking

#### 2. Health Scoring System
- Automated health scores (0-100) for each convert
- Factors: Attendance, Engagement, Response Time, Spiritual Growth, Social Connection
- At-risk identification

#### 3. Alert System
- Automatic alerts for low engagement
- At-risk member notifications
- Overdue follow-up reminders
- Severity levels (Low, Medium, High)

#### 4. Workflow Automation
- New convert onboarding workflow
- Absent member recovery workflow
- Baptism preparation workflow

#### 5. Sequences
- Welcome series for new converts
- Follow-up reminders for workers

#### 6. Retention Playbooks
- First-time visitor engagement strategy
- At-risk member recovery playbook
- New member integration guide

#### 7. Analytics & Reporting
- Convert statistics by stage
- Service attendance tracking
- Worker performance metrics
- Church growth analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- MongoDB (local or Atlas)
- Node.js 18+ (for frontend)

### 1. Setup Environment

```bash
cd demo

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your MongoDB credentials
# The demo will use database: evangelism_crm_demo
```

### 3. Populate Demo Data

```bash
# Run the population script
python scripts/populate_demo.py

# Or with custom counts
python scripts/populate_demo.py --converts 1000 --workers 20 --services 30
```

### 4. Start Demo Server

```bash
# Start the demo backend server
python backend/demo_server.py
```

The server will start on `http://localhost:8001`

### 5. Connect Frontend

The demo backend runs on port 8001. Update your frontend `.env`:

```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

Then start the frontend from the main project:

```bash
cd ../frontend
npm start
```

## 🔑 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@graceevangelical.demo | Demo@2025 |
| Follow-up Leader | followup_leader1@graceevangelical.demo | Demo@2025 |
| Follow-up Worker | followup_worker1@graceevangelical.demo | Demo@2025 |
| Data Entry | data_entry1@graceevangelical.demo | Demo@2025 |
| Mentor | mentor1@graceevangelical.demo | Demo@2025 |

## 📊 Demo API Endpoints

### Demo Information
- `GET /api/demo/info` - Get demo information
- `GET /api/demo/stats` - Get demo database statistics
- `POST /api/demo/reset` - Reset demo data to initial state

### Standard API
All standard API endpoints are available:
- `/api/auth/*` - Authentication
- `/api/users/*` - User management
- `/api/converts/*` - Convert management
- `/api/services/*` - Service management
- `/api/dashboard/*` - Dashboard data
- `/api/analytics/*` - Analytics and reports
- `/api/health-scores/*` - Health scoring
- `/api/alerts/*` - Alerts management
- `/api/workflows/*` - Workflow automation
- `/api/sequences/*` - Sequence automation
- `/api/playbooks/*` - Retention playbooks

Full API documentation: `http://localhost:8001/docs`

## 🔄 Resetting Demo Data

To reset the demo to its initial state:

```bash
# Method 1: API endpoint
curl -X POST http://localhost:8001/api/demo/reset

# Method 2: Re-run population script
python scripts/populate_demo.py

# Method 3: Direct database reset
python -c "
import asyncio
from backend.demo_database import reset_demo_database
asyncio.run(reset_demo_database())
"
```

## 📁 File Structure

```
demo/
├── backend/
│   ├── demo_database.py      # Demo database utilities
│   └── demo_server.py        # Demo FastAPI server
├── data/
│   └── nigerian_data.py      # Nigerian data generators
├── scripts/
│   └── populate_demo.py      # Data population script
├── docs/
│   └── DEMO_GUIDE.md         # Detailed demo guide
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🌍 Nigerian Data Included

### Names
- **First Names**: 100+ Nigerian first names (Emmanuel, Chioma, Olumide, etc.)
- **Last Names**: 200+ Nigerian surnames (Adeyemi, Okonkwo, Abdullahi, etc.)
- **Realistic Combinations**: Authentic Yoruba, Igbo, Hausa, and general Nigerian names

### Locations
- **36 States + FCT**: All Nigerian states with their LGAs
- **Major Cities**: Lagos, Ibadan, Abuja, Kano, Port Harcourt, etc.
- **Areas**: Specific neighborhoods and districts

### Churches
- **Denominations**: Pentecostal, Anglican, Catholic, Methodist, etc.
- **Real Church Names**: Winners Chapel, RCCG, Deeper Life, Christ Embassy, etc.

### Contact Information
- **Phone Numbers**: Valid Nigerian mobile formats (MTN, Airtel, Glo, 9mobile)
- **Email Addresses**: Realistic Nigerian email patterns
- **Addresses**: Street addresses in major Nigerian cities

## 🎨 Demo Scenarios

### Scenario 1: New Convert Journey
1. New convert "Emmanuel Adeyemi" registered after Sunday service
2. Automatic welcome SMS sent
3. Assigned to follow-up worker "Chioma Okonkwo"
4. Progresses through stages: New → Contacted → In Follow-up → In Classes
5. Health score improves from 30 to 75
6. Joins house fellowship in Ikeja

### Scenario 2: At-Risk Member Alert
1. System identifies "Sarah Ibrahim" hasn't attended in 3 weeks
2. Health score drops to 25
3. High-priority alert created
4. Welfare officer assigned for outreach
5. Follow-up call made, prayer offered
6. Member returns next Sunday

### Scenario 3: Membership Class Progression
1. New converts enrolled in Foundation Class
2. Attendance tracked over 4 weeks
3. Water baptism scheduled
4. Progresses to Discipleship Class
5. Assigned to department (Ushering)
6. Connected to house fellowship

## 📈 Sample Reports Available

### Dashboard Overview
- Total converts: 500+
- New this month: 45
- At-risk: 23
- Awaiting follow-up: 67

### Stage Distribution
- New: 15%
- In Follow-up: 25%
- In Classes: 20%
- In House Fellowship: 15%
- Established: 10%
- Inactive: 10%

### Health Score Summary
- Average: 58/100
- Excellent (80+): 15%
- Good (60-79): 30%
- Fair (40-59): 25%
- At Risk (<40): 30%

## 🔒 Security Notes

- Demo uses separate database (`evangelism_crm_demo`)
- All demo data is tagged with `is_demo: true`
- Default passwords are simple (Demo@2025)
- CORS is permissive for local development
- **DO NOT use in production**

## 🛠️ Customization

### Adding More Converts

```python
# In populate_demo.py, modify the counts
populator.converts_count = 1000  # Increase from 500
populator.workers_count = 25     # Add more workers
```

### Adding Custom Data

Edit `data/nigerian_data.py` to add:
- More names
- Additional locations
- Custom occupations
- Service types

### Changing Church Details

Edit `DEMO_CONFIG` in `data/nigerian_data.py`:

```python
DEMO_CONFIG = {
    "church_name": "Your Church Name",
    "church_location": "Your City, Nigeria",
    # ...
}
```

## 🐛 Troubleshooting

### MongoDB Connection Error
```
Check your MONGO_URL in .env file
Ensure MongoDB is running and accessible
```

### Import Errors
```bash
# Make sure you're in the demo directory
cd demo

# Ensure backend directory is accessible
export PYTHONPATH="${PYTHONPATH}:../backend"
```

### Port Already in Use
```bash
# Change the port in .env
DEMO_PORT=8002
```

## 🤝 Contributing

To add more demo scenarios or improve the data:

1. Edit `data/nigerian_data.py` for data generators
2. Edit `scripts/populate_demo.py` for population logic
3. Test with `python scripts/populate_demo.py`
4. Submit improvements

## 📞 Support

For issues or questions:
- Check the main project documentation
- Review API docs at `/docs`
- Check demo stats at `/api/demo/stats`

---

**Built with ❤️ for Nigerian Churches**
