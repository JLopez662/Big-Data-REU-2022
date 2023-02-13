# Overview - Model Customization

## Image Classification using Custom Models

This repository contains the code for two custom models that are used for image classification. Both models are built using the pre-trained model Inception V3 as a base and then adding custom layers to improve their performance.

The Inception V3 model is a deep convolutional neural network trained on the ImageNet dataset, which contains over one million images and thousands of object classes. By fine-tuning the Inception V3 model on a smaller, custom dataset, we can leverage its pre-trained weights to improve the accuracy of our image classification system.

In addition to the pre-trained Inception V3 model, this project also includes a custom model, which is trained from scratch on the same custom dataset. The custom model serves as a comparison to the fine-tuned Inception V3 model, demonstrating the potential limitations and benefits of fine-tuning versus training from scratch.

## Model using constant Learning Rate
The first custom model is a basic implementation of a deep learning model for image classification, built using the pre-trained Inception V3 model and adding custom layers on top.

## Model using Learning Rate Scheduler
The second custom model is similar to the first one but with an added callback. This callback changes the learning rate dynamically when the validation accuracy stops improving during training. This helps to optimize the training process and prevent overfitting.

## Requirements

The code in this repository was developed using the following libraries and packages:

Tensorflow
Keras
Numpy
Matplotlib
Pillow

## Note
Please note that the training process can take a long time and requires a GPU for optimal performance. 
