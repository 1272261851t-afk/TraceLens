"""
Module: analytics_view.py
Project: TraceLens - Browser & App Artifact Timeline Visualizer
Contributed by: Ayush Warudkar (Group Member 4)

Description:
Provides graphical visualizations of the timeline data using Matplotlib embedded in Tkinter.
Includes:
1. Hourly Activity Distribution (Histogram/Bar Chart)
2. Artifact Category Breakdown (Pie Chart)
3. Top Visited Web Domains (Horizontal Bar Chart)
"""

import tkinter as tk
from tkinter import ttk, messagebox


def show_analytics_window(parent, stats):
    """
    Opens an interactive Visual Analytics window displaying Matplotlib charts.
    """
    total = stats.get("total_count", 0)
    if total == 0:
        messagebox.showinfo("Analytics", "No artifacts currently loaded to visualize. Please scan artifacts or load demo data first.")
        return

    win = tk.Toplevel(parent)
    win.title("TraceLens - Visual Analytics & Forensics Metrics")
    win.geometry("980x680")
    win.minsize(800, 550)

    try:
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    except ImportError:
        # Fallback if matplotlib is missing
        fallback_lbl = tk.Label(
            win,
            text="Matplotlib is not installed.\nInstall it using: pip install matplotlib\n\nBasic Statistics Summary:\n"
                 + f"Total Events: {total}\n"
                 + f"Categories: {stats.get('category_counts')}\n"
                 + f"Sources: {stats.get('source_counts')}",
            font=("Segoe UI", 11),
            padx=20,
            pady=20,
            justify="left"
        )
        fallback_lbl.pack(fill=tk.BOTH, expand=True)
        return

    # Header
    header = tk.Frame(win, bg="#1e293b", padx=16, pady=12)
    header.pack(fill=tk.X)

    title = tk.Label(
        header,
        text=f"Artifact Timeline Analytics ({total} Total Events Analyzed)",
        font=("Segoe UI", 13, "bold"),
        fg="#ffffff",
        bg="#1e293b"
    )
    title.pack(side=tk.LEFT)

    incog_count = stats.get("incognito_count", 0)
    subtitle = tk.Label(
        header,
        text=f"Span: {stats.get('earliest_time')} → {stats.get('latest_time')} | 🕵️ Incognito/Private Traces: {incog_count}",
        font=("Segoe UI", 9),
        fg="#e9d5ff" if incog_count > 0 else "#94a3b8",
        bg="#1e293b"
    )
    subtitle.pack(side=tk.RIGHT)

    # Matplotlib Figure
    fig = Figure(figsize=(10, 6.5), dpi=100)
    fig.patch.set_facecolor("#f8fafc")

    # Subplot 1: Hourly Distribution (Top span)
    ax1 = fig.add_subplot(2, 2, (1, 2))
    hours = list(range(24))
    hour_counts = [stats.get("hourly_counts", {}).get(h, 0) for h in hours]
    hour_labels = [f"{h:02d}:00" for h in hours]

    ax1.bar(hour_labels, hour_counts, color="#3b82f6", edgecolor="#1d4ed8", alpha=0.85, width=0.6)
    ax1.set_title("Timeline Activity by Hour of the Day (00:00 to 23:00)", fontsize=11, fontweight="bold", pad=8)
    ax1.set_xlabel("Hour of the Day", fontsize=9)
    ax1.set_ylabel("Activity Count", fontsize=9)
    ax1.tick_params(axis='x', rotation=45, labelsize=8)
    ax1.tick_params(axis='y', labelsize=8)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.set_facecolor("#ffffff")

    # Subplot 2: Category Breakdown (Pie chart)
    ax2 = fig.add_subplot(2, 2, 3)
    cat_counts = stats.get("category_counts", {})
    if cat_counts:
        cat_labels = list(cat_counts.keys())
        cat_values = list(cat_counts.values())
        colors = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444", "#64748b"][:len(cat_labels)]
        ax2.pie(
            cat_values,
            labels=cat_labels,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors,
            textprops={"fontsize": 8}
        )
        ax2.set_title("Artifacts by Category", fontsize=10, fontweight="bold")
    else:
        ax2.text(0.5, 0.5, "No category data", ha="center", va="center")

    # Subplot 3: Top Web Domains (Horizontal Bar Chart)
    ax3 = fig.add_subplot(2, 2, 4)
    top_domains = stats.get("top_domains", [])
    if top_domains:
        domains = [d[0] for d in reversed(top_domains[:6])]
        d_counts = [d[1] for d in reversed(top_domains[:6])]
        ax3.barh(domains, d_counts, color="#10b981", edgecolor="#059669", height=0.55)
        ax3.set_title("Top Visited Web Domains", fontsize=10, fontweight="bold", pad=8)
        ax3.set_xlabel("Visit Count", fontsize=9)
        ax3.tick_params(axis='x', labelsize=8)
        ax3.tick_params(axis='y', labelsize=8)
        ax3.grid(axis='x', linestyle='--', alpha=0.5)
        ax3.set_facecolor("#ffffff")
    else:
        ax3.text(0.5, 0.5, "No domain activity recorded", ha="center", va="center")

    fig.tight_layout(pad=2.5)

    # Embed Figure in Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Footer close bar
    footer = tk.Frame(win, bg="#f1f5f9", padx=16, pady=8)
    footer.pack(fill=tk.X)

    close_btn = ttk.Button(footer, text="Close Analytics", command=win.destroy)
    close_btn.pack(side=tk.RIGHT)
