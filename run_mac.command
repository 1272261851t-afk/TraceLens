#!/bin/bash
cd "$(dirname "$0")"

echo "==============================================================================="
echo "  TraceLens: Browser & App Artifact Timeline Visualizer"
echo "  First Year Engineering Group Project (2026-2027) - MIT-WPU"
echo "==============================================================================="
echo ""

# Detect Python 3 on macOS
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "[ERROR] Python 3 is not installed on this Mac!"
        echo "Please download Python 3 from https://www.python.org/downloads/macos/"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo "Using Python: $($PYTHON_CMD --version)"

# Check matplotlib
$PYTHON_CMD -c "import matplotlib" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Installing matplotlib..."
    $PYTHON_CMD -m pip install -r requirements.txt --user
fi

echo "Starting TraceLens GUI..."
$PYTHON_CMD main.py
