@echo off
TITLE TraceLens - Push to GitHub
COLOR 0B

echo ===============================================================================
echo   Pushing TraceLens to GitHub: 1272261851t-afk/TraceLens
echo ===============================================================================
echo.

cd /d "%~dp0"

echo Current remote origin:
git remote -v
echo.

echo Pushing main branch to GitHub...
echo (If a GitHub sign-in window pops up, click "Sign in with your browser")
echo.
git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ===============================================================================
    echo   SUCCESS! Project successfully pushed to GitHub!
    echo   Check your repository at:
    echo   https://github.com/1272261851t-afk/TraceLens
    echo   https://github.com/1272261851t-afk/TraceLens/graphs/contributors
    echo ===============================================================================
) else (
    echo ===============================================================================
    echo   [ERROR] Push failed. Check your internet connection or GitHub login.
    echo ===============================================================================
)

echo.
pause
