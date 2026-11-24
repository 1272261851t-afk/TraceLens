"""
Module: incognito_parser.py
Project: TraceLens - Browser & App Artifact Timeline Visualizer
Contributed by: Janhavi Dahiwale (Group Member 2) & Tanishq Gunjal (Group Member 1)

Description:
Extracts digital forensic traces left during Incognito (Chrome) and InPrivate (Edge) sessions.
While Chromium browsers do not save browsing history to the on-disk SQLite History database
during private sessions, traces persist in:
1. OS DNS Resolver Cache (records hostnames resolved during incognito navigation).
2. Physical Downloads (files downloaded in incognito remain saved on the file system).
3. Session Storage and Temp Socket allocations.
"""

import os
import subprocess
from datetime import datetime
from urllib.parse import urlparse


def parse_dns_cache_traces(limit=100):
    """
    Attempts to read the operating system DNS resolver cache.
    When a user browses in incognito mode, the operating system still resolves
    the domain name and caches it in local DNS memory.
    """
    artifacts = []
    try:
        # Run ipconfig /displaydns on Windows
        res = subprocess.run(
            ["ipconfig", "/displaydns"],
            capture_output=True,
            text=True,
            timeout=4
        )
        output = res.stdout

        if "Record Name" in output:
            lines = output.splitlines()
            current_domain = None
            now = datetime.now()

            for line in lines:
                line = line.strip()
                if line.startswith("Record Name"):
                    parts = line.split(":")
                    if len(parts) >= 2:
                        domain = parts[1].strip().lower()
                        # Exclude standard internal/telemetry records
                        if domain and not any(ign in domain for ign in ["local", "arpa", "microsoft", "windowsupdate", "google"]):
                            current_domain = domain
                elif "Record Type" in line and current_domain:
                    # Found valid A / AAAA record
                    artifacts.append({
                        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                        "dt": now,
                        "source": "DNS Resolver Cache",
                        "category": "Incognito Activity",
                        "title": f"DNS Host Resolution: {current_domain}",
                        "details": f"Active OS DNS Cache Entry | Host: {current_domain}",
                        "domain": current_domain,
                        "extra": "Trace: Incognito / Private Session DNS Artifact"
                    })
                    current_domain = None
                    if len(artifacts) >= limit:
                        break
    except Exception as e:
        # Gracefully handled if non-elevated permissions or timeout
        pass

    return artifacts


def parse_incognito_downloads():
    """
    Scans for files downloaded during active sessions. Even when downloaded
    inside Incognito mode, the browser leaves the file on the physical disk.
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
                entries.append((stat.st_mtime, entry.name, entry.path, stat.st_size))
            except Exception:
                continue

        # Check most recently modified files
        entries.sort(key=lambda x: x[0], reverse=True)
        for mtime, name, path, size in entries[:15]:
            dt = datetime.fromtimestamp(mtime)
            size_mb = round(size / (1024 * 1024), 2)
            # Tag potential incognito artifacts if recent
            artifacts.append({
                "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "dt": dt,
                "source": "Downloads Storage",
                "category": "Download",
                "title": f"Physical Disk File: {name}",
                "details": f"Path: {path}",
                "domain": "Local Disk",
                "extra": f"Size: {size_mb} MB | Persistent File Artifact"
            })
    except Exception:
        pass

    return artifacts


def get_all_incognito_artifacts():
    """
    Main aggregator for live incognito forensic artifacts.
    """
    traces = []
    traces.extend(parse_dns_cache_traces())
    return traces
