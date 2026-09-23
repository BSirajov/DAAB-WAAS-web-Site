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

rem Reuse only if both IPv4 and localhost (::1) serve the real AZ home page.
rem Windows resolves localhost to ::1 first; a stale IPv6 http.server looks "up" on 127.0.0.1.
python -c "from urllib.request import urlopen; urls=('http://127.0.0.1:8010/az/index.html','http://localhost:8010/az/index.html'); raise SystemExit(0 if all('primaryNavMenu' in urlopen(u, timeout=3).read().decode('utf-8','replace') for u in urls) else 1)" 2>nul
if not errorlevel 1 (
  echo Server already running on http://127.0.0.1:8010/ and http://localhost:8010/
  start "" "http://127.0.0.1:8010/az/index.html"
  exit /b 0
)

rem Stale duplicate listeners can break responses; stop them first.
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /R /C:":8010 .*LISTENING"') do (
  taskkill /PID %%a /F >nul 2>&1
)

start "DAAB Server (keep open)" cmd /k "cd /d ""%~dp0"" && python helpers/serve_site.py --bind 127.0.0.1 --port 8010"

echo Waiting for server...
timeout /t 2 /nobreak >nul

start "" "http://127.0.0.1:8010/az/index.html"
echo.
echo  Open in browser: http://127.0.0.1:8010/az/index.html
echo  Azerbaijani: http://127.0.0.1:8010/az/   (also http://localhost:8010/az/)
echo  English:     http://127.0.0.1:8010/en/
echo  To stop: close the "DAAB Server" window or press Ctrl+C there.
echo.
pause
