#!/usr/bin/env bash
set -e

VENV_DIR=".venv"
cd "$(dirname "$0")"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR" 2>/dev/null || python -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python cli.py
