const video = document.getElementById("camera");
const resultDiv = document.getElementById("result");
const captureBtn = document.getElementById("captureBtn");

// Get webcam access
navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => (video.srcObject = stream))
  .catch((err) => alert("Camera access denied: " + err));

// Capture frame and send to backend
captureBtn.addEventListener("click", async () => {
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0);

  const imageData = canvas.toDataURL("image/jpeg");

  resultDiv.innerHTML = "Detecting emotion...";

  const res = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: imageData }),
  });

  const data = await res.json();
  resultDiv.innerHTML = `
    <h3>Detected Emotion: ${data.emotion}</h3>
    <p>Confidence: ${data.confidence}</p>
  `;
});
