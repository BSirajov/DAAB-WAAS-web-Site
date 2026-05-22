@echo off
title DAAB local site
cd /d "%~dp0"

echo.
echo  DAAB website - local preview
echo  ===========================
echo  Do NOT close the server window while browsing.
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python is not installed or not on PATH.
  echo Install Python from https://www.python.org/ then run this file again.
  pause
  exit /b 1
)

rem Reuse existing server if port is already up
powershell -NoProfile -Command "try { (Invoke-WebRequest -UseBasicParsing -Uri 'http://localhost:8010/index.html' -TimeoutSec 2).StatusCode } catch { exit 1 }" >nul 2>&1
if not errorlevel 1 (
  echo Server already running on http://localhost:8010/
  start "" "http://localhost:8010/"
  exit /b 0
)

start "DAAB Server (keep open)" cmd /k "cd /d "%~dp0" && python -m http.server 8010 --bind 127.0.0.1"

echo Waiting for server...
timeout /t 2 /nobreak >nul

start "" "http://localhost:8010/"
echo.
echo  Open in browser: http://localhost:8010/
echo  Azerbaijani: http://localhost:8010/az/
echo  English:     http://localhost:8010/en/
echo  To stop: close the "DAAB Server" window or press Ctrl+C there.
echo.
pause
