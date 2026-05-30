@echo off
chcp 65001 >nul
title Innovation Competition Platform

echo ========================================
echo    Innovation Competition Platform
echo ========================================
echo.

cd /d "%~dp0"

echo [0/4] Stopping existing services...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    echo     Killing process on port 5000 (PID: %%a)
    taskkill /f /pid %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 ^| findstr LISTENING') do (
    echo     Killing process on port 5173 (PID: %%a)
    taskkill /f /pid %%a >nul 2>&1
)

timeout /t 1 /nobreak >nul

echo.
echo [1/4] Skipping frontend dependency check...
rem call npm install --prefix frontend

echo.
echo [2/4] Starting backend service...
start cmd /k "title Backend Service && cd /d %~dp0backend && set FLASK_ENV=development&& set FLASK_APP=app.py&& D:\TOOLS\anaconda\envs\newyolo\python.exe -m flask run --host=0.0.0.0 --port=5000"

echo     Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo.
echo [3/4] Starting frontend service...
start cmd /k "title Frontend Service && cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo    Startup Complete!
echo ========================================
echo.
echo    Frontend: http://localhost:5173
echo    Backend:  http://localhost:5000
echo.
echo    Press any key to exit (services continue running)...
pause >nul
