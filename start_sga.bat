@echo off
cd /d C:\Users\KIIT0001\SGA_Assistant

echo 🔁 Activating venv...
call venv\Scripts\activate

echo 🚀 Starting Backend...
start cmd /k uvicorn backend.server:app --host 0.0.0.0 --port 8000

timeout /t 3 >nul

echo 🌐 Starting Frontend...
cd frontend
start cmd /k npm start

echo ✅ S.G.A System Started
pause