from flask import Flask, render_template, request, redirect, url_for
import re
import random
import string
import os

app = Flask(__name__)

# Bộ lưu trữ nội dung của các trang ngẫu nhiên
pages = {}

# Hàm tạo ID ngẫu nhiên
def generate_random_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Hàm để thay thế các liên kết bằng thẻ HTML anchor
def convert_links(text):
    url_pattern = r"(https?://[^\s]+)"
    return re.sub(url_pattern, r'<a href="\1">\1</a>', text)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        random_id = generate_random_id()
        # Chuyển đổi các link thành thẻ a
        content_with_links = convert_links(content)
        pages[random_id] = content_with_links
        return redirect(url_for('view_page', page_id=random_id))
    return render_template('index.html')

@app.route('/<page_id>')
def view_page(page_id):
    content = pages.get(page_id, 'Page not found')
    return render_template('page.html', content=content)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
