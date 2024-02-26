import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess
import platform

class RecAndLogsSection(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#232831")
        self.recording_path = "/home/lawrence/Desktop/Surveillance-System-with-Human-Intrusion-Detection/Video_Rec"
        self.logs_path = "/home/lawrence/Desktop/Surveillance-System-with-Human-Intrusion-Detection/logs"
        self.create_buttons()

    def create_buttons(self):
        button1 = tk.Button(
            self,
            text="View Recordings",
            command=self.open_recordings_folder,
            bg="#1565C0",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        button1.grid(row=0, column=0, padx=50)

        button2 = tk.Button(
            self,
            text="View Logs",
            command=self.open_logs_folder,
            bg="#1565C0",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        button2.grid(row=0, column=1, padx=50)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def open_recordings_folder(self):
        self.open_folder(self.recording_path)

    def open_logs_folder(self):
        self.open_folder(self.logs_path)

    def open_folder(self, folder_path):
        system_platform = platform.system().lower()

        try:
            if system_platform == "windows":
                # On Windows, use start
                subprocess.Popen(["start", " ", folder_path], shell=True)
            elif system_platform == "darwin":
                # On macOS, use open
                subprocess.Popen(["open", folder_path])
            elif system_platform == "linux":
                # On Linux, use xdg-open
                subprocess.Popen(["xdg-open", folder_path])
            else:
                print("Unsupported platform")
        except Exception as e:
            print(f"Error opening folder: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecAndLogsSection(root)
    root.mainloop()
