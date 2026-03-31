import tensorflow as tf
import numpy as np
import cv2
import os
import gdown

MODEL_PATH = "saved_models/model.h5"

# 🔥 Google Drive direct download link
MODEL_URL = "https://drive.google.com/uc?id=1qvMMTzsQsfHJucBAIKgDP3KAwQKBx1du"

def download_model():
    if not os.path.exists("saved_models"):
        os.makedirs("saved_models")

    if not os.path.exists(MODEL_PATH):
        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

# LOAD MODEL
def load_model():
    download_model()
    return tf.keras.models.load_model(MODEL_PATH, compile=False)

model = load_model()

IMG_SIZE = (299, 299)
FRAMES = 10

def preprocess_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, IMG_SIZE)
    return frame / 255.0

def sample_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    idxs = np.linspace(0, total - 1, FRAMES).astype(int)

    for i in range(total):
        ret, frame = cap.read()
        if not ret:
            break
        if i in idxs:
            frames.append(preprocess_frame(frame))

    cap.release()

    while len(frames) < FRAMES:
        frames.append(frames[-1])

    return np.array(frames)

def predict_video(video_path):
    frames = sample_video_frames(video_path)
    frames = np.expand_dims(frames, axis=0)

    pred = model.predict(frames)[0][0]

    label = "FAKE" if pred > 0.5 else "REAL"
    confidence = pred if label == "FAKE" else 1 - pred

    return label, float(confidence)
