"""
Module: app_parser.py
Project: TraceLens - Browser & App Artifact Timeline Visualizer
Contributed by: OM Nalawade (Group Member 3)

Description:
This module extracts application and file activity artifacts from the Windows OS.
Specifically, it analyzes:
1. Windows Recent items (%APPDATA%\\Microsoft\\Windows\\Recent) - shows files and apps opened.
2. User Downloads directory (%USERPROFILE%\\Downloads) - shows recently stored system files.
3. System Temp application logs (%TEMP%) - identifies recently executed software artifacts.
"""

import os
from datetime import datetime


def get_file_type_category(filename):
    """
    Categorizes file extensions into human-readable types.
    """
    ext = os.path.splitext(filename)[1].lower()

    doc_exts = {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".csv", ".ppt", ".pptx"}
    dev_exts = {".py", ".c", ".cpp", ".java", ".js", ".html", ".css", ".json", ".xml", ".sql", ".ipynb"}
    media_exts = {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".mkv", ".mp3", ".wav"}
    exec_exts = {".exe", ".msi", ".bat", ".cmd", ".ps1"}
    archive_exts = {".zip", ".rar", ".7z", ".tar", ".gz"}

    if ext in doc_exts:
        return "Document"
    elif ext in dev_exts:
        return "Source Code"
    elif ext in media_exts:
        return "Media File"
    elif ext in exec_exts:
        return "Application / Executable"
    elif ext in archive_exts:
        return "Archive / Package"
    elif ext == ".lnk":
        return "Windows Shortcut (LNK)"
    else:
        return "General File"


def parse_windows_recent_artifacts(limit=300):
    """
    Extracts recently accessed files and apps from the Windows Recent folder.
    Each .lnk file has a Last-Modified-Time indicating when the user interacted with it.
    """
    artifacts = []
    appdata = os.environ.get("APPDATA", "")
    if not appdata:
        return artifacts

    recent_dir = os.path.join(appdata, "Microsoft", "Windows", "Recent")
    if not os.path.exists(recent_dir):
        return artifacts

    try:
        entries = []
        for entry in os.scandir(recent_dir):
            if entry.name.startswith("."):
                continue
            try:
                stat = entry.stat()
                mtime = stat.st_mtime
                entries.append((mtime, entry.name, entry.path, stat.st_size))
            except Exception:
                continue

        # Sort entries by modified time descending (most recent first)
        entries.sort(key=lambda x: x[0], reverse=True)

        for mtime, name, path, size in entries[:limit]:
            dt = datetime.fromtimestamp(mtime)

            # Clean name (remove trailing .lnk)
            display_name = name
            if display_name.lower().endswith(".lnk"):
                display_name = display_name[:-4]

            file_type = get_file_type_category(display_name)

            artifacts.append({
                "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "dt": dt,
                "source": "Windows OS",
                "category": "App / File Activity",
                "title": f"Accessed: {display_name}",
                "details": f"Path: {path}",
                "domain": "Local System",
                "extra": f"Type: {file_type} | File Item"
            })

    except Exception as e:
        print(f"[Warning] Could not parse Windows Recent folder: {e}")

    return artifacts


def parse_recent_downloads(limit=100):
    """
    Scans the user's Downloads folder for recently saved files.
    Works seamlessly on both Windows and macOS.
    """
    artifacts = []
    downloads_dir = os.path.expanduser("~/Downloads")
    if not os.path.exists(downloads_dir):
        return artifacts

    try:
        entries = []
        for entry in os.scandir(downloads_dir):
            if entry.name.startswith("."):
                continue
            try:
                stat = entry.stat()
                mtime = stat.st_mtime
                entries.append((mtime, entry.name, entry.path, stat.st_size))
            except Exception:
                continue

        # Sort newest first
        entries.sort(key=lambda x: x[0], reverse=True)

        for mtime, name, path, size in entries[:limit]:
            dt = datetime.fromtimestamp(mtime)
            size_mb = round(size / (1024 * 1024), 2)
            file_type = get_file_type_category(name)

            artifacts.append({
                "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "dt": dt,
                "source": "Downloads Folder",
                "category": "File Downloaded",
                "title": f"File: {name}",
                "details": f"Path: {path}",
                "domain": "Local Disk",
                "extra": f"Type: {file_type} | Size: {size_mb} MB"
            })

    except Exception as e:
        print(f"[Warning] Could not parse Downloads directory: {e}")

    return artifacts


def get_all_app_artifacts(limit=300):
    """
    Main helper function combining Windows Recent items and Downloads.
    """
    all_artifacts = []
    all_artifacts.extend(parse_windows_recent_artifacts(limit=limit))
    all_artifacts.extend(parse_recent_downloads(limit=100))
    return all_artifacts
