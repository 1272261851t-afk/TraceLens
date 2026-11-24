# TraceLens: Browser & App Artifact Timeline Visualizer 🔍

> **A First-Year Computer Engineering Mini-Project**  
> Academic Year: 2026–2027  
> Technology Stack: Python 3, Tkinter GUI, SQLite3, Matplotlib, HTML5/CSS3  

---

## 👥 Project Group Members & Work Distribution

| # | Member Name | PRN / Roll No | Official College Email | Role | Primary Modules & Contributions |
|---|---|---|---|---|---|
| 1 | **Tanishq Gunjal** | 1272261851 | `1272261851.t@mitwpu.edu.in` | **Project Leader** | GUI Architecture (`gui/app_window.py`), Event Handling, Layout & Integration |
| 2 | **Janhavi Dahiwale** | 1272261225 | `1272261225.j@mitwpu.edu.in` | **Core Developer** | Browser Artifact Parser (`parsers/browser_parser.py`), SQLite DB Extraction & Timestamps |
| 3 | **OM Nalawade** | 1272261153 | `1272261153.o@mitwpu.edu.in` | **Core Developer** | App Artifacts (`parsers/app_parser.py`), File Activity & Timeline Engine (`core/timeline_engine.py`) |
| 4 | **Ayush Warudkar** | 1272261894 | `1272261894.a@mitwpu.edu.in` | **Core Developer** | Visual Analytics (`gui/analytics_view.py`), HTML/CSV Exporters (`core/report_exporter.py`) & Testing |

---

## 📌 Project Overview & Problem Statement

Modern computer users spend hours switching between web browsers (Google Chrome, Microsoft Edge) and desktop software (Word, VS Code, media players). When troubleshooting system incidents, investigating security anomalies, or reviewing daily activity, finding out **what happened in chronological order** is extremely difficult because every browser and application stores logs in different, isolated formats.

**TraceLens** solves this problem by collecting, parsing, and normalizing disparate digital artifacts into a single, unified, interactive chronological timeline. It enables users, students, and investigators to see exactly what web searches were conducted, which websites were visited, what files were downloaded, and which applications were launched at any given minute.

---

## 🚀 Key Features

1. **Multi-Source Artifact Extraction:**
   - **Web Browsers:** Extracts browsing history, visit counts, and downloads from Google Chrome, Microsoft Edge, and Brave.
   - **Search Query Detection:** Automatically parses query strings from Google, Bing, DuckDuckGo, Yahoo, and YouTube (`?q=`, `search_query=`).
   - **Windows Application Activity:** Scans Windows Recent shortcuts (`%APPDATA%\Microsoft\Windows\Recent`) and User Downloads (`%USERPROFILE%\Downloads`).
   - **Safe Database Parsing:** Automatically copies locked browser SQLite databases to a temporary directory to prevent file locking conflicts while browsers are running.

2. **Interactive Timeline Visualizer:**
   - Built with Python's native `tkinter` and `ttk.Treeview`.
   - Real-time search by keyword (title, URL, domain, or category).
   - Filtering by Category (`Web Visit`, `Web Search`, `Download`, `App / File Activity`).
   - Filtering by Source (`Google Chrome`, `Microsoft Edge`, `Windows OS`, `Downloads Folder`).
   - Pre-set Timeframe Filters (`All Time`, `Today`, `Last 24 Hours`, `Last 7 Days`, `Last 30 Days`).
   - Chronological Sorting (Newest First or Oldest First).

3. **Artifact Detail Inspector:**
   - Double-clicking any timeline entry opens an inspection dialog showing complete URLs, file system paths, visit timestamps, and attributes, with a one-click **"Copy Details"** button.

4. **Visual Analytics & Forensics Metrics:**
   - Embedded Matplotlib charts:
     - 📊 **Activity by Hour of the Day (00:00 to 23:00)**: Visualizes peak computer usage hours.
     - 🥧 **Artifacts by Category**: Breakdown of web browsing vs downloads vs file activities.
     - 📈 **Top Visited Web Domains**: Identifies most frequented websites.

