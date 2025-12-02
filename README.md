# leafblight-descriminator
A CNN built with keras to discriminate against the dirty diseased leaves and the healthy ones.

> [!NOTE]
> This repository is a fork of [this repo](https://github.com/Atharva-Shakargayen/Potato-Leaf-Disease-Detection-using-CNN-/blob/main/imgGen.ipynb), with a new model that is trained on rice leaves instead of potato leaves.

# overview

**MODEL FITNESS (v5)**

| train_acc | train_loss | val_acc | val_loss |
|---|---|---|---|
| 0.87 | 0.36 | 0.85 | 0.39 |

layers: [32, 64, 128, 256]

# run instructions
- navigate to working directory `Potato-Leaf-Disease-Detection`
- run `pip3 install -r requirements.txt`
- open `index1.html` through chrome or LiveServer
- run `py main.py` to start API

# Original README

# Potato-Leaf-Disease-Detection-using-CNN-
An Image Classification project to detect wheter a potato leaf has early blight or late blight disease, or its a healthy leaf. 
The model has been trained using CNN (Convolutional Neural Network). 
I used FastAPI and Tf-serving for serving the model and accessing it from the front end. 
For front end, I used HTML, CSS and JavaScript.
I have used ImageDataGenerator for all the preprocessing and Data Augmentation.
The overall accuracy of model is 88%.

*** DATASET IS ON KAGGLE : PLANTVILLAGE DATASET***
