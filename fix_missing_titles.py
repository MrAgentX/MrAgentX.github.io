import os
import re
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

POSTS_DIR = "posts"
front_pattern = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

def read_post(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    front = {}
    content = text
    m = front_pattern.match(text)
    if m:
        header = m.group(1)
        content = text[m.end():]
        for line in header.splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                front[k.strip()] = v.strip().strip('"')
    return front, content


def write_post(path, front, content):
    lines = ["---"]
    for k, v in front.items():
        lines.append(f"{k}: \"{v}\"")
    lines.append("---\n")
    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
        f.write(content.lstrip('\n'))


def find_missing_titles():
    files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.md')]
    missing = []
    for f in files:
        front, _ = read_post(os.path.join(POSTS_DIR, f))
        title = front.get('title', '')
        if not title:
            missing.append(f)
    return missing


class TitleEditor(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.master.title("Missing Title Fixer")
        self.files = find_missing_titles()

        self.listbox = tk.Listbox(self)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for f in self.files:
            self.listbox.insert(tk.END, f)
        scrollbar = tk.Scrollbar(self, command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        edit_btn = tk.Button(button_frame, text="Edit", command=self.edit_selected)
        edit_btn.pack(padx=5, pady=5)
        refresh_btn = tk.Button(button_frame, text="Refresh", command=self.refresh)
        refresh_btn.pack(padx=5, pady=5)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        self.files = find_missing_titles()
        for f in self.files:
            self.listbox.insert(tk.END, f)
        if not self.files:
            self.listbox.insert(tk.END, "All posts have titles")

    def edit_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        filename = self.files[sel[0]]
        path = os.path.join(POSTS_DIR, filename)
        front, content = read_post(path)

        top = tk.Toplevel(self)
        top.title(filename)

        tk.Label(top, text="Standard front matter:").pack(anchor='w')
        template = "---\nlayout: post\ntitle: \ndate: YYYY-MM-DD\n---"
        tk.Label(top, text=template, justify='left', font=('Courier', 10)).pack(anchor='w')

        title_var = tk.StringVar(value=front.get('title', ''))
        tk.Label(top, text="Title:").pack(anchor='w')
        title_entry = tk.Entry(top, textvariable=title_var, width=50)
        title_entry.pack(fill=tk.X, padx=5, pady=5)

        text_widget = scrolledtext.ScrolledText(top, width=80, height=20)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert('1.0', content)

        def save():
            front['title'] = title_var.get().strip()
            if not front['title']:
                messagebox.showerror("Error", "Title cannot be empty")
                return
            write_post(path, front, text_widget.get('1.0', tk.END))
            messagebox.showinfo("Saved", f"Updated {filename}")
            top.destroy()
            self.refresh()

        tk.Button(top, text="Save", command=save).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = TitleEditor(root)
    root.mainloop()
