#!/bin/bash
# iTaK CLI shim for Linux
# This script is installed to /usr/local/bin/itak and launches the bundled CLI

ITAK_APP_DIR="/opt/itak-agent"
if [ -d "/opt/iTaK Agent" ]; then
    ITAK_APP_DIR="/opt/iTaK Agent"
fi

RESOURCES_DIR="$ITAK_APP_DIR/resources"

# Check if app is installed
if [ ! -d "$ITAK_APP_DIR" ]; then
    echo "Error: iTaK Agent not found at $ITAK_APP_DIR"
    echo "Please install iTaK Agent first."
    exit 1
fi

# Find Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python not found. Please install Python 3.10 or higher."
    exit 1
fi

# Set PYTHONPATH to include bundled source
export PYTHONPATH="$RESOURCES_DIR/python-src:$PYTHONPATH"

# Run the CLI
cd "$RESOURCES_DIR/python-src"
exec "$PYTHON_CMD" -m itak.cli.cli "$@"
