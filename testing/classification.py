import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Load the saved model
model = keras.models.load_model('clothing_classifier_model.h5')

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

def load_and_preprocess_image(image_path):
    img = Image.open(image_path).convert('L')  # Load image and convert to grayscale
    img = img.resize((28, 28), Image.ANTIALIAS)  # Resize the image to 28x28 pixels
    img = np.array(img)  # Convert the image to a numpy array
    img = (255 - img) / 255.0  # Invert the image colors and normalize the pixel values
    img = np.expand_dims(img, axis=0)  # Add an extra dimension to match the input shape
    return img

image_path = 'test3.jpg'  # Change this to the path of your image
image = load_and_preprocess_image(image_path)

# Make a prediction using the loaded model
prediction = model.predict(image)

# Display the image with its predicted label
plt.figure()
plt.imshow(image[0], cmap=plt.cm.binary)
plt.xticks([])
plt.yticks([])

predicted_label = np.argmax(prediction)
plt.xlabel("{} {:2.0f}%".format(class_names[predicted_label],
                          100*np.max(prediction)),
                          color='blue')
plt.show()