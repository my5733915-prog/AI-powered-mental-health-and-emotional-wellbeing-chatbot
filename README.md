# 🌸 MAITRI — Mental AI Therapeutic Response Interface

> An AI-powered multimodal mental health companion that detects human emotions through face, voice, and text — and responds with empathy in **Hinglish**.

---

## 📌 About the Project

**MAITRI (Mental AI Therapeutic Response Interface)** is a web-based AI companion designed to provide real-time emotional support. It recognizes a user's emotional state through three channels — facial expressions, voice signals, and text input — and generates warm, empathetic responses using large language models.

Built as an MCA final year project at **Atal Bihari Vajpayee Vishwavidyalaya, Bilaspur (C.G.)**, MAITRI highlights how affective computing and AI can be applied responsibly in the mental health domain.

> ⚠️ MAITRI is a **supportive companion**, not a replacement for professional mental health services.

---

## ✨ Features

- 🎭 **Facial Emotion Detection** — Real-time webcam-based emotion recognition using CNN + Hugging Face models
- 🎙️ **Voice Emotion Recognition** — Speech-based emotion analysis using HuBERT transformer model
- 💬 **Text-Based Mood Check-in** — Structured form to capture emotional intensity, duration, and context
- 🤖 **Empathetic AI Responses** — Context-aware, supportive replies generated via Google Gemini API
- 🇮🇳 **Hinglish Interaction** — Responses in Hindi-English mix for natural, relatable communication
- 🔒 **Privacy-First Design** — No user data stored; all processing is done in real-time

---

## 🧠 System Architecture

```
User Input (Face / Voice / Text)
        ↓
Emotion Detection Modules
  ├── Facial Emotion Recognition (CNN + HuggingFace)
  ├── Voice Emotion Recognition (HuBERT Transformer)
  └── Text Emotion Analysis (NLP + LLM)
        ↓
Multimodal Emotion Fusion
        ↓
Gemini API → Empathetic Hinglish Response
        ↓
Flask Web Interface → User
```

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | Python, Flask |
| Facial Emotion | Hugging Face Transformers, OpenCV, PIL |
| Voice Emotion | HuBERT (`superb/hubert-large-superb-er`), Wav2Vec2 |
| AI Response |
| Frontend | HTML, CSS, JavaScript |
| Deep Learning | PyTorch |

---

## 📁 Project Structure

```
MAITRI/
│
├── app.py                  # Main Flask application
├── faceDetection.py        # Facial emotion detection module
├── voiceMold.py            # Voice emotion recognition module
├── chatAI.py               # Text-based chat and AI response
├── Finalvoice_Emo.py       # Voice emotion helper
├── check.py                # Utility/testing script
├── requirements.txt        # Python dependencies
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── newVoice.css
│
└── templates/
    ├── landing.html
    ├── faceDetection.html
    ├── newVoice.html
    └── mood_form.html
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/my5733915-prog/AI-powered-mental-health-and-emotional-wellbeing-chatbot.git
cd AI-powered-mental-health-and-emotional-wellbeing-chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the root directory:
```
HF_TOKEN=your_huggingface_token
GEMINI_API_KEY=your_gemini_api_key
```

Or set them directly in your terminal:
```bash
# Windows
set HF_TOKEN=your_token
set GEMINI_API_KEY=your_key

# Linux/Mac
export HF_TOKEN=your_token
export GEMINI_API_KEY=your_key
```

### 4. Run the Application
```bash
python app.py
```

Open your browser and go to: `http://localhost:5000`

---

## 🔑 API Keys Required

| Key | Where to Get |
|---|---|
| `HF_TOKEN` | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) |

---

## 📊 Results

- ✅ High accuracy facial emotion detection under proper lighting
- ✅ Effective voice emotion recognition for intense emotional states
- ✅ Multimodal fusion outperforms single-modality approaches
- ✅ Real-time response with minimal latency
- ✅ Users reported higher comfort with Hinglish responses

---



## 📄 License

This project is submitted for academic purposes under MCA program. All rights reserved by the authors.
