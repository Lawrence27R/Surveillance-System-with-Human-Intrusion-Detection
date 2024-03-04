import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import sys
import os
from datetime import datetime
from time import time, sleep
import torch
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
from gui.email_alert import send_email, call
import sys
sys.path.append("..")
from recognize import FaceRecognizer  # Import necessary functions

# Set the environment variable to disable YOLO verbose output
os.environ['YOLO_VERBOSE'] = 'False'

class ObjectDetection:
    def __init__(self):
        # default parameters
        self.email_sent = False

        self.model = YOLO("detection_model/yolov8n.pt")

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

    def send_email_alert(self, object_detected):
        # Use the send_email function from email_alert.py
        send_email(image_filename=None, object_detected=object_detected)  # Pass the necessary parameters if required

    def make_call(self):
        # Use the call function from email_alert.py
        call()

    def start_intrusion_detection(self, addr):
        if addr == "Select Camera":
            cap = cv2.VideoCapture(0)
        else:
            ip_camera_address = f"http://{addr}/video"
            cap = cv2.VideoCapture(ip_camera_address)

        # cap = cv2.VideoCapture(capture_index)
        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
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
                    self.send_email_alert(len(class_ids))

                    # Make a call
                    self.make_call()
                    # print(f"Call init {current_time}")

                    self.email_sent = True

            self.display_fps(im0)
            cv2.imshow('Human Intrusion Detection', im0)
            frame_count += 1
            key = cv2.waitKey(1) & 0xFF  # Change the waitKey delay to 1
            if key == 27 or key == ord('q'):  # Break on 'q' or ESC key
                break

        cap.release()
        cv2.destroyAllWindows()

    def stop_intrusion_detection(self):
        self.email_sent = False
        cv2.destroyAllWindows()

class HomeContent(tk.Frame):
    def __init__(self, master, add_cctv_section, intrusion_detector):
        super().__init__(master)
        self.add_cctv_section = add_cctv_section
        self.intrusion_detector = intrusion_detector
        self.load_cctv_addrs()
        self.recognizer = FaceRecognizer()
        self.configure(bg="#232831")

        # Surveillance System Controls
        self.toggle_surveillance_button = tk.Button(self, text="Button01", command=self.toggle_surveillance, font=('Century Gothic', 12), bg="#45aaf2", fg="white", padx=6, pady=5)
        self.toggle_surveillance_button.grid(row=0, column=0, sticky="w", padx=40, pady=20)

        self.surveillance_status_label = tk.Label(self, text="Surveillance System: OFF", font=('Century Gothic', 12), bg="#232831", fg="white", padx=10, pady=5)
        self.surveillance_status_label.grid(row=0, column=1, sticky="w", padx=0, pady=20)

        self.recording_status_label = tk.Label(self, text="                  ", font=('Century Gothic', 12), bg="#232831", fg="white", padx=10, pady=5)
        self.recording_status_label.grid(row=0, column=2, sticky="w", padx=0, pady=5)

        # Camera Controls
        self.toggle_recording_button = tk.Button(self, text="Button02", command=self.toggle_recording, font=('Century Gothic', 12), bg="#45aaf2", fg="white", padx=6, pady=5)
        self.toggle_recording_button.grid(row=0, column=3, sticky="w", padx=0, pady=5)

        self.recording_status_label = tk.Label(self, text="View Feed: OFF", font=('Century Gothic', 12), bg="#232831", fg="white", padx=10, pady=5)
        self.recording_status_label.grid(row=0, column=4, sticky="w", padx=0, pady=5)

        # Camera Selection
        self.view_camera_label = tk.Label(self, text="View Camera:", font=('Century Gothic', 12), bg="#232831", fg="white", padx=10, pady=5)
        self.view_camera_label.grid(row=1, column=2, sticky="w", padx=0, pady=5)

        # Create a button to trigger CCTV table update
        self.update_cctv_button = tk.Button(self, text="↺", command=self.update_cctv_table, font=('Century Gothic', 12), bg="#45aaf2", fg="white", padx=2, pady=1)
        self.update_cctv_button.grid(row=1, column=4, sticky="w", padx=10, pady=5)

        # Create a box with light blue background
        initial_width = 900
        initial_height = 550
        self.remaining_space_box = tk.Frame(self, bg="light blue", width=initial_width, height=initial_height, bd=2, relief=tk.SOLID)
        self.remaining_space_box.place(width=initial_width, height=initial_height, x=150, y=135, anchor="nw")  # Adjust the coordinates as needed

        # Add label to the box
        self.viewing_label = tk.Label(self.remaining_space_box, text="No feed to show. Select a camera from list.", font=('Century Gothic', 12), bg="light blue", padx=10, pady=10)
        self.viewing_label.pack(expand=True)

        # OpenCV variables
        self.video_source = None
        self.vid = None
        self.is_recording = False

        # Bind the <Configure> event to the function
        master.bind("<Configure>", self.on_window_configure)

    def update_cctv_table(self):
        # Call the load_cctv_addrs method to update the dropdown values
        self.load_cctv_addrs()

    def toggle_surveillance(self):
        # Add code to toggle surveillance system and update label accordingly
        current_status = self.surveillance_status_label.cget("text")
        # get the IP camera address
        new_status = ""

        addr = self.camera_selection_var.get()
        ip_addr = self.cctv_addresses[addr] if addr != 'Select Camera' else 'Select Camera'

        if current_status == "ON":
            new_status = "OFF"
            self.recognizer.destroy_window()
        else:
            new_status == "ON"
            self.recognizer.main(ip_addr)

        self.surveillance_status_label.config(text=f"Surveillance System: {new_status}")

    def toggle_recording(self):
        # Add code to toggle recording and update label accordingly
        current_status = self.recording_status_label.cget("text")
        new_status = "OFF" if "ON" in current_status else "ON"
        self.recording_status_label.config(text=f"View Feed: {new_status}")

        addr = self.camera_selection_var.get()
        ip_addr = self.cctv_addresses[addr] if addr != 'Select Camera' else 'Select Camera'

        if new_status == "ON":
            self.intrusion_detector.start_intrusion_detection(ip_addr)
        else:
            self.intrusion_detector.stop_intrusion_detection()

    def load_cctv_addrs(self):
        self.camera_selection_var = tk.StringVar()  # You can modify this based on your actual camera names

        # Load CCTV addresses from AddCCTVSection
        self.cctv_addresses = self.add_cctv_section.load_cctv_table()

        self.camera_dropdown = ttk.Combobox(self, textvariable=self.camera_selection_var, values=list(self.cctv_addresses.keys()), font=('Century Gothic', 12), state="readonly")
        self.camera_dropdown.set("Select Camera")  # Set default value
        self.camera_dropdown.grid(row=1, column=3, sticky="w", padx=10, pady=5)

    def on_window_configure(self, event):
        # Adjust the size of the box when the window is resized
        self.remaining_space_box.configure(width=event.width - 120, height=event.height - 200)