5. **Export & Reporting:**
   - 📄 **Stylized HTML Forensic Report**: Generates an executive report with summary metric cards, domain frequency tables, and an interactive colored timeline table.
   - 📑 **CSV Export**: Standard spreadsheet export compatible with Excel, Google Sheets, or data science tools.

6. **Pre-Bundled Demo Forensic Case:**
   - Includes a realistic simulated incident investigation case ("Cyber Investigation Case #2026") so evaluators and teachers can test the full capabilities of TraceLens instantly in college labs without touching local browser data.

7. **🕵️ Incognito & Private Browsing Forensic Traces:**
   - Detects and correlates traces left during private browsing sessions:
     - **OS DNS Resolver Cache:** The operating system still resolves and caches domain names accessed during incognito navigation.
     - **Physical Downloads:** Files downloaded in incognito remain on the physical file system with valid creation timestamps.
     - **Dedicated UI Filter:** Includes a 1-click **"🕵️ Incognito Only"** filter button and distinct violet row tagging in the timeline table.

---

## 📁 Project Directory Structure

```text
TraceLens/
│── main.py                   # Main project entry point & console banner
│── run.bat                   # 1-click Windows batch runner
│── requirements.txt          # Python external dependencies (matplotlib)
│── README.md                 # Project documentation & viva guide
│── PROJECT_REPORT.md         # Formal academic college project report
│
├── parsers/                  # Extraction modules
│   ├── __init__.py
│   ├── browser_parser.py     # Chrome & Edge SQLite parser (Janhavi Dahiwale)
│   ├── app_parser.py         # Windows Recent files & downloads parser (OM Nalawade)
│   └── sample_generator.py   # Pre-configured demo case study (Tanishq & OM)
│
├── core/                     # Data processing engine
│   ├── __init__.py
│   ├── timeline_engine.py    # Merging, sorting & filtering logic (OM & Tanishq)
│   └── report_exporter.py    # HTML & CSV report generator (Ayush Warudkar)
│
├── gui/                      # Tkinter User Interface
│   ├── __init__.py
│   ├── app_window.py         # Main Tkinter desktop application (Tanishq Gunjal)
│   ├── analytics_view.py     # Matplotlib charts window (Ayush Warudkar)
│   └── about_dialog.py       # Group credits & project info dialog (Tanishq Gunjal)
│
└── data/                     # Generated reports and exports
```

---

## 🛠️ System Requirements & Setup

### Prerequisites
- **Operating System:** Windows 10 or Windows 11
- **Python Version:** Python 3.8 or higher (tested on Python 3.10+)
- **Standard Libraries Used:** `tkinter`, `sqlite3`, `csv`, `datetime`, `urllib`, `shutil`, `tempfile` (all included with standard Python installation).

### Installation Steps

1. **Clone or Download the Project:**
   Extract the `TraceLens` folder to your computer.

2. **Install Required Package:**
   Open Command Prompt or PowerShell in the project directory and run:
   ```cmd
   pip install -r requirements.txt
   ```
   *(Only `matplotlib` is required for charts; all other libraries are built-in!)*

3. **Run TraceLens:**
   - **Method 1 (Easiest):** Double-click `run.bat`
   - **Method 2 (Command Line):**
     ```cmd
     python main.py
     ```

---

## 🖥️ How to Use TraceLens (Viva / Demo Walkthrough)

1. **Start the App:** Run `main.py` or double-click `run.bat`. TraceLens will launch with the pre-loaded **Demo Forensic Case** so the table immediately displays events.
2. **Scan Live Machine:** Click **"Scan System Artifacts"** on the top right to extract actual Chrome, Edge, and Windows recent history from the current PC.
3. **Filter Events:**
   - Type `"wireshark"` or `"google"` in the **Search** box.
   - Select `"Download"` from the **Category** dropdown to see only downloaded files.
   - Select `"Today"` or `"Last 7 Days"` to narrow down timeframes.
