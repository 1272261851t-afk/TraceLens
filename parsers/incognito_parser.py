"""
Module: incognito_parser.py
Project: TraceLens - Browser & App Artifact Timeline Visualizer
Contributed by: Janhavi Dahiwale (Group Member 2 - Browser Forensics & SQLite)
                & Tanishq Gunjal (Group Member 1 - Project Lead)

Description:
Extracts digital forensic traces associated with Incognito (Google Chrome) and
InPrivate (Microsoft Edge / Firefox / Safari) browsing sessions.

Academic & Forensic Foundation:
Chromium and Gecko browsers are engineered so that visited URLs are NOT written to
the on-disk SQLite History database during private browsing.
However, digital forensic investigations recover private browsing evidence via
operating system layers:
1. Active Network Sockets & QUIC/TLS Streams: The OS kernel maintains open TCP/UDP
   sockets (ports 80, 443) between the browser process and destination web servers.
2. OS DNS Resolver Cache: The operating system caches domain-to-IP resolutions.
3. Persistent Downloads: Files downloaded in private mode persist on the physical file system.
4. Process Execution Arguments: Process execution tables record '--incognito' or '-inprivate' flags.
"""

import os
import sys
import subprocess
import socket
from datetime import datetime, timedelta
from urllib.parse import urlparse

# Module-level cache for reverse DNS to ensure fast lookups
_REVERSE_DNS_CACHE = {}


def _resolve_ip(ip_str):
    """
    Performs reverse DNS resolution with timeout and caching.
    Returns domain or IP if resolution fails.
    """
    if not ip_str or ip_str in ("0.0.0.0", "127.0.0.1", "::", "::1"):
        return None
    if ip_str in _REVERSE_DNS_CACHE:
        return _REVERSE_DNS_CACHE[ip_str]

    try:
        orig_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(0.4)
        hostname, _, _ = socket.gethostbyaddr(ip_str)
        socket.setdefaulttimeout(orig_timeout)
        # Strip trailing dot if present
        hostname = hostname.rstrip(".")
        _REVERSE_DNS_CACHE[ip_str] = hostname
        return hostname
    except Exception:
        _REVERSE_DNS_CACHE[ip_str] = ip_str
        return ip_str


def get_active_browser_processes():
    """
    Scans running operating system processes to locate active web browser instances
    and determines whether they were launched with private/incognito flags.
    Returns dict: { pid_str: { "name": str, "incognito": bool, "cmd": str } }
    """
    procs = {}
    is_windows = sys.platform.startswith("win")

    if is_windows:
        # Use PowerShell CIM for process command line inspection
        try:
            ps_cmd = (
                "Get-CimInstance Win32_Process | "
                "Where-Object { $_.Name -match 'chrome|msedge|firefox|brave|opera' } | "
                "Select-Object ProcessId, Name, CommandLine | ConvertTo-Json"
            )
            res = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                timeout=5
            )
            if res.returncode == 0 and res.stdout.strip():
                import json
                data = json.loads(res.stdout)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    pid = str(item.get("ProcessId"))
                    name = (item.get("Name") or "").lower()
                    cmd = (item.get("CommandLine") or "").lower()
                    is_incog = any(flag in cmd for flag in ["--incognito", "-inprivate", "--private-window"])
                    procs[pid] = {
                        "name": name,
                        "incognito": is_incog,
                        "cmd": cmd
                    }
        except Exception:
            pass

        # Fallback to tasklist if PowerShell CIM fails
        if not procs:
            try:
                res = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True, timeout=4)
                for line in res.stdout.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    parts = [p.strip('"') for p in line.split('","')]
                    if len(parts) >= 2:
                        name = parts[0].lower()
                        pid = parts[1]
                        if any(b in name for b in ["chrome", "msedge", "firefox", "brave", "opera"]):
                            procs[pid] = {"name": name, "incognito": False, "cmd": ""}
            except Exception:
                pass
    else:
        # macOS / Linux process inspection
        try:
            res = subprocess.run(["ps", "-eo", "pid,command"], capture_output=True, text=True, timeout=4)
            for line in res.stdout.splitlines():
                parts = line.strip().split(None, 1)
                if len(parts) >= 2:
                    pid, cmd = parts[0], parts[1].lower()
                    if any(b in cmd for b in ["chrome", "edge", "safari", "firefox", "brave"]):
                        is_incog = any(flag in cmd for flag in ["--incognito", "-inprivate", "--private-window", "-private"])
                        pname = "chrome" if "chrome" in cmd else ("edge" if "edge" in cmd else ("safari" if "safari" in cmd else "browser"))
                        procs[pid] = {"name": pname, "incognito": is_incog, "cmd": cmd}
        except Exception:
            pass

    return procs


