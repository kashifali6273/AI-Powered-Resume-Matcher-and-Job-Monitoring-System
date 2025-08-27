@echo off
title Flask + Ngrok Starter

REM Change these paths if needed
set FLASK_APP=app.py
set FLASK_ENV=development

REM Step 1: Start Flask in a new terminal window
start cmd /k "python %FLASK_APP%"

REM Step 2: Wait a moment so Flask starts
timeout /t 3 >nul

REM Step 3: Start ngrok
cd C:\ngrok\
ngrok http 5000
