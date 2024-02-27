# sample_recognition.py
from recognize import FaceRecognizer

def main():
    # Create an instance of the FaceRecognizer class
    face_recognizer = FaceRecognizer()

    # Specify the path to the sample video file
    sample_video_path = "Video_Rec/03_Face.mp4"

    try:
        # Run face tracking and recognition on the sample video
        face_recognizer.main(sample_video_path)
    except KeyboardInterrupt:
        print("Interrupt received. Stopping processing...")

if __name__ == "__main__":
    main()
