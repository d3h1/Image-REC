import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/', methods=['POST'])
def upload_image():
    image = request.files['image']
    image.save(os.path.join('uploads', image.filename))
    return redirect(url_for('display_image', filename=image.filename))

@app.route('/uploads/<filename>')
def display_image(filename):
    return f'<img src="{url_for("static", filename="uploads/" + filename)}">'
