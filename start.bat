@echo off
echo Starting Review Insight System...
echo.
echo [1/2] Starting Flask API on port 5000...
start "API Server" cmd /k ".\venv\Scripts\python.exe api.py"
timeout /t 3 /nobreak >nul
echo [2/2] Starting React frontend on port 3000...
cd frontend
start "Frontend" cmd /k "npm run dev"
echo.
echo ✓ System started!
echo ✓ API: http://localhost:5000
echo ✓ Frontend: http://localhost:3000
echo.
pause