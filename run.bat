@echo off
TITLE TraceLens - Browser & App Artifact Timeline Visualizer
COLOR 0B

echo ===============================================================================
echo   TraceLens: Browser & App Artifact Timeline Visualizer
echo   First Year Engineering Group Project (2026-2027)
echo.
echo   Group Members:
echo     1. Tanishq Gunjal   (Lead / GUI & Integration)
echo     2. Janhavi Dahiwale (Browser Artifact Parser)
echo     3. OM Nalawade      (Timeline Engine)
echo     4. Ayush Warudkar   (Analytics & Reports)
echo ===============================================================================
echo.
echo Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ and ensure "Add Python to PATH" is checked.
    pause
    exit /b
)

echo Starting TraceLens GUI...
python main.py

if %errorlevel% neq 0 (
    echo.
    echo [NOTICE] Application closed or exited with an error.
    pause
)
