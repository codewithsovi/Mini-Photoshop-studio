from flask import Flask, render_template, request
from PIL import Image, ImageOps
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/upload'
PROCESSED_FOLDER = 'static/processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    # gambar_path = 'img/canvas.jpeg'
    # if request.method == 'POST':
    #     if 'gambar' in request.files:
    #         file = request.files['gambar']
    #         path = os.path.join(UPLOAD_FOLDER, 'uploaded.jpg')
    #         file.save(path)
    #         gambar_path = 'upload/uploaded.jpg'
    #     elif 'aksi' in request.form:
    #         aksi = request.form['aksi']
    #         path = os.path.join(UPLOAD_FOLDER, 'uploaded.jpg')
    #         if os.path.exists(path):
    #             img = Image.open(path)
    #             if aksi == 'grayscale':
    #                 img = ImageOps.grayscale(img)
    #             elif aksi == 'negatif':
    #                 img = ImageOps.invert(img.convert("RGB"))
    #             # Add more operations here...

    #             output_path = os.path.join(PROCESSED_FOLDER, 'hasil.jpg')
    #             img.save(output_path)
    #             gambar_path = 'processed/hasil.jpg'
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5050)