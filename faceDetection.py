from flask import Flask, render_template, request, jsonify
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import io, base64, torch
import cv2
import numpy as np
import os
from google import genai  # ✅ Gemini API client

# =====================================================
#  🌸 MAITRI: AI Mental Health Companion
#  Emotion Detection + Empathetic Response Generator
# =====================================================

app = Flask(__name__)

# 1️⃣ Hugging Face Token
HF_TOKEN = os.getenv("HF_TOKEN")

# 2️⃣ Load Hugging Face Model
processor = AutoImageProcessor.from_pretrained(
    "HardlyHumans/Facial-expression-detection",
    token=HF_TOKEN
)
model = AutoModelForImageClassification.from_pretrained(
    "HardlyHumans/Facial-expression-detection",
    token=HF_TOKEN
)

# 3️⃣ Load Haar Cascade for Face Detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# 4️⃣ Initialize Gemini Client
GEMINI_API_KEY = "AIzaSyBqswyXyB8sKOHkDBTKuYgMT7xscSqgmCA"  # 🔑 Replace this
gemini = genai.Client(api_key=GEMINI_API_KEY)

# -----------------------------------------------------
# 🧠 Function: Generate Supportive Message via Gemini
# -----------------------------------------------------
def generate_supportive_message(emotion: str) -> str:
    try:
        prompt = f"""
You are MAITRI — a caring, empathetic, and emotionally intelligent mental health companion.
The detected emotion from the user's face or voice is "{emotion}".

🎯 Your main goals:
1. Respond in *natural Hinglish* (soft mix of Hindi + English).
2. Write only 2–3 short comforting sentences that sound warm, human, and caring.
3. Validate their emotions, offer gentle reassurance — like a close friend talking.
4. Avoid medical or diagnostic advice.
5. Add one suitable emoji that fits the emotional tone.

🌸 After comforting them, MAITRI should recommend something uplifting *based on their emotion*:
- If they feel low, sad, or tired → give a short **motivational quote** (can be original or famous).
- If they feel anxious, angry, or stressed → suggest a **calming music track or meditation playlist** (with song or genre name).
- If they feel happy or peaceful → suggest a **gratitude or reflection activity** to maintain positivity.
- If they seem neutral or confused → suggest a **simple breathing or grounding exercise**.

✨ Response format:
1. Empathetic Hinglish message (2–3 lines)
2. Self-care suggestion (1 line) — auto-generated with real quote, song, or exercise idea

🧠 Example:
"Thoda tough lag raha hai na aaj... kabhi kabhi sab slow lagta hai, but you're doing your best 💛  
Try listening to 'Calm Lo-Fi Beats' on Spotify or take 3 deep breaths right now — it’ll really help 🌿"
"""


        response = gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return "I'm here for you. Sometimes it's okay to just take a moment and breathe. 💙"

# -----------------------------------------------------
# 🌐 Routes
# -----------------------------------------------------
@app.route("/")
def home():
    return render_template("faceDetection.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        image_data = data["image"].split(",")[1]
        image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert("RGB")

        # Convert PIL image to OpenCV
        open_cv_image = np.array(image)
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        # Detect faces
        faces = face_cascade.detectMultiScale(open_cv_image, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            return jsonify({
                "error": "No face detected",
                "emotion": "Neutral",
                "confidence": 0.0,
                "message": "I couldn’t detect a face, but remember you are valued and loved 💙"
            })

        # Take first detected face
        x, y, w, h = faces[0]
        face_img = open_cv_image[y:y+h, x:x+w]

        # Convert back to PIL Image for model
        face_pil = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))

        # Predict emotion
        inputs = processor(face_pil, return_tensors="pt")
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

        pred_idx = int(torch.argmax(probs))
        pred_label = model.config.id2label[pred_idx]
        confidence = round(torch.max(probs).item(), 2)

        # Generate Gemini response
        supportive_message = generate_supportive_message(pred_label)

        # Return JSON result
        return jsonify({
            "emotion": pred_label,
            "confidence": confidence,
            "message": supportive_message
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Something went wrong, but don’t worry — take a deep breath 💫"
        })

# -----------------------------------------------------
# 🚀 Run App
# -----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001, use_reloader=False)