4. **Inspect an Event:** Double-click any row to view the full URL, target path, and metadata in the **Artifact Detail Inspector**.
5. **View Charts:** Click **"Visual Analytics (Charts)"** on the bottom right to see hourly activity distribution, category pie charts, and top domains.
6. **Generate Report:** Click **"Export HTML Report"** to generate a forensics investigation report and view it in your browser.
7. **View Credits:** Click **"About Team"** to display group members and individual roles.

---

## 🎓 Viva-Voce Questions & Answers (For Practical Exam)

Here are the questions professors and external examiners typically ask for 1st-year Python projects:

### Q1: What is the main objective of TraceLens?
**Ans:** To correlate disparate digital artifacts from web browsers (Chrome, Edge) and the Windows operating system (Recent files, Downloads) into a unified chronological timeline for digital forensics and activity monitoring.

### Q2: Why did you copy the browser SQLite database to a temporary directory before reading it?
**Ans:** When Google Chrome or Microsoft Edge is running, the operating system locks the `History` database file to prevent concurrent modifications. Attempting to open it directly throws `sqlite3.OperationalError: database is locked`. Copying it to a temporary location using `shutil.copy2` circumvents this lock safely.

### Q3: How does Chrome store visit timestamps, and how did you convert them in Python?
**Ans:** Chrome uses WebKit/Chromium timestamps, which count the number of microseconds elapsed since **January 1, 1601 UTC**. In Python, we convert this using:
```python
datetime(1601, 1, 1) + timedelta(microseconds=chrome_timestamp)
```

### Q4: How did you extract search keywords from web URLs?
**Ans:** We used Python's `urllib.parse.urlparse` and `parse_qs`. Search engines pass query keywords in URL query parameters (e.g., `?q=` for Google and Bing, `search_query=` for YouTube). Our parser extracts and decodes these strings using `unquote_plus`.

### Q5: What data structures did you use in the Timeline Engine?
**Ans:** We used Python `list` of `dict` objects for standardized artifacts, `datetime` objects for chronological sorting with `sort(key=lambda x: x["dt"])`, and `collections.Counter` to compute frequency distributions for domains and categories.

### Q6: Why did you choose Tkinter over a web framework?
**Ans:** Tkinter is the standard built-in GUI library for Python. It requires zero external web server setup, runs natively on Windows desktops, and provides `ttk.Treeview` which is ideal for tabular timeline data.

### Q7: Can digital forensics detect activity conducted in Incognito / Private Browsing mode?
**Ans:** Yes! While Chromium browsers do not commit URLs to the on-disk `History.sqlite` database in Incognito mode, private browsing is not completely invisible. TraceLens captures OS-level evidence:
1. **Active Kernel Network Sockets & QUIC/TLS Streams:** When an incognito tab is open, the OS kernel maintains active TCP and UDP sockets (ports 80, 443) between the browser PID and remote servers. TraceLens captures these endpoints live and resolves hostnames via Reverse DNS.
2. **OS DNS Resolver Cache:** The operating system caches domain-to-IP resolutions (accessible via `ipconfig /displaydns` or PowerShell `Get-DnsClientCache`).
3. **Physical File Downloads:** Files downloaded inside an incognito session remain on disk in `~/Downloads` with intact creation and modification timestamps.
4. **Process Execution Table:** The OS process manager records whether the browser was launched with `--incognito` or `-inprivate` switches.

### Q8: Does TraceLens claim to read incognito history from the browser's SQLite database?
**Ans:** No! Claiming to read incognito history from SQLite would be technically and forensically false, because Chromium's `OffTheRecordProfile` explicitly prevents writing private history records to disk. TraceLens strictly recovers truthful evidence from operating system network sockets, DNS cache, and file system remnants, exactly as done in professional digital forensics investigations (NIST SP 800-86).

---

## 📜 Academic Declaration

This project titled **"Browser & App Artifact Timeline Visualizer (TraceLens)"** has been designed and implemented by **Tanishq Gunjal, Janhavi Dahiwale, OM Nalawade, and Ayush Warudkar** as a First-Year Computer Engineering mini-project.
