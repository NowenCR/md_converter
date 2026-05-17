"""
ui_components.py — UI layer for MD Forge
Dark industrial-minimal aesthetic with green accent
"""

import tkinter as tk
from tkinter import ttk
import os
from pathlib import Path


# ── Color palette ────────────────────────────────────────────────────────────
BG       = "#0d1117"     # deep dark
SURFACE  = "#161b22"     # panels
BORDER   = "#30363d"     # subtle borders
TEXT     = "#c9d1d9"     # body text
TEXT_DIM = "#8b949e"     # muted text
ACCENT   = "#3fb950"     # green accent
ACCENT2  = "#58a6ff"     # blue accent
ERROR    = "#f85149"     # red for errors
WARN     = "#d29922"     # yellow for pending
DONE     = "#3fb950"     # green for done
HEADER   = "#e6edf3"     # bright headers


class ModernUI:
    def __init__(self, app):
        self.app = app

    def setup(self, root):
        self._configure_styles()
        self._build_layout(root)

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(".", background=BG, foreground=TEXT,
                        font=("Consolas", 10), borderwidth=0)

        style.configure("TFrame", background=BG)
        style.configure("Surface.TFrame", background=SURFACE)

        style.configure("TLabel", background=BG, foreground=TEXT)
        style.configure("Dim.TLabel", background=BG, foreground=TEXT_DIM)
        style.configure("Header.TLabel", background=BG, foreground=HEADER,
                        font=("Consolas", 11, "bold"))
        style.configure("Surface.TLabel", background=SURFACE, foreground=TEXT)

        # Buttons
        style.configure("Accent.TButton",
                        background=ACCENT, foreground="#0d1117",
                        font=("Consolas", 10, "bold"),
                        padding=(14, 8), relief="flat", borderwidth=0)
        style.map("Accent.TButton",
                  background=[("active", "#2ea043"), ("pressed", "#238636")])

        style.configure("Ghost.TButton",
                        background=SURFACE, foreground=TEXT,
                        font=("Consolas", 10),
                        padding=(12, 7), relief="flat", borderwidth=1)
        style.map("Ghost.TButton",
                  background=[("active", "#21262d"), ("pressed", "#0d1117")],
                  foreground=[("active", HEADER)])

        style.configure("Danger.TButton",
                        background="#21262d", foreground=ERROR,
                        font=("Consolas", 10),
                        padding=(12, 7), relief="flat")
        style.map("Danger.TButton",
                  background=[("active", "#30363d")])

        # Progress bar
        style.configure("Green.Horizontal.TProgressbar",
                        troughcolor=SURFACE, background=ACCENT,
                        thickness=4, borderwidth=0)

        # Scrollbar
        style.configure("TScrollbar", background=SURFACE,
                        troughcolor=BG, borderwidth=0,
                        arrowcolor=TEXT_DIM)
        style.map("TScrollbar", background=[("active", BORDER)])

        # Entry
        style.configure("TEntry", fieldbackground=SURFACE,
                        foreground=TEXT, bordercolor=BORDER,
                        insertcolor=ACCENT, padding=(8, 6))

    def _build_layout(self, root):
        root.configure(bg=BG)

        # ── Top bar ──────────────────────────────────────────────────────────
        topbar = tk.Frame(root, bg=BG, pady=0)
        topbar.pack(fill="x", padx=0, pady=0)

        # Brand
        brand_frame = tk.Frame(topbar, bg=BG)
        brand_frame.pack(side="left", padx=24, pady=16)
        tk.Label(brand_frame, text="⬡", font=("Consolas", 20), bg=BG,
                 fg=ACCENT).pack(side="left", padx=(0, 10))
        tk.Label(brand_frame, text="Markdown Maker", font=("Consolas", 16, "bold"),
                 bg=BG, fg=HEADER).pack(side="left")
        tk.Label(brand_frame, text="  /  File to Markdown Converter",
                 font=("Consolas", 10), bg=BG, fg=TEXT_DIM).pack(side="left")

        # Separator line
        sep = tk.Frame(root, bg=BORDER, height=1)
        sep.pack(fill="x")

        # ── Main content ─────────────────────────────────────────────────────
        main = tk.Frame(root, bg=BG)
        main.pack(fill="both", expand=True, padx=24, pady=16)

        # Left panel (file list)
        left = tk.Frame(main, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        # Section label
        file_header = tk.Frame(left, bg=BG)
        file_header.pack(fill="x", pady=(0, 8))
        tk.Label(file_header, text="FILES", font=("Consolas", 9, "bold"),
                 bg=BG, fg=TEXT_DIM).pack(side="left")
        self._file_count_label = tk.Label(file_header, text="0 files",
                                           font=("Consolas", 9), bg=BG, fg=TEXT_DIM)
        self._file_count_label.pack(side="right")

        # File listbox
        list_frame = tk.Frame(left, bg=SURFACE, bd=1, relief="flat",
                               highlightbackground=BORDER, highlightthickness=1)
        list_frame.pack(fill="both", expand=True)

        self.file_listbox = tk.Listbox(
            list_frame,
            bg=SURFACE, fg=TEXT,
            selectbackground="#1f6feb", selectforeground=HEADER,
            font=("Consolas", 10),
            borderwidth=0, highlightthickness=0,
            activestyle="none",
            relief="flat"
        )
        list_scroll = ttk.Scrollbar(list_frame, orient="vertical",
                                     command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=list_scroll.set)
        list_scroll.pack(side="right", fill="y")
        self.file_listbox.pack(fill="both", expand=True, padx=8, pady=8)

        # Empty state hint
        self._empty_label = tk.Label(list_frame,
            text="Drop files here or click  [ + Add Files ]",
            font=("Consolas", 10), bg=SURFACE, fg=BORDER)
        self._empty_label.place(relx=0.5, rely=0.5, anchor="center")

        # File action buttons
        file_btns = tk.Frame(left, bg=BG)
        file_btns.pack(fill="x", pady=(10, 0))

        ttk.Button(file_btns, text="＋ Add Files", style="Accent.TButton",
                   command=self.app.add_files).pack(side="left", padx=(0, 6))
        ttk.Button(file_btns, text="Preview", style="Ghost.TButton",
                   command=self.app.preview_selected).pack(side="left", padx=(0, 6))
        ttk.Button(file_btns, text="Remove", style="Ghost.TButton",
                   command=self.app.remove_selected).pack(side="left", padx=(0, 6))
        ttk.Button(file_btns, text="Clear All", style="Danger.TButton",
                   command=self.app.clear_all).pack(side="right")

        # ── Right panel (options) ─────────────────────────────────────────────
        right = tk.Frame(main, bg=BG, width=260)
        right.pack(side="right", fill="y", padx=(20, 0))
        right.pack_propagate(False)

        # Output directory
        self._section_label(right, "OUTPUT DIRECTORY")

        out_frame = tk.Frame(right, bg=SURFACE, highlightbackground=BORDER,
                              highlightthickness=1)
        out_frame.pack(fill="x", pady=(6, 12))

        self.output_dir_var = tk.StringVar(value=str(Path.home() / "Desktop"))
        out_entry = tk.Entry(out_frame, textvariable=self.output_dir_var,
                              bg=SURFACE, fg=TEXT, font=("Consolas", 9),
                              insertbackground=ACCENT, borderwidth=0,
                              relief="flat", highlightthickness=0)
        out_entry.pack(side="left", fill="x", expand=True, padx=8, pady=6)

        ttk.Button(out_frame, text="…", style="Ghost.TButton",
                   command=self.app.choose_output_dir, width=3).pack(side="right", padx=(0, 4), pady=3)

        ttk.Button(right, text="Open Output Folder", style="Ghost.TButton",
                   command=self.app.open_output_dir).pack(fill="x", pady=(0, 20))

        # Info box
        self._section_label(right, "SUPPORTED FORMATS")
        info_frame = tk.Frame(right, bg=SURFACE, highlightbackground=BORDER,
                               highlightthickness=1)
        info_frame.pack(fill="x", pady=(6, 20))

        formats = [
            ("PDF", ".pdf", ACCENT2),
            ("Word", ".docx / .doc", ACCENT2),
            ("Text", ".txt / .rtf", TEXT_DIM),
            ("HTML", ".html / .htm", TEXT_DIM),
            ("CSV", ".csv", TEXT_DIM),
            ("ODT", ".odt", TEXT_DIM),
            ("EPUB", ".epub", TEXT_DIM),
            ("Markdown", ".md (passthrough)", TEXT_DIM),
        ]
        for name, ext, color in formats:
            row = tk.Frame(info_frame, bg=SURFACE)
            row.pack(fill="x", padx=10, pady=2)
            tk.Label(row, text=name, font=("Consolas", 9, "bold"),
                     bg=SURFACE, fg=color, width=9, anchor="w").pack(side="left")
            tk.Label(row, text=ext, font=("Consolas", 9),
                     bg=SURFACE, fg=TEXT_DIM).pack(side="left")

        # Spacer
        tk.Frame(right, bg=BG).pack(fill="both", expand=True)

        # Convert button
        self._convert_btn = ttk.Button(right, text="▶  CONVERT TO MARKDOWN",
                                        style="Accent.TButton",
                                        command=self.app.start_conversion)
        self._convert_btn.pack(fill="x", pady=(0, 8))

        self._stop_btn = ttk.Button(right, text="■  Stop", style="Danger.TButton",
                                     command=self.app.stop_conversion, state="disabled")
        self._stop_btn.pack(fill="x")

        # ── Bottom bar ──────────────────────────────────────────────────────
        bottom = tk.Frame(root, bg=SURFACE)
        bottom.pack(fill="x", padx=0, pady=0)

        inner = tk.Frame(bottom, bg=SURFACE)
        inner.pack(fill="x", padx=24, pady=8)

        self._status_label = tk.Label(inner, text="Ready.",
                                       font=("Consolas", 9), bg=SURFACE, fg=TEXT_DIM)
        self._status_label.pack(side="left")

        self._progress = ttk.Progressbar(inner, style="Green.Horizontal.TProgressbar",
                                          orient="horizontal", length=180, mode="determinate")
        self._progress.pack(side="right")

    def _section_label(self, parent, text):
        tk.Label(parent, text=text, font=("Consolas", 8, "bold"),
                 bg=BG, fg=TEXT_DIM).pack(anchor="w")

    # ── Public update methods ─────────────────────────────────────────────────

    def refresh_file_list(self):
        self.file_listbox.delete(0, "end")
        files = self.app.files_queue

        if not files:
            self._empty_label.place(relx=0.5, rely=0.5, anchor="center")
            self._file_count_label.config(text="0 files")
            return

        self._empty_label.place_forget()
        self._file_count_label.config(text=f"{len(files)} file{'s' if len(files) != 1 else ''}")

        status_icons = {
            "pending":    "○",
            "converting": "◌",
            "done":       "●",
            "error":      "✕",
        }
        status_colors = {
            "pending":    TEXT_DIM,
            "converting": WARN,
            "done":       DONE,
            "error":      ERROR,
        }

        for i, f in enumerate(files):
            status = f.get("status", "pending")
            icon = status_icons.get(status, "○")
            name = os.path.basename(f["path"])
            ext = Path(f["path"]).suffix.upper().lstrip(".")
            size = self._file_size(f["path"])
            display = f"  {icon}  {name}  [{ext}]  {size}"
            self.file_listbox.insert("end", display)
            self.file_listbox.itemconfig(i, fg=status_colors.get(status, TEXT))

    def update_status(self, message: str):
        self._status_label.config(text=message)

    def set_progress(self, value: float):
        self._progress["value"] = int(value * 100)

    def set_converting_state(self, converting: bool):
        if converting:
            self._convert_btn.config(state="disabled")
            self._stop_btn.config(state="normal")
        else:
            self._convert_btn.config(state="normal")
            self._stop_btn.config(state="disabled")

    def _file_size(self, path: str) -> str:
        try:
            size = os.path.getsize(path)
            if size < 1024:
                return f"{size}B"
            elif size < 1024 * 1024:
                return f"{size // 1024}KB"
            else:
                return f"{size // (1024 * 1024)}MB"
        except Exception:
            return "?"
