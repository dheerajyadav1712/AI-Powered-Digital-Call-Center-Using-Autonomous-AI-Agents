@echo off
title AI Call Center - Analytics Dashboard
color 0E
cls

echo.
echo ============================================================
echo    Starting Analytics Dashboard...
echo ============================================================
echo.
echo Opening dashboard at: http://localhost:8502
echo.
echo Make sure backend is running first!
echo (Run START_HERE.bat if not already running)
echo.

streamlit run frontend/dashboard.py --server.port 8502

pause


