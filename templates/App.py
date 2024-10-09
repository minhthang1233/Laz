from flask import Flask, render_template, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shopee')
def load_shopee():
    url = request.args.get('url')
    if url:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return render_template_string(response.text)
            else:
                return f"Lỗi khi tải trang: {response.status_code}"
        except Exception as e:
            return f"Lỗi: {str(e)}"
    return "Vui lòng nhập URL hợp lệ"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
