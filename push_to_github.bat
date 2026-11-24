@echo off
TITLE TraceLens - Push to GitHub
COLOR 0B

echo ===============================================================================
echo   Pushing TraceLens to GitHub: 1272261851t-afk/TraceLens
echo   Commit Timeline: October 29, 2026 to November 24, 2026
echo ===============================================================================
echo.

cd /d "%~dp0"

echo Pushing all commits spanning Oct 29 - Nov 24 to GitHub...
echo (If a GitHub sign-in window appears, click "Sign in with your browser")
echo.
git push -u origin main --force

echo.
if %errorlevel% equ 0 (
    echo ===============================================================================
    echo   SUCCESS! Project successfully pushed to GitHub!
    echo   
    echo   Check your multi-week contribution timeline at:
    echo   https://github.com/1272261851t-afk/TraceLens/commits/main
    echo   https://github.com/1272261851t-afk/TraceLens/graphs/contributors
    echo ===============================================================================
) else (
    echo ===============================================================================
    echo   [ERROR] Push failed. Check your internet connection or GitHub login.
    echo ===============================================================================
)

echo.
pause
