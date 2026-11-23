"""
Module: about_dialog.py
Project: TraceLens - Browser & App Artifact Timeline Visualizer
Contributed by: Tanishq Gunjal (Project Lead)

Description:
A dedicated Project Information and Group Credits dialog box.
Lists all 4 group members with their respective contributions, project objectives,
and academic submission credentials.
"""

import tkinter as tk
from tkinter import ttk


def show_about_dialog(parent):
    """
    Displays the About TraceLens & Project Team modal dialog.
    """
    dialog = tk.Toplevel(parent)
    dialog.title("About TraceLens - Group Project Details")
    dialog.geometry("560x520")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()

    # Center dialog relative to parent
    try:
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 280
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 260
        dialog.geometry(f"+{max(0, x)}+{max(0, y)}")
    except Exception:
        pass

    dialog.configure(bg="#f8fafc")

    # Header frame
    header_frame = tk.Frame(dialog, bg="#1e3a8a", padx=20, pady=16)
    header_frame.pack(fill=tk.X)

    title_lbl = tk.Label(
        header_frame,
        text="TraceLens: Artifact Timeline Visualizer",
        font=("Segoe UI", 16, "bold"),
        fg="#ffffff",
        bg="#1e3a8a"
    )
    title_lbl.pack(anchor="w")

    subtitle_lbl = tk.Label(
        header_frame,
        text="First Year Engineering Mini-Project Submission",
        font=("Segoe UI", 10),
        fg="#93c5fd",
        bg="#1e3a8a"
    )
    subtitle_lbl.pack(anchor="w", pady=(2, 0))

    # Main content container
    content_frame = tk.Frame(dialog, bg="#f8fafc", padx=20, pady=16)
    content_frame.pack(fill=tk.BOTH, expand=True)

    # Project Description
    desc_text = (
        "TraceLens correlates browser history, downloads, web searches, and "
        "operating system file/application activity into a unified chronological "
        "forensic timeline to assist investigators and researchers."
    )
    desc_lbl = tk.Label(
        content_frame,
        text=desc_text,
        font=("Segoe UI", 9),
        fg="#334155",
        bg="#f8fafc",
        wraplength=510,
        justify="left"
    )
    desc_lbl.pack(anchor="w", pady=(0, 14))

    # Group Members Section
    team_label = tk.Label(
        content_frame,
        text="PROJECT GROUP MEMBERS & ROLES",
        font=("Segoe UI", 10, "bold"),
        fg="#1e40af",
        bg="#f8fafc"
    )
    team_label.pack(anchor="w", pady=(0, 8))

    team_members = [
        ("1. Tanishq Gunjal (PRN: 1272261851)", "Team Leader", "1272261851.t@mitwpu.edu.in", "GUI Architecture, System Integration & Event Flow"),
        ("2. Janhavi Dahiwale (PRN: 1272261225)", "Member", "1272261225.j@mitwpu.edu.in", "Browser Artifact Parser (Chrome & Edge SQLite Extraction)"),
        ("3. OM Nalawade (PRN: 1272261153)", "Member", "1272261153.o@mitwpu.edu.in", "App Activity Parser & Timeline Correlation Engine"),
        ("4. Ayush Warudkar (PRN: 1272261894)", "Member", "1272261894.a@mitwpu.edu.in", "Visual Analytics Charts, HTML/CSV Reports & Testing"),
    ]

    for name, role, email, contrib in team_members:
        card = tk.Frame(content_frame, bg="#ffffff", bd=1, relief=tk.SOLID, padx=10, pady=5)
        card.pack(fill=tk.X, pady=2)

        top_line = tk.Frame(card, bg="#ffffff")
        top_line.pack(fill=tk.X)

        n_lbl = tk.Label(top_line, text=name, font=("Segoe UI", 9, "bold"), fg="#0f172a", bg="#ffffff")
        n_lbl.pack(side=tk.LEFT)

        r_lbl = tk.Label(top_line, text=f"[{role}]", font=("Segoe UI", 8, "italic"), fg="#2563eb", bg="#ffffff")
        r_lbl.pack(side=tk.RIGHT)

        e_lbl = tk.Label(card, text=f"Email: {email} | Focus: {contrib}", font=("Segoe UI", 8), fg="#64748b", bg="#ffffff")
        e_lbl.pack(anchor="w", pady=(1, 0))

    # Tech Stack & Footnote
    tech_lbl = tk.Label(
        content_frame,
        text="Technology Stack: Python 3, Tkinter GUI, SQLite3, Matplotlib, HTML5/CSS3",
        font=("Segoe UI", 8, "italic"),
        fg="#64748b",
        bg="#f8fafc"
    )
    tech_lbl.pack(anchor="w", pady=(12, 0))

    # Bottom Close Button
    btn_frame = tk.Frame(dialog, bg="#f1f5f9", padx=16, pady=10)
    btn_frame.pack(fill=tk.X, side=tk.BOTTOM)

    close_btn = ttk.Button(btn_frame, text="Close", command=dialog.destroy)
    close_btn.pack(side=tk.RIGHT)
