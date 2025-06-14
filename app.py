from flask import Flask, render_template, request, redirect, url_for, session
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'mini_photoshop_secret'

UPLOAD_FOLDER = 'static/upload'
PROCESSED_FOLDER = 'static/processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    gambar_path = session.get('gambar_path', 'img/canvas.jpeg')
    histogram = session.pop('histogram_path', None)
    frekuensi = session.pop('frekuensi_path', None)
    return render_template('index.html', gambar=gambar_path, histogram=histogram, frekuensi=frekuensi)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['gambar']
    if file:
        path = os.path.join(UPLOAD_FOLDER, 'uploaded.jpg')
        file.save(path)
        session['gambar_path'] = 'upload/uploaded.jpg'
    return redirect(url_for('index'))

@app.route('/proses', methods=['POST'])
def proses():

    # variabel awal
    proses = request.form['proses']
    size = format = mode = None
    hasil_path = None
    preview_pixels = None
    frekuensi_path = None
    path = os.path.join(UPLOAD_FOLDER, 'uploaded.jpg')

    if not os.path.exists(path):
        return redirect(url_for('index'))

    img = Image.open(path)

    if proses == 'detail_gambar':
        size = img.size
        format = img.format
        mode = img.mode
        pixel_values = list(img.getdata())

        preview_pixels = pixel_values[:5]

        hasil_path = session.get('gambar_path', 'upload/uploaded.jpg')
    else:
        session.pop('histogram_path', None) 

        if proses == 'grayscale':
            img = ImageOps.grayscale(img)
        elif proses == 'negatif':
            img = ImageOps.invert(img.convert("RGB"))
        elif proses == 'biner':
            img = ImageOps.grayscale(img)
            threshold = 128
            img = img.point(lambda p: 255 if p > threshold else 0)
        elif proses == 'blur':
            img = img.filter(ImageFilter.BLUR) 
        elif proses == 'brightening':
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.5)
        elif proses == 'zoom_in':
            width, height = img.size
            img = img.resize((int(width * 2.5), int(height * 2.5)))
        elif proses == 'zoom_out':
            width, height = img.size
            img = img.resize((int(width * 0.3), int(height * 0.3)))
        elif proses == 'rotasi':
            img = img.rotate(-90, expand=True)
        elif proses == 'flipping_horizontal':
            img = ImageOps.mirror(img)
        elif proses == 'flipping_vertikal':
            img = ImageOps.flip(img)
        elif proses == 'histogram':
            gray_img = ImageOps.grayscale(img)
            histogram = gray_img.histogram()

            plt.figure(figsize=(6, 4))
            plt.plot(histogram, color='blue')
            plt.title('Histogram Grayscale')
            plt.xlabel('Intensitas Piksel')
            plt.ylabel('Frekuensi')
            plt.tight_layout()

            hist_path = os.path.join(PROCESSED_FOLDER, 'histogram.png')
            plt.savefig(hist_path)
            plt.close()

            session['histogram_path'] = 'processed/histogram.png'
            hasil_path = session.get('gambar_path', 'upload/uploaded.jpg')
        elif proses == 'frekuensi':
            gray = ImageOps.grayscale(img)
            fft = np.fft.fft2(np.array(gray))
            fshift = np.fft.fftshift(fft)
            magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)

            plt.figure(figsize=(6, 4))
            plt.imshow(magnitude_spectrum, cmap='gray')
            plt.title('Ranah Frekuensi')
            plt.axis('off')
            freq_path = os.path.join(PROCESSED_FOLDER, 'frekuensi.png')
            plt.savefig(freq_path, bbox_inches='tight', pad_inches=0)
            plt.close()

            session['frekuensi_path'] = 'processed/frekuensi.png'
            hasil_path = session.get('gambar_path', 'upload/uploaded.jpg')
            frekuensi_path = session['frekuensi_path']

        # konversi
        if img.mode == 'RGBA':
            img = img.convert('RGB') 

        # Simpan hasil dan update session
        hasil_path = 'processed/hasil.jpg'
        img.save(os.path.join(PROCESSED_FOLDER, 'hasil.jpg'))
        session['gambar_path'] = hasil_path

    if not hasil_path:
        hasil_path = session.get('gambar_path', 'upload/uploaded.jpg')

    return render_template('index.html', gambar=hasil_path, size=size, format=format, mode=mode, pixels=preview_pixels,
    histogram=session.get('histogram_path'), frekuensi=frekuensi_path)

if __name__ == '__main__':
    app.run(debug=True, port=5050)
