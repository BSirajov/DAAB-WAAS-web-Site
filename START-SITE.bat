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

rem Reuse existing server if it responds correctly.
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8010/index.html' -TimeoutSec 3; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if not errorlevel 1 (
  echo Server already running on http://localhost:8010/
  start "" "http://localhost:8010/"
  exit /b 0
)

rem Stale duplicate listeners can break responses; stop them first.
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /R /C:"127\.0\.0\.1:8010 .*LISTENING"') do (
  taskkill /PID %%a /F >nul 2>&1
)

start "DAAB Server (keep open)" cmd /k "cd /d ""%~dp0"" && python -m http.server 8010 --bind 127.0.0.1"

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
