import subprocess
import os

repo_dir = r"C:\Users\ASUS\Documents\TraceLens"
os.chdir(repo_dir)

# 1. Git add
subprocess.run(["git", "add", "-A"], check=True)

# 2. Git commit
commit_msg = (
    "feat(incognito): Multi-vector live private browsing forensic detection and methodology guide\n\n"
    "Implemented real-time OS kernel socket enumeration (TCP/UDP ports 80/443) mapped to browser PIDs,\n"
    "Reverse DNS resolution, OS DNS resolver cache extraction, and persistent download residue detection.\n"
    "Added interactive Incognito Forensics Methodology guide modal in GUI and updated academic documentation."
)

env = os.environ.copy()
env["GIT_AUTHOR_NAME"] = "Janhavi Dahiwale"
env["GIT_AUTHOR_EMAIL"] = "1272261225.j@mitwpu.edu.in"
env["GIT_COMMITTER_NAME"] = "Janhavi Dahiwale"
env["GIT_COMMITTER_EMAIL"] = "1272261225.j@mitwpu.edu.in"

res_commit = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True, env=env)
print("Commit output:\n", res_commit.stdout, res_commit.stderr)

# 3. Git push
print("Pushing to GitHub origin main...")
res_push = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("Push output:\n", res_push.stdout, res_push.stderr)
