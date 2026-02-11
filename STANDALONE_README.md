# Evangelism CRM - Standalone Demo

A complete, self-contained demo application with **Voice Agent** capability. This standalone version includes both backend and frontend, populated with realistic Nigerian church data.

## 🎯 What's Included

### Complete Application Stack
```
┌─────────────────┐
│  React Frontend │  ← Modern UI with Tailwind CSS
│   (Port 3000)   │
└────────┬────────┘
         │ API Calls
         ▼
┌─────────────────┐
│  FastAPI Backend│  ← Complete REST API
│   (Port 8000)   │    + Voice Agent AI
└────────┬────────┘
         │ In-Memory
         ▼
┌─────────────────┐
│   Demo Database │  ← 100+ Converts, 15+ Workers,
│    (In-Memory)  │    Services, Calls, Alerts, etc.
└─────────────────┘
```

### Demo Church: Grace Evangelical Ministries
- 📍 Ikeja, Lagos, Nigeria
- 👥 2,500+ Members
- 🎙️ **AI Voice Agent Enabled**

## 🚀 Quick Start

### Option 1: One-Click Start (Recommended)

**Windows:**
```bash
cd demo
start-standalone.bat
```

**macOS/Linux:**
```bash
cd demo
chmod +x start-standalone.sh
./start-standalone.sh
```

### Option 2: Manual Start

**Step 1: Start Backend**
```bash
cd demo/standalone-backend

# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start server
python server.py
```
Backend runs at: `http://localhost:8000`

**Step 2: Start Frontend (New Terminal)**
```bash
cd demo/standalone-frontend

# Serve with any static server
npx http-server -p 3000

# Or with Python
python -m http.server 3000
```
Frontend runs at: `http://localhost:3000`

## 🔑 Login Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@graceevangelical.demo | Demo@2025 |
| Follow-up Leader | followup_leader1@graceevangelical.demo | Demo@2025 |
| Follow-up Worker | followup_worker1@graceevangelical.demo | Demo@2025 |
| Voice Agent | voice_agent1@graceevangelical.demo | Demo@2025 |

## 🎙️ Voice Agent Feature

The Voice Agent is a fully functional AI calling system for convert follow-up.

### Features

#### 1. Automated Calling
- Schedule calls to converts
- AI-powered voice conversations
- Automatic call transcription
- Sentiment analysis

#### 2. Call Scripts
Pre-built scripts for different scenarios:
- **Welcome Call** - For new converts
- **Follow-up Call** - Regular check-ins
- **Service Invitation** - Invite to upcoming events
- **Welfare Check** - For absent members

#### 3. Call Management
- View all scheduled/completed calls
- Listen to call recordings (simulated)
- Read call transcripts
- Track call outcomes

#### 4. Demo Simulation
Since this is a demo, calls are simulated:
- Click "Simulate Call" to see the AI conversation
- Real-time chat display between agent and convert
- Automatic stage updates based on call outcome

### Using the Voice Agent

1. **Navigate to Voice Agent Tab**
   - Click "Voice Agent" in the sidebar

2. **View Scheduled Calls**
   - See list of upcoming and past calls
   - Each call shows convert name, phone, and status

3. **Simulate a Call**
   - Find a call with "scheduled" status
   - Click "Simulate Call" button
   - Watch the real-time conversation unfold

4. **View Call Details**
   - Click "View Details" on any call
   - See full conversation transcript
   - Review call outcome and notes

5. **Manage Call Scripts**
   - Switch to "Scripts" tab
   - View pre-built scripts
   - Customize for your church

## 📊 Demo Data

### Converts (100+)
- Realistic Nigerian names
- Valid phone numbers (0803, 0805, etc.)
- Locations across Nigeria (Lagos, Kano, Rivers, etc.)
- Various stages: New, In Follow-up, In Classes, Established
- Health scores (0-100)

### Workers (15+)
- Admin
- Follow-up Leaders
- Follow-up Workers
- Mentors
- Voice Agents
- Data Entry staff

### Voice Calls (15+)
- Mix of scheduled, completed, failed
- Realistic transcripts
- Different outcomes (interested, callback, not interested)
- 2-10 minute durations

### Alerts
- Low engagement alerts
- At-risk member notifications
- Follow-up overdue warnings

## 🎯 Demo Scenarios

### Scenario 1: Dashboard Overview
1. Login as admin
2. View dashboard statistics
3. Check recent activity feed
4. Review stage distribution chart

### Scenario 2: Convert Management
1. Go to Converts tab
2. Search for converts by name
3. Filter by stage
4. Click on a convert to view details
5. See health score breakdown

### Scenario 3: Voice Agent Demo
1. Go to Voice Agent tab
2. Click on "Calls" sub-tab
3. Find a "scheduled" call
4. Click "Simulate Call"
5. Watch the conversation unfold
6. Check how convert stage updates

### Scenario 4: Alert Management
1. Go to Alerts tab
2. View open alerts
3. Acknowledge an alert
4. Mark alert as resolved

### Scenario 5: Analytics Review
1. Go to Analytics tab
2. View voice call statistics
3. Check convert source distribution
4. Review monthly trends

## 📁 File Structure

