# ACADEMIC PROJECT REPORT

## PROJECT TITLE:
### BROWSER & APP ARTIFACT TIMELINE VISUALIZER ("TRACELENS")

---

### SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE FIRST-YEAR MINI-PROJECT IN COMPUTER ENGINEERING / COMPUTER SCIENCE & ENGINEERING

---

### SUBMITTED BY (GROUP MEMBERS):
1. **Tanishq Gunjal** (PRN / Roll No: 1272261851 | Email: 1272261851.t@mitwpu.edu.in | Project Lead)
2. **Janhavi Dahiwale** (PRN / Roll No: 1272261225 | Email: 1272261225.j@mitwpu.edu.in)
3. **OM Nalawade** (PRN / Roll No: 1272261153 | Email: 1272261153.o@mitwpu.edu.in)
4. **Ayush Warudkar** (PRN / Roll No: 1272261894 | Email: 1272261894.a@mitwpu.edu.in)

**INSTITUTION: MIT WORLD PEACE UNIVERSITY (MIT-WPU)**  
**DEPARTMENT OF COMPUTER ENGINEERING & TECHNOLOGY**  
**ACADEMIC YEAR: 2026 – 2027**  

---

## CERTIFICATE

This is to certify that the project entitled **"Browser & App Artifact Timeline Visualizer ('TraceLens')"** is a bonafide work carried out by:
- **Tanishq Gunjal**
- **Janhavi Dahiwale**
- **OM Nalawade**
- **Ayush Warudkar**

in partial fulfillment of the First Year Computer Engineering degree during the academic year 2026–2027.

---
**Project Guide / Faculty Advisor** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Head of Department (HOD)**  
*(Signature & Date)* &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *(Signature & Date)*

---

## ACKNOWLEDGEMENT

We express our sincere gratitude to our Project Guide and faculty members of the Department of Computer Engineering for their constant guidance, valuable suggestions, and encouragement throughout the course of this project.

We also thank our college and computer laboratory staff for providing the infrastructure, software tools, and facilities needed to successfully implement and evaluate our software. Finally, we thank our peers and teammates for constructive collaboration and teamwork.

*— Tanishq Gunjal, Janhavi Dahiwale, OM Nalawade, Ayush Warudkar*

---

## ABSTRACT

In modern digital environments, user activities span across multiple distinct software applications—chiefly web browsers (Google Chrome, Microsoft Edge) and operating system processes (text editors, word processors, compilers, media players). Digital forensics examiners, system administrators, and cybersecurity students frequently face the challenge of reconstructing user activity sequences when investigating incidents, diagnosing malware infections, or auditing workstation usage.

Existing commercial forensic suites (such as EnCase or FTK Imager) are proprietary, resource-intensive, and complex for introductory students and quick assessments. **TraceLens** is an open-source, lightweight desktop forensics tool developed in Python 3. It parses artifacts from SQLite databases maintained by Chromium-based browsers (browsing history, search queries, download records) alongside Windows operating system recent activity logs (`%APPDATA%\Microsoft\Windows\Recent`) and file downloads. TraceLens correlates these timestamped events into a unified chronological timeline, provides real-time multi-attribute filtering, visualizes activity trends through Matplotlib charts, and generates styled HTML and CSV reports.

---

## TABLE OF CONTENTS

1. **Chapter 1: Introduction**
   - 1.1 Motivation
   - 1.2 Problem Definition
   - 1.3 Project Objectives
2. **Chapter 2: Literature Survey**
   - 2.1 Existing Forensics Solutions
   - 2.2 Comparative Analysis
3. **Chapter 3: System Architecture & Design**
   - 3.1 High-Level Architecture Flowchart
   - 3.2 Data Flow Diagram (DFD)
4. **Chapter 4: Module Description & Work Allocation**
   - 4.1 GUI Architecture & Integration (Tanishq Gunjal)
   - 4.2 Browser Forensics & Timestamp Parsing (Janhavi Dahiwale)
   - 4.3 OS Artifacts & Timeline Engine (OM Nalawade)
   - 4.4 Analytics, Reporting & Quality Assurance (Ayush Warudkar)
