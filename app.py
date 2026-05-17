import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
from pathlib import Path
from converter import FileConverter
from ui_components import ModernUI

class MarkdownConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MD Forge — File to Markdown Converter")
        self.root.geometry("900x680")
        self.root.minsize(700, 500)
        self.root.configure(bg="#0d1117")

        self.converter = FileConverter()
        self.files_queue = []
        self.converting = False

        self.ui = ModernUI(self)
        self.ui.setup(root)

    def add_files(self):
        filetypes = [
            ("Supported files", "*.pdf *.docx *.doc *.txt *.rtf *.html *.htm *.csv *.odt *.epub *.md"),
            ("PDF files", "*.pdf"),
            ("Word documents", "*.docx *.doc"),
            ("Text files", "*.txt *.rtf"),
            ("HTML files", "*.html *.htm"),
            ("CSV files", "*.csv"),
            ("All files", "*.*"),
        ]
        paths = filedialog.askopenfilenames(title="Select files to convert", filetypes=filetypes)
        for path in paths:
            if path not in [f["path"] for f in self.files_queue]:
                self.files_queue.append({"path": path, "status": "pending"})
        self.ui.refresh_file_list()

    def remove_selected(self):
        selected = self.ui.file_listbox.curselection()
        for i in reversed(selected):
            del self.files_queue[i]
        self.ui.refresh_file_list()

    def clear_all(self):
        self.files_queue.clear()
        self.ui.refresh_file_list()

    def choose_output_dir(self):
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.ui.output_dir_var.set(directory)

    def start_conversion(self):
        if not self.files_queue:
            messagebox.showwarning("No files", "Please add files to convert.")
            return
        output_dir = self.ui.output_dir_var.get().strip()
        if not output_dir:
            messagebox.showwarning("No output directory", "Please select an output directory.")
            return
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create output directory:\n{e}")
                return
        self.converting = True
        self.ui.set_converting_state(True)
        thread = threading.Thread(target=self._convert_all, args=(output_dir,), daemon=True)
        thread.start()

    def _convert_all(self, output_dir):
        total = len(self.files_queue)
        for i, file_info in enumerate(self.files_queue):
            if not self.converting:
                break
            path = file_info["path"]
            file_info["status"] = "converting"
            self.root.after(0, self.ui.refresh_file_list)
            self.root.after(0, lambda p=path: self.ui.update_status(f"Converting: {os.path.basename(p)}"))
            self.root.after(0, lambda v=(i / total): self.ui.set_progress(v))

            try:
                md_content = self.converter.convert(path)
                stem = Path(path).stem
                out_path = os.path.join(output_dir, f"{stem}.md")
                # Avoid overwriting
                counter = 1
                while os.path.exists(out_path):
                    out_path = os.path.join(output_dir, f"{stem}_{counter}.md")
                    counter += 1
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(md_content)
                file_info["status"] = "done"
                file_info["output"] = out_path
            except Exception as e:
                file_info["status"] = "error"
                file_info["error"] = str(e)

            self.root.after(0, self.ui.refresh_file_list)

        self.converting = False
        self.root.after(0, lambda: self.ui.set_progress(1.0))
        self.root.after(0, lambda: self.ui.set_converting_state(False))
        done = sum(1 for f in self.files_queue if f["status"] == "done")
        errors = sum(1 for f in self.files_queue if f["status"] == "error")
        self.root.after(0, lambda: self.ui.update_status(
            f"✅ Finished: {done} converted, {errors} errors."
        ))

    def stop_conversion(self):
        self.converting = False

    def open_output_dir(self):
        output_dir = self.ui.output_dir_var.get().strip()
        if output_dir and os.path.isdir(output_dir):
            import subprocess, platform
            if platform.system() == "Windows":
                os.startfile(output_dir)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", output_dir])
            else:
                subprocess.Popen(["xdg-open", output_dir])
        else:
            messagebox.showinfo("Info", "Output directory not set or doesn't exist.")

    def preview_selected(self):
        selected = self.ui.file_listbox.curselection()
        if not selected:
            messagebox.showinfo("Info", "Select a file to preview.")
            return
        file_info = self.files_queue[selected[0]]
        if file_info["status"] == "done":
            out = file_info.get("output", "")
            if out and os.path.exists(out):
                self._show_preview(out)
        elif file_info["status"] == "pending":
            # Preview conversion on the fly
            try:
                self.ui.update_status("Generating preview...")
                md = self.converter.convert(file_info["path"])
                self._show_preview_text(md, Path(file_info["path"]).name)
                self.ui.update_status("Preview ready.")
            except Exception as e:
                messagebox.showerror("Preview Error", str(e))

    def _show_preview(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self._show_preview_text(content, os.path.basename(filepath))

    def _show_preview_text(self, content, title):
        win = tk.Toplevel(self.root)
        win.title(f"Preview — {title}")
        win.geometry("750x600")
        win.configure(bg="#0d1117")

        header = tk.Label(win, text=f"📄 {title}", font=("Courier New", 11, "bold"),
                          bg="#0d1117", fg="#58a6ff", anchor="w", padx=16, pady=8)
        header.pack(fill="x")

        frame = tk.Frame(win, bg="#161b22")
        frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        text = tk.Text(frame, wrap="word", bg="#161b22", fg="#c9d1d9",
                       font=("Courier New", 10), insertbackground="#58a6ff",
                       relief="flat", padx=12, pady=12, selectbackground="#1f6feb")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        text.pack(side="left", fill="both", expand=True)
        text.insert("1.0", content)
        text.configure(state="disabled")


def main():
    root = tk.Tk()
    app = MarkdownConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
