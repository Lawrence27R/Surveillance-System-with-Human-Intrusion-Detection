import tkinter as tk
from PIL import Image, ImageTk
import os

class RecAndLogsSection(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#232831")
        self.recording_path = "D:/Final Year"
        self.logs_path = "D:/My Project"
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
        os.startfile(self.recording_path)

    def open_logs_folder(self):
        os.startfile(self.logs_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = RecAndLogsSection(root)
    root.mainloop()
