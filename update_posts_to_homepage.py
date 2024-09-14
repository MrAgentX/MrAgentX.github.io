import os
from datetime import datetime
import re

def get_latest_posts(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")
    
    files = [f for f in os.listdir(directory) if f.endswith('.md')]
    posts_with_dates = []
    
    for file in files:
        # 提取文件名中的日期部分
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', file)
        if date_match:
            date_str = date_match.group(1)
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            print(f"Processing file: {file}, extracted date: {date_str}")
            posts_with_dates.append((file, date_obj))
    
    # 根據日期排序文件
    posts_with_dates.sort(key=lambda x: x[1], reverse=True)
    
    latest_posts = [post[0] for post in posts_with_dates]
    return latest_posts

def generate_html(posts, directory):
    html_content = """
    <html>
    <head>
        <title>MrAgentX的部落格</title>
        <style>
            .post-images {
                display: flex;
                overflow-x: auto;
                white-space: nowrap;
            }
            .post-images img {
                margin-right: 10px;
                max-height: 200px;
            }
            .post-content {
                max-width: 800px;
                margin: auto;
            }
            .post-title {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h1>MrAgentX的部落格</h1>
        <a href="https://www.threads.net/@ofcourse.i.still.love.you">Visit my Threads profile</a>
    """
    
    for post in posts:
        with open(os.path.join(directory, post), 'r', encoding='utf-8') as f:
            content = f.read()
            # 移除 YAML 頭部
            content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
            # 提取標題
            title = os.path.splitext(post)[0]
            # 將圖片路徑轉換為 HTML 語法
            images_html = ""
            def replace_image_path(match):
                nonlocal images_html
                alt_text = match.group(1)
                image_path = match.group(2)
                new_image_path = f'images/posts/{os.path.basename(image_path)}'
                print(f"Markdown image: {match.group(0)}")
                print(f"Converted HTML image: <img src=\"{new_image_path}\" alt=\"{alt_text}\" width=\"300\">")
                images_html += f'<img src="{new_image_path}" alt="{alt_text}" width="300">'
                return ""
            
            content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_image_path, content)
            # 將 Markdown 連結轉換為 HTML 超連結
            content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', content)
            # 將網址轉換為 HTML 超連結
            content = re.sub(r'(https?://[^\s]+)', r'<a href="\1">\1</a>', content)
            # 將 Markdown 內容轉換為 HTML
            content = content.replace('\n', '<br>')  # 簡單的換行處理
            html_content += f"<h2 class='post-title'>{title}</h2>"
            html_content += f'<div class="post-content">{content}</div>'
            if images_html:
                html_content += f'<div class="post-images">{images_html}</div>'

    html_content += "</body></html>"
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    current_directory = os.path.dirname(__file__)
    posts_directory = os.path.join(current_directory, 'posts')
    latest_posts = get_latest_posts(posts_directory)
    generate_html(latest_posts, posts_directory)