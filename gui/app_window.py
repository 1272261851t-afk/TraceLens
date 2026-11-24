"""
Module: app_window.py
Project: TraceLens - Browser & App Artifact Timeline Visualizer
Contributed by: Tanishq Gunjal (Project Lead)

Description:
The core graphical user interface for TraceLens built using Python's standard Tkinter
and ttk widgets. Provides a responsive desktop window with search, filtering,
chronological timeline display, artifact inspection modal, and reporting hooks.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser

from core.timeline_engine import TimelineEngine
from core.report_exporter import export_to_csv, export_to_html
from gui.about_dialog import show_about_dialog
from gui.analytics_view import show_analytics_window


class TraceLensApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TraceLens - Browser & App Artifact Timeline Visualizer")
        self.geometry("1150x720")
        self.minsize(900, 580)

        # Core engine
        self.engine = TimelineEngine()

        # UI state variables
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="All")
        self.source_var = tk.StringVar(value="All")
        self.date_var = tk.StringVar(value="All Time")
        self.sort_asc_var = tk.BooleanVar(value=False)
        self.incognito_only_var = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value="Welcome to TraceLens. Click 'Scan System Artifacts' or 'Load Demo Forensic Case' to begin.")

        # Setup styling and components
        self.setup_styles()
        self.create_header()
        self.create_filter_toolbar()
        self.create_timeline_table()
        self.create_footer_statusbar()

        # Auto-load demo data on launch so user immediately sees a working visualizer
        self.after(300, self.on_load_demo_case)

    def setup_styles(self):
        """
        Configures ttk style colors and typography for a clean desktop presentation.
        """
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # General colors
        self.configure(bg="#f8fafc")

        # Treeview styling
        style.configure(
            "Treeview",
            background="#ffffff",
            foreground="#0f172a",
            rowheight=26,
            fieldbackground="#ffffff",
            font=("Segoe UI", 9)
        )
        style.configure(
            "Treeview.Heading",
            background="#e2e8f0",
            foreground="#1e293b",
            font=("Segoe UI", 9, "bold")
        )
        style.map("Treeview", background=[("selected", "#3b82f6")], foreground=[("selected", "#ffffff")])

        # Buttons
        style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"))
        style.configure("TButton", font=("Segoe UI", 9))
        style.configure("TCombobox", font=("Segoe UI", 9))

    def create_header(self):
        """
        Constructs the top header banner with project details and group credits.
        """
        header_frame = tk.Frame(self, bg="#1e3a8a", padx=16, pady=10)
        header_frame.pack(fill=tk.X)

        # Left title section
        title_box = tk.Frame(header_frame, bg="#1e3a8a")
        title_box.pack(side=tk.LEFT)

        app_title = tk.Label(
            title_box,
            text="TraceLens",
            font=("Segoe UI", 16, "bold"),
            fg="#ffffff",
            bg="#1e3a8a"
        )
        app_title.pack(side=tk.LEFT)

        badge = tk.Label(
            title_box,
            text=" Forensic Visualizer ",
            font=("Segoe UI", 8, "bold"),
            fg="#1e3a8a",
            bg="#93c5fd",
            padx=4,
            pady=1
        )
        badge.pack(side=tk.LEFT, padx=8)

        app_desc = tk.Label(
            title_box,
            text="Browser & App Artifact Timeline Correlator",
            font=("Segoe UI", 9),
            fg="#cbd5e1",
            bg="#1e3a8a"
        )
        app_desc.pack(side=tk.LEFT, padx=4)

        # Right action buttons
        actions_box = tk.Frame(header_frame, bg="#1e3a8a")
        actions_box.pack(side=tk.RIGHT)

        btn_scan = tk.Button(
            actions_box,
            text="Scan System Artifacts",
            command=self.on_scan_system,
            bg="#2563eb",
            fg="#ffffff",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2"
        )
        btn_scan.pack(side=tk.LEFT, padx=4)

        btn_demo = tk.Button(
            actions_box,
            text="Load Demo Forensic Case",
            command=self.on_load_demo_case,
            bg="#059669",
            fg="#ffffff",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2"
        )
        btn_demo.pack(side=tk.LEFT, padx=4)

        btn_clear = tk.Button(
            actions_box,
            text="Clear",
            command=self.on_clear_timeline,
            bg="#475569",
            fg="#ffffff",
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2"
        )
        btn_clear.pack(side=tk.LEFT, padx=4)

        # Team sub-strip
        team_strip = tk.Frame(self, bg="#0f172a", padx=16, pady=3)
        team_strip.pack(fill=tk.X)

        team_text = (
            "Project Team (1st Year Engg): 1. Tanishq Gunjal (Lead)  |  "
            "2. Janhavi Dahiwale  |  3. OM Nalawade  |  4. Ayush Warudkar"
        )
        team_lbl = tk.Label(
            team_strip,
            text=team_text,
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#0f172a"
        )
        team_lbl.pack(side=tk.LEFT)

    def create_filter_toolbar(self):
        """
        Creates search entry and filter dropdowns for real-time timeline queries.
        """
        filter_frame = tk.Frame(self, bg="#ffffff", bd=1, relief=tk.SOLID, padx=12, pady=8)
        filter_frame.pack(fill=tk.X, padx=12, pady=(10, 4))

        # Search Query Box
        tk.Label(filter_frame, text="Search:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 4))
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=22)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.apply_filters())

        # Category Filter
        tk.Label(filter_frame, text="Category:", font=("Segoe UI", 9), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 4))
        self.category_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.category_var,
            state="readonly",
            values=["All"],
            width=16
        )
        self.category_cb.pack(side=tk.LEFT, padx=(0, 10))
        self.category_cb.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())

        # Source Filter
        tk.Label(filter_frame, text="Source:", font=("Segoe UI", 9), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 4))
        self.source_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.source_var,
            state="readonly",
            values=["All"],
            width=16
        )
        self.source_cb.pack(side=tk.LEFT, padx=(0, 10))
        self.source_cb.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())

        # Date Range Filter
        tk.Label(filter_frame, text="Timeframe:", font=("Segoe UI", 9), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 4))
        self.date_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.date_var,
            state="readonly",
            values=["All Time", "Today", "Last 24 Hours", "Last 7 Days", "Last 30 Days"],
            width=13
        )
        self.date_cb.pack(side=tk.LEFT, padx=(0, 10))
        self.date_cb.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())

        # Sort Order Checkbox
        sort_chk = tk.Checkbutton(
            filter_frame,
            text="Oldest First",
            variable=self.sort_asc_var,
            command=self.apply_filters,
            bg="#ffffff",
            font=("Segoe UI", 9)
        )
        sort_chk.pack(side=tk.LEFT, padx=(0, 10))

        # Incognito Only Filter Checkbox
        incognito_chk = tk.Checkbutton(
            filter_frame,
            text="🕵️ Incognito Only",
            variable=self.incognito_only_var,
            command=self.apply_filters,
            bg="#ffffff",
            fg="#7e22ce",
            activeforeground="#581c87",
            font=("Segoe UI", 9, "bold")
        )
        incognito_chk.pack(side=tk.LEFT, padx=(0, 4))

        # Incognito Forensics Methodology Guide button
        incognito_guide_btn = ttk.Button(
            filter_frame,
            text="ℹ️ Methodology",
            command=self.show_incognito_info
        )
        incognito_guide_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Reset button
        reset_btn = ttk.Button(filter_frame, text="Reset Filters", command=self.reset_filters)
        reset_btn.pack(side=tk.RIGHT)

    def create_timeline_table(self):
        """
        Creates the main chronological Treeview table with scrollbars.
        """
        container = tk.Frame(self, bg="#f8fafc", padx=12, pady=4)
        container.pack(fill=tk.BOTH, expand=True)

        columns = ("num", "timestamp", "source", "category", "title", "domain", "extra")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse")

        # Headings
        self.tree.heading("num", text="#")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("source", text="Source")
        self.tree.heading("category", text="Category")
        self.tree.heading("title", text="Event / Title")
        self.tree.heading("domain", text="Domain / Scope")
        self.tree.heading("extra", text="Extra Attributes")

        # Column widths
        self.tree.column("num", width=45, minwidth=40, anchor="center")
        self.tree.column("timestamp", width=140, minwidth=130, anchor="w")
        self.tree.column("source", width=110, minwidth=90, anchor="w")
        self.tree.column("category", width=125, minwidth=100, anchor="w")
        self.tree.column("title", width=380, minwidth=250, anchor="w")
        self.tree.column("domain", width=140, minwidth=110, anchor="w")
        self.tree.column("extra", width=170, minwidth=120, anchor="w")

        # Scrollbars
        vsb = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Row tag colors
        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("oddrow", background="#f8fafc")
        self.tree.tag_configure("incognitorow", background="#faf5ff", foreground="#581c87")

        # Double click to open artifact details
        self.tree.bind("<Double-1>", self.on_item_double_click)

    def create_footer_statusbar(self):
        """
        Creates bottom status summary and export action buttons.
        """
        footer_frame = tk.Frame(self, bg="#f1f5f9", bd=1, relief=tk.SOLID, padx=12, pady=6)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        status_lbl = tk.Label(
            footer_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            fg="#334155",
            bg="#f1f5f9"
        )
        status_lbl.pack(side=tk.LEFT)

        # Right buttons
        about_btn = ttk.Button(footer_frame, text="About Team", command=lambda: show_about_dialog(self))
        about_btn.pack(side=tk.RIGHT, padx=4)

        csv_btn = ttk.Button(footer_frame, text="Export CSV", command=self.on_export_csv)
        csv_btn.pack(side=tk.RIGHT, padx=4)

        html_btn = ttk.Button(footer_frame, text="Export HTML Report", command=self.on_export_html)
        html_btn.pack(side=tk.RIGHT, padx=4)

        analytics_btn = tk.Button(
            footer_frame,
            text="Visual Analytics (Charts)",
            command=self.on_show_analytics,
            bg="#2563eb",
            fg="#ffffff",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=8,
            pady=2,
            cursor="hand2"
        )
        analytics_btn.pack(side=tk.RIGHT, padx=6)

    def refresh_filter_dropdowns(self):
        """
        Updates the category and source comboboxes based on loaded data.
        """
        cats = self.engine.get_categories()
        srcs = self.engine.get_sources()

        self.category_cb["values"] = cats
        if self.category_var.get() not in cats:
            self.category_var.set("All")

        self.source_cb["values"] = srcs
        if self.source_var.get() not in srcs:
            self.source_var.set("All")

    def populate_table(self, artifacts):
        """
        Renders the artifacts list into the Treeview.
        """
        self.tree.delete(*self.tree.get_children())
        for idx, item in enumerate(artifacts, start=1):
            is_incognito = (
                "incognito" in item.get("category", "").lower()
                or "incognito" in item.get("source", "").lower()
                or "inprivate" in item.get("source", "").lower()
            )
            if is_incognito:
                tag = "incognitorow"
            else:
                tag = "evenrow" if idx % 2 == 0 else "oddrow"

            self.tree.insert(
                "",
                tk.END,
                iid=str(idx - 1),
                values=(
                    idx,
                    item.get("timestamp", ""),
                    item.get("source", ""),
                    item.get("category", ""),
                    item.get("title", ""),
                    item.get("domain", ""),
                    item.get("extra", "")
                ),
                tags=(tag,)
            )

        total_loaded = len(self.engine.raw_artifacts)
        showing = len(artifacts)
        mode_str = "Demo Forensic Case" if self.engine.is_demo_mode else "Live System Data"

        if self.incognito_only_var.get():
            if showing > 0:
                self.status_var.set(
                    f"🕵️ Incognito Filter: Showing {showing} private session traces (Sockets, DNS, and Downloads) | Mode: {mode_str}"
                )
            else:
                self.status_var.set(
                    f"🕵️ Incognito Filter: 0 traces found. Tip: Open a site in Incognito and re-scan, or click 'Load Demo Forensic Case'."
                )
        else:
            self.status_var.set(
                f"Mode: {mode_str} | Displaying {showing} of {total_loaded} events | Double-click row for full details"
            )

    def apply_filters(self):
        """
        Filters the artifacts based on the UI controls.
        """
        query = self.search_var.get()
        category = self.category_var.get()
        source = self.source_var.get()
        date_filter = self.date_var.get()
        sort_asc = self.sort_asc_var.get()
        incognito_only = self.incognito_only_var.get()

        filtered = self.engine.filter_artifacts(
            query=query,
            category=category,
            source=source,
            date_filter=date_filter,
            sort_ascending=sort_asc,
            incognito_only=incognito_only
        )
        self.populate_table(filtered)

    def reset_filters(self):
        """
        Resets search and all filter criteria.
        """
        self.search_var.set("")
        self.category_var.set("All")
        self.source_var.set("All")
        self.date_var.set("All Time")
        self.sort_asc_var.set(False)
        self.incognito_only_var.set(False)
        self.apply_filters()

    def on_load_demo_case(self):
        """
        Loads the pre-configured forensic scenario dataset.
        """
        count = self.engine.load_artifacts(demo_mode=True)
        self.refresh_filter_dropdowns()
        self.reset_filters()
        messagebox.showinfo(
            "Demo Forensic Case Loaded",
            f"Successfully loaded {count} forensic timeline events!\n\n"
            "This simulated case demonstrates web searches, downloads, and app executions "
            "typical of a digital forensics investigation."
        )

    def on_scan_system(self):
        """
        Scans real browser and system artifacts on the machine.
        """
        self.status_var.set("Scanning system artifacts (Chrome, Edge, Windows Recent)... Please wait.")
        self.update_idletasks()

        count = self.engine.load_artifacts(demo_mode=False, limit_per_source=400)
        self.refresh_filter_dropdowns()
        self.reset_filters()

        if count == 0:
            messagebox.showwarning(
                "Scan Complete",
                "No browser or system artifacts found or browser databases were locked.\n"
                "Tip: You can use 'Load Demo Forensic Case' to test the full visualizer."
            )
        else:
            messagebox.showinfo(
                "Scan Complete",
                f"Successfully parsed and correlated {count} digital artifacts from your system!"
            )

    def on_clear_timeline(self):
        """
        Clears the current timeline.
        """
        self.engine.raw_artifacts = []
        self.engine.filtered_artifacts = []
        self.populate_table([])
        self.refresh_filter_dropdowns()
        self.status_var.set("Timeline cleared.")

    def on_item_double_click(self, event):
        """
        Opens a detailed popup showing the full artifact metadata.
        """
        selected_item = self.tree.focus()
        if not selected_item:
            return

        idx = int(selected_item)
        if idx >= len(self.engine.filtered_artifacts):
            return

        art = self.engine.filtered_artifacts[idx]

        is_incog = (
            "incognito" in art.get("category", "").lower()
            or "incognito" in art.get("source", "").lower()
            or "inprivate" in art.get("source", "").lower()
            or "incognito" in art.get("extra", "").lower()
        )

        header_bg = "#581c87" if is_incog else "#1e3a8a"

        # Popup dialog
        detail_win = tk.Toplevel(self)
        detail_win.title(f"Artifact Detail Inspector - Event #{idx + 1}")
        detail_win.geometry("660x520")
        detail_win.minsize(500, 380)
        detail_win.configure(bg="#f8fafc")

        header = tk.Frame(detail_win, bg=header_bg, padx=16, pady=12)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text=f"Artifact: {art.get('category')} ({art.get('source')})",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg=header_bg
        ).pack(anchor="w")

        body = tk.Frame(detail_win, bg="#f8fafc", padx=16, pady=14)
        body.pack(fill=tk.BOTH, expand=True)

        if is_incog:
            banner = tk.Frame(body, bg="#f5d0fe", padx=10, pady=8, highlightbackground="#c084fc", highlightthickness=1)
            banner.pack(fill=tk.X, pady=(0, 10))
            tk.Label(
                banner,
                text="🕵️ Private Browsing Forensic Artifact (Non-SQLite Trace)\n"
                     "Chromium does not commit visited private URLs to disk databases. TraceLens recovers "
                     "this artifact from operating system network sockets, DNS cache, or filesystem persistence.",
                font=("Segoe UI", 8, "italic"),
                fg="#581c87",
                bg="#f5d0fe",
                justify="left"
            ).pack(anchor="w")

        fields = [
            ("Timestamp", art.get("timestamp", "")),
            ("Source", art.get("source", "")),
            ("Category", art.get("category", "")),
            ("Domain / Host", art.get("domain", "")),
            ("Title / Event Name", art.get("title", "")),
            ("Extra Attributes", art.get("extra", "")),
        ]

        for label, val in fields:
            row = tk.Frame(body, bg="#f8fafc")
            row.pack(fill=tk.X, pady=3)
            tk.Label(row, text=f"{label}:", font=("Segoe UI", 9, "bold"), width=16, anchor="w", bg="#f8fafc").pack(side=tk.LEFT)
            tk.Label(row, text=str(val), font=("Segoe UI", 9), anchor="w", bg="#f8fafc", wraplength=460, justify="left").pack(side=tk.LEFT)

        # Full URL / Path details
        tk.Label(body, text="Full Details (URL / Path):", font=("Segoe UI", 9, "bold"), bg="#f8fafc").pack(anchor="w", pady=(10, 2))
        detail_text = tk.Text(body, height=5, font=("Consolas", 9), wrap="break")
        detail_text.insert(tk.END, art.get("details", ""))
        detail_text.configure(state="disabled")
        detail_text.pack(fill=tk.BOTH, expand=True)

        # Bottom buttons
        btn_box = tk.Frame(detail_win, bg="#f1f5f9", padx=16, pady=8)
        btn_box.pack(fill=tk.X)

        def copy_details():
            self.clipboard_clear()
            self.clipboard_append(art.get("details", ""))
            messagebox.showinfo("Copied", "Artifact details copied to clipboard!", parent=detail_win)

        ttk.Button(btn_box, text="Copy Details", command=copy_details).pack(side=tk.LEFT)
        ttk.Button(btn_box, text="Close", command=detail_win.destroy).pack(side=tk.RIGHT)

    def on_show_analytics(self):
        """
        Opens the Matplotlib Visual Analytics charts window.
        """
        stats = self.engine.compute_statistics()
        show_analytics_window(self, stats)

    def on_export_csv(self):
        """
        Exports the current timeline view to a CSV file.
        """
        if not self.engine.filtered_artifacts:
            messagebox.showwarning("Export CSV", "No artifacts available to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            initialfile="TraceLens_Timeline_Export.csv"
        )
        if not file_path:
            return

        try:
            export_to_csv(self.engine.filtered_artifacts, file_path)
            messagebox.showinfo("Export Successful", f"Exported {len(self.engine.filtered_artifacts)} events to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export CSV:\n{e}")

    def on_export_html(self):
        """
        Exports the current timeline view to a stylized HTML report and prompts to view it.
        """
        if not self.engine.filtered_artifacts:
            messagebox.showwarning("Export HTML", "No artifacts available to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")],
            initialfile="TraceLens_Forensic_Report.html"
        )
        if not file_path:
            return

        try:
            stats = self.engine.compute_statistics()
            export_to_html(self.engine.filtered_artifacts, stats, file_path)
            res = messagebox.askyesno(
                "Report Generated",
                f"HTML Forensic Report successfully generated!\n\nWould you like to open it in your web browser now?"
            )
            if res:
                webbrowser.open(file_path)
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export HTML Report:\n{e}")

    def show_incognito_info(self):
        """
        Displays a structured academic explanation of how private browsing artifacts
        are forensically recovered from the operating system.
        """
        info_win = tk.Toplevel(self)
        info_win.title("TraceLens - Incognito Forensics Methodology")
        info_win.geometry("700x540")
        info_win.minsize(600, 420)
        info_win.configure(bg="#ffffff")

        header = tk.Frame(info_win, bg="#581c87", padx=18, pady=14)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="🕵️ Incognito & Private Browsing Forensic Methodology",
            font=("Segoe UI", 13, "bold"),
            fg="#ffffff",
            bg="#581c87"
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Scientific & Forensic Principles for 1st Year Engineering Demonstration",
            font=("Segoe UI", 9),
            fg="#f5d0fe",
            bg="#581c87"
        ).pack(anchor="w", pady=(2, 0))

        content_frame = tk.Frame(info_win, bg="#ffffff", padx=18, pady=14)
        content_frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(content_frame, wrap="word", font=("Segoe UI", 9), bg="#ffffff", relief=tk.FLAT)
        vsb = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        explanation = (
            "1. Why Browsers Do Not Save History to SQLite in Incognito Mode:\n"
            "   Chromium (Google Chrome, Microsoft Edge, Brave) and Gecko (Firefox) explicitly isolate "
            "private sessions in RAM. Visited URLs are never written to the on-disk 'History' SQLite database. "
            "Therefore, any forensic tool claiming to read SQLite history during private sessions is technically invalid.\n\n"
            "2. How TraceLens Recovers Evidence from the Host Operating System:\n"
            "   TraceLens uses multi-vector operating system forensics complying with standard digital forensic principles:\n\n"
            "   a. Active Network Sockets & QUIC Streams:\n"
            "      While an incognito tab is open, the OS kernel (Windows/macOS) maintains active TCP and UDP "
            "connections to remote servers (ports 80, 443). TraceLens enumerates these sockets, maps them to "
            "browser process IDs (PIDs), and performs Reverse DNS lookups to identify visited domains.\n\n"
            "   b. Operating System DNS Resolver Cache:\n"
            "      When resolving domain names, the OS DNS client stores resolved IP addresses in local memory "
            "(accessible via 'ipconfig /displaydns' or PowerShell 'Get-DnsClientCache').\n\n"
            "   c. Persistent Download Metadata:\n"
            "      Files downloaded in Incognito mode are NOT wiped upon browser exit; they remain saved on "
            "physical storage with file creation and modification timestamps intact.\n\n"
            "   d. Process Execution Inspection:\n"
            "      The process management table records command-line switches like '--incognito' or '-inprivate'.\n\n"
            "3. Key Takeaway for Academic Viva & Evaluation:\n"
            "   In encrypted HTTPS traffic, the domain name is exposed via DNS, SNI, and IP reverse resolution, "
            "while the exact URL query path is encrypted. TraceLens forensically reports the accurate, truthful "
            "domain traces without fabricating inaccessible encrypted data."
        )

        text_widget.insert(tk.END, explanation)
        text_widget.configure(state="disabled")

        btn_box = tk.Frame(info_win, bg="#f8fafc", padx=16, pady=10)
        btn_box.pack(fill=tk.X)
        ttk.Button(btn_box, text="Close", command=info_win.destroy).pack(side=tk.RIGHT)
