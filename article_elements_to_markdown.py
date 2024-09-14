import tkinter as tk
from tkinter import messagebox

def generate_markdown(title, date, content, image_filenames):
    markdown_content = f"""---
title: "{title}"
date: "{date}"
---
# {title}

{content}

"""
    if image_filenames.strip():  # 檢查是否有圖片文件名
        for i, image in enumerate(image_filenames.split(',')):
            markdown_content += f"![{title} {i+1}](../images/posts/{image.strip()})\n"
    
    return markdown_content

def save_markdown(title, date, content, image_filenames):
    formatted_date = date.replace('-', '')
    filename = f"posts/{date}-{title}.md"
    markdown_content = generate_markdown(title, date, content, image_filenames)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(markdown_content)
    messagebox.showinfo("Success", f"Markdown file '{filename}' has been created.")

def create_gui():
    root = tk.Tk()
    root.title("Markdown Generator")
    root.geometry("1200x400")  # 调整窗口大小

    font_large = ("Arial", 16)

    # 标题
    tk.Label(root, text="Title:", font=font_large).grid(row=0, column=0, sticky=tk.W)
    title_entry = tk.Entry(root, width=60, font=font_large)
    title_entry.grid(row=0, column=1, columnspan=4)

    # 年月日
    tk.Label(root, text="Year:", font=font_large).grid(row=1, column=0, sticky=tk.W)
    year_entry = tk.Entry(root, width=5, font=font_large)
    year_entry.grid(row=1, column=1)
    year_entry.insert(0, "2024")

    tk.Label(root, text="Month:", font=font_large).grid(row=1, column=2, sticky=tk.W)
    month_entry = tk.Entry(root, width=3, font=font_large)
    month_entry.grid(row=1, column=3)
    month_entry.insert(0, "08")

    tk.Label(root, text="Day:", font=font_large).grid(row=1, column=4, sticky=tk.W)
    day_entry = tk.Entry(root, width=3, font=font_large)
    day_entry.grid(row=1, column=5)
    day_entry.insert(0, "01")

    # 内容
    tk.Label(root, text="Content:", font=font_large).grid(row=2, column=0, sticky=tk.W)
    content_text = tk.Text(root, width=60, height=10, font=font_large)
    content_text.grid(row=2, column=1, columnspan=4)

    # 图片文件名
    tk.Label(root, text="Image Filenames (comma separated):", font=font_large).grid(row=3, column=0, sticky=tk.W)
    image_entry = tk.Entry(root, width=60, font=font_large)
    image_entry.grid(row=3, column=1, columnspan=4)

    # 生成按钮
    def on_submit():
        title = title_entry.get()
        year = year_entry.get()
        month = month_entry.get()
        day = day_entry.get()
        date = f"{year}-{month}-{day}"
        content = content_text.get("1.0", tk.END).strip()
        image_filenames = image_entry.get()
        save_markdown(title, date, content, image_filenames)

    submit_button = tk.Button(root, text="Generate Markdown", font=font_large, command=on_submit)
    submit_button.grid(row=4, column=0, columnspan=6, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()