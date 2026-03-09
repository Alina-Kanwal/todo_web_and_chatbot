@echo off
echo ========================================
echo Hackathon Todo App - Development Servers
echo ========================================
echo.

REM Check if backend virtual environment exists
IF NOT EXIST "backend\.venv" (
    echo Creating backend virtual environment...
    cd backend
    python -m venv .venv
    call .venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
)

REM Start backend in a new window
echo Starting backend server on http://localhost:8000...
start "Backend - FastAPI" cmd /k "cd backend && .venv\Scripts\activate && python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Check if node_modules exists
IF NOT EXIST "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
)

REM Start frontend in a new window
echo Starting frontend server on http://localhost:3000...
start "Frontend - Next.js" cmd /k "cd frontend && npx next dev --port 3000"

echo.
echo ========================================
echo Servers starting...
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo API Docs: http://localhost:8000/docs
echo Health:   http://localhost:8000/api/health
echo.
echo Press any key to exit this window...
pause >nul
