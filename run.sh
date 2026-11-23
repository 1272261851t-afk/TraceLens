#!/bin/bash
cd "$(dirname "$0")"

echo "==============================================================================="
echo "  TraceLens: Browser & App Artifact Timeline Visualizer"
echo "  First Year Engineering Group Project (2026-2027) - MIT-WPU"
echo "==============================================================================="

PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

$PYTHON_CMD -c "import matplotlib" &> /dev/null
if [ $? -ne 0 ]; then
    $PYTHON_CMD -m pip install -r requirements.txt --user
fi

$PYTHON_CMD main.py
