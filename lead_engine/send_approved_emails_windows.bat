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

echo [run] Sending approved queue rows (live mode)...
python send\email_sender_agent.py --queue queue\pending_emails.csv --send-live

if errorlevel 1 (
  echo [error] Sender failed.
) else (
  echo [done] Sender finished.
)

echo.
pause
