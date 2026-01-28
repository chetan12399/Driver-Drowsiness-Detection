import cv2
import mediapipe as mp
import pygame
import time

# Initialize Mediapipe for face and eye detection
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Initialize pygame mixer for alarm sound
pygame.mixer.init()

# Load the alarm sound (ensure 'alarm.mp3' is in the same folder)
pygame.mixer.music.load('alarm.mp3')

# Function to play the alarm sound
def play_alarm():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()

# Function to calculate the Eye Aspect Ratio (EAR)
def eye_aspect_ratio(landmarks, left_eye, right_eye):
    def calculate_distance(p1, p2):
        return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2) ** 0.5

    left_ear = (calculate_distance(landmarks[left_eye[1]], landmarks[left_eye[5]]) +
                calculate_distance(landmarks[left_eye[2]], landmarks[left_eye[4]])) / (
                2 * calculate_distance(landmarks[left_eye[0]], landmarks[left_eye[3]]))

    right_ear = (calculate_distance(landmarks[right_eye[1]], landmarks[right_eye[5]]) +
                 calculate_distance(landmarks[right_eye[2]], landmarks[right_eye[4]])) / (
                 2 * calculate_distance(landmarks[right_eye[0]], landmarks[right_eye[3]]))

    return (left_ear + right_ear) / 2

# Parameters for EAR threshold and consecutive frames
EAR_THRESHOLD = 0.2
FRAME_THRESHOLD = 30
frame_counter = 0

# Start video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Error: Could not read frame.")
        break

    # Convert frame to RGB for Mediapipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame and detect facial landmarks
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            # Eye indices for Mediapipe's 468-landmark model
            left_eye = [362, 385, 387, 263, 373, 380]
            right_eye = [33, 160, 158, 133, 153, 144]
            ear = eye_aspect_ratio(landmarks, left_eye, right_eye)

            # Check if eyes are closed
            if ear < EAR_THRESHOLD:
                frame_counter += 1
                if frame_counter >= FRAME_THRESHOLD:
                    cv2.putText(frame, "Eyes Closed", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    play_alarm()
            else:
                frame_counter = 0
                pygame.mixer.music.stop()

    # Display the video frame with eye state indication
    cv2.imshow('Eye Tracker', frame)
    if cv2.waitKey(5) & 0xFF in [27, ord('q')]:  # Press 'Esc' or 'q' to exit
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
