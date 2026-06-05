from flask import Flask, render_template, request, jsonify
from transformers import Wav2Vec2FeatureExtractor, HubertForSequenceClassification
import torch
import numpy as np
import io
import wave

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = "superb/hubert-large-superb-er"

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME, token=HF_TOKEN)
model = HubertForSequenceClassification.from_pretrained(MODEL_NAME, token=HF_TOKEN)

@app.route("/")
def home():
    return render_template("audio.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No audio file uploaded!"})

        file = request.files["file"]
        file_bytes = io.BytesIO(file.read())

        # -----------------------------
        # Read WAV using wave module
        # -----------------------------
        with wave.open(file_bytes, "rb") as wav:
            n_channels = wav.getnchannels()
            sample_rate = wav.getframerate()
            n_frames = wav.getnframes()
            audio_data = wav.readframes(n_frames)

        # Convert bytes to numpy array
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
        # Stereo to mono if needed
        if n_channels > 1:
            audio_np = audio_np.reshape(-1, n_channels)
            audio_np = audio_np.mean(axis=1)
        # Normalize to [-1, 1]
        audio_np /= 32768.0

        # -----------------------------
        # Hugging Face prediction
        # -----------------------------
        inputs = feature_extractor(audio_np, sampling_rate=sample_rate, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = model(**inputs).logits

        probs = torch.nn.functional.softmax(logits, dim=-1)
        pred_id = torch.argmax(probs, dim=-1).item()
        label = model.config.id2label[pred_id]
        confidence = round(torch.max(probs).item(), 2)

        return jsonify({"emotion": label, "confidence": confidence})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
