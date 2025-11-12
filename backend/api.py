from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import uvicorn
import io
import json
import os

app = FastAPI()

# ✅ Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/garbage_classifier_model.h5")
model = load_model(MODEL_PATH)

# ✅ Load class label order
LABEL_PATH = os.path.join(os.path.dirname(__file__), "../models/class_indices.json")
with open(LABEL_PATH, "r") as f:
    class_indices = json.load(f)

idx_to_class = {v: k for k, v in class_indices.items()}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Receives image → returns predicted label + confidence"""

    content = await file.read()

    img = load_img(io.BytesIO(content), target_size=(128, 128))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)[0]
    pred_idx = int(np.argmax(pred))
    confidence = round(float(pred[pred_idx] * 100), 2)

    predicted_label = idx_to_class[pred_idx]

    return {
        "prediction": predicted_label,
        "confidence": confidence
    }

# ✅ Run app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