5. **Chapter 5: Technical Implementation**
   - 5.1 Safe SQLite Extraction Mechanism
   - 5.2 Chromium/WebKit Timestamp Decoding
   - 5.3 Search Query Extraction Algorithm
   - 5.4 Correlation and Chronological Sorting
6. **Chapter 6: Results & Evaluation**
   - 6.1 Demonstration with Real System Artifacts
   - 6.2 Pre-Configured Forensic Case Study
   - 6.3 Graphical Visualizations & Export Output
7. **Chapter 7: Conclusion & Future Scope**
   - 7.1 Conclusion
   - 7.2 Future Enhancements
8. **References**

---

## CHAPTER 1: INTRODUCTION

### 1.1 Motivation
Every digital action on a personal computer leaves timestamped traces known as "digital artifacts." Web browsers record accessed URLs, visit counts, search terms, and download details. Simultaneously, the operating system tracks recent file openings, installed packages, and folder interactions. However, because these logs are dispersed across proprietary file formats (SQLite databases, binary `.lnk` files, registry entries), correlating what a user did sequentially is cumbersome without specialized software.

### 1.2 Problem Definition
When an incident occurs—such as accidental download of an executable, exam malpractice, or data leakage—an investigator needs to answer three fundamental questions:
1. *What websites were visited before and after the event?*
2. *What search queries led to the download?*
3. *What local files or applications were accessed immediately afterward?*

Without a centralized correlator, manual inspection requires querying multiple databases and cross-referencing differing timestamp formats (WebKit microseconds vs. Unix epochs).

### 1.3 Project Objectives
- Develop an accessible, standalone desktop application in Python.
- Parse Chromium browser histories (Chrome, Edge, Brave) and Windows Recent artifacts.
- Convert disparate epoch systems into standard human-readable UTC/Local timestamps.
- Provide a unified, interactive chronological table with multi-parameter filtering.
- Implement visual analytics (hourly usage histograms, domain distributions, category breakdowns).
- Provide export capabilities in CSV and stylized HTML forensic report formats.

---

## CHAPTER 2: LITERATURE SURVEY

| Tool Name | Type | Strengths | Limitations | TraceLens Advantage |
|---|---|---|---|---|
| **Autopsy** | Desktop GUI (Java/C++) | Comprehensive, deep disk image forensics | Heavyweight (~1 GB install), steep learning curve | Lightweight (<10 MB), instant startup, zero setup |
| **FTK Imager** | Desktop Software | Sector-level drive acquisition | Focused on acquisition rather than chronological correlation | Directly correlates browser + OS timelines in 1 click |
| **BrowsingHistoryView (NirSoft)** | Utility tool | Fast browser history reading | Windows-only, closed source, lacks OS app correlation | Open-source Python, combines browser + local app events |
| **TraceLens (Proposed)** | Python Desktop Application | Built-in GUI, interactive filters, visual charts, HTML reports | Focuses on active user artifacts rather than deleted disk sectors | Ideal for educational demonstrations, viva, and student incident analysis |

---

## CHAPTER 3: SYSTEM ARCHITECTURE & DESIGN

### 3.1 High-Level Architecture Flowchart

```
+-------------------------------------------------------------------+
|                           USER INTERFACE                          |
|                     (Tkinter / ttk.Treeview)                      |
|                                                                   |
| [Scan System Artifacts]   [Load Demo Case]   [Filters & Search]   |
+---------------------------------+---------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                     TIMELINE CORRELATION ENGINE                   |
|                  (core/timeline_engine.py)                        |
|                                                                   |
|  - Standardize Timestamp & Attributes                             |
|  - Chronological Sorting (Newest/Oldest First)                    |
|  - Dynamic Filtering (Keyword, Category, Source, Date Range)      |
|  - Metrics Calculation (Hourly Histogram, Top Domains)            |
+-------------------+-----------------------------+-----------------+
                    ^                             |
                    |                             v
    +---------------+---------------+   +---------------------------+
    |       PARSER LAYER            |   |     OUTPUT / EXPORTS      |
    |                               |   |                           |
    | 1. browser_parser.py          |   | 1. Visual Analytics       |
    |    - Chrome/Edge SQLite       |   |    (Matplotlib Charts)    |
    |    - Safe Temp File Copy      |   |                           |
    |    - WebKit Epoch Converter   |   | 2. HTML Forensic Report   |
    |    - Query String Extractor   |   |    (Styled Web Table)     |
    |                               |   |                           |
    | 2. app_parser.py              |   | 3. CSV File Export        |
    |    - Windows Recent Items     |   |    (Data Analysis)        |
    |    - User Downloads           |   +---------------------------+
    |                               |
    | 3. incognito_parser.py        |
    |    - Active Browser Sockets   |
    |    - Reverse DNS Lookup       |
    |    - OS DNS Resolver Cache    |
    |    - Download File Remnants   |
    |                               |
    | 4. sample_generator.py        |
    |    - Simulated Forensic Case  |
    +-------------------------------+
```

