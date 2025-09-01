@echo off
REM Start all containers in the background
docker compose up -d

REM Wait for services to be ready
:waitloop
curl --silent http://localhost:8000/classify >nul 2>nul
if errorlevel 1 (
    timeout /t 5
    goto waitloop
)
curl --silent http://localhost:8001/retrieve >nul 2>nul
if errorlevel 1 (
    timeout /t 5
    goto waitloop
)
curl --silent http://localhost:8002 >nul 2>nul
if errorlevel 1 (
    timeout /t 5
    goto waitloop
)


REM Activate your venv
call .\venv\Scripts\activate

REM Run your terminal chat client
python AgentRun.py