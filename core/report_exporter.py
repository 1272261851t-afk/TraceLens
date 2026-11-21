"""
Module: report_exporter.py
Project: TraceLens - Browser & App Artifact Timeline Visualizer
Contributed by: Ayush Warudkar (Group Member 4)

Description:
This module formats and exports the correlated timeline artifacts and metrics
into professional digital forensics reports in CSV and styled HTML formats.
These reports can be submitted for academic evaluations or case documentation.
"""

import csv
import html
from datetime import datetime


def export_to_csv(artifacts, filepath):
    """
    Exports the given artifacts list into a standard CSV file.
    """
    fieldnames = ["Timestamp", "Source", "Category", "Title", "Domain", "Details", "Extra Info"]
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for a in artifacts:
            writer.writerow([
                a.get("timestamp", ""),
                a.get("source", ""),
                a.get("category", ""),
                a.get("title", ""),
                a.get("domain", ""),
                a.get("details", ""),
                a.get("extra", "")
            ])
    return True


def export_to_html(artifacts, stats, filepath, case_name="TraceLens Forensic Investigation"):
    """
    Generates a modern, clean HTML report containing executive statistics,
    visual summaries, and a complete chronological timeline table.
    """
    gen_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate Category badges HTML
    cat_badges = ""
    for cat, cnt in stats.get("category_counts", {}).items():
        cat_badges += f'<span class="badge badge-cat">{html.escape(cat)}: <strong>{cnt}</strong></span> '

    # Generate Top Domains Rows
    top_domains_html = ""
    for dom, cnt in stats.get("top_domains", []):
        top_domains_html += f"<tr><td>{html.escape(dom)}</td><td><strong>{cnt}</strong> visits</td></tr>"
    if not top_domains_html:
        top_domains_html = "<tr><td colspan='2'>No web domains in this timeline view</td></tr>"

    # Generate Timeline Table Rows
    table_rows = []
    for i, a in enumerate(artifacts, 1):
        cat = a.get("category", "")
        # Color coding class
        badge_cls = "badge-other"
        if "Search" in cat:
            badge_cls = "badge-search"
        elif "Visit" in cat:
            badge_cls = "badge-visit"
        elif "Download" in cat:
            badge_cls = "badge-download"
        elif "App" in cat or "File" in cat:
            badge_cls = "badge-app"

        row_html = f"""
        <tr>
            <td class="mono">{i}</td>
            <td class="mono time-col">{html.escape(a.get('timestamp', ''))}</td>
            <td><span class="source-tag">{html.escape(a.get('source', ''))}</span></td>
            <td><span class="badge {badge_cls}">{html.escape(cat)}</span></td>
            <td class="title-cell"><strong>{html.escape(a.get('title', ''))}</strong></td>
            <td><code>{html.escape(a.get('domain', ''))}</code></td>
            <td class="details-cell">{html.escape(a.get('details', ''))}</td>
            <td class="extra-cell">{html.escape(a.get('extra', ''))}</td>
        </tr>
        """
        table_rows.append(row_html)

    timeline_rows_str = "\n".join(table_rows)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TraceLens - Forensic Artifact Timeline Report</title>
    <style>
        :root {{
            --primary: #2563eb;
            --primary-dark: #1e40af;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-dark: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }}
        body {{
            background-color: var(--bg);
            color: var(--text-dark);
            padding: 24px;
            line-height: 1.5;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            color: white;
            padding: 28px;
            border-radius: 12px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 6px;
        }}
        .header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .team-banner {{
            margin-top: 14px;
            padding-top: 14px;
            border-top: 1px solid rgba(255,255,255,0.2);
            font-size: 13px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .stat-card {{
            background: var(--card-bg);
            padding: 18px;
            border-radius: 10px;
            border: 1px solid var(--border);
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .stat-card .label {{
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
        }}
        .stat-card .value {{
            font-size: 22px;
            font-weight: 700;
            color: var(--primary);
            margin-top: 4px;
        }}
        .section {{
            background: var(--card-bg);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid var(--border);
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 14px;
            color: #1e293b;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
        }}
        .badge-cat {{ background: #e0f2fe; color: #0369a1; margin-right: 6px; margin-bottom: 6px; }}
        .badge-visit {{ background: #dbeafe; color: #1d4ed8; }}
        .badge-search {{ background: #f3e8ff; color: #7e22ce; }}
        .badge-download {{ background: #dcfce7; color: #15803d; }}
        .badge-app {{ background: #ffedd5; color: #c2410c; }}
        .badge-other {{ background: #f1f5f9; color: #475569; }}
        .source-tag {{
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        th, td {{
            padding: 10px 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{
            background-color: #f1f5f9;
            color: #334155;
            font-weight: 600;
            position: sticky;
            top: 0;
        }}
        tr:hover {{
            background-color: #f8fafc;
        }}
        .mono {{
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 12px;
        }}
        .time-col {{
            white-space: nowrap;
            color: #475569;
        }}
        .title-cell {{
            max-width: 250px;
            word-wrap: break-word;
        }}
        .details-cell {{
            max-width: 320px;
            word-break: break-all;
            color: #64748b;
            font-size: 11px;
        }}
        .extra-cell {{
            font-size: 11px;
            color: #64748b;
            white-space: nowrap;
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 30px;
            padding-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>TraceLens: Browser & App Artifact Timeline Visualizer</h1>
        <p>Comprehensive Forensics Investigation Report & Artifact Correlation</p>
        <div class="team-banner">
            <strong>Group Project Developed By (1st Year Engineering Team):</strong><br>
            1. Tanishq Gunjal (Lead / GUI & Integration) &bull;
            2. Janhavi Dahiwale (Browser Artifact Parser) &bull;
            3. OM Nalawade (Timeline Correlation Engine) &bull;
            4. Ayush Warudkar (Visual Analytics & Reporting)
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="label">Total Artifacts Correlated</div>
            <div class="value">{stats.get('total_count', 0)}</div>
        </div>
        <div class="stat-card">
            <div class="label">Timeline Earliest Activity</div>
            <div class="value" style="font-size: 15px; margin-top: 8px;">{stats.get('earliest_time', 'N/A')}</div>
        </div>
        <div class="stat-card">
            <div class="label">Timeline Latest Activity</div>
            <div class="value" style="font-size: 15px; margin-top: 8px;">{stats.get('latest_time', 'N/A')}</div>
        </div>
        <div class="stat-card">
            <div class="label">Report Generated At</div>
            <div class="value" style="font-size: 15px; margin-top: 8px;">{gen_time}</div>
        </div>
    </div>

    <div class="section">
        <div class="section-title">Artifact Category Breakdown</div>
        <div>
            {cat_badges}
        </div>
    </div>

    <div class="section">
        <div class="section-title">Top Visited Web Domains</div>
        <table style="max-width: 600px;">
            <thead>
                <tr>
                    <th>Domain</th>
                    <th>Frequency</th>
                </tr>
            </thead>
            <tbody>
                {top_domains_html}
            </tbody>
        </table>
    </div>

    <div class="section">
        <div class="section-title">Chronological Activity Timeline ({len(artifacts)} Records)</div>
        <div style="overflow-x: auto;">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Timestamp</th>
                        <th>Source</th>
                        <th>Category</th>
                        <th>Title / Event</th>
                        <th>Domain / Scope</th>
                        <th>Details (URL / Path)</th>
                        <th>Extra Attributes</th>
                    </tr>
                </thead>
                <tbody>
                    {timeline_rows_str}
                </tbody>
            </table>
        </div>
    </div>

    <div class="footer">
        Generated by TraceLens &bull; First-Year Computer Engineering Project Submission &bull; Academic Year 2026-2027
    </div>
</body>
</html>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    return True
