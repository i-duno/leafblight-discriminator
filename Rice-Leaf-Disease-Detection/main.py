from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import os

MODEL_NAME = 'bacterial-leaf-blight-model-12022025.keras'
#CLASS_NAMES = ['bacterial_leaf_blight', 'brown_spot', 'healthy', 'leaf_blast', 'leaf_scald', 'narrow_brown_spot']
CLASS_NAMES = ['bacterial_leaf_blight', 'bacterial_leaf_blight', 'healthy', 'bacterial_leaf_blight', 'bacterial_leaf_blight', 'bacterial_leaf_blight']
# Renamed stuff since reasearch and dataset is different lol

IMAGE_SIZE = (128, 128)

app = FastAPI()

# Enable CORS (adjust origins based on your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
print('Model path:', os.path.join(os.getcwd(), MODEL_NAME))
MODEL = tf.keras.models.load_model( #type: ignore
    os.path.join(os.getcwd(), MODEL_NAME)
) 

@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}


@app.get("/ping")
async def ping():
    return "Hello, I am live!"


def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data))
    # Resize the image to the input size of your model
    image = image.resize(IMAGE_SIZE)  # Adjust size based on your model's requirements
    return np.array(image)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, axis=0)  # Add batch dimension

        # Normalize image if required
        #img_batch = img_batch / 255.0  # Normalization for many models
        
        prediction = MODEL.predict(img_batch)
        probabilities = tf.nn.softmax(prediction[0]).numpy() #type: ignore
        predicted_class = CLASS_NAMES[np.argmax(probabilities)]
        #print(prediction)
        confidence = float(np.max(probabilities) * 100)

        all_predictions = {}
        for i in range(len(CLASS_NAMES)):
            class_name = CLASS_NAMES[i]
            percent = float(probabilities[i] * 100)
            all_predictions[class_name] = percent

        return {
            "class": predicted_class,
            "confidence": confidence,
            "all-predictions": all_predictions
        }
    
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)