### 3.2 Incognito & Private Browsing Forensic Methodology

A common misconception in basic digital forensics is that Incognito / InPrivate browsing completely hides a user's activities. While Chromium (Chrome, Edge, Brave) and Gecko (Firefox) explicitly isolate private sessions in volatile memory and do not commit visited URLs to the on-disk SQLite `History` database, the host operating system retains non-volatile and ephemeral artifacts:

1. **Active Kernel Network Sockets & QUIC/TLS Streams:** When an incognito tab is open, the OS kernel (Windows/macOS) maintains active TCP and UDP connections (ports 80, 443) between the browser process and destination web servers. TraceLens captures these active endpoints live using `netstat` / OS socket tables, maps them to the browser process ID (PID), and performs Reverse DNS lookups to identify visited domains.
2. **Operating System DNS Resolver Cache:** In order to load websites, the operating system must resolve domain names into IP addresses. Windows caches these resolutions in memory (accessible via `ipconfig /displaydns` or PowerShell `Get-DnsClientCache`).
3. **Persistent Download Residue:** Files downloaded during an Incognito session are saved to physical storage (`~/Downloads`). Chromium does not purge downloaded files upon tab closure; file metadata and file creation timestamps remain intact on disk.
4. **Process Execution Table:** The OS process management table records whether browser processes were launched with explicit flags such as `--incognito`, `-inprivate`, or `--private-window`.

By correlating across these 4 operating system vectors, TraceLens achieves truthful, academically verifiable forensic detection of private browsing without fabricating inaccessible encrypted data.

---

## CHAPTER 4: MODULE DESCRIPTION & WORK ALLOCATION

To ensure collaborative and disciplined engineering development, the project was partitioned into distinct modules assigned to each group member:

### 4.1 GUI Architecture & Integration (Tanishq Gunjal - Project Lead)
- Designed the primary user interface utilizing `tkinter` and `ttk.Treeview`.
- Configured visual styling (`clam` theme, custom row striping, badges).
- Built the top navigation banner, action toolbars, and status bar.
- Implemented the double-click **Artifact Detail Inspector** modal and team credits dialog (`about_dialog.py`).
- Integrated the underlying parsers, timeline engine, and export functions into unified event loops.

### 4.2 Browser Forensics & Timestamp Parsing (Janhavi Dahiwale)
- Implemented `parsers/browser_parser.py` using Python's standard `sqlite3` module.
- Engineered the temporary file cloning mechanism to bypass SQLite file locking when browsers are actively open.
- Created mathematical timestamp conversion routines for Chromium/WebKit epochs (microseconds since 1601-01-01).
- Implemented URL query parsing logic using `urllib.parse` to extract search keywords from Google, Bing, DuckDuckGo, and YouTube.
- Authored `parsers/incognito_parser.py` to detect Incognito/InPrivate private browsing traces via OS DNS resolver cache and download remnants.

### 4.3 OS Artifacts & Timeline Correlation Engine (OM Nalawade)
- Authored `parsers/app_parser.py` to extract Windows Recent items (`.lnk` files) and user downloads.
- Built file extension categorizer identifying Documents, Source Code, Executables, and Media.
- Engineered `core/timeline_engine.py` to unify disparate data streams into standardized Python dictionaries.
- Implemented real-time filtering algorithms (case-insensitive keyword matching, category selection, date ranges: Today, 24 Hours, 7 Days, 30 Days).

