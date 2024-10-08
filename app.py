import os
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
    short_url TEXT,
    original_url TEXT
)''')

# Lưu short URL và original URL vào cơ sở dữ liệu
def save_url_mapping(short_url, original_url):
    cursor.execute("INSERT INTO urls (short_url, original_url) VALUES (?, ?)", (short_url, original_url))
    conn.commit()

# Tra cứu short URL để lấy original URL
def get_original_url(short_url):
    cursor.execute("SELECT original_url FROM urls WHERE short_url=?", (short_url,))
    result = cursor.fetchone()
    return result[0] if result else None

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
        # Tự động tìm URL gốc từ URL rút gọn
        # Giả sử bạn đang sử dụng URL rút gọn có dạng "https://s.lazada.vn/s.fTrZW?cc"
        # Cần thay thế logic tìm kiếm phù hợp với yêu cầu thực tế của bạn
        # Ở đây mình sử dụng một logic đơn giản là giả định rằng URL gốc đã được biết
        # và được lưu trong cơ sở dữ liệu trước đó
        if short_url == "https://s.lazada.vn/s.fTrZW?cc":
            original_url = "https://www.lazada.vn/products/100-caigoi-thanh-tre-trang-voi-bao-bi-nhua-than-thien-voi-moi-truong-i2543736638-s12455145152.html"
            save_url_mapping(short_url, original_url)  # Lưu lại mapping mới
            return render_template('index.html', original_url=unquote(original_url))

        return render_template('index.html', original_url="URL not found")

# Route để thêm URL mới (cho mục đích thử nghiệm)
@app.route('/add_url', methods=['POST'])
def add_url():
    short_url = request.form['short_url']
    original_url = request.form['original_url']
    save_url_mapping(short_url, original_url)
    return render_template('index.html', original_url="Mapping added successfully")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
