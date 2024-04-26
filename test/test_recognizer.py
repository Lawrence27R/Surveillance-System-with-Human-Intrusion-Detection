import cv2
import sys
sys.path.append(".")
from gui.homecontent import ObjectDetection

if __name__ == "__main__":
    # Instantiate the ObjectDetection class
    detector = ObjectDetection()

    # Specify the path to the sample video
    sample_video_path = "Video_Rec/01_Intruder.mp4"

    # Open the sample video
    cap = cv2.VideoCapture(sample_video_path)

    # Set video properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_count = 0
    while True:
        ret, im0 = cap.read()
        if not ret:
            break

        results = detector.predict(im0)
        im0, _ = detector.plot_bboxes(results, im0)

        detector.display_fps(im0)
        cv2.imshow('YOLOv8 Detection', im0)

        frame_count += 1
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):  # Break on 'q' or ESC key
            break

    cap.release()
    cv2.destroyAllWindows()
