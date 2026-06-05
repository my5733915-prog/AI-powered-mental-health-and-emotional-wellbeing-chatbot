from flask import Flask, render_template, jsonify
from google import genai
import speech_recognition as sr
import threading
import re, json

app = Flask(__name__)

# 🌟 Gemini setup
client = genai.Client(api_key="AIzaSyBqswyXyB8sKOHkDBTKuYgMT7xscSqgmCA")

# 🎤 Speech setup
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Global status
is_listening = False
result_data = {"text": "", "analysis": "", "status": "Idle"}


# 🧠 Emotion analysis using Gemini
def analyze_emotion(recognized_text):
    global result_data
    try:
        prompt = f"""
You are **MAITRI**, an empathetic and emotionally intelligent AI companion.
You just listened to a short voice clip spoken by the user.
Based on **the tone, energy, and emotion in their voice**, understand how they are truly feeling.

Here’s the transcribed speech:
"{recognized_text}"

Now act as if you actually *heard their voice*, not just the words.
Focus on:
- Vocal tone (energy, pace, positivity, stress, calmness)
- Emotional undertone (hidden mood, not just literal meaning)
- The human feeling behind the voice

🎯 Your tasks:
1. Identify the most dominant emotion from this list:
   [Happy, Sad, Angry, Fear, Disgust, Surprise, Neutral]
2. Describe briefly (one line) **why** you felt that emotion.
3. Reply as MAITRI — warm, friendly Hinglish, like a close friend who genuinely cares ❤️  
   Use 2–3 short sentences max, include one suitable emoji.
4. Suggest one of these:
   - Motivational quote (if Sad/Angry/Fear)
   - Calming song or meditation (if Sad/Fear/Neutral)
   - Breathing tip (if Angry/Stress)
   - Cheerful nudge (if Happy/Surprise)

🎁 Respond strictly in JSON:
{{
  "emotion": "<dominant emotion>",
  "reason": "<short reason>",
  "maitri_reply": "<empathetic Hinglish response with emoji>",
  "suggestion": "<quote / playlist / tip>"
}}
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_text = getattr(response, "text", str(response)).strip()
        print("💬 Raw Gemini Output:", raw_text)

        # 🔹 CLEANING Gemini response to ensure valid JSON
        cleaned = re.sub(r"```json|```", "", raw_text).strip()

        try:
            parsed = json.loads(cleaned)  # convert to dict
            analysis = json.dumps(parsed)  # send human-readable JSON to frontend
        except Exception as e:
            # fallback: send as string if not valid JSON
            analysis = cleaned

        result_data["analysis"] = analysis
        result_data["status"] = "Done"

    except Exception as e:
        result_data = {
            "status": "Done",
            "text": recognized_text,
            "analysis": f"Error: {str(e)}"
        }


# 🎙️ Listen once (mic activates only when called)
def listen_once():
    global result_data, is_listening
    try:
        with mic as source:
            print("🎧 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            recognizer.dynamic_energy_threshold = True
            recognizer.energy_threshold = 250

            print("🎧 Listening for 5 seconds...")
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)

        print("🔍 Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {text}")

        result_data["text"] = text
        result_data["status"] = "Analyzing..."
        analyze_emotion(text)

    except sr.WaitTimeoutError:
        result_data = {"status": "Done", "text": "", "analysis": "❌ No speech detected (timeout)."}
    except sr.UnknownValueError:
        result_data = {"status": "Done", "text": "", "analysis": "❌ Could not understand speech."}
    except Exception as e:
        result_data = {"status": "Done", "text": "", "analysis": f"Error: {str(e)}"}
    finally:
        is_listening = False


# 🏠 Home route
@app.route("/")
def home():
    return render_template("newVoice.html")


# ▶️ Start listening
@app.route("/start", methods=["POST"])
def start_listening():
    global is_listening, result_data
    if is_listening:
        return jsonify({"status": "Already listening"})

    is_listening = True
    result_data = {"text": "", "analysis": "", "status": "Listening..."}

    threading.Thread(target=listen_once, daemon=True).start()
    print("🎙️ Background listening thread started.")
    return jsonify({"status": "Listening..."})


# 📊 Status route
@app.route("/status")
def get_status():
    return jsonify(result_data)


# 🚀 Run server
if __name__ == "__main__":
    app.run(debug=True, port=5002, use_reloader=False)
