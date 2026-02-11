@echo off
REM Start Evangelism CRM Demo Frontend on Port 3005
REM =================================================

echo.
echo Starting Frontend Server on Port 3005...
echo.

cd standalone-frontend

REM Check if http-server is available
where npx >nul 2>&1
if errorlevel 1 (
    echo ERROR: npx not found. Please install Node.js.
    exit /b 1
)

echo.
echo ===========================================
echo   FRONTEND STARTED!
echo ===========================================
echo.
echo Open your browser to: http://localhost:3005
echo.
echo Press Ctrl+C to stop the server
echo.

npx http-server -p 3005 -c-1 -o

cd ..
