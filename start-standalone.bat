@echo off
REM Evangelism CRM Standalone Demo - Quick Start
REM =============================================

echo.
echo ===========================================
echo   EVANGELISM CRM - STANDALONE DEMO
echo ===========================================
echo.

set BACKEND_DIR=standalone-backend
set FRONTEND_DIR=standalone-frontend

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)

REM Setup Backend
echo [1/3] Setting up backend...
if not exist %BACKEND_DIR%\venv (
    echo Creating virtual environment...
    python -m venv %BACKEND_DIR%\venv
)

call %BACKEND_DIR%\venv\Scripts\activate
pip install -q -r %BACKEND_DIR%\requirements.txt
call deactivate

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Node.js not found. Frontend will not start automatically.
    echo Please install Node.js or serve the frontend manually.
)

echo.
echo ===========================================
echo   STARTING DEMO APPLICATIONS
echo ===========================================
echo.

REM Start Backend
echo [2/3] Starting Backend Server...
cd %BACKEND_DIR%
start "Demo Backend" cmd /k "call venv\Scripts\activate && python server.py"
cd ..

echo Backend starting on http://localhost:8000

echo.
echo [3/3] Starting Frontend Server...

REM Start Frontend
cd %FRONTEND_DIR%
if exist node_modules (
    start "Demo Frontend" cmd /k "npx http-server -p 3005 -c-1 -o"
) else (
    echo Installing frontend dependencies...
    npm install
    start "Demo Frontend" cmd /k "npx http-server -p 3000 -c-1 -o"
)
cd ..

echo.
echo ===========================================
echo   DEMO STARTED SUCCESSFULLY!
echo ===========================================
echo.
echo Frontend: http://localhost:3005
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Login Credentials:
echo   Email: admin@dependifygospel.demo
echo   Password: Demo@2025
echo.
echo Features:
echo   - Convert Management with Kanban Board
echo   - Health Scoring System
echo   - Alert Management
echo   - VOICE AGENT with AI Calling
echo   - Call Scripts
echo   - Analytics Dashboard
echo.
echo Press any key to stop...
pause >nul

echo.
echo Stopping servers...
taskkill /FI "WINDOWTITLE eq Demo Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Demo Frontend*" /F >nul 2>&1
echo Done!
