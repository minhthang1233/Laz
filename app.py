import os
import requests
from flask import Flask, request, render_template, jsonify
from urllib.parse import unquote
import sqlite3

app = Flask(__name__)

# Kết nối tới cơ sở dữ liệu SQLite
conn = sqlite3.connect('url_mappings.db', check_same_thread=False)
cursor = conn.cursor()

# Tạo bảng nếu chưa có
cursor.execute('''CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY,
    short_url TEXT UNIQUE,
    original_url TEXT
)''')

# Lưu short URL và original URL vào cơ sở dữ liệu
def save_url_mapping(short_url, original_url):
    try:
        cursor.execute("INSERT INTO urls (short_url, original_url) VALUES (?, ?)", (short_url, original_url))
        conn.commit()
    except sqlite3.IntegrityError:
        pass

# Tra cứu short URL để lấy original URL
def get_original_url(short_url):
    cursor.execute("SELECT original_url FROM urls WHERE short_url=?", (short_url,))
    result = cursor.fetchone()
    return result[0] if result else None

# Tự động tìm URL gốc từ URL rút gọn Lazada
def resolve_lazada_short_url(short_url):
    # Chẳng hạn, bạn có thể sử dụng một regex hoặc một phương thức cụ thể để ánh xạ
    # URL rút gọn của Lazada tới URL sản phẩm.
    # Đây chỉ là một ví dụ đơn giản và có thể cần được điều chỉnh
    if "lazada.vn" in short_url:
        # Giả sử URL rút gọn là một sản phẩm cụ thể, bạn có thể chuyển đổi như sau:
        # Cần thay đổi logic dưới đây theo cách mà Lazada xử lý URL rút gọn của họ
        return "https://www.lazada.vn/products/100-caigoi-thanh-tre-trang-voi-bao-bi-nhua-than-thien-voi-moi-truong-i2543736638-s12455145152.html"

    return None

# Route trang chủ với form nhập URL rút gọn
@app.route('/')
def index():
    return render_template('index.html')

# Route để xử lý form nhập URL rút gọn và trả về kết quả
@app.route('/resolve_url', methods=['POST'])
def resolve_url():
    short_url = request.form['short_url']
    original_url = get_original_url(short_url)
    
    if original_url:
        return render_template('index.html', original_url=unquote(original_url))
    else:
        original_url = resolve_lazada_short_url(short_url)  # Tìm URL gốc từ Lazada
        
        if original_url:
            save_url_mapping(short_url, original_url)  # Lưu lại mapping mới
            return render_template('index.html', original_url=unquote(original_url))

        return render_template('index.html', original_url="URL not found")

# Route để thêm URL mới
@app.route('/add_url', methods=['POST'])
def add_url():
    short_url = request.form['short_url']
    original_url = request.form['original_url']
    save_url_mapping(short_url, original_url)
    return render_template('index.html', original_url="Mapping added successfully")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
