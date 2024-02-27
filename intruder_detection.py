import torch
import os
import numpy as np
import cv2
from datetime import datetime
from time import time
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
from gui.email_alert import send_email, call  # Import necessary functions

# Set the environment variable to disable YOLO verbose output
os.environ['YOLO_VERBOSE'] = 'False'

class ObjectDetection:
    def __init__(self):
        # default parameters
        self.email_sent = False

        self.model = YOLO("detection_model/yolov8m.pt")

        # visual information
        self.annotator = None
        self.start_time = 0
        self.end_time = 0

        # device information
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        # Set the class of interest (person)
        self.person_class_name = 'person'

    def predict(self, im0):
        results = self.model(im0)
        return results

    def display_fps(self, im0):
        self.end_time = time()
        fps = 1 / np.round(self.end_time - self.start_time, 2)
        text = f'FPS: {int(fps)}'
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
        gap = 10
        cv2.rectangle(im0, (20 - gap, 70 - text_size[1] - gap), (20 + text_size[0] + gap, 70 + gap), (255, 255, 255), -1)
        cv2.putText(im0, text, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)

    def plot_bboxes(self, results, im0):
        class_ids = []
        self.annotator = Annotator(im0, 3, results[0].names)
        boxes = results[0].boxes.xyxy.cpu()
        clss = results[0].boxes.cls.cpu().tolist()
        names = results[0].names
        for box, cls in zip(boxes, clss):
            if names[int(cls)] == self.person_class_name:  # Only consider person class
                class_ids.append(cls)
                label_text = "Intruder"
                self.annotator.box_label(box, label=label_text, color=colors(int(cls), True))
        return im0, class_ids

    def send_email(self, object_detected):
        # Use the send_email function from email_alert.py
        send_email(image_filename=None, object_detected=object_detected) # Pass the necessary parameters if required

    def make_call(self):
        # Use the call function from email_alert.py
        call()

    def __call__(self, addr):
        if addr == "Select Camera":
            cap = cv2.VideoCapture(0)
        else:
            ip_camera_address = f"http://{addr}/video"
            cap = cv2.VideoCapture(ip_camera_address)

        # cap = cv2.VideoCapture(capture_index)
        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        frame_count = 0
        while True:
            self.start_time = time()
            ret, im0 = cap.read()
            assert ret
            results = self.predict(im0)
            im0, class_ids = self.plot_bboxes(results, im0)

            if len(class_ids) > 0:  # Only send email if not sent before
                if not self.email_sent:
                    current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
                    # self.send_email(len(class_ids))

                    # Make a call
                    # self.make_call()
                    print(f"Call init {current_time}")

                    self.email_sent = True

            self.display_fps(im0)
            cv2.imshow('YOLOv8 Detection', im0)
            frame_count += 1
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):  # Break on 'q' or ESC key
                break
        cap.release()
        cv2.destroyAllWindows()