def parse_active_browser_sockets(browser_procs=None, limit=50):
    """
    Forensically inspects active TCP and UDP network connections established by
    running browser processes.
    
    Even if a browser tab is in Incognito mode, the host OS kernel tracks all
    established connections to destination web servers. By resolving these destination
    IPs back to domains via Reverse DNS, we identify sites active in private sessions.
    """
    artifacts = []
    if browser_procs is None:
        browser_procs = get_active_browser_processes()

    if not browser_procs:
        return artifacts

    now = datetime.now()
    is_windows = sys.platform.startswith("win")

    if is_windows:
        try:
            res = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=6)
            seen_hosts = set()
            for line in res.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 5 and parts[3] in ("ESTABLISHED", "TIME_WAIT", "CLOSE_WAIT"):
                    proto, l_addr, r_addr, state, pid = parts[0], parts[1], parts[2], parts[3], parts[4]
                    if pid in browser_procs:
                        # Extract IP and Port handling both IPv4 and IPv6 [ip]:port
                        if ":" in r_addr:
                            r_ip = r_addr.rsplit(":", 1)[0].strip("[]")
                            r_port = r_addr.rsplit(":", 1)[1]
                            if r_port in ("80", "443", "8080", "8443", "5228"):
                                proc_info = browser_procs[pid]
                                bname = proc_info["name"]
                                is_incog = proc_info["incognito"]

                                host = _resolve_ip(r_ip)
                                if not host or host in ("localhost", "0.0.0.0"):
                                    continue
                                
                                # Avoid duplicating the exact same host in a single live scan
                                if host in seen_hosts:
                                    continue
                                seen_hosts.add(host)

                                # Determine browser display name
                                if "msedge" in bname or "edge" in bname:
                                    display_source = "Edge InPrivate Socket" if is_incog else "Edge Active Socket"
                                elif "chrome" in bname:
                                    display_source = "Chrome Incognito Socket" if is_incog else "Chrome Active Socket"
                                else:
                                    display_source = f"{bname.capitalize()} Active Socket"

                                artifacts.append({
                                    "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                                    "dt": now,
                                    "source": display_source,
                                    "category": "Incognito Activity",
                                    "title": f"Active Session Host: {host}",
                                    "details": (
                                        f"Forensic Evidence: Active OS Socket (PID: {pid}, Process: {bname})\n"
                                        f"Remote Endpoint: {r_ip}:{r_port} ({proto} {state})\n"
                                        f"Method: OS Kernel TCP/IP Endpoint Enumeration & Reverse DNS\n"
                                        f"Incognito CLI Flag Detected: {'YES' if is_incog else 'No (Standard/Tab Invocation)'}"
                                    ),
                                    "domain": host,
                                    "extra": f"Port {r_port} | Socket State: {state}"
                                })

                                if len(artifacts) >= limit:
                                    break
        except Exception:
            pass
    else:
        # macOS / Linux: Use lsof or netstat
        try:
            res = subprocess.run(["lsof", "-iTCP", "-sTCP:ESTABLISHED", "-n", "-P"], capture_output=True, text=True, timeout=5)
            seen_hosts = set()
            for line in res.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 9:
                    pname = parts[0].lower()
                    pid = parts[1]
                    name_field = parts[8]  # local->remote
                    if any(b in pname for b in ["chrome", "edge", "safari", "firefox"]):
                        if "->" in name_field:
                            r_endpoint = name_field.split("->")[1]
                            if ":" in r_endpoint:
                                r_ip, r_port = r_endpoint.rsplit(":", 1)
                                if r_port in ("80", "443", "8080", "8443"):
                                    host = _resolve_ip(r_ip)
                                    if host and host not in seen_hosts:
                                        seen_hosts.add(host)
                                        artifacts.append({
                                            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                                            "dt": now,
                                            "source": f"{pname.capitalize()} Active Socket",
                                            "category": "Incognito Activity",
                                            "title": f"Active Session Host: {host}",
                                            "details": f"macOS Socket Trace (PID {pid}) | Remote: {r_ip}:{r_port}",
                                            "domain": host,
                                            "extra": f"macOS lsof Socket | Port: {r_port}"
                                        })
                                        if len(artifacts) >= limit:
                                            break
        except Exception:
            pass

    return artifacts


