@echo off
TITLE TraceLens - Browser & App Artifact Timeline Visualizer
COLOR 0B

echo ===============================================================================
echo   TraceLens: Browser & App Artifact Timeline Visualizer
echo   First Year Engineering Group Project (2026-2027)
echo.
echo   Group Members:
echo     1. Tanishq Gunjal   (PRN: 1272261851) - Project Lead
echo     2. Janhavi Dahiwale (PRN: 1272261225) - Browser Forensics Parser
echo     3. OM Nalawade      (PRN: 1272261153) - OS Artifacts & Timeline Engine
echo     4. Ayush Warudkar   (PRN: 1272261894) - Visual Analytics & Reports
echo ===============================================================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to PATH on this laptop!
    echo Please install Python from https://www.python.org and check "Add python.exe to PATH".
    echo.
    pause
    exit /b
)
python --version

echo.
echo [2/3] Checking required libraries (matplotlib)...
python -c "import matplotlib" >nul 2>&1
if %errorlevel% neq 0 (
    echo Matplotlib not found. Automatically installing via pip...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [Warning] Pip install failed or no internet. TraceLens will continue in fallback mode.
    )
) else (
    echo All libraries are ready!
)

echo.
echo [3/3] Starting TraceLens GUI...
python main.py

if %errorlevel% neq 0 (
    echo.
    echo [NOTICE] Application closed or exited with an error.
    pause
)
