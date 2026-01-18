@echo off
title Installing All Dependencies - AI Digital Call Center
color 0B
cls

echo.
echo ============================================================
echo    AI Digital Call Center - Complete Installation Script
echo ============================================================
echo.
echo This script will:
echo   1. Check Python installation
echo   2. Upgrade pip to latest version
echo   3. Install all required packages from requirements.txt
echo   4. Verify installation
echo.
echo ============================================================
echo.

REM Check if Python is installed
echo [Step 1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.10 or higher:
    echo   1. Go to: https://www.python.org/downloads/
    echo   2. Download Python 3.11+
    echo   3. During installation, CHECK "Add Python to PATH"
    echo   4. Run this script again
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python is installed!
echo.

REM Upgrade pip
echo [Step 2/4] Upgrading pip to latest version...
python -m pip install --upgrade pip -q
if errorlevel 1 (
    echo [WARNING] Could not upgrade pip. Continuing anyway...
) else (
    echo [OK] pip upgraded successfully!
)
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found!
    echo Please make sure you're in the project root directory.
    pause
    exit /b 1
)

REM Install dependencies
echo [Step 3/4] Installing all dependencies from requirements.txt...
echo This may take 2-5 minutes depending on your internet speed...
echo Please wait...
echo.
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Some packages failed to install!
    echo.
    echo Troubleshooting:
    echo   1. Check your internet connection
    echo   2. Try: python -m pip install --upgrade pip
    echo   3. Try: python -m pip install -r requirements.txt --user
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] All dependencies installed successfully!
echo.

REM Verify installation
echo [Step 4/4] Verifying installation...
python -c "import fastapi, streamlit, sqlalchemy, plotly, requests, pydantic; print('[OK] All core packages verified!')" 2>nul

if errorlevel 1 (
    echo [WARNING] Some packages may not be installed correctly.
    echo Try running: python -m pip install -r requirements.txt
) else (
    echo [OK] Installation verified successfully!
)

echo.
echo ============================================================
echo    ✅ INSTALLATION COMPLETE!
echo ============================================================
echo.
echo Next steps:
echo   1. Run: START.bat (to start the application)
echo   2. Or run: RUN_EVERYTHING.bat (to start all services)
echo.
echo Application will be available at:
echo   - Backend API: http://localhost:8000
echo   - Chat Interface: http://localhost:8501
echo   - Dashboard: http://localhost:8502
echo.
echo ============================================================
pause


