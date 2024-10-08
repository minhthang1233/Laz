import os
from flask import Flask, request, redirect, render_template
from hashlib import md5
import sqlite3

app = Flask(__name__)

# Kết nối đến database SQLite
conn = sqlite3.connect('urls.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, original_url TEXT, short_url TEXT)''')

# Hàm để tạo short URL
def generate_short_url(original_url):
    return md5(original_url.encode()).hexdigest()[:6]

# Route trang chủ để nhập URL
@app.route('/')
def index():
    return render_template('index.html')

# Route để rút gọn URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    short_url = generate_short_url(original_url)
    cursor.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)", (original_url, short_url))
    conn.commit()
    return f"Shortened URL: https://your-app-name.onrender.com/{short_url}"

# Route để chuyển hướng từ short URL
@app.route('/<short_url>')
def redirect_url(short_url):
    cursor.execute("SELECT original_url FROM urls WHERE short_url=?", (short_url,))
    result = cursor.fetchone()
    if result:
        return redirect(result[0])
    else:
        return "URL not found", 404

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # Lấy cổng từ biến môi trường hoặc mặc định là 5000
    app.run(host='0.0.0.0', port=port)  # Lắng nghe trên tất cả các địa chỉ IP
