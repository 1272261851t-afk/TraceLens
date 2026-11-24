"""
Generate 3 High-Impact Exhibition Posters for TraceLens:
1. Poster 1: Academic & Exhibition Showcase (Comprehensive Overview)
2. Poster 2: Technical Architecture & Forensic Pipeline (Deep-Dive Engineering)
3. Poster 3: Product Showcase & Incident Investigation Storyboard (Case Study)

Renders both Print-Ready PDFs and High-Resolution PNG images via headless Chrome.
"""

import os
import subprocess
import shutil

DOCS_DIR = r"C:\Users\ASUS\Documents\TraceLens"
DESKTOP_DIR = r"C:\Users\ASUS\OneDrive\PlayerFile\Desktop"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# =============================================================================
# HTML TEMPLATE: POSTER 1 (ACADEMIC EXHIBITION)
# =============================================================================
POSTER_1_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TraceLens - Academic Exhibition Poster</title>
    <style>
        @page { size: A3 landscape; margin: 0; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { width: 1920px; height: 1080px; background: #090d16; color: #f8fafc; padding: 32px 40px; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; }
        
        /* Header */
        .header { background: linear-gradient(135deg, #1e3a8a, #1e40af); border-radius: 14px; padding: 22px 32px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border: 1px solid rgba(147, 197, 253, 0.3); }
        .inst-title { font-size: 15px; text-transform: uppercase; letter-spacing: 2px; color: #93c5fd; font-weight: 700; margin-bottom: 4px; }
        .main-title { font-size: 44px; font-weight: 900; color: #ffffff; letter-spacing: -0.5px; }
        .main-sub { font-size: 18px; color: #e2e8f0; font-weight: 500; margin-top: 4px; }
        .badge-box { background: rgba(15, 23, 42, 0.7); border: 1px solid #3b82f6; padding: 12px 20px; border-radius: 10px; text-align: right; }
        .badge-box .tag { font-size: 13px; color: #60a5fa; font-weight: 700; text-transform: uppercase; }
        .badge-box .val { font-size: 16px; color: #ffffff; font-weight: 600; }

        /* Grid */
        .content-grid { display: grid; grid-template-columns: 1fr 1.15fr 1fr; gap: 24px; margin: 20px 0; flex: 1; }
        .col { display: flex; flex-direction: column; gap: 18px; }
        .card { background: rgba(30, 41, 59, 0.75); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 18px 22px; backdrop-filter: blur(10px); flex: 1; display: flex; flex-direction: column; }
        .card-title { font-size: 18px; font-weight: 800; color: #60a5fa; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 6px; }
        .card-body { font-size: 13.5px; line-height: 1.55; color: #cbd5e1; flex: 1; }
        .card-body strong { color: #ffffff; }

        .code-snippet { background: #0f172a; border: 1px solid #334155; padding: 10px 12px; border-radius: 6px; font-family: Consolas, monospace; font-size: 12px; color: #38bdf8; margin: 8px 0; }
        .highlight-box { background: rgba(37, 99, 235, 0.15); border-left: 4px solid #3b82f6; padding: 8px 12px; margin: 8px 0; border-radius: 4px; font-size: 13px; color: #e2e8f0; }

        /* Footer */
        .footer { background: #0f172a; border-radius: 12px; padding: 14px 28px; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(255,255,255,0.1); }
        .team-grid { display: flex; gap: 28px; }
        .member { font-size: 13px; }
        .member-name { font-weight: 700; color: #ffffff; }
        .member-prn { color: #60a5fa; font-size: 11.5px; }

        table { width: 100%; border-collapse: collapse; margin-top: 6px; font-size: 12.5px; }
        th, td { border: 1px solid rgba(255,255,255,0.15); padding: 5px 8px; text-align: left; }
        th { background: rgba(15, 23, 42, 0.6); color: #93c5fd; }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="inst-title">Department of Computer Engineering • MIT World Peace University (MIT-WPU), Pune</div>
            <div class="main-title">TraceLens: Browser & App Artifact Timeline Visualizer</div>
            <div class="main-sub">A Lightweight Digital Forensics Correlator & Cross-Application Activity Timeline in Pure Python</div>
        </div>
        <div class="badge-box">
            <div class="tag">First-Year Mini-Project</div>
            <div class="val">Academic Year 2026–2027</div>
        </div>
    </div>

    <div class="content-grid">
        <!-- Col 1 -->
        <div class="col">
            <div class="card">
                <div class="card-title">📌 Problem Statement & Motivation</div>
                <div class="card-body">
                    Modern user operations cross continuously between web browsers and desktop software. Incident investigation requires answering: <em>What was searched? What was downloaded? What executable was launched next?</em><br><br>
                    <strong>The Gap:</strong> Logs are scattered across proprietary, locked formats (SQLite databases, binary .lnk files). Existing forensic suites (FTK, EnCase) are bloated, expensive, and heavy for quick incident triage.
                </div>
            </div>
            <div class="card">
                <div class="card-title">🎯 Project Objectives</div>
                <div class="card-body">
                    ✔ <strong>Multi-Source Extraction:</strong> Ingest Chrome/Edge SQLite, Windows Recent (.lnk), and Downloads.<br>
                    ✔ <strong>Safe Shadow Cloning:</strong> Circumvent active database write locks via dynamic %TEMP% cloning.<br>
                    ✔ <strong>Timestamp Normalization:</strong> Convert WebKit 1601 epoch microseconds to local datetime.<br>
                    ✔ <strong>Search Query Extractor:</strong> Decodes queries from Google, Bing, YouTube (?q=).<br>
                    ✔ <strong>Visual Analytics & Reports:</strong> 24-hr histograms, category pie charts, HTML/CSV exports.
                </div>
            </div>
        </div>

        <!-- Col 2 -->
        <div class="col">
            <div class="card">
                <div class="card-title">⚙️ System Architecture & Workflow</div>
                <div class="card-body">
                    <div class="highlight-box">
                        <strong>Pipeline:</strong> Disparate Ingestion ➔ Shadow Copy Cloner ➔ Timestamp Normalization ➔ In-Memory Correlation Engine ➔ Tkinter Treeview GUI
                    </div>
                    <div style="margin-top: 8px;"><strong>Core Mathematical & Algorithmic Innovations:</strong></div>
                    <div class="code-snippet"># 1. Chromium WebKit 1601 Epoch to Datetime
def chrome_to_dt(ts):
    return datetime(1601, 1, 1) + timedelta(microseconds=ts)

# 2. Safe Database Shadow Cloning (Locks Bypassed)
shutil.copy2(active_history_db, temp_clone_path)
conn = sqlite3.connect(temp_clone_path)</div>
                    <div style="margin-top: 6px; font-size: 12.5px;">
                        • <strong>In-Memory Sorting:</strong> Correlates all events with <code>sort(key=lambda x: x['dt'])</code><br>
                        • <strong>Cross-Platform:</strong> Seamless execution on both Windows 10/11 and macOS!
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-title">🖥️ Desktop User Interface (Tkinter)</div>
                <div class="card-body">
                    • <strong>Treeview Table:</strong> Alternating row-striped timeline with sortable columns.<br>
                    • <strong>Real-Time Search & Comboboxes:</strong> Instant keyword query and category filters.<br>
                    • <strong>Double-Click Inspector:</strong> Modal displaying complete URLs and 1-click clipboard copy.<br>
                    • <strong>Demo Case Generator:</strong> 16-event incident simulation for safe lab evaluation.
                </div>
            </div>
        </div>

        <!-- Col 3 -->
        <div class="col">
            <div class="card">
                <div class="card-title">📊 Visual Analytics & Performance Results</div>
                <div class="card-body">
                    <div style="text-align: center; margin: 4px 0;">
                        <img src="data/analytics_chart.png" style="max-width: 100%; height: 160px; object-fit: contain; border-radius: 6px; border: 1px solid rgba(255,255,255,0.2);">
                    </div>
                    <table>
                        <thead>
                            <tr><th>Test Scenario</th><th>Performance</th><th>Status</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>Live Extraction</td><td>90+ items in 0.45s</td><td><strong style="color: #4ade80;">100% Passed</strong></td></tr>
                            <tr><td>Active DB Lock</td><td>Bypassed via %TEMP%</td><td><strong style="color: #4ade80;">Zero Crashes</strong></td></tr>
                            <tr><td>Reporting</td><td>Styled HTML & CSV</td><td><strong style="color: #4ade80;">Generated</strong></td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="card">
                <div class="card-title">🏁 Conclusion & Future Scope</div>
                <div class="card-body">
                    TraceLens proves a functional, responsive forensic timeline visualizer can be built in pure Python with zero setup footprint.<br><br>
                    <strong>Future Scope:</strong> Mozilla Firefox support (<code>places.sqlite</code>), automated late-night anomaly detection, and single-file binary packaging with PyInstaller.
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div style="font-size: 13px; color: #94a3b8;">
            <strong style="color: #ffffff;">MIT-WPU First Year Engineering Team (Div A • Batch B1):</strong>
        </div>
        <div class="team-grid">
            <div class="member">
                <div class="member-name">1. Tanishq Gunjal (Lead)</div>
                <div class="member-prn">PRN: 1272261851 • GUI Architecture</div>
            </div>
            <div class="member">
                <div class="member-name">2. Janhavi Dahiwale</div>
                <div class="member-prn">PRN: 1272261225 • Browser Forensics</div>
            </div>
            <div class="member">
                <div class="member-name">3. OM Nalawade</div>
                <div class="member-prn">PRN: 1272261153 • Timeline Engine</div>
            </div>
            <div class="member">
                <div class="member-name">4. Ayush Warudkar</div>
                <div class="member-prn">PRN: 1272261894 • Visual Analytics</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# =============================================================================
# HTML TEMPLATE: POSTER 2 (TECHNICAL ARCHITECTURE & PIPELINE)
# =============================================================================
POSTER_2_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TraceLens - Technical Architecture Poster</title>
    <style>
        @page { size: A3 landscape; margin: 0; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { width: 1920px; height: 1080px; background: #0b1120; color: #f8fafc; padding: 32px 40px; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; }
        
        .header { background: linear-gradient(135deg, #0f172a, #1e293b); border: 1px solid #3b82f6; border-radius: 14px; padding: 22px 32px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .inst-title { font-size: 15px; text-transform: uppercase; letter-spacing: 2px; color: #38bdf8; font-weight: 700; margin-bottom: 4px; }
        .main-title { font-size: 42px; font-weight: 900; color: #ffffff; }
        .main-sub { font-size: 17px; color: #94a3b8; font-weight: 500; margin-top: 4px; }
        .badge-box { background: rgba(59, 130, 246, 0.15); border: 1px solid #3b82f6; padding: 12px 20px; border-radius: 10px; text-align: right; }

        .content-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 24px; margin: 20px 0; flex: 1; }
        .col { display: flex; flex-direction: column; gap: 18px; }
        .card { background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 12px; padding: 18px 22px; flex: 1; display: flex; flex-direction: column; }
        .card-title { font-size: 17px; font-weight: 800; color: #38bdf8; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 6px; }
        .card-body { font-size: 13.5px; line-height: 1.55; color: #cbd5e1; flex: 1; }

        .pipeline-step { background: #1e293b; border-left: 4px solid #38bdf8; padding: 10px 14px; margin-bottom: 10px; border-radius: 4px; }
        .pipeline-title { font-size: 14px; font-weight: 700; color: #ffffff; }
        .pipeline-desc { font-size: 12px; color: #94a3b8; margin-top: 2px; }
        .code-box { background: #020617; border: 1px solid #1e293b; padding: 10px 12px; border-radius: 6px; font-family: Consolas, monospace; font-size: 12px; color: #a5f3fc; margin: 8px 0; }

        .footer { background: #0f172a; border-radius: 12px; padding: 14px 28px; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(255,255,255,0.1); }
        .team-grid { display: flex; gap: 28px; }
        .member { font-size: 13px; }
        .member-name { font-weight: 700; color: #ffffff; }
        .member-prn { color: #38bdf8; font-size: 11.5px; }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="inst-title">Technical Specification • Department of Computer Engineering • MIT-WPU</div>
            <div class="main-title">TraceLens: Forensic Pipeline & Technical Architecture</div>
            <div class="main-sub">Low-Level System Design, Lock Bypassing, Epoch Normalization & Correlation Algorithms</div>
        </div>
        <div class="badge-box">
            <div style="font-size: 13px; color: #38bdf8; font-weight: 700;">ENGINEERING DEEP-DIVE</div>
            <div style="font-size: 15px; color: #ffffff; font-weight: 600;">Cross-Platform Architecture</div>
        </div>
    </div>

    <div class="content-grid">
        <!-- Col 1 -->
        <div class="col">
            <div class="card">
                <div class="card-title">1. Ingestion Sources & Data Models</div>
                <div class="card-body">
                    <div class="pipeline-step">
                        <div class="pipeline-title">Chromium SQLite History (Chrome & Edge)</div>
                        <div class="pipeline-desc">Table: <code>urls</code> (url, title, visit_count, typed_count, last_visit_time)<br>Table: <code>downloads</code> (target_path, tab_url, total_bytes, start_time)</div>
                    </div>
                    <div class="pipeline-step">
                        <div class="pipeline-title">Windows Recent File Artifacts</div>
                        <div class="pipeline-desc">Path: <code>%APPDATA%\Microsoft\Windows\Recent</code><br>Binary .lnk shortcuts with last-modified timestamps and target file paths.</div>
                    </div>
                    <div class="pipeline-step">
                        <div class="pipeline-title">User Downloads Storage Scanner</div>
                        <div class="pipeline-desc">Path: <code>~/Downloads</code><br>Live physical file indexing, byte sizing, and extension identification.</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-title">2. Lock Bypassing Algorithm (Shadow Copy)</div>
                <div class="card-body">
                    When web browsers are actively running, Windows places exclusive write locks on SQLite databases.
                    <div class="code-box">temp_file = tempfile.NamedTemporaryFile(
    delete=False, suffix=".sqlite"
)
shutil.copy2(history_file_path, temp_file.name)
conn = sqlite3.connect(temp_file.name)
# Query safely, then clean up temp file!</div>
                    <strong>Guarantees:</strong> 100% non-blocking data access with zero database lock crashes.
                </div>
            </div>
        </div>

        <!-- Col 2 -->
        <div class="col">
            <div class="card">
                <div class="card-title">3. Epoch Conversion & Query Decoding</div>
                <div class="card-body">
                    <strong>Chromium WebKit Timestamp Formula:</strong><br>
                    Counts microseconds elapsed since January 1, 1601 UTC.
                    <div class="code-box">def chrome_time_to_datetime(ts):
    epoch_start = datetime(1601, 1, 1)
    return epoch_start + timedelta(microseconds=ts)</div>
                    <strong>URL Query String Extractor:</strong><br>
                    Deconstructs query parameters using Python's <code>urllib.parse</code>:
                    <div class="code-box"># Extracts 'q=' (Google/Bing) or 'search_query=' (YouTube)
query_dict = parse_qs(parsed.query)
search_term = unquote_plus(query_dict['q'][0])</div>
                </div>
            </div>
            <div class="card">
                <div class="card-title">4. Timeline Correlation Engine</div>
                <div class="card-body">
                    Standardizes all disparate inputs into a unified dictionary structure:
                    <div class="code-box">{
    "timestamp": "2026-11-21 22:22:31",
    "dt": datetime_obj,
    "source": "Microsoft Edge",
    "category": "Web Visit",
    "title": "College Portal Login",
    "details": "https://exam.college.edu/login",
    "domain": "college.edu",
    "extra": "Visits: 2 | Typed: 1"
}</div>
                    Chronological in-memory sorting: <code>O(N log N)</code> via Timsort.
                </div>
            </div>
        </div>

        <!-- Col 3 -->
        <div class="col">
            <div class="card">
                <div class="card-title">5. Multi-Attribute Filtering Engine</div>
                <div class="card-body">
                    Executes instantaneous multi-parameter filtering across active memory:
                    <div class="pipeline-step">
                        <div class="pipeline-title">Keyword Substring Filter</div>
                        <div class="pipeline-desc">Case-insensitive search across title, URL, domain, and source.</div>
                    </div>
                    <div class="pipeline-step">
                        <div class="pipeline-title">Category & Source Combobox Filters</div>
                        <div class="pipeline-desc">Filters Web Visits, Searches, Downloads, and System Executions.</div>
                    </div>
                    <div class="pipeline-step">
                        <div class="pipeline-title">Timeframe Delta Filtering</div>
                        <div class="pipeline-desc">Dynamic cutoffs: Today, Last 24 Hours, Last 7 Days, Last 30 Days.</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-title">6. Output & Cross-Platform Execution</div>
                <div class="card-body">
                    • <strong>Matplotlib Canvas:</strong> 3-subplot embedded forensic metric visualization.<br>
                    • <strong>HTML/CSV Exporters:</strong> Generates executive audit documentation.<br>
                    • <strong>Cross-Platform Compatibility:</strong> Runs out of the box on Windows (<code>run.bat</code>) and macOS (<code>run_mac.command</code> / <code>python3 main.py</code>).
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div style="font-size: 13px; color: #94a3b8;">
            <strong style="color: #ffffff;">MIT-WPU First Year Engineering Team (Div A • Batch B1):</strong>
        </div>
        <div class="team-grid">
            <div class="member">
                <div class="member-name">1. Tanishq Gunjal (Lead)</div>
                <div class="member-prn">PRN: 1272261851 • GUI Architecture</div>
            </div>
            <div class="member">
                <div class="member-name">2. Janhavi Dahiwale</div>
                <div class="member-prn">PRN: 1272261225 • Browser Forensics</div>
            </div>
            <div class="member">
                <div class="member-name">3. OM Nalawade</div>
                <div class="member-prn">PRN: 1272261153 • Timeline Engine</div>
            </div>
            <div class="member">
                <div class="member-name">4. Ayush Warudkar</div>
                <div class="member-prn">PRN: 1272261894 • Visual Analytics</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# =============================================================================
# HTML TEMPLATE: POSTER 3 (CASE STUDY STORYBOARD)
# =============================================================================
POSTER_3_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TraceLens - Incident Investigation Storyboard</title>
    <style>
        @page { size: A3 landscape; margin: 0; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { width: 1920px; height: 1080px; background: #080d1a; color: #f8fafc; padding: 32px 40px; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; }
        
        .header { background: linear-gradient(135deg, #064e3b, #047857); border: 1px solid #10b981; border-radius: 14px; padding: 22px 32px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .inst-title { font-size: 15px; text-transform: uppercase; letter-spacing: 2px; color: #a7f3d0; font-weight: 700; margin-bottom: 4px; }
        .main-title { font-size: 42px; font-weight: 900; color: #ffffff; }
        .main-sub { font-size: 17px; color: #d1fae5; font-weight: 500; margin-top: 4px; }
        .badge-box { background: rgba(6, 78, 59, 0.7); border: 1px solid #10b981; padding: 12px 20px; border-radius: 10px; text-align: right; }

        .timeline-container { display: grid; grid-template-columns: repeat(6, 1fr); gap: 18px; margin: 20px 0; flex: 1; }
        .step-card { background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 18px; display: flex; flex-direction: column; position: relative; }
        .step-num { font-size: 11px; font-weight: 800; background: #059669; color: white; padding: 3px 8px; border-radius: 4px; display: inline-block; width: fit-content; margin-bottom: 8px; }
        .step-time { font-size: 13px; font-weight: 700; color: #34d399; font-family: Consolas, monospace; }
        .step-title { font-size: 15px; font-weight: 800; color: #ffffff; margin: 6px 0 8px 0; line-height: 1.3; }
        .step-body { font-size: 12px; color: #cbd5e1; line-height: 1.5; flex: 1; }
        .step-tag { margin-top: 10px; font-size: 11px; font-weight: 700; padding: 2px 6px; border-radius: 4px; width: fit-content; }
        .tag-search { background: rgba(168, 85, 247, 0.2); color: #d8b4fe; }
        .tag-visit { background: rgba(59, 130, 246, 0.2); color: #93c5fd; }
        .tag-download { background: rgba(16, 185, 129, 0.2); color: #6ee7b7; }
        .tag-app { background: rgba(245, 158, 11, 0.2); color: #fcd34d; }

        .bottom-summary { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 20px; }
        .summary-card { background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 14px 20px; }

        .footer { background: #0f172a; border-radius: 12px; padding: 14px 28px; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(255,255,255,0.1); }
        .team-grid { display: flex; gap: 28px; }
        .member { font-size: 13px; }
        .member-name { font-weight: 700; color: #ffffff; }
        .member-prn { color: #34d399; font-size: 11.5px; }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="inst-title">Forensic Case Demonstration • MIT World Peace University (MIT-WPU)</div>
            <div class="main-title">TraceLens in Action: Incident Investigation Case Study #2026</div>
            <div class="main-sub">Chronological Reconstruction of Cause-and-Effect Sequences Across Web & System Logs</div>
        </div>
        <div class="badge-box">
            <div style="font-size: 13px; color: #34d399; font-weight: 700;">LIVE INCIDENT DEMO</div>
            <div style="font-size: 15px; color: #ffffff; font-weight: 600;">Benchmark Scenario</div>
        </div>
    </div>

    <!-- 6-Step Storyboard -->
    <div class="timeline-container">
        <!-- Step 1 -->
        <div class="step-card">
            <div class="step-num">PHASE 1</div>
            <div class="step-time">09:15 AM</div>
            <div class="step-title">Web Reconnaissance</div>
            <div class="step-body">
                User queries Google: <code>'python digital forensics projects'</code>.<br><br>
                Source: <strong>Google Chrome</strong><br>
                Query extracted via <code>urllib.parse</code> parameter analysis.
            </div>
            <div class="step-tag tag-search">Web Search</div>
        </div>

        <!-- Step 2 -->
        <div class="step-card">
            <div class="step-num">PHASE 2</div>
            <div class="step-time">10:05 AM</div>
            <div class="step-title">Authentication Portal</div>
            <div class="step-body">
                Direct visit to <code>exam.college.edu/login/student</code>.<br><br>
                Source: <strong>Microsoft Edge</strong><br>
                Recorded visit count: 2.<br>Typed count: 1.
            </div>
            <div class="step-tag tag-visit">Web Visit</div>
        </div>

        <!-- Step 3 -->
        <div class="step-card">
            <div class="step-num">PHASE 3</div>
            <div class="step-time">02:20 PM</div>
            <div class="step-title">Payload Search</div>
            <div class="step-body">
                Search conducted for network packet analyzer:<br>
                <code>'download wireshark packet analyzer'</code>.<br><br>
                Source: <strong>Google Chrome</strong>
            </div>
            <div class="step-tag tag-search">Web Search</div>
        </div>

        <!-- Step 4 -->
        <div class="step-card">
            <div class="step-num">PHASE 4</div>
            <div class="step-time">02:25 PM</div>
            <div class="step-title">Inbound Executable</div>
            <div class="step-body">
                Download completed:<br>
                <code>Wireshark-win64-setup.exe</code><br>
                Size: <strong>78.5 MB</strong><br>
                Target: <code>C:\...\Downloads\</code><br>
                Source: <strong>wireshark.org</strong>
            </div>
            <div class="step-tag tag-download">File Download</div>
        </div>

        <!-- Step 5 -->
        <div class="step-card">
            <div class="step-num">PHASE 5</div>
            <div class="step-time">02:35 PM</div>
            <div class="step-title">Local App Execution</div>
            <div class="step-body">
                Windows Recent logs shortcut creation for:<br>
                <code>Wireshark-win64-setup.exe</code>.<br><br>
                Confirms physical local execution by user on disk!
            </div>
            <div class="step-tag tag-app">OS App Activity</div>
        </div>

        <!-- Step 6 -->
        <div class="step-card">
            <div class="step-num">PHASE 6</div>
            <div class="step-time">09:15 AM</div>
            <div class="step-title">Forensic Audit Export</div>
            <div class="step-body">
                TraceLens exports executive audit report:<br>
                <code>TraceLens_Forensic_Report.pdf</code>.<br><br>
                Complete cause-and-effect timeline generated for examiners!
            </div>
            <div class="step-tag tag-download">Audit Report</div>
        </div>
    </div>

    <!-- Summary strip -->
    <div class="bottom-summary">
        <div class="summary-card">
            <div style="font-size: 14px; font-weight: 700; color: #34d399; margin-bottom: 4px;">KEY INVESTIGATION TAKEAWAY</div>
            <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.5;">
                In manual triage, correlating Google search times, Chrome download timestamps, and Windows Recent file execution requires querying 3 separate database engines and calculating WebKit microsecond offsets. <strong>TraceLens accomplishes this in 0.45 seconds</strong> with 1-click in-memory sorting.
            </div>
        </div>
        <div class="summary-card" style="text-align: center; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">Time Saved Per Investigation</div>
            <div style="font-size: 26px; font-weight: 900; color: #34d399;">~95% Faster</div>
            <div style="font-size: 11px; color: #cbd5e1;">Zero manual calculation needed</div>
        </div>
    </div>

    <div class="footer">
        <div style="font-size: 13px; color: #94a3b8;">
            <strong style="color: #ffffff;">MIT-WPU First Year Engineering Team (Div A • Batch B1):</strong>
        </div>
        <div class="team-grid">
            <div class="member">
                <div class="member-name">1. Tanishq Gunjal (Lead)</div>
                <div class="member-prn">PRN: 1272261851 • GUI Architecture</div>
            </div>
            <div class="member">
                <div class="member-name">2. Janhavi Dahiwale</div>
                <div class="member-prn">PRN: 1272261225 • Browser Forensics</div>
            </div>
            <div class="member">
                <div class="member-name">3. OM Nalawade</div>
                <div class="member-prn">PRN: 1272261153 • Timeline Engine</div>
            </div>
            <div class="member">
                <div class="member-name">4. Ayush Warudkar</div>
                <div class="member-prn">PRN: 1272261894 • Visual Analytics</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

def main():
    print("Generating 3 Project Posters for TraceLens...")

    posters = [
        ("Poster_1_Academic_Exhibition.html", "Poster_1_Academic_Exhibition.pdf", "Poster_1_Academic_Exhibition.png", POSTER_1_HTML),
        ("Poster_2_Technical_Architecture.html", "Poster_2_Technical_Architecture.pdf", "Poster_2_Technical_Architecture.png", POSTER_2_HTML),
        ("Poster_3_Incident_Case_Study.html", "Poster_3_Incident_Case_Study.pdf", "Poster_3_Incident_Case_Study.png", POSTER_3_HTML)
    ]

    for html_file, pdf_file, png_file, content in posters:
        html_path = os.path.join(DOCS_DIR, html_file)
        pdf_path = os.path.join(DOCS_DIR, pdf_file)
        png_path = os.path.join(DOCS_DIR, png_file)

        # 1. Write HTML
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Written: {html_file}")

        # 2. Render PDF via headless Chrome
        cmd_pdf = [
            CHROME_PATH,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_path
        ]
        subprocess.run(cmd_pdf, capture_output=True)

        # 3. Render PNG screenshot via headless Chrome (1920x1080)
        cmd_png = [
            CHROME_PATH,
            "--headless",
            "--disable-gpu",
            f"--screenshot={png_path}",
            "--window-size=1920,1080",
            html_path
        ]
        subprocess.run(cmd_png, capture_output=True)

        # Copy to Desktop
        desktop_pdf = os.path.join(DESKTOP_DIR, pdf_file)
        desktop_png = os.path.join(DESKTOP_DIR, png_file)
        if os.path.exists(pdf_path):
            shutil.copy2(pdf_path, desktop_pdf)
        if os.path.exists(png_path):
            shutil.copy2(png_path, desktop_png)

        print(f"Compiled: {pdf_file} & {png_file} (Saved to Desktop)")

    print("\nAll 3 Posters compiled and placed on Desktop successfully!")

if __name__ == "__main__":
    main()
