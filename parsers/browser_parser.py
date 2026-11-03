"""
Module: browser_parser.py
Project: TraceLens - Browser & App Artifact Timeline Visualizer
Contributed by: Janhavi Dahiwale (Group Member 2)

Description:
This module extracts browsing history and download history from Chromium-based browsers
such as Google Chrome and Microsoft Edge on Windows.
Browsers store their records in SQLite database files ('History').
Because active browsers lock this database file, we create a temporary copy
before querying it using Python's built-in sqlite3 library.
"""

import os
import shutil
import sqlite3
import tempfile
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs, unquote_plus


def chrome_time_to_datetime(chrome_timestamp):
    """
    Converts Chrome/WebKit timestamp to Python datetime.
    Chrome timestamp counts microseconds since January 1, 1601 UTC.
    """
    if not chrome_timestamp or chrome_timestamp <= 0:
        return None
    try:
        # Microseconds from 1601 to timestamp
        epoch_start = datetime(1601, 1, 1)
        return epoch_start + timedelta(microseconds=chrome_timestamp)
    except (OverflowError, ValueError):
        return None


def extract_domain(url):
    """
    Extracts the clean host domain from a full URL.
    Example: 'https://www.google.com/search?q=test' -> 'google.com'
    """
    if not url:
        return "Unknown"
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain if domain else "Local/Direct"
    except Exception:
        return "Unknown"


def extract_search_query(url):
    """
    Detects if the visited URL is a web search and extracts the query term.
    Supports Google, Bing, DuckDuckGo, Yahoo, and YouTube.
    """
    if not url:
        return None
    try:
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        query_dict = parse_qs(parsed.query)

        # Check for Google, Bing, DuckDuckGo searches ('q' parameter)
        if any(search_engine in netloc for search_engine in ["google.", "bing.", "duckduckgo."]):
            if "q" in query_dict:
                return unquote_plus(query_dict["q"][0])

        # Check for YouTube searches ('search_query' parameter)
        if "youtube.com" in netloc and "search_query" in query_dict:
            return unquote_plus(query_dict["search_query"][0])

        # Check for Yahoo searches ('p' parameter)
        if "yahoo.com" in netloc and "p" in query_dict:
            return unquote_plus(query_dict["p"][0])

    except Exception:
        pass
    return None


def get_default_history_paths():
    """
    Returns default file paths for Chrome and Edge history on Windows.
    Uses environment variable %LOCALAPPDATA%.
    """
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if not local_app_data:
        return {}

    paths = {
        "Google Chrome": os.path.join(
            local_app_data, "Google", "Chrome", "User Data", "Default", "History"
        ),
        "Microsoft Edge": os.path.join(
            local_app_data, "Microsoft", "Edge", "User Data", "Default", "History"
        ),
        "Brave Browser": os.path.join(
            local_app_data, "BraveSoftware", "Brave-Browser", "User Data", "Default", "History"
        ),
    }
    return paths


def parse_sqlite_history(history_file_path, browser_name="Browser", limit=500):
    """
    Reads the SQLite history file and extracts visits and downloads.
    Safely copies the database to temp to prevent database locking errors.
    """
    artifacts = []

    if not os.path.exists(history_file_path):
        return artifacts

    temp_db = None
    try:
        # Step 1: Create a safe temporary copy of the SQLite file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite")
        temp_db = temp_file.name
        temp_file.close()

        shutil.copy2(history_file_path, temp_db)

        # Step 2: Connect to the SQLite database copy
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # Step 3: Query URLs & History
        # Querying URL table for visits, titles, and visit timestamps
        url_query = """
            SELECT url, title, visit_count, typed_count, last_visit_time 
            FROM urls 
            WHERE last_visit_time > 0 
            ORDER BY last_visit_time DESC 
            LIMIT ?
        """
        try:
            cursor.execute(url_query, (limit,))
            rows = cursor.fetchall()

            for row in rows:
                url, title, visit_count, typed_count, last_visit_time = row
                dt = chrome_time_to_datetime(last_visit_time)
                if not dt:
                    continue

                domain = extract_domain(url)
                search_query = extract_search_query(url)

                # Determine category
                if search_query:
                    category = "Web Search"
                    display_title = f"Search: '{search_query}'"
                    details = f"Query: {search_query} ({url})"
                else:
                    category = "Web Visit"
                    display_title = title if title and title.strip() else domain
                    details = url

                extra_info = f"Visits: {visit_count} | Typed: {typed_count}"

                artifacts.append({
                    "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "dt": dt,
                    "source": browser_name,
                    "category": category,
                    "title": display_title,
                    "details": details,
                    "domain": domain,
                    "extra": extra_info
                })
        except sqlite3.OperationalError:
            # Table might have slightly different schema in older versions
            pass

        # Step 4: Query Downloads if available
        download_query = """
            SELECT target_path, tab_url, total_bytes, start_time 
            FROM downloads 
            WHERE start_time > 0 
            ORDER BY start_time DESC 
            LIMIT 100
        """
        try:
            cursor.execute(download_query)
            download_rows = cursor.fetchall()
            for d_row in download_rows:
                target_path, tab_url, total_bytes, start_time = d_row
                dt = chrome_time_to_datetime(start_time)
                if not dt:
                    continue

                filename = os.path.basename(target_path) if target_path else "Unknown File"
                size_mb = round(total_bytes / (1024 * 1024), 2) if total_bytes and total_bytes > 0 else 0

                artifacts.append({
                    "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "dt": dt,
                    "source": browser_name,
                    "category": "Download",
                    "title": f"Downloaded: {filename}",
                    "details": f"Path: {target_path} | From: {tab_url}",
                    "domain": extract_domain(tab_url),
                    "extra": f"Size: {size_mb} MB"
                })
        except sqlite3.OperationalError:
            pass

        conn.close()

    except Exception as e:
        # Graceful handling so GUI doesn't crash if access is denied
        print(f"[Warning] Could not parse {browser_name} history: {e}")

    finally:
        # Step 5: Clean up temporary file
        if temp_db and os.path.exists(temp_db):
            try:
                os.remove(temp_db)
            except Exception:
                pass

    return artifacts


def get_all_browser_artifacts(limit_per_browser=500):
    """
    Main helper function to scan all available browsers on the system.
    """
    all_artifacts = []
    browser_paths = get_default_history_paths()

    for browser_name, path in browser_paths.items():
        if os.path.exists(path):
            artifacts = parse_sqlite_history(path, browser_name=browser_name, limit=limit_per_browser)
            all_artifacts.extend(artifacts)

    return all_artifacts
