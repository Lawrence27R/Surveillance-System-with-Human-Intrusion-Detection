import time
import cv2
import yaml
from face_detection.scrfd.detector import SCRFD
from face_detection.yolov5_face.detector import Yolov5Face
from face_tracking.tracker.byte_tracker import BYTETracker
from face_tracking.tracker.visualize import plot_tracking


# Function to load a YAML configuration file
def load_config(file_name):
    with open(file_name, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


# Function for performing object detection and tracking
def inference(detector, args):
    # Open a video capture object
    cap = cv2.VideoCapture(0)

    # Initialize variables for measuring frame rate
    start_time = time.time_ns()
    frame_count = 0
    fps = -1

    # Initialize a tracker and a timer
    tracker = BYTETracker(args=args, frame_rate=30)
    frame_id = 0

    # Save video
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)
    video = cv2.VideoWriter(
        "/Video_Rec/face-tracking.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, size
    )

    while True:
        # Read a frame from the video capture
        ret_val, frame = cap.read()

        if ret_val:
            # Perform face detection and tracking on the frame
            outputs, img_info, bboxes, landmarks = detector.detect_tracking(image=frame)

            if outputs is not None:
                online_targets = tracker.update(
                    outputs, [img_info["height"], img_info["width"]], (128, 128)
                )
                online_tlwhs = []
                online_ids = []
                online_scores = []

                for t in online_targets:
                    tlwh = t.tlwh
                    tid = t.track_id
                    vertical = tlwh[2] / tlwh[3] > args["aspect_ratio_thresh"]
                    if tlwh[2] * tlwh[3] > args["min_box_area"] and not vertical:
                        online_tlwhs.append(tlwh)
                        online_ids.append(tid)
                        online_scores.append(t.score)

                online_im = plot_tracking(
                    img_info["raw_img"],
                    online_tlwhs,
                    online_ids,
                    frame_id=frame_id + 1,
                    fps=fps,
                )
            else:
                online_im = img_info["raw_img"]

            # Calculate and display the frame rate
            frame_count += 1
            if frame_count >= 30:
                fps = 1e9 * frame_count / (time.time_ns() - start_time)
                frame_count = 0
                start_time = time.time_ns()

            # Save the frame to the video
            video.write(online_im)

            cv2.imshow("Face Tracking", online_im)

            # Check for user exit input
            ch = cv2.waitKey(1)
            if ch == 27 or ch == ord("q") or ch == ord("Q"):
                break
        else:
            break
        frame_id += 1

    # Release video and camera, and close all OpenCV windows
    video.release()
    cap.release()
    cv2.destroyAllWindows()


def main():
    file_name = "./face_tracking/config/config_tracking.yaml"
    config_tracking = load_config(file_name)
    detector = SCRFD(model_file="face_detection/scrfd/weights/scrfd_2.5g_bnkps.onnx")

    inference(detector=detector, args=config_tracking)


if __name__ == "__main__":
    main()