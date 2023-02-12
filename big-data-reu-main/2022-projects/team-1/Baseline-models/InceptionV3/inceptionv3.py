# -*- coding: utf-8 -*-
"""InceptionV3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dj2Ibr7QA2eqBvVzPGPfDPpxwJm5-5I-
"""

# connects colab to your google drive
# skip if your dataset is not on google drive or you're not using colab
from google.colab import drive
drive.mount('/content/drive')

!pip install preprocess

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from random import shuffle
import pickle, datetime
import preprocess as pp
import tensorflow as tf
from keras.layers import Layer
from keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications import EfficientNetV2L
from keras import regularizers
from tensorflow import keras
from keras.datasets import cifar10
from keras import models, layers
from keras.models import Model, Sequential
from keras.layers import Input, Dense, Dropout, Flatten, Activation, Conv2D, Convolution2D, MaxPooling2D, BatchNormalization
from keras.utils import np_utils
from keras import optimizers
from keras.preprocessing import sequence
from keras.preprocessing.image import ImageDataGenerator
import  PIL.Image
from sklearn.model_selection import KFold
from keras.metrics import Precision, Recall, BinaryAccuracy

data_path = 'put your dataset path here'
img_path= data_path


os.chdir(img_path) # changes the current working directory to the file path specified. This directory should be the directory of data you plan on using for the model'
print(os.path.abspath(os.getcwd()))

# stops training if training accuracy exceeds 97%
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.97):
      print("\nReached 97.0% accuracy so cancelling training!")
      self.model.stop_training = True

base_model = InceptionV3(input_shape = (256,256,3), include_top = False, weights = 'imagenet')
# base_model = ResNet50(input_shape = (256,256,3), include_top = False, weights = 'imagenet')
# base_model = VGG16(input_shape = (256, 256 ,3), include_top=False, weights="imagenet")
# base_model = EfficientNetV2L(input_shape=(256, 256, 3), include_top=False, weights="imagenet")

for layer in base_model.layers:
    layer.trainable = False # make sure layers are not trainable

last_layer = base_model.layers[-1]

last_output = last_layer.output

x = layers.Flatten()(last_output)

x = layers.Dense(1, activation='sigmoid')(x) # add binary classification layer

model = Model(base_model.input, x) 



model.summary()

batch_size = 32

# this is the augmentation configuration used for training
train_datagen = ImageDataGenerator(
        width_shift_range = 0.2,
        rescale=1./255,
        shear_range=0.2,
        horizontal_flip=True,
        )

# this is the augmentation configuration used for testing
test_datagen = ImageDataGenerator(
        rescale=1./255)

# this is a generator that will read pictures found in
# subfolers of 'data/train', and indefinitely generate
# batches of augmented image data
train_generator = train_datagen.flow_from_directory(
        './train', # target directory
        target_size=(256, 256),
        batch_size=batch_size,
        class_mode='binary')

# this is the same generator, but for validation data
validation_generator = train_datagen.flow_from_directory(
        './validation',
        target_size=(256, 256),
        batch_size=batch_size,
        class_mode='binary')

# this is the same generator, but for test data
test_generator = test_datagen.flow_from_directory(
        './test',
        target_size=(256, 256),
        batch_size=batch_size,
        class_mode= 'binary')

model.compile(optimizer = keras.optimizers.Adam(), 
              loss = 'binary_crossentropy', 
              metrics = ['accuracy'])

callbacks = myCallback()

k = 100
h2 = model.fit(        
        train_generator,
        epochs = k,
        validation_data=validation_generator,
        callbacks = [callbacks],
        )

# set k to be the number of epochs reached before the training stopped
k = 146

print("Average training accuracy: ",sum(h2.history['accuracy'])/k)
print("Average training loss: ",sum(h2.history['loss'])/k)
print("Average validation accuracy: ",sum(h2.history['val_accuracy'])/k)
print("Average validation loss: ",sum(h2.history['val_loss'])/k)

# plot training and validation accuracies
plt.plot(h2.history['accuracy'])
plt.plot(h2.history['val_accuracy'])
plt.title('Training and Validation Accuracies')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training', 'Validation'], loc = 'upper left')
plt.show()

# plot training and validation losses
plt.plot(h2.history['loss'])
plt.plot(h2.history['val_loss'])
plt.title('Training and Validation Losses')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Training', 'Validation'], loc = 'upper left')
plt.show()

import sklearn.metrics as metrics

# get confusion matrix
pred = model2.predict(validation_generator)

print("Confusion Matrix: \n")
true_classes = validation_generator.classes
class_labels = list(validation_generator.class_indices.keys())
pred = np.round(pred)
confusion_matrix = metrics.confusion_matrix(y_true=true_classes, y_pred=pred)
confusion_matrix

# get test accuracy
_, acc = model.evaluate(test_generator)
print(acc)