"""
Module: sample_generator.py
Project: TraceLens - Browser & App Artifact Timeline Visualizer
Contributed by: Tanishq Gunjal & OM Nalawade

Description:
Generates a realistic, pre-configured digital forensics scenario dataset.
This allows teachers, evaluators, and students to demonstrate TraceLens instantly
in college labs without relying on local browser state or locked databases.
Case Scenario: 'Cyber Investigation Case #2026 - Incident Timeline'
"""

from datetime import datetime, timedelta


def generate_forensic_case_artifacts():
    """
    Returns an interconnected sequence of digital events simulating
    an investigation timeline (Browsing, Searching, Downloading, App Launches).
    """
    base_time = datetime.now() - timedelta(days=2)
    artifacts = []

    scenario_events = [
        # Day -2: Initial reconnaissance and web searches
        (
            base_time + timedelta(hours=9, minutes=15),
            "Google Chrome",
            "Web Search",
            "Search: 'python digital forensics projects'",
            "https://www.google.com/search?q=python+digital+forensics+projects",
            "google.com",
            "Visits: 1 | Typed: 1"
        ),
        (
            base_time + timedelta(hours=9, minutes=18),
            "Google Chrome",
            "Web Visit",
            "GitHub: Forensics Toolkits & Artifact Parsers",
            "https://github.com/topics/digital-forensics",
            "github.com",
            "Visits: 4 | Typed: 0"
        ),
        (
            base_time + timedelta(hours=10, minutes=5),
            "Microsoft Edge",
            "Web Visit",
            "College Examination Portal - Student Login",
            "https://exam.college.edu/login/student",
            "college.edu",
            "Visits: 2 | Typed: 1"
        ),
        (
            base_time + timedelta(hours=10, minutes=45),
            "Windows OS",
            "App / File Activity",
            "Accessed: visual_studio_code.exe",
            "C:\\Program Files\\Microsoft VS Code\\Code.exe",
            "Local System",
            "Type: Application / Executable"
        ),
        (
            base_time + timedelta(hours=11, minutes=12),
            "Windows OS",
            "App / File Activity",
            "Accessed: Project_Abstract_TraceLens.docx",
            "C:\\Users\\Student\\Documents\\College\\Project_Abstract_TraceLens.docx",
            "Local System",
            "Type: Document"
        ),
        # Day -1: Suspicious research & download
        (
            base_time + timedelta(days=1, hours=14, minutes=20),
            "Google Chrome",
            "Web Search",
            "Search: 'download wireshark packet analyzer'",
            "https://www.google.com/search?q=download+wireshark+packet+analyzer",
            "google.com",
            "Visits: 2 | Typed: 1"
        ),
        (
            base_time + timedelta(days=1, hours=14, minutes=25),
            "Google Chrome",
            "Download",
            "Downloaded: Wireshark-win64-setup.exe",
            "Path: C:\\Users\\Student\\Downloads\\Wireshark-win64-setup.exe",
            "wireshark.org",
            "Size: 78.5 MB"
        ),
        (
            base_time + timedelta(days=1, hours=14, minutes=35),
            "Windows OS",
            "App / File Activity",
            "Accessed: Wireshark-win64-setup.exe",
            "C:\\Users\\Student\\Downloads\\Wireshark-win64-setup.exe",
            "Local System",
            "Type: Application / Executable"
        ),
        (
            base_time + timedelta(days=1, hours=16, minutes=40),
            "Microsoft Edge",
            "Web Visit",
            "Stack Overflow: Extract Chrome SQLite database with Python",
            "https://stackoverflow.com/questions/15011703/extract-chrome-history-sqlite",
            "stackoverflow.com",
            "Visits: 6 | Typed: 0"
        ),
        (
            base_time + timedelta(days=1, hours=18, minutes=10),
            "Google Chrome",
            "Web Search",
            "Search: 'tkinter ttk table styling tutorial'",
            "https://www.google.com/search?q=tkinter+ttk+table+styling+tutorial",
            "google.com",
            "Visits: 3 | Typed: 1"
        ),
        (
            base_time + timedelta(days=1, hours=19, minutes=0),
            "Windows OS",
            "App / File Activity",
            "Accessed: TraceLens_Final_Presentation.pptx",
            "C:\\Users\\Student\\Documents\\TraceLens_Final_Presentation.pptx",
            "Local System",
            "Type: Document"
        ),
        (
            base_time + timedelta(days=1, hours=21, minutes=30),
            "Google Chrome",
            "Web Visit",
            "YouTube: Computer Science Engineering 1st Year Projects Showcase",
            "https://www.youtube.com/watch?v=sample1stYearProjects",
            "youtube.com",
            "Visits: 2 | Typed: 0"
        ),
        # Incognito / InPrivate Sessions (Forensic Traces)
        (
            base_time + timedelta(days=1, hours=22, minutes=10),
            "Chrome Incognito",
            "Incognito Activity",
            "Incognito Search: 'how to clear browser history and DNS cache'",
            "https://duckduckgo.com/?q=how+to+clear+browser+history+and+DNS+cache",
            "duckduckgo.com",
            "Session: Private / Incognito Mode | DNS Resolver Trace"
        ),
        (
            base_time + timedelta(days=1, hours=22, minutes=15),
            "Chrome Incognito",
            "Incognito Activity",
            "Incognito Visit: 'anonymous-proxy-list.org'",
            "https://anonymous-proxy-list.org/secure-browsing",
            "anonymous-proxy-list.org",
            "Session: Private / Incognito Mode | Host Recovered via OS DNS"
        ),
        (
            base_time + timedelta(days=1, hours=22, minutes=25),
            "Chrome Incognito",
            "Incognito Activity",
            "Incognito Download: 'bypass_exam_firewall_proxy.py'",
            "Path: C:\\Users\\Student\\Downloads\\bypass_exam_firewall_proxy.py",
            "github.com",
            "Session: Incognito Mode | Physical File Left on Disk (0.12 MB)"
        ),
        (
            base_time + timedelta(days=2, hours=0, minutes=40),
            "Edge InPrivate",
            "Incognito Activity",
            "InPrivate Visit: 'onion-directory-index.net'",
            "https://onion-directory-index.net/database",
            "onion-directory-index.net",
            "Session: InPrivate Session | DNS Resolver Host Trace"
        ),
        # Today: Final checks and submission
        (
            base_time + timedelta(days=2, hours=8, minutes=15),
            "Microsoft Edge",
            "Web Visit",
            "Python Official Docs: sqlite3 module",
            "https://docs.python.org/3/library/sqlite3.html",
            "python.org",
            "Visits: 5 | Typed: 1"
        ),
        (
            base_time + timedelta(days=2, hours=9, minutes=0),
            "Google Chrome",
            "Download",
            "Downloaded: TraceLens_Forensic_Report.pdf",
            "Path: C:\\Users\\Student\\Downloads\\TraceLens_Forensic_Report.pdf",
            "college.edu",
            "Size: 3.2 MB"
        ),
        (
            base_time + timedelta(days=2, hours=9, minutes=15),
            "Windows OS",
            "App / File Activity",
            "Accessed: TraceLens_Forensic_Report.pdf",
            "C:\\Users\\Student\\Downloads\\TraceLens_Forensic_Report.pdf",
            "Local System",
            "Type: Document"
        ),
        (
            base_time + timedelta(days=2, hours=11, minutes=45),
            "Google Chrome",
            "Web Visit",
            "GitHub Repository: TraceLens Project Submission",
            "https://github.com/TraceLens/tracelens-visualizer",
            "github.com",
            "Visits: 8 | Typed: 1"
        )
    ]

    for dt, source, category, title, details, domain, extra in scenario_events:
        artifacts.append({
            "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "dt": dt,
            "source": source,
            "category": category,
            "title": title,
            "details": details,
            "domain": domain,
            "extra": extra
        })

    # Sort descending by default
    artifacts.sort(key=lambda x: x["dt"], reverse=True)
    return artifacts
