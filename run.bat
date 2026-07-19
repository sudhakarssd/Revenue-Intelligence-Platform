@echo off
SETLOCAL

if not exist ".venv" (
    echo [Platform] Virtual environment not found. Creating .venv...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment. Ensure Python is installed and in PATH.
        exit /b 1
    )
    echo [Platform] Installing dependencies...
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo [Platform] Launching FastAPI App Server...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

ENDLOCAL
