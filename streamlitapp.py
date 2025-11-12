import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import json
import os
import io

# -------------------------------------------------------------------
# 🔥 EXACT SAME PATHS AS BACKEND (Adjust if needed)
# -------------------------------------------------------------------
MODEL_PATH = os.path.join("models", "garbage_classifier_model.h5")
LABEL_PATH = os.path.join("models", "class_indices.json")

# -------------------------------------------------------------------
# 🔥 Load Model + Labels
# -------------------------------------------------------------------
st.cache_resource
def load_model_files():
    model = load_model(MODEL_PATH)
    with open(LABEL_PATH, "r") as f:
        class_indices = json.load(f)
    idx_to_class = {v: k for k, v in class_indices.items()}
    return model, idx_to_class

model, idx_to_class = load_model_files()

# -------------------------------------------------------------------
# 🔥 Streamlit UI
# -------------------------------------------------------------------
st.set_page_config(page_title="Garbage Waste Classifier", layout="centered")

st.title("♻️ Garbage Waste Classifier (Streamlit)")
st.write("Upload an image to classify it as **Organic**, **Recyclable**, or **E-waste**.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

# -------------------------------------------------------------------
# 🔥 Prediction function (identical to FastAPI)
# -------------------------------------------------------------------
def predict_image(image_bytes):
    img = load_img(io.BytesIO(image_bytes), target_size=(128, 128))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)[0]
    pred_idx = int(np.argmax(preds))
    predicted_label = idx_to_class[pred_idx]
    confidence = round(float(preds[pred_idx] * 100), 2)

    return predicted_label, confidence, preds


# -------------------------------------------------------------------
# 🔥 UI Logic
# -------------------------------------------------------------------
if uploaded_file is not None:
    image_bytes = uploaded_file.read()

    # Show image
    st.image(image_bytes, caption="Uploaded Image", use_container_width=True)

    # Predict
    label, conf, full_probs = predict_image(image_bytes)

    st.success(f"### 🟢 Prediction: **{label}**")
    st.info(f"### 🔍 Confidence: **{conf}%**")

    # Show probability breakdown
    st.subheader("🔬 Class Probabilities")
    for idx, prob in enumerate(full_probs):
        st.write(f"**{idx_to_class[idx]}** → {round(prob*100, 2)}%")
