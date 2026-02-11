# Evangelism CRM Demo - Comprehensive Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Demo Architecture](#demo-architecture)
3. [Data Model](#data-model)
4. [Features Walkthrough](#features-walkthrough)
5. [API Reference](#api-reference)
6. [Customization](#customization)

---

## Introduction

This demo provides a fully functional instance of the Evangelism CRM system with realistic Nigerian church data. It's designed to:

- **Showcase Features**: Demonstrate all CRM capabilities
- **Training**: Train church staff on system usage
- **Sales Demos**: Present to potential church clients
- **Development**: Test features with realistic data

### Demo Church Profile

**Grace Evangelical Ministries**
- 📍 15 Church Street, Ikeja, Lagos
- 📞 +234 801 234 5678
- 📧 info@graceevangelical.ng
- 🌐 https://graceevangelical.ng
- 👥 2,500+ Members
- 📅 Founded: 2005
- ⛪ Denomination: Pentecostal

### Service Schedule
- Sunday: 8:00 AM, 10:00 AM, 12:00 PM
- Wednesday: 6:00 PM
- Friday: 6:30 PM

---

## Demo Architecture

### Database Design

```
Main Database: evangelism_crm
Demo Database: evangelism_crm_demo (auto-created)
```

The demo uses a separate database to ensure complete isolation from production data.

### Data Flow

```
┌─────────────────┐
│   Demo Script   │
│  (populate.py)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Nigerian Data   │
│   Generators    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  Demo Database  │◄────│   Demo Server   │
│ (MongoDB)       │     │   (FastAPI)     │
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                          ┌─────────────────┐
                          │    Frontend     │
                          │    (React)      │
                          └─────────────────┘
```

---

## Data Model

### Core Entities

#### 1. Converts (Contacts)
```json
{
  "id": "uuid",
  "first_name": "Emmanuel",
  "last_name": "Adeyemi",
  "phone": "08031234567",
  "email": "emmanuel.adeyemi@gmail.com",
  "gender": "male",
  "city": "Lagos",
  "state": "Lagos",
  "occupation": "Software Developer",
  "source": "service",
  "stage": "in_followup",
  "health_score": 72,
  "assigned_worker_id": "uuid",
  "created_at": "2025-01-15T10:30:00Z"
}
```

#### 2. Users (Workers)
```json
{
  "id": "uuid",
  "name": "Pastor Chioma Okonkwo",
  "email": "chioma.okonkwo@graceevangelical.demo",
  "role": "followup_leader",
  "phone": "08098765432",
  "location": "Lagos",
  "is_active": true
}
```

#### 3. Services
```json
{
  "id": "uuid",
  "title": "Sunday Worship Service - January 12, 2025",
  "type": "Sunday Service",
  "date": "2025-01-12",
  "time": "10:00",
  "attendance": 450,
  "converts_count": 23,
  "theme": "Faith That Moves Mountains",
  "preacher": "Rev. Dr. Emmanuel Adeyemi"
}
```

#### 4. Health Scores
```json
{
  "convert_id": "uuid",
  "score": 72,
  "factors": {
    "attendance_rate": 85,
    "engagement_level": 70,
    "response_time": 65,
    "spiritual_growth": 75,
    "social_connection": 80
  }
}
```

### Relationships

```
Client (Church)
    ├── Users (Workers)
    ├── Converts
    │   ├── Health Scores
    │   ├── Follow-up Records
    │   ├── Alerts
    │   └── Convert Lists
    ├── Services
    ├── House Fellowships
    ├── Membership Classes
    ├── Workflows
    ├── Sequences
    └── Playbooks
```

---

## Features Walkthrough

### 1. Dashboard Overview

**URL**: `http://localhost:3000/dashboard`

**Key Metrics Displayed**:
- Total Converts: 500+
- New This Month: 45
- Awaiting Follow-up: 67
- At-Risk Converts: 23
- Average Health Score: 58/100

**Charts**:
- Converts by Stage (Pie Chart)
- Health Score Distribution (Bar Chart)
- Monthly Trends (Line Chart)
- Worker Activity (Bar Chart)

### 2. Convert Management (Kanban)

**URL**: `http://localhost:3000/converts`

**Kanban Columns**:
1. **New** (Orange) - Just registered
2. **Contacted** (Yellow) - First contact made
3. **In Follow-up** (Green) - Active follow-up
4. **In Classes** (Blue) - Attending membership classes
5. **In House Fellowship** (Purple) - Joined cell group
6. **Established** (Teal) - Fully integrated member

**Actions**:
- Drag converts between stages
- Click for detailed profile
- Assign workers
- View health score
- Add notes

### 3. Health Scoring System

**Algorithm**:
```
Health Score = Weighted Average of:
- Attendance Rate (30%)
- Engagement Level (25%)
- Response Time (20%)
- Spiritual Growth (15%)
- Social Connection (10%)
```

**Score Ranges**:
- 🟢 80-100: Excellent
- 🟡 60-79: Good
- 🟠 40-59: Fair
- 🔴 0-39: At Risk

### 4. Alert System

**Alert Types**:
1. **Low Engagement Alert** - No attendance for 2+ weeks
2. **At Risk Alert** - Health score dropped below 40
3. **Follow-up Overdue** - Scheduled follow-up missed
4. **No Response Alert** - Not responding to communication

**Severity Levels**:
- 🔴 High - Immediate attention required
- 🟡 Medium - Address within 48 hours
- 🟢 Low - Monitor and address when possible

**Alert Workflow**:
```
System Detects Issue
        ↓
Create Alert (Open)
        ↓
Assign to Worker
        ↓
Worker Acknowledges
        ↓
Action Taken
        ↓
Alert Resolved
```

### 5. Workflow Automation

**Workflow 1: New Convert Onboarding**
```
Hour 0:   Send Welcome SMS
Hour 2:   Assign Follow-up Worker
Hour 24:  Send Follow-up Email
Hour 48:  Create Follow-up Task
Hour 72:  Schedule Welcome Call
```

**Workflow 2: Absent Member Recovery**
```
Day 0:   Send Care SMS
Day 1:   Create Welfare Task
Day 3:   Pastor Call
Day 7:   Home Visit
```

### 6. Retention Playbooks

**Playbook: First-Time Visitor Engagement**

| Step | Action | Owner | Timeline |
|------|--------|-------|----------|
| 1 | Immediate Welcome SMS | Automation | 0 hours |
| 2 | Personal Call | Follow-up Worker | 24 hours |
| 3 | Invite to Fellowship | Follow-up Worker | 3 days |
| 4 | Sunday Reminder | Automation | 6 days |
| 5 | Personal Greeting | Usher Team | Next Sunday |

**Expected Outcome**: 70% return for second visit

### 7. Analytics & Reporting

**Reports Available**:

1. **Convert Summary Report**
   - Total by stage
   - Conversion rate
   - Average time in each stage

2. **Worker Performance Report**
   - Follow-ups completed
   - Converts assigned
   - Health score improvements

3. **Service Report**
   - Attendance trends
   - Converts per service
   - Theme effectiveness

4. **Retention Analysis**
   - Attrition rate
   - Re-engagement success
   - At-risk trends

---

## API Reference

### Demo Endpoints

#### Get Demo Info
```http
GET /api/demo/info
```

**Response**:
```json
{
  "name": "Evangelism CRM Demo",
  "church": "Grace Evangelical Ministries",
  "credentials": {
    "admin_email": "admin@graceevangelical.demo",
    "admin_password": "Demo@2025"
  }
}
```

#### Get Demo Stats
```http
GET /api/demo/stats
```

**Response**:
```json
{
  "status": "success",
  "stats": {
    "clients": 1,
    "users": 15,
    "converts": 500,
    "services": 20,
    "health_scores": 500,
    "alerts": 23
  },
  "metrics": {
    "stage_distribution": {
      "new": 75,
      "in_followup": 125,
      "in_classes": 100,
      "established": 50
    },
    "average_health_score": 58.5
  }
}
```

#### Reset Demo
```http
POST /api/demo/reset
```

**Response**:
```json
{
  "status": "success",
  "message": "Demo data reset successfully"
}
```

### Standard Endpoints

See full API documentation at `http://localhost:8001/docs`

---

## Customization

### Adding Custom Nigerian States

Edit `data/nigerian_data.py`:

```python
NIGERIAN_STATES_LGAS["YourState"] = {
    "capital": "YourCapital",
    "lgas": ["LGA1", "LGA2"],
    "areas": ["Area1", "Area2"]
}
```

### Adding Custom Churches

```python
NIGERIAN_CHURCHES.append({
    "name": "Your Church Name",
    "denomination": "Pentecostal",
    "headquarters": "City, State"
})
```

### Creating Custom Workflows

Edit `scripts/populate_demo.py`, method `create_workflows()`:

```python
{
    "id": str(uuid.uuid4()),
    "client_id": self.client_id,
    "name": "Your Workflow Name",
    "description": "What it does",
    "trigger": "event_name",
    "steps": [
        {"step": 1, "action": "action_name", "delay_hours": 0},
    ],
    "is_active": True,
    "is_demo": True
}
```

### Modifying Health Score Algorithm

Edit the health score generation in `scripts/populate_demo.py`:

```python
# Custom scoring logic
score = (
    attendance_rate * 0.30 +
    engagement_level * 0.25 +
    response_time * 0.20 +
    spiritual_growth * 0.15 +
    social_connection * 0.10
)
```

---

## Demo Scenarios for Training

### Scenario 1: Sunday Service Registration

**Setup**:
1. Create a new service (Today, 10:00 AM)
2. 25 new converts registered

**Training Points**:
- Data entry process
- Convert list creation
- Kanban board usage
- Worker assignment

### Scenario 2: Follow-up Worker Dashboard

**Login**: followup_worker1@graceevangelical.demo

**Activities**:
- View assigned converts
- Log follow-up calls
- Update convert stages
- View performance metrics

### Scenario 3: Admin Analytics Review

**Login**: admin@graceevangelical.demo

**Activities**:
- Review dashboard metrics
- Check alert queue
- Monitor worker performance
- Generate reports

---

## Troubleshooting

### Database Connection Issues

```bash
# Test MongoDB connection
python -c "
from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient('your-mongo-url')
print(client.list_database_names())
"
```

### Reset Demo Data

```bash
# Full reset
python scripts/populate_demo.py --reset

# Or via API
curl -X POST http://localhost:8001/api/demo/reset
```

### Check Demo Stats

```bash
curl http://localhost:8001/api/demo/stats | python -m json.tool
```

---

## Best Practices

### For Demo Presentations

1. **Reset Before Demo**: Always reset to ensure consistent data
2. **Prepare Scenarios**: Have specific user journeys ready
3. **Use Real Names**: Refer to converts by name for realism
4. **Show Alerts**: Demonstrate the alert system actively
5. **Highlight Automation**: Show workflows running automatically

### For Training

1. **Start Simple**: Begin with convert management
2. **Progress Gradually**: Move to workflows and automation
3. **Practice Scenarios**: Have trainees perform common tasks
4. **Review Analytics**: Show how to interpret reports

---

## Summary

This demo provides a complete, realistic environment for showcasing and training on the Evangelism CRM system. With 500+ Nigerian converts, automated workflows, and comprehensive analytics, it demonstrates the full capability of the platform for church evangelism and retention management.

**Key Takeaways**:
- ✅ Separate demo database ensures data isolation
- ✅ Realistic Nigerian data for authentic demos
- ✅ All features enabled and functional
- ✅ Easy reset for consistent presentations
- ✅ Comprehensive API for custom integrations

---

*For questions or support, refer to the main project documentation or API docs at `/docs`.*
