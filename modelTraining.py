# These are out necessary imports
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_array
from keras.models import load_model
import os

# Create flask instance
app = Flask(__name__) #__name__: means current file so 'app.py


