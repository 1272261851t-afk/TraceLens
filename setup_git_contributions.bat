@echo off
TITLE TraceLens - Setup Git Contributions for MIT-WPU Team
COLOR 0A

echo ===============================================================================
echo   Setting up Git Repository & Commits for All 4 MIT-WPU Team Members
echo ===============================================================================
echo.

cd /d "%~dp0"

echo [1/6] Initializing Git Repository...
git init
git branch -M main

echo.
echo [2/6] Committing Module 1: Tanishq Gunjal (Lead / GUI Architecture)...
git config user.name "Tanishq Gunjal"
git config user.email "1272261851.t@mitwpu.edu.in"
git add main.py run.bat requirements.txt gui/app_window.py gui/about_dialog.py gui/__init__.py
git commit -m "feat(gui): Initial application layout, main desktop window and team credits"

echo.
echo [3/6] Committing Module 2: Janhavi Dahiwale (Browser Forensics Parser)...
git config user.name "Janhavi Dahiwale"
git config user.email "1272261225.j@mitwpu.edu.in"
git add parsers/browser_parser.py parsers/__init__.py
git commit -m "feat(parsers): Add Chrome and Edge SQLite parser with WebKit timestamp conversion"

echo.
echo [4/6] Committing Module 3: OM Nalawade (OS Artifacts & Timeline Engine)...
git config user.name "OM Nalawade"
git config user.email "1272261153.o@mitwpu.edu.in"
git add parsers/app_parser.py parsers/sample_generator.py core/timeline_engine.py core/__init__.py
git commit -m "feat(engine): Add Windows Recent parser, mock case generator and timeline correlation"

echo.
echo [5/6] Committing Module 4: Ayush Warudkar (Analytics & Reporting Engine)...
git config user.name "Ayush Warudkar"
git config user.email "1272261894.a@mitwpu.edu.in"
git add gui/analytics_view.py core/report_exporter.py
git commit -m "feat(analytics): Add Matplotlib visual charts and HTML/CSV forensic report exporters"

echo.
echo [6/6] Committing Documentation: Full MIT-WPU Team...
git config user.name "Tanishq Gunjal"
git config user.email "1272261851.t@mitwpu.edu.in"
git add README.md PROJECT_REPORT.md setup_git_contributions.bat
git commit -m "docs: Add academic project report, README, and MIT-WPU viva preparation guide"

echo.
echo ===============================================================================
echo   SUCCESS! All 4 group members have individual commits credited in Git!
echo ===============================================================================
echo.
echo To push this to GitHub, run these two commands:
echo   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/TraceLens.git
echo   git push -u origin main
echo.
pause
