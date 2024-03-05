import threading
import time
import cv2
import numpy as np
import os
import torch
import yaml
from torchvision import transforms
from driver_code.face_alignment.alignment import norm_crop
from driver_code.face_detection.scrfd.detector import SCRFD
from driver_code.face_recognitions.arcface.model import iresnet_inference
from driver_code.face_recognitions.arcface.utils import compare_encodings, read_features
from driver_code.face_tracking.tracker.byte_tracker import BYTETracker
from driver_code.face_tracking.tracker.visualize import plot_tracking    
from gui.logs import LogsHandler  

class FaceRecognizer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.detector = SCRFD(model_file="driver_code/face_detection/scrfd/weights/scrfd_2.5g_bnkps.onnx")
        self.recognizer = iresnet_inference(
            model_name="r100", path="driver_code/face_recognitions/arcface/weights/arcface_r100.pth", device=self.device
        )
        self.images_names, self.images_embs = read_features(feature_path="datasets/face_features/feature")
        self.id_face_mapping = {}
        self.data_mapping = {
            "raw_image": None,
            "tracking_ids": [],
            "detection_bboxes": [],
            "detection_landmarks": [],
            "tracking_bboxes": [],
        }
        self.exit_threads = False
        self.logs_folder = "logs"
        os.makedirs(self.logs_folder, exist_ok=True)
        self.logs_handler = LogsHandler(logs_folder=self.logs_folder)

    def load_config(self, file_name):
        with open(file_name, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def process_tracking(self, frame, detector, tracker, args, frame_id, fps):
        outputs, img_info, bboxes, landmarks = detector.detect_tracking(image=frame)

        if outputs is not None:
            tracking_tlwhs, tracking_ids, tracking_scores, tracking_bboxes = [], [], [], []

            for t in tracker.update(outputs, [img_info["height"], img_info["width"]], (128, 128)):
                tlwh, tid = t.tlwh, t.track_id
                vertical = tlwh[2] / tlwh[3] > args["aspect_ratio_thresh"]

                if tlwh[2] * tlwh[3] > args["min_box_area"] and not vertical:
                    x1, y1, w, h = tlwh
                    tracking_bboxes.append([x1, y1, x1 + w, y1 + h])
                    tracking_tlwhs.append(tlwh)
                    tracking_ids.append(tid)
                    tracking_scores.append(t.score)

            tracking_image = plot_tracking(img_info["raw_img"], tracking_tlwhs, tracking_ids, names=self.id_face_mapping, frame_id=frame_id + 1, fps=fps)
        else:
            tracking_image = img_info["raw_img"]

        self.data_mapping["raw_image"] = img_info["raw_img"]
        self.data_mapping["detection_bboxes"] = bboxes
        self.data_mapping["detection_landmarks"] = landmarks
        self.data_mapping["tracking_ids"] = tracking_ids
        self.data_mapping["tracking_bboxes"] = tracking_bboxes

        return tracking_image

    @torch.no_grad()
    def get_feature(self, face_image):
        face_preprocess = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((112, 112)),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
        ])

        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        face_image = face_preprocess(face_image).unsqueeze(0).to(self.device)
        emb_img_face = self.recognizer(face_image).cpu().numpy()
        images_emb = emb_img_face / np.linalg.norm(emb_img_face)

        return images_emb

    def recognition(self, face_image):
        query_emb = self.get_feature(face_image)
        score, id_min = compare_encodings(query_emb, self.images_embs)
        name = self.images_names[id_min]
        score = score[0]
        return score, name

    def mapping_bbox(self, box1, box2):
        x_min_inter = max(box1[0], box2[0])
        y_min_inter = max(box1[1], box2[1])
        x_max_inter = min(box1[2], box2[2])
        y_max_inter = min(box1[3], box2[3])
        intersection_area = max(0, x_max_inter - x_min_inter + 1) * max(0, y_max_inter - y_min_inter + 1)
        area_box1 = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
        area_box2 = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)
        union_area = area_box1 + area_box2 - intersection_area
        iou = intersection_area / union_area
        return iou
    

    def tracking(self, detector, args, addr):
        start_time = time.time_ns()
        frame_count, fps = 0, 0
        tracker = BYTETracker(args=args, frame_rate=30)
        frame_id = 0
        
        if addr == "Select Camera":
            self.cap = cv2.VideoCapture(0)
        else:
            ip_camera_address = f"http://{addr}/video"
            self.cap = cv2.VideoCapture(ip_camera_address)

        try:
            while True:
                _, img = self.cap.read()
                tracking_image = self.process_tracking(img, detector, tracker, args, frame_id, fps)

                frame_count += 1
                if frame_count >= 30:
                    fps = 1e9 * frame_count / (time.time_ns() - start_time)
                    frame_count = 0
                    start_time = time.time_ns()

                cv2.imshow("Face Recognition Intruder Detection", tracking_image)
                ch = cv2.waitKey(1) & 0xFF
                if ch == 27 or ch == ord("q") or ch == ord("Q") or self.exit_threads:
                    break

                # Recognition logic within the tracking loop
                self.process_recognition()

        finally:
            self.cap.release()
            cv2.destroyAllWindows()

    def process_recognition(self):
        raw_image = self.data_mapping["raw_image"]
        detection_landmarks = self.data_mapping["detection_landmarks"]
        detection_bboxes = self.data_mapping["detection_bboxes"]
        tracking_ids = self.data_mapping["tracking_ids"]
        tracking_bboxes = self.data_mapping["tracking_bboxes"]

        for i, track_bbox in enumerate(tracking_bboxes):
            for j, detection_bbox in enumerate(detection_bboxes):
                mapping_score = self.mapping_bbox(box1=track_bbox, box2=detection_bbox)
                if mapping_score > 0.9:
                    face_alignment = norm_crop(img=raw_image, landmark=detection_landmarks[j])
                    score, name = self.recognition(face_image=face_alignment)
                    if name is not None:
                        caption = self.logs_handler.perform_alert(name, score, face_alignment)

                    self.id_face_mapping[tracking_ids[i]] = caption

                    detection_bboxes = np.delete(detection_bboxes, j, axis=0)
                    detection_landmarks = np.delete(detection_landmarks, j, axis=0)
                    break

    def recognize(self):
        while True:
            self.process_recognition()

    def main(self, addr):
        config_tracking = self.load_config("driver_code/face_tracking/config/config_tracking.yaml")

        try:
            self.tracking(self.detector, config_tracking, addr)
        except KeyboardInterrupt:
            print("Interrupt received. Stopping processing...")
            self.exit_threads = True
            self.logs_handler.stop_processing()
