from flask import Flask, request, render_template, jsonify
import tensorflow as tf
from PIL import Image
import numpy as np
from keras.models import load_model
import os

# Load the model outside the predict function
model = load_model('clothing_classifier_model_v2.h5')
model.graph = tf.compat.v1.get_default_graph()

app = Flask(__name__)

# We are setting max size of file as 10mb
app.config['MAX CONTENT HEIGHT'] = 10 * 1024 * 1024

# This will allow files with extensions such as png, jpg, and jpeg
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
def allowed_files(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
# This will load and prepare the image to the right shape
def read_image(filename):
    # Load the image
    img = tf.keras.utils.load_img(filename, grayscale=True, target_size=(28, 28))
    
    # Converting the image to array
    img = tf.keras.utils.img_to_array(img)
    
    # Reshape the image into a sample of 1 channel
    img = img.reshape(1, 28, 28, 1)
    
    # Prepare this as pixel data
    img = img.astype('float32')
    img = img / 255.0
    return img
    
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('home.html')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        try:
            if file and allowed_files(file.filename):
                filename = file.filename
                file_path = os.path.join('static/images', filename)
                file.save(file_path)
                img = Image.open(file_path).convert('L')
                img = img.resize((28, 28), Image.ANTIALIAS)
                img = np.array(img)
                img = (255 - img) / 255.0
                img = np.expand_dims(img, axis=0)
                img = np.expand_dims(img, axis=-1)

                with model.graph.as_default():
                    class_prediction = model.predict(img)
                    predicted_label = int(np.argmax(class_prediction))
                
                # We will map apparel category with numerical classes
                if predicted_label == 0:
                    product = "TShirt/top"
                elif predicted_label == 1:
                    product = "Trouser"
                elif predicted_label == 2:
                    product = "Pullover"
                elif predicted_label == 3:
                    product = "Dress"
                elif predicted_label == 4:
                    product = "Coat"
                elif predicted_label == 5:
                    product = "Sandal"
                elif predicted_label == 6:
                    product = "Shirt"
                elif predicted_label == 7:
                    product = "Sneaker"
                elif predicted_label == 8:
                    product = "Bag"
                else:
                    product = "Ankle Boot"
                return render_template('predict.html', product=product, user_image=file_path)
                response = {
                        "product": product,
                        "user_image": file_path
                    }
                return jsonify(response)

        except Exception as e:
            return "Unable to read the file. Please check if the file extension is correct."
    return render_template('predict.html')

if __name__ == "__main__":
    app.run()