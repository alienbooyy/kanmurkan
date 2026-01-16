@echo off
REM Start script for Windows

echo Starting Restaurant Automation System...

REM Start backend
echo Starting backend server...
cd backend
start /B python main.py
cd ..

REM Wait for backend to start
timeout /t 3 /nobreak >nul

echo Backend server started

REM Start frontend (development mode)
echo Starting frontend...
cd frontend
start /B npm start
cd ..

echo Frontend started
echo.
echo System is running!
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop all services...
pause

REM Kill processes
taskkill /F /IM python.exe /T
taskkill /F /IM node.exe /T
