import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class HomeContent(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg="#232831")

        # Surveillance System Controls
        self.toggle_surveillance_button = tk.Button(self, text="ON/OFF", command=self.toggle_surveillance, font=('Century Gothic', 12), bg="#45aaf2", fg="white", padx=6, pady=5)
        self.toggle_surveillance_button.grid(row=0, column=0, sticky="w", padx=40, pady=20)

        self.surveillance_status_label = tk.Label(self, text="Surveillance System: OFF", font=('Century Gothic', 12), bg="#232831", fg="white", padx=10, pady=5)
        self.surveillance_status_label.grid(row=0, column=1, sticky="w", padx=0, pady=20)

        self.recording_status_label = tk.Label(self, text="                  ", font=('Century Gothic', 12), bg="#232831", fg="white", padx=10, pady=5)
        self.recording_status_label.grid(row=0, column=2, sticky="w", padx=0, pady=5)

        # Camera Controls
        self.toggle_recording_button = tk.Button(self, text="START/STOP", command=self.toggle_recording, font=('Century Gothic', 12), bg="#45aaf2", fg="white", padx=6, pady=5)
        self.toggle_recording_button.grid(row=0, column=3, sticky="w", padx=0, pady=5)

        self.recording_status_label = tk.Label(self, text="Recording: OFF", font=('Century Gothic', 12), bg="#232831", fg="white", padx=10, pady=5)
        self.recording_status_label.grid(row=0, column=4, sticky="w", padx=0, pady=5)

        # Camera Selection
        self.view_camera_label = tk.Label(self, text="View Camera:", font=('Century Gothic', 12), bg="#232831", fg="white", padx=10, pady=5)
        self.view_camera_label.grid(row=1, column=2, sticky="w", padx=0, pady=5)

        self.camera_selection_var = tk.StringVar()
        camera_choices = ["Cam1", "Cam2"]  # You can modify this based on your actual camera names
        self.camera_dropdown = ttk.Combobox(self, textvariable=self.camera_selection_var, values=camera_choices, font=('Century Gothic', 12), state="readonly")
        self.camera_dropdown.set("Cam1")  # Set default camera
        self.camera_dropdown.grid(row=1, column=3, sticky="w", padx=10, pady=5)

        # Create a box with light blue background
        initial_width = 900
        initial_height = 550
        self.remaining_space_box = tk.Frame(self, bg="light blue", width=initial_width, height=initial_height, bd=2, relief=tk.SOLID)
        self.remaining_space_box.place(width=initial_width, height=initial_height, x=150, y=135, anchor="nw")  # Adjust the coordinates as needed

        # Add label to the box
        self.viewing_label = tk.Label(self.remaining_space_box, text="Viewing Cam1", font=('Century Gothic', 12), bg="light blue", padx=10, pady=10)
        self.viewing_label.pack(expand=True)

        # Bind the <Configure> event to the function
        master.bind("<Configure>", self.on_window_configure)

    def toggle_surveillance(self):
        # Add code to toggle surveillance system and update label accordingly
        current_status = self.surveillance_status_label.cget("text")
        new_status = "OFF" if "ON" in current_status else "ON"
        self.surveillance_status_label.config(text=f"Surveillance System: {new_status}")

    def toggle_recording(self):
        # Add code to toggle recording and update label accordingly
        current_status = self.recording_status_label.cget("text")
        new_status = "OFF" if "ON" in current_status else "ON"
        self.recording_status_label.config(text=f"Recording: {new_status}")

    def on_window_configure(self, event):
        # Adjust the size of the box when the window is resized
        self.remaining_space_box.configure(width=event.width - 120, height=event.height - 200)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = HomeContent(root)
    root.mainloop()