def parse_dns_cache_traces(limit=60):
    """
    Attempts to read the operating system DNS resolver cache.
    When a user browses in incognito mode, the operating system still resolves
    the domain name and caches it in local DNS memory.
    """
    artifacts = []
    is_windows = sys.platform.startswith("win")
    now = datetime.now()

    if is_windows:
        # 1. Try ipconfig /displaydns (works when elevated or on compatible Windows builds)
        try:
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
                for line in lines:
                    line = line.strip()
                    if line.startswith("Record Name"):
                        parts = line.split(":")
                        if len(parts) >= 2:
                            domain = parts[1].strip().lower().rstrip(".")
                            # Filter internal/telemetry noise
                            if domain and not any(ign in domain for ign in ["local", "arpa", "microsoft", "windowsupdate", "google"]):
                                current_domain = domain
                    elif "Record Type" in line and current_domain:
                        artifacts.append({
                            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                            "dt": now,
                            "source": "DNS Resolver Cache",
                            "category": "Incognito Activity",
                            "title": f"DNS Host Resolution: {current_domain}",
                            "details": (
                                f"Forensic Evidence: Active OS DNS Cache Record\n"
                                f"Resolved Domain: {current_domain}\n"
                                f"Forensic Mechanism: Windows DnsClient Cache Enumeration"
                            ),
                            "domain": current_domain,
                            "extra": "Evidence: OS DNS Cache Entry"
                        })
                        current_domain = None
                        if len(artifacts) >= limit:
                            break
        except Exception:
            pass

        # 2. Try PowerShell Get-DnsClientCache
        if not artifacts:
            try:
                ps_dns = "Get-DnsClientCache -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Entry | Select-Object -Unique -First 30"
                res = subprocess.run(
                    ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_dns],
                    capture_output=True,
                    text=True,
                    timeout=4
                )
                if res.returncode == 0 and res.stdout.strip():
                    for line in res.stdout.splitlines():
                        domain = line.strip().lower().rstrip(".")
                        if domain and len(domain) > 3 and "." in domain:
                            if not any(ign in domain for ign in ["local", "arpa", "msft", "microsoft", "windows"]):
                                artifacts.append({
                                    "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                                    "dt": now,
                                    "source": "DNS Resolver Cache",
                                    "category": "Incognito Activity",
                                    "title": f"DNS Host Resolution: {domain}",
                                    "details": f"PowerShell DNS Cache Entry | Host: {domain}",
                                    "domain": domain,
                                    "extra": "Evidence: DnsClientCache Record"
                                })
            except Exception:
                pass

    return artifacts


def parse_incognito_downloads(limit=15):
    """
    Scans for files downloaded during active sessions. Even when downloaded
    inside Incognito mode, the browser leaves the file on the physical disk.
    Files modified within the last 24 hours are cataloged.
    """
    artifacts = []
    downloads_dir = os.path.expanduser("~/Downloads")
    if not os.path.exists(downloads_dir):
        return artifacts

    try:
        entries = []
        now = datetime.now()
        yesterday_ts = (now - timedelta(hours=24)).timestamp()

        for entry in os.scandir(downloads_dir):
            if entry.name.startswith("."):
                continue
            try:
                stat = entry.stat()
                # Include files downloaded in last 24 hours
                if stat.st_mtime >= yesterday_ts:
                    entries.append((stat.st_mtime, entry.name, entry.path, stat.st_size))
            except Exception:
                continue

        # Sort newest first
        entries.sort(key=lambda x: x[0], reverse=True)
        for mtime, name, path, size in entries[:limit]:
            dt = datetime.fromtimestamp(mtime)
            size_mb = round(size / (1024 * 1024), 2)
            artifacts.append({
                "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "dt": dt,
                "source": "Persistent Downloads",
                "category": "Incognito Activity",
                "title": f"Physical Disk File: {name}",
                "details": (
                    f"Forensic Evidence: Physical File Persistence in Downloads\n"
                    f"File Name: {name}\n"
                    f"File Path: {path}\n"
                    f"Size: {size_mb} MB | Modified: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Forensic Principle: Files downloaded in private browsing persist on disk despite history deletion."
                ),
                "domain": "Local File System",
                "extra": f"Size: {size_mb} MB | Physical Artifact"
            })
    except Exception:
        pass

    return artifacts


def detect_private_process_launches():
    """
    Checks if any browser process is currently executing with explicit private
    browsing CLI arguments.
    """
    artifacts = []
    procs = get_active_browser_processes()
    now = datetime.now()

    for pid, info in procs.items():
        if info.get("incognito"):
            pname = info["name"]
            artifacts.append({
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "dt": now,
                "source": "Process Audit Table",
                "category": "Incognito Activity",
                "title": f"Active Private Window Instance: {pname} (PID: {pid})",
                "details": (
                    f"Forensic Evidence: Active Browser Process with Private CLI Flag\n"
                    f"Process Name: {pname} | PID: {pid}\n"
                    f"Command Line: {info.get('cmd', '')}\n"
                    f"Forensic Method: OS Process Management Table Inspection"
                ),
                "domain": "Local System Process",
                "extra": f"PID: {pid} | Flag: Private Browsing Active"
            })

    return artifacts


def get_all_incognito_artifacts():
    """
    Master aggregator for live incognito forensic artifacts.
    Combines:
    1. Active Browser Sockets (TCP/IP network endpoint correlation)
    2. OS DNS Resolver Cache
    3. Persistent Downloads
    4. Private Process Execution Audit
    """
    traces = []

    # 1. Active Process Flags
    try:
        traces.extend(detect_private_process_launches())
    except Exception:
        pass

    # 2. Active Sockets
    try:
        traces.extend(parse_active_browser_sockets())
    except Exception:
        pass

    # 3. DNS Cache
    try:
        traces.extend(parse_dns_cache_traces())
    except Exception:
        pass

    # 4. Downloads
    try:
        traces.extend(parse_incognito_downloads())
    except Exception:
        pass

    return traces
