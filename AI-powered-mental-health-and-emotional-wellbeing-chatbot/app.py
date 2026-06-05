import subprocess
import sys
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/face")
def run_face():
    subprocess.Popen(
        [sys.executable, "faceDetection.py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    return redirect(url_for("home"))  # 👈 direct back to landing

@app.route("/voice")
def run_voice():
    subprocess.Popen(
        [sys.executable, "Finalvoice_Emo.py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    return redirect(url_for("home"))

@app.route("/chat")
def run_chat():
    subprocess.Popen(
        [sys.executable, "chatAI.py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=8000, use_reloader=False)
