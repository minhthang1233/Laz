from flask import Flask, request, render_template, redirect
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shopee', methods=['GET'])
def shopee():
    # URL cần duyệt mặc định là link affiliate của Shopee
    url = 'https://affiliate.shopee.vn/offer/custom_link'

    try:
        # Thực hiện request GET tới URL
        response = requests.get(url)
        # Kiểm tra response
        if response.status_code == 200:
            return response.text
        else:
            return f"Không thể tải trang, mã lỗi: {response.status_code}"
    except Exception as e:
        return f"Lỗi: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
