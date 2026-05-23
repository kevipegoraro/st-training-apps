#!/usr/bin/env bash
set -e

APP_FILE="app2.py"
VENV_DIR=".venv"

cd "$(dirname "$0")"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR" 2>/dev/null || python -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt
streamlit run "$APP_FILE" --server.address 127.0.0.1 --server.port 8501
