# 👁️ Eye Blink Detection for Drowsiness Prevention

A real-time drowsiness detection system that monitors eye activity using computer vision techniques and triggers an alarm when prolonged eye closure is detected.

---

## 📌 Project Overview

This project detects drowsiness by analyzing eye movements through a webcam. It uses **MediaPipe Face Mesh** to detect facial landmarks and calculates the **Eye Aspect Ratio (EAR)** to determine whether the eyes are open or closed.  
If the eyes remain closed beyond a predefined threshold, an alarm sound is triggered to alert the user.

This system is useful in **driver monitoring systems** and other **safety-critical environments**.

---

## 🎯 Features

- Real-time face and eye detection
- Eye Aspect Ratio (EAR) based eye-closure detection
- Audio alarm for drowsiness alert
- Live video stream with visual warning
- Lightweight and efficient implementation

---

## 🛠️ Technologies Used

- **Python**
- **OpenCV** – Video capture and processing
- **MediaPipe** – Facial landmark detection (468 points)
- **Pygame** – Audio alarm playback
- **NumPy** – Mathematical calculations

---

## ⚙️ How It Works

1. Webcam captures live video feed.
2. MediaPipe detects 468 facial landmarks.
3. Six eye landmarks per eye are used to calculate EAR.
4. If EAR drops below `0.2` for more than `60 consecutive frames`, drowsiness is detected.
5. An alarm sound is triggered using Pygame.
6. Visual alerts are displayed on the video stream.

---

## 🧮 Eye Aspect Ratio (EAR) Formula

