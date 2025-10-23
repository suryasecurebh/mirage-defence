@echo off
REM NeuroHoneypot - Start All Components
REM Windows Batch Script

echo ================================================
echo    NeuroHoneypot - Starting All Components
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo [*] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [!] No virtual environment found. Using system Python.
)

REM Check if dependencies are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [!] Dependencies not installed. Installing now...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo [1/3] Starting Honeypot on port 5000...
start "NeuroHoneypot - Honeypot" cmd /k "python honeypot.py"
timeout /t 3 /nobreak >nul

echo [2/3] Starting Orchestrator on port 5001...
start "NeuroHoneypot - Orchestrator" cmd /k "python orchestrator.py"
timeout /t 3 /nobreak >nul

echo [3/3] Starting Dashboard on port 8501...
start "NeuroHoneypot - Dashboard" cmd /k "python -m streamlit run dashboard.py"
timeout /t 5 /nobreak >nul

echo.
echo ================================================
echo    All Components Started!
echo ================================================
echo.
echo  Honeypot:     http://localhost:5000
echo  Orchestrator: http://localhost:5001
echo  Dashboard:    http://localhost:8501
echo.
echo ================================================
echo.
echo Next Steps:
echo   1. Wait for all services to fully start (10-15 seconds)
echo   2. Open dashboard: http://localhost:8501
echo   3. Run attacker: python sim_attacker.py full
echo   4. Run analyzer: python decision.py
echo.
echo To stop all services: Close all terminal windows
echo.
pause

