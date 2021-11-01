import matplotlib.pyplot as plt
import seaborn as sns

import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout 
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import adam_v2

from sklearn.metrics import classification_report,confusion_matrix

import tensorflow as tf

import cv2
import os

import numpy as np

labels = ['bar chart', 'line chart', 'pie chart','scatter plot']
img_size = 224

def get_data(data_dir):
    data = [] 
    for label in labels: 
        path = os.path.join(data_dir, label)
        print(path)
        class_num = labels.index(label)
        for img in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, img))[...,::-1] #convert BGR to RGB format
                resized_arr = cv2.resize(img_arr, (img_size, img_size)) # Reshaping images to preferred size
                data.append([resized_arr, class_num])
            except Exception as e:
                print(e)
    return np.array(data)

train = get_data('./data/all')

#     if(i[1] == b):
#         l.append("bar_chart")
#     elif(i[1] == s):
#         l.append("scatter_plot")
#     elif(i[1] == p):
#         l.append("pie_chart")
#     elif(i[1] == l):
#         l.append("line_graph")
# sns.set_style('darkgrid')
# sns.countplot(l)