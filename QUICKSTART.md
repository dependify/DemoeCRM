# Evangelism CRM Demo - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Navigate to Demo Folder
```bash
cd demo
```

### Step 2: Setup Environment (First Time Only)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your MongoDB credentials
# The demo database will be named: evangelism_crm_demo
```

### Step 4: Run the Demo

**Option A: Quick Start Script**
```bash
# Windows
start-demo.bat

# macOS/Linux
./start-demo.sh
```

**Option B: Manual Steps**
```bash
# Populate demo data
python scripts/populate_demo.py

# Start the server
python backend/demo_server.py
```

### Step 5: Access the Demo

- **Frontend**: http://localhost:3000 (if running separately)
- **API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **Demo Info**: http://localhost:8001/api/demo/info

---

## 🔑 Default Login Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@graceevangelical.demo | Demo@2025 |
| Follow-up Leader | followup_leader1@graceevangelical.demo | Demo@2025 |
| Follow-up Worker | followup_worker1@graceevangelical.demo | Demo@2025 |
| Data Entry | data_entry1@graceevangelical.demo | Demo@2025 |
| Mentor | mentor1@graceevangelical.demo | Demo@2025 |

---

## 📊 What's Included

### Demo Data
- ✅ **500+ Converts** with Nigerian names and realistic data
- ✅ **15+ Workers** across different roles
- ✅ **20+ Church Services** from the past 6 months
- ✅ **Membership Classes** and **House Fellowships**
- ✅ **Health Scores** and **Alerts** for at-risk converts
- ✅ **Workflows** and **Sequences** for automation
- ✅ **Playbooks** for retention strategies

### Demo Church
- **Name**: Grace Evangelical Ministries
- **Location**: Ikeja, Lagos, Nigeria
- **Denomination**: Pentecostal
- **Members**: 2,500+

---

## 🔄 Reset Demo Data

To reset to initial state:
```bash
python scripts/populate_demo.py
```

Or via API:
```bash
curl -X POST http://localhost:8001/api/demo/reset
```

---

## 🛠️ Troubleshooting

### Port Already in Use
Edit `.env` and change:
```env
DEMO_PORT=8002
```

### MongoDB Connection Error
Check your `MONGO_URL` in `.env`:
```env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
```

### Import Errors
Make sure you're in the `demo` directory and have activated the virtual environment.

---

## 📖 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [docs/DEMO_GUIDE.md](docs/DEMO_GUIDE.md) for comprehensive guides
- Explore API docs at http://localhost:8001/docs

---

**Ready to showcase your Evangelism CRM! 🎉**
