import cv2
import os
import tkinter as tk
from tkinter import messagebox

def capture_images(user_id, username):
    user_image_dir = os.path.join('datasets/new_persons', f"{user_id}_{username}")
    os.makedirs(user_image_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)

    face_cascade_frontal = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_cascade_profile = cv2.CascadeClassifier('haarcascade_profileface.xml') 
    image_number = 1

    while True:
        ret, frame = cap.read()

        if not ret:
            messagebox.showerror("Capture Error", "Failed to capture video.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frontal_faces = face_cascade_frontal.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        profile_faces = face_cascade_profile.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        for (x, y, width, height) in frontal_faces:
            face_pixels = frame[y:y + height, x:x + width]
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
            cv2.imshow("Capture Images", frame)

            key = cv2.waitKey(1)
            if key in (27, ord('q')):
                break
            elif key == 99 or key == 67:
                img_file = os.path.join(user_image_dir, f"{username}_{image_number}.jpg")
                cv2.imwrite(img_file, face_pixels)
                print(f"Image {image_number} captured and saved as {img_file}")
                image_number += 1

        for (x, y, width, height) in profile_faces:
            face_pixels = frame[y:y + height, x:x + width]
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
            cv2.imshow("Capture Images", frame)

            key = cv2.waitKey(1)
            if key in (27, ord('q')):
                break
            elif key == 99 or key == 67:
                img_file = os.path.join(user_image_dir, f"{username}_{image_number}.jpg")
                cv2.imwrite(img_file, face_pixels)
                print(f"Image {image_number} captured and saved as {img_file}")
                image_number += 1

        cv2.imshow("Capture Images", frame)

        if cv2.waitKey(1) & 0xFF in (27, ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()
