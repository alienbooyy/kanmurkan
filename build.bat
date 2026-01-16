@echo off
REM Build script for Windows

echo Building Restaurant Automation System...

REM Build Frontend
echo Building frontend...
cd frontend
call npm install
call npm run build
cd ..

REM Build Backend
echo Building backend executable...
cd backend
pip install -r requirements.txt
pip install pyinstaller

REM Create executable
pyinstaller --onefile --name restaurant-server.exe main.py

echo Build complete!
echo Executable location: backend\dist\restaurant-server.exe
echo Frontend build: frontend\build\
pause
