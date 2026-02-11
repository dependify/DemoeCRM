@echo off
REM Evangelism CRM Demo - Windows Quick Start
REM ==========================================

echo.
echo ===========================================
echo   EVANGELISM CRM DEMO - QUICK START
echo ===========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo ===========================================
echo   POPULATING DEMO DATA
echo ===========================================
echo.
python scripts\populate_demo.py

echo.
echo ===========================================
echo   STARTING DEMO SERVER
echo ===========================================
echo.
echo The demo server will start on http://localhost:8001
echo.
echo Press Ctrl+C to stop the server
echo.

python backend\demo_server.py

echo.
echo Demo server stopped.
echo.

REM Deactivate virtual environment
call deactivate

pause
