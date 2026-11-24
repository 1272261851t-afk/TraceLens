"""
Script to generate:
1. Deliverables_Document.pdf
2. Project_Documentation.pdf
3. Project_Documentation.docx
"""

import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

DOCS_DIR = r"C:\Users\ASUS\Documents\TraceLens"
DESKTOP_DIR = r"C:\Users\ASUS\OneDrive\PlayerFile\Desktop"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def generate_pdfs():
    print("[1/3] Generating PDFs via headless Chrome...")
    files = [
        ("Deliverables_Document.html", "Deliverables_Document.pdf"),
        ("Project_Documentation.html", "Project_Documentation.pdf")
    ]
    for html_name, pdf_name in files:
        html_path = os.path.join(DOCS_DIR, html_name)
        pdf_path = os.path.join(DOCS_DIR, pdf_name)
        cmd = [
            CHROME_PATH,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(pdf_path):
            print(f"      Created: {pdf_name} ({os.path.getsize(pdf_path)} bytes)")
            # Copy to Desktop
            desktop_pdf = os.path.join(DESKTOP_DIR, pdf_name)
            subprocess.run(["cmd", "/c", f"copy /y \"{pdf_path}\" \"{desktop_pdf}\""], capture_output=True)
            print(f"      Copied to Desktop: {desktop_pdf}")
        else:
            print(f"      Error generating {pdf_name}: {res.stderr}")

def generate_word_document():
    print("[2/3] Generating Word Document (Project_Documentation.docx)...")
    doc = docx.Document()

    # Page Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Styles helper
    def add_heading_styled(text, level=1):
        h = doc.add_heading(text, level=level)
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        run = h.runs[0]
        run.font.name = "Segoe UI"
        run.font.color.rgb = RGBColor(30, 58, 138)
        return h

    # Header / Title
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("MIT WORLD PEACE UNIVERSITY (MIT-WPU), PUNE\nDEPARTMENT OF COMPUTER ENGINEERING & TECHNOLOGY\nACADEMIC YEAR 2026–2027\n")
    r_inst.font.bold = True
    r_inst.font.size = Pt(11)
    r_inst.font.color.rgb = RGBColor(37, 99, 235)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("MINI PROJECT DOCUMENTATION REPORT\n")
    r_title.font.bold = True
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    r_proj = p_title.add_run("Browser & App Artifact Timeline Visualizer (\"TraceLens\")")
    r_proj.font.bold = True
    r_proj.font.size = Pt(14)
    r_proj.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Point 1: Title of Project
    add_heading_styled("1. Title of Project", level=2)
    p = doc.add_paragraph()
    r = p.add_run("Browser & App Artifact Timeline Visualizer (\"TraceLens\")")
    r.font.bold = True
    p.add_run("\nA Lightweight Digital Forensics Correlator & Activity Timeline Application in Python 3.")

    # Point 2: Details of Team Members
    add_heading_styled("2. Details of Team Members", level=2)
    table = doc.add_table(rows=1, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    hdr[0].text = "Sr."
    hdr[1].text = "Student Name"
    hdr[2].text = "PRN / Roll No"
    hdr[3].text = "Batch"
    hdr[4].text = "Division"
    hdr[5].text = "Institutional Email"

    members = [
        ("1", "Tanishq Gunjal (Lead)", "1272261851", "B1", "Div A", "1272261851.t@mitwpu.edu.in"),
        ("2", "Janhavi Dahiwale", "1272261225", "B1", "Div A", "1272261225.j@mitwpu.edu.in"),
        ("3", "OM Nalawade", "1272261153", "B1", "Div A", "1272261153.o@mitwpu.edu.in"),
        ("4", "Ayush Warudkar", "1272261894", "B1", "Div A", "1272261894.a@mitwpu.edu.in"),
    ]
    for row in members:
        r_cells = table.add_row().cells
        for i, val in enumerate(row):
            r_cells[i].text = val

    p_guide = doc.add_paragraph()
    p_guide.paragraph_format.space_before = Pt(8)
    p_guide.add_run("Faculty In-Charge: ").font.bold = True
    p_guide.add_run("Department of Computer Engineering Faculty Panel, MIT-WPU")

    # Point 3: Introduction of Mini project problem statement
    add_heading_styled("3. Introduction & Problem Statement", level=2)
    p = doc.add_paragraph()
    p.add_run("In modern desktop computing, user activities cross seamlessly between web browsers (Google Chrome, Microsoft Edge) and desktop software (code compilers, document processors, file managers). When security breaches, accidental downloads, or system incidents occur, reconstructive forensic triage requires determining exactly what actions took place in strict chronological sequence.\n\n")
    p.add_run("Problem Statement: ").font.bold = True
    p.add_run("Digital activity artifacts are dispersed across proprietary, incompatible file formats (SQLite databases for browser history, binary .lnk structures for recently accessed files, file system timestamps). Existing commercial forensics suites (such as EnCase or FTK Imager) are proprietary, resource-heavy (~1 GB), and steep in complexity for rapid incident auditing.\n\n")
    p.add_run("Proposed Solution: ").font.bold = True
    p.add_run("TraceLens is an open-source, lightweight desktop forensics tool developed in Python 3. It parses Chromium SQLite databases, Windows Recent artifacts, and user downloads, normalizes disparate epochs into human-readable local time, and provides an interactive graphical timeline with real-time filtering, visual analytics, and exportable forensic audit reports.")

    # Point 4: Dataset Used
    add_heading_styled("4. Dataset Used", level=2)
    p = doc.add_paragraph()
    p.add_run("TraceLens uses real host workstation forensic repositories alongside a standardized benchmark scenario:\n")
    p.add_run("• Live Chromium SQLite History: ").font.bold = True
    p.add_run("Extracted from %LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\History and Microsoft Edge equivalent. Contains visit URLs, page titles, visit counts, and download records.\n")
    p.add_run("• Windows OS Recent Shortcuts: ").font.bold = True
    p.add_run("Extracted from %APPDATA%\\Microsoft\\Windows\\Recent (.lnk binary shortcuts indicating file/application access times).\n")
    p.add_run("• Live OS Sockets & DNS Resolver Cache: ").font.bold = True
    p.add_run("Active TCP/UDP endpoints mapped to browser PIDs and system DNS cache for Incognito/InPrivate forensic detection.\n")
    p.add_run("• Simulated Forensic Incident Scenario: ").font.bold = True
    p.add_run("20 chronological forensic events (searches, proxy lookups, bypass downloads, app launches, document drafts) enabling instant demonstration without scanning personal workstation data.")

    # Point 5: Algorithm & Flowchart of functions used
    add_heading_styled("5. Algorithm & Flowchart of Implementation", level=2)
    p = doc.add_paragraph()
    p.add_run("Core Algorithm (Shadow Cloning & Timestamp Conversion):\n").font.bold = True
    p.add_run("1. Clone active SQLite DB to %TEMP% to prevent database locking errors.\n")
    p.add_run("2. Connect via sqlite3 and query 'urls' and 'downloads' tables.\n")
    p.add_run("3. Normalize Chromium WebKit timestamp: Datetime = Epoch(1601-01-01 UTC) + timedelta(microseconds=ts).\n")
    p.add_run("4. Deconstruct query URLs with urllib.parse to extract search terms (?q=, search_query=).\n")
    p.add_run("5. Scan Windows Recent folder and extract last-modified timestamps for local application events.\n")
    p.add_run("6. Enumerate active browser sockets (ports 80/443) and DNS cache to recover Incognito/InPrivate traces.\n")
    p.add_run("7. Merge disparate events into normalized dictionaries and sort chronologically.\n")
    p.add_run("8. Render records in Tkinter Treeview with real-time filtering, Matplotlib charts, and HTML/CSV exports.")

    # Point 6: Screenshots of obtained results
    add_heading_styled("6. Screenshots of Obtained Results", level=2)
    chart_img = os.path.join(DOCS_DIR, "data", "analytics_chart.png")
    if os.path.exists(chart_img):
        doc.add_picture(chart_img, width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure: Multi-Chart Forensics Analytics Output (Hourly Usage, Categories, Top Domains)")
        r_cap.font.italic = True
        r_cap.font.size = Pt(9)
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

    # Point 7: Conclusion
    add_heading_styled("7. Conclusion", level=2)
    p = doc.add_paragraph()
    p.add_run("The TraceLens project successfully fulfills all prescribed mini-project objectives. Built entirely with Python 3 and standard desktop libraries, it bridges the gap between complex enterprise forensic suites and introductory incident response needs. The application reliably bypasses database locks, standardizes diverse epoch formats, and delivers clear chronological timeline insights with embedded visual analytics.\n\nFuture Scope includes adding support for Mozilla Firefox (places.sqlite) and compiling the codebase into a standalone executable binary using PyInstaller.")

    docx_path = os.path.join(DOCS_DIR, "Project_Documentation.docx")
    doc.save(docx_path)
    print(f"      Created: Project_Documentation.docx ({os.path.getsize(docx_path)} bytes)")

    desktop_docx = os.path.join(DESKTOP_DIR, "Project_Documentation.docx")
    subprocess.run(["cmd", "/c", f"copy /y \"{docx_path}\" \"{desktop_docx}\""], capture_output=True)
    print(f"      Copied to Desktop: {desktop_docx}")

def main():
    generate_pdfs()
    generate_word_document()
    print("\n[3/3] All Deliverables & Documentation generated successfully!")

if __name__ == "__main__":
    main()
