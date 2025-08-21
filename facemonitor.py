import cv2
import pygame
import time
from monitor_flag import MonitorFlags

def start_exam_monitoring():
    print("📸 [Monitor] Face monitoring initialized...")

    # Load Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                         'haarcascade_frontalface_default.xml')

    # Initialize pygame for sound alert
    pygame.mixer.init()
    horn = pygame.mixer.Sound("horn.mp3")

    # Access the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ [Monitor] Could not access webcam. Is another app using it?")
        return
    print("✅ [Monitor] Webcam successfully opened.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ [Monitor] Failed to capture frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,
                                               scaleFactor=1.1,
                                               minNeighbors=5)

        print(f"🧠 [Monitor] Detected {len(faces)} face(s).")

        if len(faces) > 1 and not MonitorFlags.terminate_exam:
            print("🚨 [Monitor] Multiple faces detected! Terminating exam...")
            MonitorFlags.terminate_exam = True
            horn.play()
            break

        # Optional: delay to reduce CPU usage
        cv2.waitKey(200)

    cap.release()
    cv2.destroyAllWindows()
    print("🛑 [Monitor] Webcam released and monitoring ended.")
