# Deploy Evangelism CRM Demo to Vercel

This guide explains how to deploy the Evangelism CRM Demo as a monolithic app to Vercel.

## Project Structure

```
demo/
├── api/                    # Vercel serverless functions
│   └── index.py           # Main API entry point
├── standalone-backend/    # FastAPI Python backend
│   ├── server.py          # Main FastAPI application
│   ├── models/            # Pydantic models
│   ├── routes/            # API routes
│   ├── services/          # Business logic
│   └── utils/             # Utilities
├── standalone-frontend/   # React frontend (single HTML file)
│   ├── index.html         # Main application
│   └── package.json       # Build configuration
├── vercel.json            # Vercel deployment config
├── requirements.txt       # Python dependencies
└── .vercelignore          # Files to exclude from deployment
```

## Prerequisites

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

## Deployment Steps

### Option 1: Deploy via Vercel CLI

1. Navigate to the demo folder:
   ```bash
   cd demo
   ```

2. Deploy to Vercel:
   ```bash
   vercel --prod
   ```

3. Follow the prompts to configure your project.

### Option 2: Deploy via Git Integration

1. Push the `demo` folder to a Git repository (GitHub, GitLab, or Bitbucket).

2. Import the project in the Vercel dashboard:
   - Go to https://vercel.com/new
   - Import your Git repository
   - Vercel will automatically detect the `vercel.json` configuration

3. Configure environment variables (if needed):
   - `DEMO_MODE`: `true` (already set in code)
   - `PYTHONIOENCODING`: `utf-8` (already set in code)

4. Deploy!

## Architecture

This is a **monolithic deployment** where:

- **Frontend**: Static HTML file served from `standalone-frontend/`
- **Backend**: Python FastAPI serverless functions in `api/`
- **API Routes**: All `/api/*` requests are handled by the Python backend
- **Static Routes**: All other requests serve the frontend

### Key Features

- In-memory database (data resets on each deployment)
- 100 demo converts pre-populated
- 8 demo users with different roles
- Voice Agent with ElevenLabs integration
- Health scoring system
- Alerts and notifications
- Kanban board
- Analytics dashboard

## Demo Credentials

After deployment, use these credentials to login:

- **Email**: `admin@dependifygospel.demo`
- **Password**: `Demo@2025`

## API Endpoints

All API endpoints are available at `https://your-domain.vercel.app/api/`:

- `POST /api/auth/login` - Login
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/converts` - List converts
- `GET /api/analytics/converts` - Convert analytics
- `GET /api/analytics/voice-calls` - Voice call analytics
- And more...

## Troubleshooting

### Unicode Encoding Issues
If you see encoding errors, make sure `PYTHONIOENCODING=utf-8` is set.

### Module Not Found Errors
Ensure all Python files are properly imported with the path setup in `api/index.py`.

### CORS Errors
CORS is configured to allow all origins (`*`). If you need specific origins, update the `CORSMiddleware` in `server.py`.

## Limitations

- **Data Persistence**: Since this uses in-memory storage, all data resets when the serverless function cold starts or on redeployment.
- **File Uploads**: Not supported in this demo version.
- **WebSockets**: Not supported in serverless environment.

## Customization

To customize the demo data, modify the `populate_demo_data()` function in `standalone-backend/server.py`.

## Support

For issues or questions, refer to the main project documentation or create an issue in the repository.
