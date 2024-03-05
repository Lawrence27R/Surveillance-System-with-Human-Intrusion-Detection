from datetime import datetime
import cv2
import os
import pandas as pd
from gui.email_alert import send_email, call
import threading
import queue

class LogsHandler:
    def __init__(self, logs_folder=""):
        self.logs_folder = logs_folder
        os.makedirs(self.logs_folder, exist_ok=True)

        # Create a new Excel file with today's date
        current_date = datetime.now().strftime("%d-%m-%Y")
        log_file_path = os.path.join(self.logs_folder, f"{current_date}.xlsx")

        # Check if the file already exists
        if not os.path.exists(log_file_path):
            pd.DataFrame(columns=["Name", "Time"]).to_excel(log_file_path, index=False)

        # Read the Excel file into the DataFrame
        self.log_df = pd.read_excel(log_file_path)
        self.stop_event = threading.Event()
        self.log_queue = queue.Queue()

    def process_log_queue(self):
        while not self.stop_event.is_set():
            try:
                log_entry = self.log_queue.get(timeout=1)
                if log_entry is None:
                    break
                name, time, date = log_entry
                self.log_entry(name, time, date)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing log queue: {e}")
                import traceback
                traceback.print_exc()
        print("Exiting log processing loop.")

    def start_log_processing_thread(self):
        self.log_processing_thread = threading.Thread(target=self.process_log_queue)
        self.log_processing_thread.start()

    def stop_log_processing_thread(self):
        self.log_queue.put(None)
        self.log_processing_thread.join()

    def log_entry(self, name, time, date):
        try:
            log_file_name = f"{date}.xlsx"
            log_file_path = os.path.join(self.logs_folder, log_file_name)

            # Check if DataFrame is initialized
            if self.log_df is None:
                # Load existing log file if it exists, otherwise create a new DataFrame
                if os.path.exists(log_file_path):
                    self.log_df = pd.read_excel(log_file_path)
                else:
                    self.log_df = pd.DataFrame(columns=["Name", "Time"])

            # Check for duplicates and update the entry
            duplicate_mask = (self.log_df["Name"] == name)
            if duplicate_mask.any():
                self.log_df.loc[duplicate_mask, ["Time"]] = time
            else:
                # Add a new entry
                new_entry = {"Name": name, "Time": time}
                self.log_df = self.log_df.append(new_entry, ignore_index=True)

            # Save the updated log file
            self.log_df.to_excel(log_file_path, index=False)

        except Exception as e:
            print(f"Error while adding log entry: {e}")
            import traceback
            traceback.print_exc()

    def email_alert(self, image_filename, object_detected):
            # Implement your email alert logic here
            send_email(image_filename, object_detected)

    def call_alert(self):
        # Implement your call alert logic here
        call()

    def perform_alert(self, name, score, face_alignment):
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            current_date = datetime.now().strftime("%d-%m-%Y")

            caption = None

            if 0.25 < score < 0.50:
                caption = "INTRUDER"
                self.log_queue.put((caption, current_time, current_date))
                image_filename = f"email_alert/alert_{current_time}.jpg"
                cv2.imwrite(image_filename, face_alignment)

                # Move alert processing to a separate thread
                alert_thread = threading.Thread(target=self.process_alert, args=(image_filename, caption))
                alert_thread.start()
            elif 0 < score < 0.25:
                caption = "INTRUDER"
                self.log_queue.put((caption, current_time, current_date))
                self.call_alert()
            else:
                caption = f"{name}"
                # self.log_queue.put((caption, current_time, current_date))
            return caption

        except Exception as e:
            print(f"Error in perform_alert: {e}")
            import traceback
            traceback.print_exc()
            return None

    def process_alert(self, image_filename, caption):
        # Your actual alert processing logic (email, etc.) goes here
        self.email_alert(image_filename, caption)

    def stop_processing(self):
        self.stop_log_processing_thread()