import logging
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import re
import os
import uuid

app = Flask(__name__)

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)

# Cấu hình cơ sở dữ liệu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'  # Đối với SQLite
# Hoặc sử dụng PostgreSQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@host:port/database_name'
db = SQLAlchemy(app)

# Mô hình kết quả
class Result(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    converted_text = db.Column(db.Text, nullable=False)

db.create_all()

def extract_and_convert_links(text):
    link_pattern = r'(https?://[^\s]+)'
    converted_text = re.sub(link_pattern, r'<a href="\g<0>" target="_blank">\g<0></a>', text)
    return converted_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_text = request.form['text']
        converted_text = extract_and_convert_links(original_text)
        
        # Tạo một ID duy nhất cho kết quả
        result_id = str(uuid.uuid4())
        new_result = Result(id=result_id, converted_text=converted_text)
        db.session.add(new_result)
        db.session.commit()
        
        # Tạo liên kết có thể chia sẻ
        share_link = url_for('result', result_id=result_id, _external=True)
        return render_template('result.html', converted_text=converted_text, share_link=share_link)

    return render_template('index.html')

@app.route('/result/<result_id>', methods=['GET'])
def result(result_id):
    result = Result.query.get(result_id)
    if result is None:
        return "Kết quả không tìm thấy", 404
    
    return render_template('result.html', converted_text=result.converted_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
