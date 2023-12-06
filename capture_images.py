import cv2
import os
import tkinter as tk
from tkinter import messagebox

def capture_images(user_id, username):
    # Create a directory for the user's images
    user_image_dir = os.path.join('User_Images', f"{user_id}_{username}")
    os.makedirs(user_image_dir, exist_ok=True)

    # Open a video capture stream
    cap = cv2.VideoCapture(0)

    # Load the Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Counter for image numbering
    image_number = 1

    while True:
        ret, frame = cap.read()

        if not ret:
            messagebox.showerror("Capture Error", "Failed to capture video.")
            break

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces using Haar Cascade
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        for (x, y, width, height) in faces:
            face_pixels = frame[y:y + height, x:x + width]

            # Display the frame
            cv2.imshow("Capture Images", frame)

            # Save the face image only when 'C' key is pressed
            key = cv2.waitKey(1)
            if key in (27, ord('q')):  # 'ESC' key or 'q' key
                break
            elif key == 99 or key == 67:  # 'c' or 'C' key
                # Save the face image
                img_file = os.path.join(user_image_dir, f"{user_id}_{username}_{image_number}.jpg")
                cv2.imwrite(img_file, face_pixels)
                print(f"Image {image_number} captured and saved as {img_file}")
                image_number += 1

                # Add some padding around the face rectangle
                padding = 30
                cv2.rectangle(frame, (x - padding, y - padding), (x + width + padding, y + height + padding), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Capture Images", frame)

        # Break the loop when 'q' key is pressed or all images are captured
        if cv2.waitKey(1) & 0xFF in (27, ord('q')):
            break

    # Release the video capture and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
