#!/bin/bash

echo "🚀 Starting SmartBusinessAnalyser App (No Scraping)..."

# Start the FastAPI backend for Trends & Analysis in the background
echo "Starting backend API (aura.py) on port 8000..."
venv/bin/uvicorn aura:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start the React Frontend
echo "Starting React frontend on port 8080..."
npm run dev &
FRONTEND_PID=$!

echo "✅ All systems running! Press CTRL+C to cleanly shut down both servers."

# Wait for CTRL+C and kill both background processes
trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT SIGTERM
wait
