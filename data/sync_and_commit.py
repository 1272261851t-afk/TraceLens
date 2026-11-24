"""
Sync files, update zip, and commit incognito feature to Git.
"""

import os
import shutil
import subprocess

SRC = r"C:\Users\ASUS\Documents\TraceLens"
DST = r"C:\Users\ASUS\OneDrive\PlayerFile\Desktop\TraceLens"
DESKTOP = r"C:\Users\ASUS\OneDrive\PlayerFile\Desktop"

def sync_files():
    print("[1/3] Syncing files to Desktop folder...")
    files = [
        r"parsers\incognito_parser.py",
        r"parsers\sample_generator.py",
        r"core\timeline_engine.py",
        r"core\report_exporter.py",
        r"gui\app_window.py",
        r"README.md",
        r"PROJECT_REPORT.md",
        r"Deliverables_Document.html",
        r"Deliverables_Document.pdf",
        r"Project_Documentation.html",
        r"Project_Documentation.pdf",
        r"Project_Documentation.docx"
    ]
    for f in files:
        s = os.path.join(SRC, f)
        d = os.path.join(DST, f)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if os.path.exists(s):
            shutil.copy2(s, d)

    # Update zip
    zip_path = os.path.join(DESKTOP, "TraceLens.zip")
    subprocess.run(["powershell", "-Command", f"Compress-Archive -Path '{SRC}\\*' -DestinationPath '{zip_path}' -Force"])
    print(f"      TraceLens.zip updated ({os.path.getsize(zip_path)} bytes)")

def commit_to_git():
    print("[2/3] Committing incognito feature to Git...")
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = "Janhavi Dahiwale"
    env["GIT_AUTHOR_EMAIL"] = "1272261225.j@mitwpu.edu.in"
    env["GIT_COMMITTER_NAME"] = "Janhavi Dahiwale"
    env["GIT_COMMITTER_EMAIL"] = "1272261225.j@mitwpu.edu.in"

    subprocess.run(["git", "add", "."], cwd=SRC, env=env)
    res = subprocess.run(
        ["git", "commit", "-m", "feat(incognito): Add incognito and private browsing forensic artifact detection"],
        cwd=SRC,
        env=env,
        capture_output=True,
        text=True
    )
    print("      Git commit output:", res.stdout if res.returncode == 0 else res.stderr)

    # Sync .git to Desktop folder
    dst_git = os.path.join(DST, ".git")
    src_git = os.path.join(SRC, ".git")
    if os.path.exists(dst_git):
        subprocess.run(["cmd", "/c", f"rmdir /s /q \"{dst_git}\""], capture_output=True)
    shutil.copytree(src_git, dst_git, dirs_exist_ok=True)
    print("      Git repository mirrored to Desktop.")

def main():
    sync_files()
    commit_to_git()
    print("[3/3] Done!")

if __name__ == "__main__":
    main()
