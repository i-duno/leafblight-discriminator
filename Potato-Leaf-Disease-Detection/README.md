# Potato-Leaf-Disease-Detection-using-CNN-
An Image Classification project to detect wheter a potato leaf has early blight or late blight disease, or its a healthy leaf. 
The model has been trained using CNN (Convolutional Neural Network). 
I used FastAPI and Tf-serving for serving the model and accessing it from the front end. 
For front end, I used HTML, CSS and JavaScript.
I have used ImageDataGenerator for all the preprocessing and Data Augmentation.
The overall accuracy of model is 88%.




*** DATASET IS ON KAGGLE : PLANTVILLAGE DATASET***

# Notice!
This repository is a fork on the above, with a new model that is trained on rice leaves instead of potato leaves.

The current model its using is version 5.


*** MODEL FITNESS ***
train_acc: 0.87

train_loss: 0.36

val_acc: 0.85

val_loss: 0.39

layers: [32, 64, 128, 256]