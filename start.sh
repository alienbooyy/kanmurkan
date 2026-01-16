#!/bin/bash

# Start script for Linux/Mac

echo "Starting Restaurant Automation System..."

# Start backend
echo "Starting backend server..."
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
   echo "Failed to start backend server"
   exit 1
fi

echo "Backend server started with PID: $BACKEND_PID"

# Start frontend (development mode)
echo "Starting frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "Frontend started with PID: $FRONTEND_PID"
echo ""
echo "System is running!"
echo "Backend API: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "To stop manually:"
echo "  kill $BACKEND_PID  # Stop backend"
echo "  kill $FRONTEND_PID  # Stop frontend"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