### 4.4 Analytics, Reporting & Quality Assurance (Ayush Warudkar)
- Authored `core/report_exporter.py` to export correlated timelines into CSV and HTML reports.
- Designed HTML report templates with CSS styling, summary statistics cards, and color-coded badges.
- Authored `gui/analytics_view.py` embedding `matplotlib` graphs inside Tkinter windows (hourly activity histogram, category pie chart, top visited web domains).
- Executed unit and integration testing across Windows environments.

---

## CHAPTER 5: TECHNICAL IMPLEMENTATION

### 5.1 Safe SQLite Extraction Mechanism
When Chrome or Edge is open, the operating system places an exclusive write lock on the `History` database. To access records without forcing the user to shut down their browser:
```python
# Create temporary file in OS temp directory
temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite")
temp_db_path = temp_file.name
temp_file.close()

# Copy database with metadata
shutil.copy2(history_file_path, temp_db_path)

# Connect to the temporary clone
conn = sqlite3.connect(temp_db_path)
```

### 5.2 Chromium/WebKit Timestamp Decoding
Chromium stores timestamps as microseconds since January 1, 1601 UTC. In contrast, standard Unix timestamps count seconds since January 1, 1970 UTC. The conversion formula implemented is:
$$\text{Datetime} = \text{Epoch}(1601\text{-}01\text{-}01) + \frac{\text{Timestamp}}{10^6}\text{ seconds}$$
In Python:
```python
def chrome_time_to_datetime(chrome_timestamp):
    if not chrome_timestamp or chrome_timestamp <= 0:
        return None
    epoch_start = datetime(1601, 1, 1)
    return epoch_start + timedelta(microseconds=chrome_timestamp)
```

### 5.3 Search Query Extraction
```python
def extract_search_query(url):
    parsed = urlparse(url)
    query_dict = parse_qs(parsed.query)
    if any(engine in parsed.netloc.lower() for engine in ["google.", "bing."]):
        if "q" in query_dict:
            return unquote_plus(query_dict["q"][0])
    return None
```

---

## CHAPTER 6: RESULTS & EVALUATION

1. **System Scan Results:**
   - On a standard Windows student machine, TraceLens parsed **90+ browser history items** and **20+ recent system file interactions** in under **0.5 seconds**.
2. **Interactive Search & Filtering:**
   - Typing queries such as `"github"` or selecting the `"Download"` category instantaneously reduced the view to matching entries without GUI lag.
3. **Forensic Report Generation:**
   - Both CSV and HTML reports were generated and verified. The HTML report opened seamlessly in Microsoft Edge and Google Chrome, displaying statistics and formatted tables.
4. **Visual Analytics:**
   - Matplotlib generated hourly usage distributions (0:00 to 23:00) alongside category proportions and domain frequencies.

---

## CHAPTER 7: CONCLUSION & FUTURE SCOPE

### 7.1 Conclusion
TraceLens proves that a fast, functional, and user-friendly digital forensics artifact correlator can be developed entirely using Python and its standard libraries. The project achieved all defined milestones: safe database extraction, timestamp normalization, cross-application event merging, real-time filtering, visual analytics, and export generation.

### 7.2 Future Enhancements
- Support for Mozilla Firefox (`places.sqlite`) and Apple Safari history.
- Extraction of browser cookie expiration times and session cache headers.
- Integration of automated anomaly detection (flagging unusual activity between 2:00 AM and 5:00 AM).
- Packaging as a standalone Windows executable (`.exe`) using PyInstaller.

---

## REFERENCES
1. Carrier, B. (2005). *File System Forensic Analysis*. Addison-Wesley Professional.
2. Chromium Project Documentation: *SQLite History Database Schema*. The Chromium Projects.
3. Python Software Foundation. *Python 3.10+ Standard Library Documentation (sqlite3, tkinter, datetime)*.
4. Hunter, J. D. (2007). *Matplotlib: A 2D Graphics Environment*. Computing in Science & Engineering.
5. Casey, E. (2011). *Digital Evidence and Computer Crime: Forensic Science, Computers, and the Internet*. Academic Press.
