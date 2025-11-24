@echo off
echo Starting Wordle Backend and Frontend Setup...


echo Installing all Python Dependencies...

pip install fastapi
pip install "uvicorn[standard]"
pip install pygame
pip install requests


echo.
echo Starting FastAPI Backend service via Docker Compose...
docker compose up --build -d

if errorlevel 1 (
echo.
echo ERROR: Docker Compose failed to start the backend service.
echo Please ensure Docker Desktop is running.
PAUSE
exit /b 1
)
echo Backend service is running on http://127.0.0.1:8000.


echo.
echo Starting Pygame Frontend...
python frontend/gamePanel.py

echo.
echo Frontend game closed. Stopping Docker containers...
docker compose down

PAUSE