# Hosting
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

# For keras
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

from pathlib import Path

import os

MODEL_NAME = 'bacterial-leaf-blight-model-12022025.keras'
CLASS_NAMES = ['bacterial_leaf_blight', 'brown_spot', 'healthy', 'leaf_blast', 'leaf_scald', 'narrow_brown_spot']

IMAGE_SIZE = (128, 128)

app = FastAPI()

MODEL_PATH = Path(__file__).resolve().parent / MODEL_NAME
STATIC_PATH = Path(__file__).resolve().parent.parent / 'static'
ENTRY_PATH = STATIC_PATH / 'index.html'

app.mount('/static', StaticFiles(
    directory=STATIC_PATH
), name='static')

# Enable CORS (adjust origins based on your frontend)
# no thank you (note: Update origins to)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
print('Model path:', MODEL_PATH)
MODEL = tf.keras.models.load_model(MODEL_PATH) #type: ignore

@app.get("/")
async def root():
    return FileResponse(path=ENTRY_PATH)

@app.get("/ping")
async def ping():
    return "Ah, ah, ah, ah staying alive, staying alive."

def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data))
    image = image.resize(IMAGE_SIZE)
    return np.array(image)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, axis=0)  # Add batch dimension (not 100% sure why)
        # img_batch = img_batch / 255.0  # Model already normalizes image
        
        prediction = MODEL.predict(img_batch)
        probabilities = tf.nn.softmax(prediction[0]).numpy() #type: ignore
        predicted_class = CLASS_NAMES[np.argmax(probabilities)]
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
    PORT = int(os.environ.get('PORT', 8080))
    #uvicorn.run(app, host='0.0.0.0', port=PORT)