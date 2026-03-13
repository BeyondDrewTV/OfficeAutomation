@echo off
setlocal

REM One-click helper for Windows users.
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [setup] Creating virtual environment...
  py -m venv .venv 2>nul || python -m venv .venv
)

if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
)

echo [run] Processing leads into queue\pending_emails.csv...
python run_lead_engine.py --input data/prospects.csv

if errorlevel 1 (
  echo [error] Lead engine failed.
) else (
  echo [done] Draft generation complete.
)

echo.
pause
