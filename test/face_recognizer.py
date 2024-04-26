import cv2
import sys
sys.path.append(".")
from recognize import FaceRecognizer
import threading

if __name__ == "__main__":
    # Instantiate the FaceRecognizer class for face recognition
    face_recognizer = FaceRecognizer()

    # Specify the path to the sample video
    sample_video_path = "Video_Rec/03_Face.mp4"

    # Open the sample video
    cap = cv2.VideoCapture(sample_video_path)

    # Set video properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Get video properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create a VideoWriter object
    out = cv2.VideoWriter('result_video.avi', cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 10, (frame_width, frame_height))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Face recognition and tracking
        face_recognizer.data_mapping["raw_image"] = frame

        # Start the recognition thread
        recognition_thread = threading.Thread(target=face_recognizer.recognize)
        recognition_thread.start()

        # Display the frame if needed
        cv2.imshow('Face Recognition', frame)

        # Write the frame to the result video
        out.write(frame)

        frame_count += 1
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):  # Break on 'q' or ESC key
            break

    # Release the VideoWriter and capture objects
    out.release()
    cap.release()
    cv2.destroyAllWindows()
    face_recognizer.destroy_window()
