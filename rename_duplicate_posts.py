import os
import re
import tkinter as tk
from tkinter import messagebox, simpledialog

POSTS_DIR = "posts"

# Extract slug part after the date prefix
slug_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.*)\.md$")


def get_slug(filename):
    m = slug_pattern.match(filename)
    if m:
        return m.group(2)
    return None


def find_duplicates():
    files = [f for f in os.listdir(POSTS_DIR) if f.endswith(".md")]
    slug_map = {}
    for f in files:
        slug = get_slug(f)
        if slug is None:
            continue
        slug_map.setdefault(slug, []).append(f)
    duplicates = {s: flist for s, flist in slug_map.items() if len(flist) > 1 or s == ""}
    return duplicates


class DuplicateRenamer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.master.title("Duplicate Post Renamer")

        self.listbox = tk.Listbox(self)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(self, command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        rename_btn = tk.Button(button_frame, text="Rename", command=self.rename_selected)
        rename_btn.pack(padx=5, pady=5)
        refresh_btn = tk.Button(button_frame, text="Refresh", command=self.refresh)
        refresh_btn.pack(padx=5, pady=5)

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        self.dup_files = []
        duplicates = find_duplicates()
        for slug, files in duplicates.items():
            for f in files:
                self.listbox.insert(tk.END, f)
                self.dup_files.append(f)
        if not self.dup_files:
            self.listbox.insert(tk.END, "No duplicates found")

    def rename_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        filename = self.dup_files[index]
        slug = get_slug(filename)
        new_slug = simpledialog.askstring("Rename", f"Enter new slug for {filename}", initialvalue=slug)
        if not new_slug:
            return
        date_prefix = filename[:10]
        new_name = f"{date_prefix}-{new_slug}.md"
        src = os.path.join(POSTS_DIR, filename)
        dst = os.path.join(POSTS_DIR, new_name)
        try:
            os.rename(src, dst)
        except OSError as e:
            messagebox.showerror("Error", str(e))
            return
        self.refresh()


if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateRenamer(root)
    root.mainloop()
