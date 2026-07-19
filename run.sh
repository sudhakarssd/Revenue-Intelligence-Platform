#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

if [ ! -d ".venv" ]; then
    echo "[Platform] Virtual environment not found. Creating .venv..."
    python3 -m venv .venv
    echo "[Platform] Installing dependencies..."
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

echo "[Platform] Launching FastAPI App Server..."
exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
