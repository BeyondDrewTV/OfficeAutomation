@echo off
title Missed Call Lead Capture Service
color 0A

echo ============================================================
echo   MISSED CALL LEAD CAPTURE — Automation Biz
echo ============================================================
echo.

REM ── Navigate to this script's directory ──────────────────────
cd /d "%~dp0"

REM ── Check venv exists ─────────────────────────────────────────
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found.
    echo.
    echo Run this first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM ── Check .env exists ─────────────────────────────────────────
if not exist ".env" (
    echo [ERROR] .env file not found.
    echo Copy .env.example to .env and fill in your credentials.
    echo.
    pause
    exit /b 1
)

REM ── Check service_account.json exists ────────────────────────
if not exist "service_account.json" (
    echo [WARNING] service_account.json not found.
    echo Google Sheets logging will fail until this file is added.
    echo.
)

REM ── Activate venv and load .env ───────────────────────────────
call venv\Scripts\activate.bat

REM Load .env variables into this session
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
    if not "%%A"=="" if not "%%A:~0,1%"=="#" (
        set "%%A=%%B"
    )
)

echo [OK] Environment loaded
echo [OK] Virtual environment active
echo.
echo Starting Flask server on http://localhost:%PORT%
echo Press Ctrl+C to stop.
echo.
echo ============================================================
echo.

python app.py

echo.
echo [INFO] Server stopped.
pause
