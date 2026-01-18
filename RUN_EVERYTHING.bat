@echo off
title AI Digital Call Center - Complete Auto Setup & Run (All Services)
color 0A
cls

echo.
echo ============================================================
echo    AI Digital Call Center - Complete Auto Setup ^& Run
echo ============================================================
echo.
echo This ONE file will:
echo   1. Install all dependencies (if needed)
echo   2. Initialize database
echo   3. Start Backend API (port 8000)
echo   4. Start Chat Interface (port 8501)
echo   5. Start Analytics Dashboard (port 8502)
echo.
echo All services will open in separate windows.
echo.
echo Please wait...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

REM Check if dependencies are installed (quick check)
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies... This may take a few minutes.
    echo.
    python -m pip install --upgrade pip -q
    python -m pip install -r requirements.txt -q
    echo Dependencies installed!
    echo.
)

REM Initialize database if needed
if not exist "database\call_center.db" (
    echo Initializing database...
    cd backend
    python -c "from pathlib import Path; Path('../database').mkdir(exist_ok=True); from app.core.database import init_db; init_db(); print('Database initialized!')" 2>nul
    cd ..
    echo.
)

echo ============================================================
echo Starting all services...
echo ============================================================
echo.

REM Start backend in new window
echo [1/3] Starting Backend API...
start "Backend API - Port 8000" cmd /k "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Start chat interface in new window
echo [2/3] Starting Chat Interface...
start "Chat Interface - Port 8501" cmd /k "streamlit run frontend/chat_interface.py --server.port 8501"

REM Wait a bit
timeout /t 3 /nobreak >nul

REM Start dashboard in new window
echo [3/3] Starting Analytics Dashboard...
start "Analytics Dashboard - Port 8502" cmd /k "streamlit run frontend/dashboard.py --server.port 8502"

echo.
echo ============================================================
echo ✅ ALL SERVICES STARTED SUCCESSFULLY!
echo ============================================================
echo.
echo 🌐 Services are running at:
echo.
echo    📡 Backend API:        http://localhost:8000
echo    📚 API Documentation:  http://localhost:8000/docs
echo    💬 Chat Interface:     http://localhost:8501
echo    📊 Analytics Dashboard: http://localhost:8502
echo.
echo ============================================================
echo.
echo 💡 Tips:
echo    - All services are running in separate windows
echo    - Close any window to stop that service
echo    - Backend must stay running for Chat and Dashboard
echo.
echo Press any key to close this window (services will keep running)...
pause >nul


