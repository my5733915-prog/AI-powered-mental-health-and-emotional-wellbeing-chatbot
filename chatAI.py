from flask import Flask, request, jsonify, render_template
from google import genai
import json, re

app = Flask(__name__)

# 🌟 Gemini setup
client = genai.Client(api_key="AIzaSyBqswyXyB8sKOHkDBTKuYgMT7xscSqgmCA")

# 🏠 GET route to render the form
@app.route("/", methods=["GET"])
def mood_form():
    return render_template("mood_form.html")  # Form HTML

# ▶️ POST route to handle form submission and Gemini analysis
@app.route("/api/chat", methods=["POST"])
def chat_api():
    try:
        # 1️⃣ Collect all form data
        mood = request.form.get("mood", "")
        intensity = request.form.get("intensity", "")
        duration = request.form.get("duration", "")
        sleep = request.form.get("sleepQuality", "")
        message = request.form.get("message", "")

        if not message:
            return jsonify({"error": "Message is required!"})

        # 2️⃣ Prepare Gemini prompt (request JSON but we'll parse backend)
        prompt = f"""
You are **MAITRI**, an empathetic AI companion.
A user submitted a mental health check-in form:

- Mood: {mood}
- Intensity: {intensity}/10
- Duration: {duration}
- Sleep Quality: {sleep}
- Additional Message: "{message}"

Analyze their emotional state, give a warm empathetic reply in Hinglish (2-3 short sentences, include emoji),
and provide a helpful suggestion or nudge.

Respond strictly in JSON:
{{
  "analysis": "<short human-like analysis>",
  "maitri_reply": "<empathetic response in Hinglish with emoji>",
  "suggestion": "<motivational tip, calming advice, or cheerful nudge>"
}}
"""

        # 3️⃣ Call Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_text = getattr(response, "text", str(response)).strip()

        # 4️⃣ Clean Gemini JSON if wrapped in markdown or code fences
        clean_text = re.sub(r"```(?:json)?|```", "", raw_text).strip()

        try:
            clean_json = json.loads(clean_text)
        except Exception:
            # fallback if Gemini didn't give valid JSON
            clean_json = {"analysis": clean_text}

        # 5️⃣ Prepare human-readable string for frontend
        human_readable = f"🎤 You said:\n{message}\n\n🧠 MAITRI's Analysis:\n{clean_json.get('analysis', '')}\n\n💬 MAITRI Reply:\n{clean_json.get('maitri_reply', '')}\n\n✨ Suggestion:\n{clean_json.get('suggestion', '')}"

        return jsonify({"result": human_readable})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5003, use_reloader=False)
