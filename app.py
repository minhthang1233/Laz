import os
from flask import Flask, request, jsonify
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

# Route để thêm URL mới
@app.route('/add_url', methods=['POST'])
def add_url():
    short_url = request.form['short_url']
    original_url = request.form['original_url']
    save_url_mapping(short_url, original_url)
    return jsonify({"message": "URL mapping saved successfully"}), 201

# Route để giải mã URL
@app.route('/resolve/<short_url>', methods=['GET'])
def resolve_url(short_url):
    original_url = get_original_url(short_url)
    if original_url:
        return jsonify({"original_url": unquote(original_url)}), 200
    else:
        return jsonify({"error": "URL not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
