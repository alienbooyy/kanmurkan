#!/bin/bash

# Build script for creating executables

echo "Building Restaurant Automation System..."

# Build Frontend
echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Build Backend
echo "Building backend executable..."
cd backend
pip install -r requirements.txt
pip install pyinstaller

# Create executable
pyinstaller --onefile --name restaurant-server main.py

echo "Build complete!"
echo "Executable location: backend/dist/restaurant-server"
echo "Frontend build: frontend/build/"
