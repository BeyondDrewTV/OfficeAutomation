@echo off
title Copperline — Lead Operations
echo.
echo  =========================================
echo   Copperline — Lead Operations
echo  =========================================
echo.
cd /d "%~dp0lead_engine"

REM Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else if exist "..\venv\Scripts\activate.bat" (
    call ..\venv\Scripts\activate.bat
) else (
    echo No .venv found. Using system Python.
)

REM Install Flask if missing
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Installing Flask...
    pip install flask -q
)

REM ── Load credentials from .env ─────────────────────────────
if exist "%~dp0.env" (
    for /f "usebackq tokens=1,* delims==" %%A in ("%~dp0.env") do (
        if not "%%A"=="" set %%A=%%B
    )
) else (
    echo WARNING: .env file not found. Credentials not loaded.
)
REM ────────────────────────────────────────────────────────────

echo  Starting dashboard server...
echo  Browser will open automatically at http://localhost:5000
echo.
echo  Press Ctrl+C to stop the server.
echo.
python dashboard_server.py
pause
