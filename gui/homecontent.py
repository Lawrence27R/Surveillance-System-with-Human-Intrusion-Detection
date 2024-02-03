import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import sys
sys.path.append("..")
from recognize import FaceRecognizer

class HomeContent(tk.Frame):
    def __init__(self, master, add_cctv_section):
        super().__init__(master)
        self.add_cctv_section = add_cctv_section
        self.load_cctv_addrs()
        self.recognizer = FaceRecognizer()
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

        if new_status == "ON":
            self.start_video_feed()
        else:
            self.stop_video_feed()

    def load_cctv_addrs(self):
        self.camera_selection_var = tk.StringVar() # You can modify this based on your actual camera names

        # Load CCTV addresses from AddCCTVSection
        self.cctv_addresses = self.add_cctv_section.load_cctv_table()

        self.camera_dropdown = ttk.Combobox(self, textvariable=self.camera_selection_var, values=list(self.cctv_addresses.keys()), font=('Century Gothic', 12), state="readonly")
        self.camera_dropdown.set("Select Camera")  # Set default value
        self.camera_dropdown.grid(row=1, column=3, sticky="w", padx=10, pady=5)

    def start_video_feed(self):
        # get the IP camera address
        addr = self.camera_selection_var.get()
        if addr == "Select Camera":
            self.vid = cv2.VideoCapture(0)
        else:
            ip_addr = self.cctv_addresses[addr]
            ip_camera_address = f"http://{ip_addr}/video"
            self.vid = cv2.VideoCapture(ip_camera_address)

        if self.vid.isOpened():
            self.is_recording = True
            self.after(10, self.update_video_feed)
        else:
            messagebox.showerror("Error", "Unable to open the video feed.")

    def update_video_feed(self):
        if self.is_recording:
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.viewing_label.configure(image=photo)
                self.viewing_label.image = photo
                self.after(10, self.update_video_feed)
            else:
                self.stop_video_feed()

    def stop_video_feed(self):
        if self.vid:
            self.vid.release()

        # Update the image to a default blue image or clear it
        default_image = Image.new("RGB", (1, 1), color="#add8e6")  # Default blue color
        default_photo = ImageTk.PhotoImage(default_image)
        self.viewing_label.configure(image=default_photo)
        self.viewing_label.image = default_photo

        self.is_recording = False

    def on_window_configure(self, event):
        # Adjust the size of the box when the window is resized
        self.remaining_space_box.configure(width=event.width - 120, height=event.height - 200)

# Driver code
if __name__ == "__main__":
    root = tk.Tk()
    app = HomeContent(root)
    root.mainloop()