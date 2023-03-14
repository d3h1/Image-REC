from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import tensorflow as tf
from keras.models import load_model
import os

#
# img = tf.keras.utils.load_img(
#     'whiteTshirt.jpg',
#     target_size=(300, 600),
#     color_mode="grayscale"
# )

# img.show()

# We have to first Flask Instance 
app = Flask(__name__)

# We are setting max size of file as 10mb
app.config['MAX CONTENT HEIGHT'] = 10 * 1024 * 1024

# This will allow files with extensions such as png, jpg, and jpeg
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
def allowed_files(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init():
    global graph
    graph = tf.get_default_graph()
    
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

@app.route("/predict", methods = ['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        try:
            if file and allowed_files(file.filename):
                filename = file.filename
                file_path = os.path.join('static/images', filename)
                file.save(file_path)
                img = read_image(file_path)
                
                # We will now predict the class of an image
                with graph.as_default():
                    model1 = load_model('classification_model.h5')
                    class_prediction = model1.predict_classes(img)
                    print(class_prediction)
                    
                # We will map apparel category with numerical classes
                if class_prediction[0] == 0:
                    product = "TShirt/top"
                elif class_prediction[0] == 1:
                    product = "Trouser"
                elif class_prediction[0] == 2:
                    product = "Pullover"
                elif class_prediction[0] == 3:
                    product = "Dress"
                elif class_prediction[0] == 4:
                    product = "Coat"
                elif class_prediction[0] == 5:
                    product = "Sandal"
                elif class_prediction[0] == 6:
                    product = "Shirt"
                elif class_prediction[0] == 7:
                    product = "Sneaker"
                elif class_prediction[0] == 8:
                    product = "Bag"
                else:
                    product = "Ankle Boot"
                return render_template('predict.html', product = product, user_image = file_path)
            
        except Exception as e:
            return "Unable to read the file. Please check if the file extension is correct."
    return render_template('predict.html')

if __name__ == "__main__":
    init()
    app.run()