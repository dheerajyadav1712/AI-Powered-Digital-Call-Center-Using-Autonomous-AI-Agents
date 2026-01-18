@echo off
title AI Call Center - Chat Interface
color 0B
cls

echo.
echo ============================================================
echo    Starting Chat Interface...
echo ============================================================
echo.
echo Opening chat interface at: http://localhost:8501
echo.
echo Make sure backend is running first!
echo (Run START_HERE.bat if not already running)
echo.

streamlit run frontend/chat_interface.py --server.port 8501

pause