```
demo/
├── standalone-backend/
│   ├── server.py              # Complete FastAPI app (56 KB)
│   ├── requirements.txt       # Python dependencies
│   └── venv/                  # Virtual environment
├── standalone-frontend/
│   ├── index.html             # Main HTML file
│   ├── app.js                 # React application (64 KB)
│   ├── package.json
│   └── node_modules/          # Frontend dependencies
├── start-standalone.bat       # Windows quick start
├── start-standalone.sh        # Mac/Linux quick start
└── STANDALONE_README.md       # This file
```

## 🔧 Customization

### Adding More Converts
Edit `standalone-backend/server.py`, line ~280:
```python
for i in range(100):  # Change to desired number
```

### Changing Church Info
Edit `standalone-backend/server.py`, line ~350:
```python
church_name = "Your Church Name"
```

### Modifying Call Scripts
Edit `standalone-backend/server.py`, line ~410:
```python
scripts = [
    {
        "name": "Your Script Name",
        "content": "Your script content...",
        "purpose": "your_purpose"
    },
]
```

### Customizing Voice Agent
Edit `standalone-backend/server.py`, line ~400:
```python
db.voice_agents[agent_id] = {
    "name": "Your Agent Name",
    "greeting_template": "Your greeting...",
    # ...
}
```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Converts
- `GET /api/converts` - List converts
- `GET /api/converts/{id}` - Get convert details
- `POST /api/converts` - Create convert
- `PATCH /api/converts/{id}` - Update convert

### Voice Agent
- `GET /api/voice-agent/config` - Get agent config
- `GET /api/voice-agent/calls` - List calls
- `GET /api/voice-agent/calls/{id}` - Get call details
- `POST /api/voice-agent/calls` - Schedule call
- `POST /api/voice-agent/calls/{id}/simulate` - Simulate call
- `GET /api/voice-agent/scripts` - List scripts

### Dashboard
- `GET /api/dashboard/stats` - Get statistics
- `GET /api/dashboard/stage-distribution` - Get stage breakdown

### Alerts
- `GET /api/alerts` - List alerts
- `PATCH /api/alerts/{id}` - Update alert status

### Analytics
- `GET /api/analytics/converts` - Convert analytics
- `GET /api/analytics/voice-calls` - Voice call analytics

### Demo
- `GET /api/demo/info` - Demo information
- `POST /api/demo/reset` - Reset demo data

Full API docs: `http://localhost:8000/docs`

## 🐛 Troubleshooting

### Port Already in Use

**Backend (8000):**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

**Frontend (3000):**
Change port in `package.json` or use different port:
```bash
npx http-server -p 3001
```

### CORS Errors
The backend is configured to allow all origins. If you see CORS errors:
1. Check backend is running: `http://localhost:8000/health`
2. Ensure frontend URL matches expected origin

### Python Import Errors
```bash
# Make sure you're in the backend directory
cd standalone-backend

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Not Loading
1. Check if `http-server` is installed:
   ```bash
   npm install -g http-server
   ```
2. Or use Python:
   ```bash
   python -m http.server 3000
   ```

## 🎨 UI Features

### Responsive Design
- Works on desktop, tablet, and mobile
- Sidebar navigation
- Card-based layouts

### Interactive Elements
- Real-time search
- Modal dialogs
- Loading states
- Hover effects

### Visual Indicators
- Health score color coding
- Stage badges
- Alert severity colors
- Call status indicators

## 📱 Screens

1. **Login Screen**
   - Church branding
   - Demo credentials shown
   - Error handling

2. **Dashboard**
   - Statistics cards
   - Stage distribution
   - Recent activity

3. **Converts List**
   - Search and filter
   - Table view with actions
   - Health score rings
   - Detail modal

4. **Voice Agent**
   - Call list with status
   - Simulate call button
   - Scripts management
   - Call transcript viewer

5. **Alerts**
   - Alert cards with severity
   - Acknowledge/resolve actions
   - Convert info

6. **Analytics**
   - Voice call stats
   - Convert analytics
   - Trend charts

## 🔒 Security Notes

This is a **demo application** with the following considerations:

- In-memory database (data resets on restart)
- Simple base64 tokens (not JWT)
- No password hashing complexity
- CORS allows all origins
- **DO NOT use in production**

## 🚀 Deployment

For demo presentations, you can deploy to:

### Heroku
```bash
cd standalone-backend
git init
git add .
git commit -m "Initial commit"
heroku create your-demo-app
heroku config:set PORT=8000
git push heroku main
```

### Vercel (Frontend)
```bash
cd standalone-frontend
npm i -g vercel
vercel
```

### Railway/Render
Connect your GitHub repo and deploy both services.

## 📝 Changelog

### v1.0.0
- Complete standalone application
- Voice Agent with AI calling
- 100+ Nigerian converts
- Health scoring system
- Alert management
- Analytics dashboard

## 🤝 Contributing

To add features or improve the demo:

1. Edit `standalone-backend/server.py` for backend changes
2. Edit `standalone-frontend/app.js` for frontend changes
3. Test locally
4. Submit improvements

## 📞 Support

For issues or questions:
- Check API docs: `http://localhost:8000/docs`
- Review demo info: `http://localhost:8000/api/demo/info`
- Check browser console for errors

---

**Built with ❤️ for Nigerian Churches**

Experience the future of church evangelism management with AI-powered Voice Agent technology!
