@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM One-click publish script for DAAB-WAAS project
REM Usage:
REM   scripts\push-to-github.bat
REM   scripts\push-to-github.bat "Your custom commit message"

set "REPO_URL=https://github.com/BSirajov/DAAB-WAAS-web-Site.git"
set "TARGET_BRANCH=main"
set "DEFAULT_COMMIT_MSG=Upload project files"

REM Ensure script runs from repository root
pushd "%~dp0\.."

if not exist ".git" (
  echo [ERROR] This folder is not a git repository.
  echo         Run this script from inside your project repo.
  popd
  exit /b 1
)

echo.
echo ============================
echo Current repository snapshot
echo ============================
git status
echo.
git remote -v
echo.
git branch --show-current
echo.
git log --oneline -n 5
echo.

echo ============================
echo Configure GitHub remote
echo ============================
git remote get-url origin >nul 2>&1
if errorlevel 1 (
  echo origin remote not found. Adding origin...
  git remote add origin "%REPO_URL%"
) else (
  echo origin remote exists. Updating URL to expected repo...
  git remote set-url origin "%REPO_URL%"
)
if errorlevel 1 (
  echo [ERROR] Failed to configure origin remote.
  popd
  exit /b 1
)

echo.
echo ============================
echo Stage and commit (if needed)
echo ============================
git add -A
if errorlevel 1 (
  echo [ERROR] Failed during git add.
  popd
  exit /b 1
)

set "COMMIT_MSG=%DEFAULT_COMMIT_MSG%"
if not "%~1"=="" set "COMMIT_MSG=%~1"

git diff --cached --quiet
if errorlevel 1 (
  echo Creating commit: "%COMMIT_MSG%"
  git commit -m "%COMMIT_MSG%"
  if errorlevel 1 (
    echo [ERROR] Commit failed. Resolve the issue and re-run.
    popd
    exit /b 1
  )
) else (
  echo No new changes to commit.
)

echo.
echo ============================
echo Push to GitHub
echo ============================
git branch -M "%TARGET_BRANCH%"
if errorlevel 1 (
  echo [ERROR] Failed to set branch name to %TARGET_BRANCH%.
  popd
  exit /b 1
)

git push -u origin "%TARGET_BRANCH%"
if errorlevel 1 (
  echo [ERROR] Push failed.
  echo         If prompted, complete GitHub sign-in or PAT auth and re-run.
  popd
  exit /b 1
)

echo.
echo ============================
echo Success
echo ============================
echo Project is now published to:
echo   %REPO_URL%
echo.
start "" "https://github.com/BSirajov/DAAB-WAAS-web-Site"

popd
exit /b 0
