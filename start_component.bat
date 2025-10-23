@echo off
REM NeuroHoneypot - Individual Component Starter
REM Usage: start_component.bat [honeypot|orchestrator|dashboard|attacker|decision|cluster]

if "%1"=="" (
    echo Usage: start_component.bat [component]
    echo.
    echo Available components:
    echo   honeypot     - Start Flask honeypot
    echo   orchestrator - Start orchestrator API
    echo   dashboard    - Start Streamlit dashboard
    echo   attacker     - Run simulated attacker
    echo   decision     - Run decision engine
    echo   cluster      - Run ML clustering
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

if "%1"=="honeypot" (
    echo Starting Honeypot...
    python honeypot.py
) else if "%1"=="orchestrator" (
    echo Starting Orchestrator...
    python orchestrator.py
) else if "%1"=="dashboard" (
    echo Starting Dashboard...
    python -m streamlit run dashboard.py
) else if "%1"=="attacker" (
    echo Running Simulated Attacker...
    python sim_attacker.py full
) else if "%1"=="decision" (
    echo Running Decision Engine...
    python decision.py
) else if "%1"=="cluster" (
    echo Running ML Clustering...
    python ai/feature_cluster.py
) else (
    echo Unknown component: %1
    echo Use: honeypot, orchestrator, dashboard, attacker, decision, or cluster
    pause
    exit /b 1
)

