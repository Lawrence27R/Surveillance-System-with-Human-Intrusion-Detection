import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import cv2
from gui.mysql_db import DatabaseHandler
# from capture_images import capture_images
from PIL import Image, ImageTk
from add_persons import add_persons

class NewRegistrationSection(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#232831", padx=40, pady=20)
        self.user_id_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.data_entries = []
        self.initialize_connection()
        self.create_registration_widgets()
        self.create_table()
        self.create_delete_button()
        self.update_table()

    def initialize_connection(self):
        self.database = DatabaseHandler()
        self.conn, self.cursor = self.database.initialize_connection()

    def create_registration_widgets(self):
        title_label = tk.Label(self, text="Register New User:", font=('Century Gothic', 16, 'bold'), bg="#232831", fg="white", pady=8)
        title_label.grid(row=0, column=0, columnspan=3, sticky="w")

        user_id_label = tk.Label(self, text="User ID:", font=('Century Gothic', 12), bg="#232831", fg="white")
        user_id_label.grid(row=1, column=0, pady=6, sticky="w")
        user_id_entry = tk.Entry(self, textvariable=self.user_id_var, font=('Century Gothic', 12))
        user_id_entry.grid(row=1, column=1, pady=6, sticky="w")

        username_label = tk.Label(self, text="Username:", font=('Century Gothic', 12), bg="#232831", fg="white")
        username_label.grid(row=2, column=0, pady=6, sticky="w")
        username_entry = tk.Entry(self, textvariable=self.username_var, font=('Century Gothic', 12))
        username_entry.grid(row=2, column=1, pady=6, padx=4, sticky="w")

        capture_button = tk.Button(
            self,
            text="Capture Images",
            command=self.capture_images,
            bg="#1565C0",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        capture_button.grid(row=3, column=0, pady=(10, 20), sticky="w")

        or_label = tk.Label(self, text="                    OR ", font=('Century Gothic', 12), bg="#232831", fg="white")
        or_label.grid(row=3, column=1, pady=6, sticky="w")

        upload_button = tk.Button(
            self,
            text="Upload Images",
            command=self.upload_images,
            bg="#1565C0",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        upload_button.grid(row=3, column=2, pady=(10, 20), padx=5, sticky="w")

        add_person_button = tk.Button(
            self,
            text="Add Persons",
            command=self.add_person_button_clicked,
            bg="#1565C0",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        add_person_button.grid(row=7, column=0, pady=(8, 25), sticky="w")


    def create_table(self):
        headers = ["User ID", "Username"]
        self.table = ttk.Treeview(self, columns=headers, show="headings", selectmode="browse", height=11)
        for header in headers:
            self.table.heading(header, text=header)
            self.table.column(header, width=200)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.grid(row=4, column=0, columnspan=3, pady=8, sticky="w")
        scrollbar.grid(row=4, column=3, pady=8, sticky="ns")
        self.table.bind("<Delete>", self.delete_selected_entry)

    def create_delete_button(self):
        delete_button = tk.Button(
            self,
            text="Delete Entry",
            command=self.delete_selected_entry,
            bg="#C62828",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        delete_button.grid(row=5, column=0, pady=(8, 25), sticky="w")
    
    def add_person_button_clicked(self):
        # Call the add_persons function here
        backup_dir = "datasets/backup/"
        add_persons_dir = "datasets/new_persons/"
        faces_save_dir = "datasets/data/"
        features_path = "datasets/face_features/feature"

        add_persons(backup_dir, add_persons_dir, faces_save_dir, features_path)
        

    def capture_images(self):
        user_id = self.user_id_var.get()
        username = self.username_var.get()
        if not user_id or not username:
            messagebox.showwarning("Incomplete Information", "Please enter User ID and Username.")
            return

        user_image_dir = os.path.join('datasets/new_persons/', f"{user_id}_{username}")
        os.makedirs(user_image_dir, exist_ok=True)

        cap = cv2.VideoCapture(0)

        face_cascade_frontal = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        face_cascade_profile = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml') 
        image_number = 1

        while True:
            ret, frame = cap.read()

            if not ret:
                messagebox.showerror("Capture Error", "Failed to capture video.")
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frontal_faces = face_cascade_frontal.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)
            profile_faces = face_cascade_profile.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

            for (x, y, width, height) in frontal_faces:
                face_pixels = frame[y:y + height, x:x + width]
                if not face_pixels.size == 0:
                    cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                    cv2.imshow("Capture Images", frame)

                    key = cv2.waitKey(1)
                    if key in (27, ord('q')):
                        break
                    elif key == 99 or key == 67:
                        img_file = os.path.join(user_image_dir, f"{username}_{image_number}.jpg")
                        cv2.imwrite(img_file, face_pixels)
                        print(f"Image {image_number} captured and saved as {img_file}")
                        image_number += 1

            for (x, y, width, height) in profile_faces:
                face_pixels = frame[y:y + height, x:x + width]
                if not face_pixels.size == 0:
                    cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                    cv2.imshow("Capture Images", frame)

                    key = cv2.waitKey(1)
                    if key in (27, ord('q')):
                        break
                    elif key == 99 or key == 67:
                        img_file = os.path.join(user_image_dir, f"{username}_{image_number}.jpg")
                        cv2.imwrite(img_file, face_pixels)
                        print(f"Image {image_number} captured and saved as {img_file}")
                        image_number += 1

            cv2.imshow("Capture Images", frame)

            if cv2.waitKey(1) & 0xFF in (27, ord('q')):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.insert_user_into_database(user_id, username)
        self.update_table()

    def insert_user_into_database(self, user_id, username):
        insert_query = "INSERT INTO newreg (user_id, username) VALUES (%s, %s)"
        self.cursor.execute(insert_query, (int(user_id), username))
        self.conn.commit()

    def update_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self.data_entries = self.get_data_from_database()
        for entry in self.data_entries:
            self.table.insert("", "end", values=entry)

    def get_data_from_database(self):
        select_query = "SELECT * FROM newreg"
        self.cursor.execute(select_query)
        data = self.cursor.fetchall()
        return data

    def delete_selected_entry(self, event=None):
        selected_item = self.table.focus()
        selected_item = self.table.item(selected_item, 'values')[0]
        if selected_item:
            selected_id = selected_item
            self.delete_user_from_database(selected_id)
            for i, entry in enumerate(self.data_entries):
                if entry[0] == selected_id:
                    del self.data_entries[i]
                    break
            self.update_table()

    def delete_user_from_database(self, user_id):
        folder_path = os.path.join('../datasets/new_persons', f"{user_id}_{self.username_var.get()}")
        delete_query = f"DELETE FROM newreg WHERE user_id = {user_id}"
        try:
            self.cursor.execute(delete_query)
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Delete Error", f"Error deleting user from the database: {str(e)}")
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path, ignore_errors=True)

    def upload_images(self):
        file_paths = filedialog.askopenfilenames(
            initialdir="/home/lawrence/Downloads",  # Set your initial directory
            title="Select Images",
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png")],
        )

        if file_paths:
            destination_folder = filedialog.askdirectory(
                initialdir="/home/lawrence/Downloads",  # Set your initial directory
                title="Select Destination Folder",
            )

            if destination_folder:
                for file_path in file_paths:
                    # Get the file name from the path
                    file_name = os.path.basename(file_path)
                    # Create the destination path
                    destination_path = os.path.join(destination_folder, file_name)

                    try:
                        # Copy the file to the destination folder
                        shutil.copy(file_path, destination_path)

                        # Display the copied image on a canvas
                        self.display_image(destination_path)

                    except Exception as e:
                        messagebox.showerror(
                            "Copy Error",
                            f"Error copying image '{file_name}': {str(e)}"
                        )

                messagebox.showinfo("Upload Successful", "Images uploaded successfully.")

    def display_image(self, image_path):
        # Open the image using PIL
        image = Image.open(image_path)
        # Convert the PIL Image to Tkinter PhotoImage
        tk_image = ImageTk.PhotoImage(image)

        # Create a canvas to display the image
        canvas = tk.Canvas(self, width=image.width, height=image.height)
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        canvas.pack()


    def close_connection(self):
        self.cursor.close()
        self.conn.close()
