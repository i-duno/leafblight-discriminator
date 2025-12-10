import os
import numpy as np
import keras
from tensorflow import data as tf_data
import matplotlib.pyplot as plt

from keras import layers
import keras

# I dont think this is what we're supposed to do but here we are
# generate dataset
image_size = (128, 128)
batch_size = 32

train_ds: tf_data.Dataset = keras.utils.image_dataset_from_directory(
    "train-data/train",
    image_size=image_size,
    batch_size=batch_size,
) #type: ignore


valid_ds: tf_data.Dataset = keras.utils.image_dataset_from_directory(
    "train-data/validation",
    image_size=image_size,
    batch_size=batch_size,
) #type: ignore

print('======================')
print(train_ds.class_names) #type: ignore
print("Start of training")

'''
data_augmentation_layers = [
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
]

def data_augmentation(images):
    for layer in data_augmentation_layers:
        images = layer(images)
    return images

# Apply `data_augmentation` to the training images.
train_ds = train_ds.map(
    lambda img, label: (data_augmentation(img), label),
    num_parallel_calls=tf_data.AUTOTUNE,
)
'''

# Prefetching samples in GPU memory helps maximize GPU utilization.
train_ds = train_ds.prefetch(tf_data.AUTOTUNE)
valid_ds = valid_ds.prefetch(tf_data.AUTOTUNE)

data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1)
])

# mini version of Xception framework
def make_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)

    # Filters used to be [128, 256, 512, 728] 12/2/2025

    # Entry block
    x = data_augmentation(inputs)
    x = layers.Rescaling(1.0 / 255)(x)
    x = layers.Conv2D(16, 3, strides=2, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    for size in [32, 64, 128]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    x = layers.SeparableConv2D(256, 3, padding="same")(x) #orig 1024
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.GlobalAveragePooling2D()(x)
    if num_classes == 2:
        units = 1
    else:
        units = num_classes

    x = layers.Dropout(0.5)(x) #used to be 0.25
    # We specify activation=None so as to return logits
    outputs = layers.Dense(units, activation=None)(x)
    return keras.Model(inputs, outputs)

model = make_model(input_shape=image_size + (3,), num_classes=6)
keras.utils.plot_model(model, show_shapes=True)

epochs = 25

callbacks = [
    keras.callbacks.ModelCheckpoint("save_at_{epoch}.keras")
]
#compile
#1e-4 -> val 0.8 accuracy, 0.6 loss
#1e-5 
model: any = keras.models.load_model("final_model.keras", compile=False)  #type: ignore
model.compile(
    optimizer=keras.optimizers.Adam(4e-5), #type: ignore #used to be 3e-4, 1e-4 -> 1e-5 -> 4e-5
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=[keras.metrics.SparseCategoricalAccuracy(name="accuracy")],
)

model.fit(
    train_ds,
    epochs=epochs,
    callbacks=callbacks,
    validation_data=valid_ds,
)

model.save("final_model.keras")
print("Done training!")