# home.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import os
import mysql_db
from change_password import ChangePasswordWindow
from navbar import NavigationBar
from rec_and_logs import RecAndLogsSection
from new_registration import NewRegistrationSection
from add_details import AddDetailsSection  # Import the add details section

class Homepage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Surveillance System with Human Intrusion Detection")
        self.master.geometry("1400x720")

        # Use ThemedStyle for a dark theme
        style = ThemedStyle(self.master)
        style.set_theme("arc")

        self.configure(bg="#232831")  # Set background color for the main window

        # Create the navigation bar
        self.navbar = NavigationBar(self)
        self.navbar.pack(side=tk.TOP, fill=tk.X)

        # Create a frame to hold the sidebar and main content with a border in between
        self.sidebar_frame = tk.Frame(self, bg="#21252b", bd=2, relief=tk.SUNKEN)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)  # Adjust padx as needed

        # Create the sidebar
        self.sidebar = tk.Frame(self.sidebar_frame, width=160, bg="#21252b")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # Display username and change password fields
        self.display_username_change_password_fields()

        # Add labels with images for each item in the sidebar
        self.create_sidebar_labels()

        # Create a border between the sidebar and the main content
        tk.Frame(self.sidebar_frame, width=2, bg="#21252b").pack(side=tk.LEFT, fill=tk.Y)

        # Create the main content area
        self.main_content = tk.Frame(self, bg="#232831")
        self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)  # Adjust padx and pady as needed


        self.pack(fill=tk.BOTH, expand=True)  # Pack to fill the entire window

        # MySQL connection
        self.conn, self.cursor = mysql_db.initialize_connection()

        # Store logged-in user's email
        self.logged_in_email = "rootuser@gmail.com"

        # RecAndLogs section
        self.rec_and_logs_section = RecAndLogsSection(self.main_content)

        # New Registration section
        self.new_registration_section = NewRegistrationSection(self.main_content)

        # Add Details section
        self.add_details_section = AddDetailsSection(self.main_content)

        self.current_section = None

    def create_sidebar_labels(self):
        # Replace these paths with actual image paths
        logo_paths = {
            "Home": "images/icons/cil-home.png",
            "New Registration": "images/icons/icons8-add-administrator-18.png",
            "Add CCTV": "images/icons/icons8-add-camera-18.png",
            "Add Details": "images/icons/icons8-registration-18.png",
            "REC & LOGS": "images/icons/icons8-recording-18.png",
        }

        for item, logo_path in logo_paths.items():
            # Load and resize the image
            logo_image = self.load_and_resize_image(logo_path, width=20, height=20, resampling=Image.LANCZOS)

            # Create a label with the logo image
            label = tk.Label(
                self.sidebar,
                text=item,
                image=logo_image,
                compound="left",
                font=('Century Gothic', 12),
                bg="#21252b",
                fg="white",
                padx=10,
                pady=20,
                anchor="w",
            )
            label.image = logo_image  # Keep a reference to the image

            # Bind the label to a command that changes the main content
            label.bind("<Button-1>", lambda event, item=item: self.change_main_content(item))

            label.pack(side=tk.TOP, fill=tk.X)

    def display_username_change_password_fields(self):
        # Display username
        self.username_label = tk.Label(self.navbar, text="Username: ", font=('Century Gothic', 12), bg="#232831", fg="white")
        self.username_label.pack(side=tk.LEFT, expand=True)  # Expand to fill the available space

    def show_username(self):
        self.cursor.execute(f"SELECT email FROM users WHERE email = '{self.logged_in_email}'")
        result = self.cursor.fetchone()
        if result:
            self.username_label.config(text=f"Username: {result[0]}")
        else:
            self.username_label.config(text="Username not found")

    def open_change_password_window(self):
        ChangePasswordWindow(self, self.change_password)

    def change_password(self):
        old_password = self.logged_in_email  # Replace this with the actual old password
        new_password = ChangePasswordWindow.get_new_password()
        confirm_new_password = ChangePasswordWindow.get_confirm_new_password()

        if new_password == confirm_new_password:
            self.cursor.execute(f"UPDATE users SET password = '{new_password}' WHERE email = '{self.logged_in_email}' AND password = '{old_password}'")
            self.conn.commit()
            messagebox.showinfo("Password Changed", "Password has been changed successfully.")
        else:
            messagebox.showerror("Error", "New password and confirm password do not match.")

    def logout(self):
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            # Perform logout actions here
            # For example, destroy the current window or switch to a login screen
            self.master.destroy()

    def load_and_resize_image(self, image_path, width=None, height=None, resampling=Image.LANCZOS):
        try:
            original_image = Image.open(image_path)
            if width and height:
                resized_image = original_image.resize((width, height), resampling)
                return ImageTk.PhotoImage(resized_image)
            else:
                return ImageTk.PhotoImage(original_image)
        except Exception as e:
            print(f"Error opening image: {e}")
            return None

    def change_main_content(self, item):

        if item == "REC & LOGS":
            self.show_section(self.rec_and_logs_section)
        elif item == "New Registration":
            self.show_section(self.new_registration_section)
        elif item == "Add Details":
            self.show_section(self.add_details_section)
        else:
            self.hide_current_section()

    def show_section(self, section):
        if self.current_section:
            self.current_section.pack_forget()
        section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.current_section = section

    def hide_current_section(self):
        if self.current_section:
            self.current_section.pack_forget()
            self.current_section = None


if __name__ == "__main__":
    root = tk.Tk()
    app = Homepage(root)
    root.mainloop()
