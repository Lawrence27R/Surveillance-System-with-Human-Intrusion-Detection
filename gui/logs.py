from datetime import datetime
import cv2
import os
import pandas as pd
from .email_alert import send_email, call
import threading
import queue

class LogsHandler:
    def __init__(self, logs_folder=""):
        self.logs_folder = logs_folder
        self.notified = False
        os.makedirs(self.logs_folder, exist_ok=True)

        # Create a new Excel file with today's date
        current_date = datetime.now().strftime("%d-%m-%Y")
        log_file_path = os.path.join(self.logs_folder, f"{current_date}.xlsx")

        # Check if the file already exists
        if not os.path.exists(log_file_path):
            pd.DataFrame(columns=["Name", "Time"]).to_excel(log_file_path, index=False)

        # Read the Excel file into the DataFrame
        self.log_df = pd.read_excel(log_file_path)
        self.log_queue = queue.Queue()
        self.lock = threading.Lock()
        self.log_thread = threading.Thread(target=self.process_log_queue)
        self.log_thread.start()

    def process_log_queue(self):
        while True:
            try:
                log_entry = self.log_queue.get()
                if log_entry is None:
                    break
                name, time, date = log_entry
                self.log_entry(name, time, date)
            except Exception as e:
                print(f"Error processing log queue: {e}")
                import traceback
                traceback.print_exc()

    def log_entry(self, name, time, date):
        try:
            log_file_name = f"{date}.xlsx"
            log_file_path = os.path.join(self.logs_folder, log_file_name)

            with self.lock:
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
                    self.log_df = self.log_df._append(new_entry, ignore_index=True)

                # Save the updated log file
                self.log_df.to_excel(log_file_path, index=False)
                # print(f"Log entry added successfully: {log_file_path}")

        except Exception as e:
            print(f"Error while adding log entry: {e}")
            import traceback
            traceback.print_exc()

    # def email_alert(self, image_filename):
    #     # Implement your email alert logic here
    #     send_email(image_filename)

    # def call_alert(self):
    #     # Implement your call alert logic here
    #     call()

    def process_log_queue(self):
        while True:
            log_entry = self.log_queue.get()
            if log_entry is None:
                break
            name, time, date = log_entry
            self.log_entry(name, time, date)

    def perform_alert(self, name, score, face_alignment):
        try:
            # print("Before perform_alert")
            current_time = datetime.now().strftime("%H:%M:%S")
            current_date = datetime.now().strftime("%d-%m-%Y")

            caption = None  # Default caption value

            if score > 0.25 and score < 0.50:
                caption = "INTRUDER"
                with self.lock:
                    self.log_queue.put((caption, current_time, current_date))
                
                image_filename = f"email_alert/alert_{current_time}.jpg"
                cv2.imwrite(image_filename, face_alignment)
                
                if not self.notified:
                    with self.lock:
                        send_email(image_filename)
                        print(f"Email sent: {current_time}")
                            
            elif score > 0 and score < 0.25:
                caption = "INTRUDER"
                with self.lock:
                    self.log_queue.put((caption, current_time, current_date))
                    if not self.notified:
                        # print(f"Call Initiated: {current_time}")
                        call()
            else:
                    caption = f"{name}"
                    with self.lock:
                        self.log_queue.put((caption, current_time, current_date))

            self.notified = True

            return caption

        except Exception as e:
            print(f"Error in perform_alert: {e}")
            import traceback
            traceback.print_exc()

            # Return None in case of an error
            return None

    def stop_processing(self):
        self.log_queue.put(None)
        self.log_thread.join()
