# Traffic-Sign-Recognition-System-using-YOLOv11
Project Overview

The Traffic Sign Recognition System is a real-time object detection solution designed to enhance road safety by identifying and classifying traffic signs using the YOLOv11 deep learning algorithm.

This system is deployed on a Raspberry Pi, enabling edge-based detection without the need for high-end GPUs. It processes live video input, detects multiple traffic sign classes, and provides accurate results under varying environmental conditions such as lighting, angle, and background noise.

🎯 Key Features
🚀 Real-time traffic sign detection using YOLOv11
⚡ Low-latency performance on Raspberry Pi (edge computing)
🎥 Live video stream processing via camera module / webcam
🌗 Robust detection under different lighting and weather conditions
📊 Multi-class traffic sign classification
🔊 (Optional) Voice alert system for detected signs

🛠️ Technologies Used
Programming Language: Python
Deep Learning Model: YOLOv11
Libraries: OpenCV, NumPy
Hardware: Raspberry Pi 4 Model B, Camera Module
Tools & Platforms: Google Colab, Roboflow

⚙️ System Architecture
Image/Video Input from Camera
Preprocessing (Resizing, Normalization, Augmentation)
YOLOv11 Model Detection
Bounding Box & Label Prediction
Output Display (Live Detection Results)

🧠 Model Training
Dataset collected and enhanced using data augmentation techniques:
Rotation
Flipping
Scaling
Brightness adjustment
Model trained using YOLOv11 on Google Colab
Performance evaluated using:
Precision
Recall
mAP (Mean Average Precision)

2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run the Application
python app.py
