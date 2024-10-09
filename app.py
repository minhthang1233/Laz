from flask import Flask, render_template, request, redirect, url_for
import re
import random
import string
import sqlite3
import os

app = Flask(__name__)

# Hàm kết nối đến cơ sở dữ liệu
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Tạo bảng nếu chưa có
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pages (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Hàm tạo ID ngẫu nhiên
def generate_random_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Hàm để thay thế các liên kết và ký tự xuống dòng bằng thẻ HTML
def convert_links(text):
    # Thay thế link thành thẻ <a>
    url_pattern = r"(https?://[^\s]+)"
    text_with_links = re.sub(url_pattern, r'<a href="\1">\1</a>', text)
    
    # Thay thế ký tự xuống dòng (\n) bằng thẻ <br>
    return text_with_links.replace('\n', '<br>')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        random_id = generate_random_id()
        content_with_links = convert_links(content)
        
        # Lưu vào database
        conn = get_db_connection()
        conn.execute('INSERT INTO pages (id, content) VALUES (?, ?)', (random_id, content_with_links))
        conn.commit()
        conn.close()
        
        return redirect(url_for('view_page', page_id=random_id))
    return render_template('index.html')

@app.route('/<page_id>')
def view_page(page_id):
    conn = get_db_connection()
    page = conn.execute('SELECT * FROM pages WHERE id = ?', (page_id,)).fetchone()
    conn.close()
    
    if page is None:
        return 'Page not found', 404
    return render_template('page.html', content=page['content'])

if __name__ == '__main__':
    create_table()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
