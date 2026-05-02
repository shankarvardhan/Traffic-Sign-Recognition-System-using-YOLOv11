from flask import Flask, render_template, request, Response, jsonify, send_from_directory
import cv2
import os
from ultralytics import YOLO
import pyttsx3

app = Flask(__name__)

# ---------------- VOICE FUNCTION (FINAL FIX) ----------------
def speak(text):
    try:
        engine = pyttsx3.init()   # 🔥 reinitialize every time
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)   # female voice
        engine.setProperty('rate', 160)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("Voice error:", e)

# ---------------- PATHS ----------------
UPLOAD_FOLDER = r"C:\webapp\webapp\uploads1"
MODEL_PATH = r"C:\webapp\webapp\best_final.pt"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load YOLO model once
model = YOLO(MODEL_PATH)

# --------------------------------------------------
# Serve uploaded images
# --------------------------------------------------
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# --------------------------------------------------
# Home
# --------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# --------------------------------------------------
# Image Upload + Detection
# --------------------------------------------------
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save input image
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Read image
    image = cv2.imread(input_path)
    if image is None:
        return jsonify({"error": "Failed to read image using OpenCV"}), 500

    # YOLO inference
    results = model(image)

    detections = []
    detected_classes = []

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            cls_name = r.names[cls_id]
            conf = float(box.conf[0]) * 100

            detections.append(f"{cls_name} ({conf:.2f}%)")
            detected_classes.append(cls_name)

            # Draw box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Label
            label = f"{cls_name} {conf:.1f}%"
            cv2.putText(
                image,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # Save output image
    output_name = "detected_" + file.filename
    output_path = os.path.join(UPLOAD_FOLDER, output_name)
    cv2.imwrite(output_path, image)

    # Clean result text
    unique_classes = list(set(detected_classes))

    if unique_classes:
        result_text = "Detected " + ", ".join(unique_classes)
    else:
        result_text = "No objects detected"

    # 🔊 Voice output (FIXED)
    speak(result_text)

    return jsonify({
        "image": output_name,
        "result": result_text
    })

# --------------------------------------------------
# Webcam Detection
# --------------------------------------------------
@app.route("/video_feed")
def video_feed():
    def generate():
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("❌ Camera not accessible")
            return

        last_spoken = ""

        while True:
            success, frame = cap.read()
            if not success:
                break

            results = model(frame)

            current_detected = []

            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = r.names[int(box.cls[0])]
                    conf = float(box.conf[0]) * 100

                    current_detected.append(cls)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        f"{cls} {conf:.1f}%",
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )

            # 🔊 Speak only if changed
            if current_detected:
                unique_classes = list(set(current_detected))
                current_text = "Detected " + ", ".join(unique_classes)

                if current_text != last_spoken:
                    speak(current_text)
                    last_spoken = current_text

            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )

        cap.release()

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

# --------------------------------------------------
# Run Flask
# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)