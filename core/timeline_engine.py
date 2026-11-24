"""
Module: timeline_engine.py
Project: TraceLens - Browser & App Artifact Timeline Visualizer
Contributed by: OM Nalawade (Group Member 3) & Tanishq Gunjal (Group Member 1)

Description:
This module acts as the central correlation engine for TraceLens.
It takes disparate artifact streams from various web browsers and operating system
locations, standardizes them into unified timeline events, provides filtering and
search functions, and computes forensic metrics and statistics.
"""

from datetime import datetime, timedelta
from collections import Counter

from parsers.browser_parser import get_all_browser_artifacts
from parsers.app_parser import get_all_app_artifacts
from parsers.sample_generator import generate_forensic_case_artifacts
from parsers.incognito_parser import get_all_incognito_artifacts


class TimelineEngine:
    def __init__(self):
        # Master list of all loaded artifacts
        self.raw_artifacts = []
        # Current active/filtered artifacts
        self.filtered_artifacts = []
        self.is_demo_mode = False

    def load_artifacts(self, demo_mode=False, limit_per_source=300):
        """
        Loads artifacts from either the real system or the pre-bundled forensic case.
        """
        self.is_demo_mode = demo_mode
        self.raw_artifacts = []

        if demo_mode:
            self.raw_artifacts = generate_forensic_case_artifacts()
        else:
            # 1. Fetch browser artifacts
            try:
                browser_items = get_all_browser_artifacts(limit_per_browser=limit_per_source)
                self.raw_artifacts.extend(browser_items)
            except Exception as e:
                print(f"[Error] Failed to load browser artifacts: {e}")

            # 2. Fetch OS / App artifacts
            try:
                app_items = get_all_app_artifacts(limit=limit_per_source)
                self.raw_artifacts.extend(app_items)
            except Exception as e:
                print(f"[Error] Failed to load app artifacts: {e}")

            # 3. Fetch Incognito & DNS traces
            try:
                incognito_items = get_all_incognito_artifacts()
                self.raw_artifacts.extend(incognito_items)
            except Exception as e:
                print(f"[Error] Failed to load incognito artifacts: {e}")

        # Ensure all artifacts have a sorting key and valid datetime
        valid_items = []
        for item in self.raw_artifacts:
            if not isinstance(item.get("dt"), datetime):
                # Try parsing timestamp string if dt missing
                try:
                    item["dt"] = datetime.strptime(item["timestamp"], "%Y-%m-%d %H:%M:%S")
                except Exception:
                    continue
            valid_items.append(item)

        # Sort chronologically descending (newest first)
        valid_items.sort(key=lambda x: x["dt"], reverse=True)
        self.raw_artifacts = valid_items
        self.filtered_artifacts = list(self.raw_artifacts)
        return len(self.raw_artifacts)

    def filter_artifacts(self, query="", category="All", source="All", date_filter="All Time", sort_ascending=False, incognito_only=False):
        """
        Filters artifacts based on keyword search, category, source, date range, and incognito flag.
        """
        results = list(self.raw_artifacts)
        now = datetime.now()

        # 0. Incognito Mode Filtering
        if incognito_only:
            results = [
                a for a in results
                if "incognito" in a.get("category", "").lower()
                or "incognito" in a.get("source", "").lower()
                or "inprivate" in a.get("source", "").lower()
            ]

        # 1. Date Range Filtering
        if date_filter == "Today":
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            results = [a for a in results if a["dt"] >= today_start]
        elif date_filter == "Last 24 Hours":
            cutoff = now - timedelta(hours=24)
            results = [a for a in results if a["dt"] >= cutoff]
        elif date_filter == "Last 7 Days":
            cutoff = now - timedelta(days=7)
            results = [a for a in results if a["dt"] >= cutoff]
        elif date_filter == "Last 30 Days":
            cutoff = now - timedelta(days=30)
            results = [a for a in results if a["dt"] >= cutoff]

        # 2. Category Filtering
        if category and category != "All":
            results = [a for a in results if a.get("category") == category]

        # 3. Source Filtering
        if source and source != "All":
            results = [a for a in results if a.get("source") == source]

        # 4. Keyword Query Filtering
        if query and query.strip():
            q = query.strip().lower()
            results = [
                a for a in results
                if q in a.get("title", "").lower()
                or q in a.get("details", "").lower()
                or q in a.get("domain", "").lower()
                or q in a.get("source", "").lower()
                or q in a.get("category", "").lower()
            ]

        # 5. Sorting direction
        results.sort(key=lambda x: x["dt"], reverse=not sort_ascending)

        self.filtered_artifacts = results
        return self.filtered_artifacts

    def get_categories(self):
        """
        Returns unique categories present in loaded data.
        """
        cats = sorted(list(set(a.get("category", "General") for a in self.raw_artifacts)))
        return ["All"] + cats

    def get_sources(self):
        """
        Returns unique sources present in loaded data.
        """
        srcs = sorted(list(set(a.get("source", "System") for a in self.raw_artifacts)))
        return ["All"] + srcs

    def compute_statistics(self):
        """
        Calculates summary statistics and data distributions for charts and reports.
        """
        data = self.filtered_artifacts if self.filtered_artifacts else self.raw_artifacts

        total_count = len(data)
        category_counter = Counter()
        source_counter = Counter()
        domain_counter = Counter()
        hour_counter = {h: 0 for h in range(24)}

        earliest_time = None
        latest_time = None

        for item in data:
            dt = item.get("dt")
            if dt:
                hour_counter[dt.hour] += 1
                if earliest_time is None or dt < earliest_time:
                    earliest_time = dt
                if latest_time is None or dt > latest_time:
                    latest_time = dt

            category_counter[item.get("category", "Other")] += 1
            source_counter[item.get("source", "Other")] += 1

            dom = item.get("domain", "")
            if dom and dom not in ["Local System", "Local Disk", "Unknown", "Local/Direct"]:
                domain_counter[dom] += 1

        top_domains = domain_counter.most_common(8)

        stats = {
            "total_count": total_count,
            "earliest_time": earliest_time.strftime("%Y-%m-%d %H:%M:%S") if earliest_time else "N/A",
            "latest_time": latest_time.strftime("%Y-%m-%d %H:%M:%S") if latest_time else "N/A",
            "category_counts": dict(category_counter),
            "source_counts": dict(source_counter),
            "top_domains": top_domains,
            "hourly_counts": hour_counter,
            "is_demo_mode": self.is_demo_mode
        }
        return stats
