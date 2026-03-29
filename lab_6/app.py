from flask import Flask
import sys
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Це код із твого попереднього завдання (п. 7)
    python_ver = sys.version
    path = sys.executable
    
    # Формуємо HTML-сторінку для виводу
    html_content = f"""
    <html>
        <head><title>Poetry + Flask Lab</title></head>
        <body>
            <h1>Результат роботи програми через Flask</h1>
            <p><b>Версія Python:</b> {python_ver}</p>
            <p><b>Шлях до інтерпретатора Poetry:</b> {path}</p>
            <hr>
            <p>Сайт успішно запущено у віртуальному середовищі!</p>
        </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(debug=True)
